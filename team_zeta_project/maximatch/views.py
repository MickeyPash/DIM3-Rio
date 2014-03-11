from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from maximatch.models import Experiment, Participant, Researcher, Application
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
from maximatch.forms import ExperimentForm, ParticipantForm, UserForm, ResearcherForm

def encode_url(url):
    return url.replace(' ', '_')

def decode_url(url):
    return url.replace('_', ' ')

def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    experiment_list = Experiment.objects.all()
    context_dict = {'experiments': experiment_list}

    for experiment in experiment_list:
        experiment.url = encode_url(experiment.title)

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('maximatch/index.html', context_dict, context)

def experiment(request, experiment_title_url):
    context = RequestContext(request)

    # Change underscores in the category name to spaces.
    experiment_title = decode_url(experiment_title_url)

    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    context_dict = {'experiment_title': experiment_title}

    try:
        # If we can't find, the .get() method raises a DoesNotExist exception.
        experiment = Experiment.objects.get(title=experiment_title)

        experiment.url = encode_url(experiment.title)

        # Adds our results list to the template context under name pages.
        context_dict['experiment'] = experiment

    except Experiment.DoesNotExist:
        # We get here if we didn't find the specified experiment.
        pass

    # Go render the response and return it to the client.
    return render_to_response('maximatch/experiment.html', context_dict, context)

def add_experiment(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = ExperimentForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = ExperimentForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('maximatch/add_experiment.html', {'form': form}, context)

@login_required
def edit_experiment(request, experiment_title_url=None):
    context = RequestContext(request)

    experiment_title = decode_url(experiment_title_url)

    context_dict = {'experiment_title': experiment_title}

    try:
        # If we can't find, the .get() method raises a DoesNotExist exception.
        experiment = Experiment.objects.get(title=experiment_title)
        experiment.url = encode_url(experiment.title)

        # Adds our results list to the template context under name pages.
        context_dict['experiment'] = experiment

    except Experiment.DoesNotExist:
        # We get here if we didn't find the specified experiment.
        return render_to_response('maximatch/edit_experiment.html', context_dict, context)

    if request.POST:
        form = ExperimentForm(request.POST, instance=experiment)
        if form.is_valid():
            form.save()

            # If the save was successful, redirect to the details page
            return HttpResponseRedirect('/maximatch/experiment/' + encode_url(form.cleaned_data['title']))

        else:
            print form.errors

    else:
        form = ExperimentForm(instance=experiment)

    context_dict['form'] = form

    return render_to_response('maximatch/edit_experiment.html', context_dict, context)

def apply_experiment(request, experiment_title_url=None):
    # Get the context from the request.

    success = False
    context_dict = {'success': success}

    context = RequestContext(request)
    user_id = request.user.id

    try:
        user = User.objects.get(id=user_id)
        experiment = Experiment.objects.get(title=decode_url(experiment_title_url))
        participant = Participant.objects.get(user=user)
    except (Experiment.DoesNotExist, User.DoesNotExist, Participant.DoesNotExist):
        context_dict['error_message'] = 'Participant or experiment does not exist.'
        return render_to_response('maximatch/applied_experiment.html', context_dict, context)

    try:
        application = Application.objects.get(participant=participant, experiment=experiment)
        context_dict['error_message'] = 'You have already applied to this experiment.'
        return render_to_response('maximatch/applied_experiment.html', context_dict, context)

    except Application.DoesNotExist:
        pass

    application = Application(participant=participant, experiment=experiment, status='Waiting for confirmation')
    application.save()

    success = True
    context_dict = {'success': success}

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('maximatch/applied_experiment.html', context_dict, context)

def register(request):
    context = RequestContext(request)

    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        participant_form = ParticipantForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and participant_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            participant = participant_form.save(commit=False)
            participant.user = user

            participant.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, participant_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        participant_form = ParticipantForm()

    # Render the template depending on the context.
    return render_to_response(
            'maximatch/register.html', {
                        'user_form': user_form, 
                        'participant_form': participant_form, 
                        'registered': registered
                    },
                    context)


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/maximatch/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Maxi-Match account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('maximatch/login.html', {}, context)

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/maximatch/')

@login_required
def settings(request):
    context = RequestContext(request)

    user_id = request.user.id
    updated = False

    context_dict = {'user_id': user_id}

    try:
        # If we can't find, the .get() method raises a DoesNotExist exception.
        user = User.objects.get(id=user_id)
        # Adds our results list to the template context under name pages.
        context_dict['user'] = user

        try:
            participant = Participant.objects.get(user=user)
        except Participant.DoesNotExist:
            participant = None

        try:
            researcher = Researcher.objects.get(user=user)
        except Researcher.DoesNotExist:
            researcher = None

    except User.DoesNotExist:
        # We get here if we didn't find the specified experiment.
        return render_to_response('maximatch/settings.html', context_dict, context)

    if participant is None:
        # Handling the case that the user is not a participant but a researcher
        if request.POST:
            user_form = UserForm(data=request.POST, instance=user)
            researcher_form = ResearcherForm(data=request.POST, instance=researcher)
            if user_form.is_valid() and researcher_form.is_valid():

                user = user_form.save()

                user.set_password(user.password)
                user.save()

                researcher = researcher_form.save(commit=False)
                researcher.user = user

                researcher.save()

                updated = True
                
                context_dict['updated'] = updated
                context_dict['user_form'] = user_form
                context_dict['researcher_form'] = researcher_form

                return render_to_response('maximatch/settings.html', context_dict, context)

            else:
                print user_form.errors, researcher_form.errors

        else:
            user_form = UserForm(instance=user)
            researcher_form = ResearcherForm(instance=researcher)

        context_dict['user_form'] = user_form
        context_dict['researcher_form'] = researcher_form
        context_dict['updated'] = updated

        return render_to_response('maximatch/settings.html', context_dict, context)

    elif researcher is None:
        if request.POST:
            user_form = UserForm(data=request.POST, instance=user)
            participant_form = ParticipantForm(data=request.POST, instance=participant)
            if user_form.is_valid() and participant_form.is_valid():

                user = user_form.save()

                user.set_password(user.password)
                user.save()

                participant = participant_form.save(commit=False)
                participant.user = user

                participant.save()

                updated = True

                context_dict['updated'] = updated
                context_dict['user_form'] = user_form
                context_dict['participant_form'] = participant_form

                return render_to_response('maximatch/settings.html', context_dict, context)

            else:
                print user_form.errors, participant_form.errors

        else:
            user_form = UserForm(instance=user)
            participant_form = ParticipantForm(instance=participant)

        context_dict['user_form'] = user_form
        context_dict['participant_form'] = participant_form
        context_dict['updated'] = updated

        return render_to_response('maximatch/settings.html', context_dict, context)
