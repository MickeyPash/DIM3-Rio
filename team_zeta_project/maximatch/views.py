from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from maximatch.models import Experiment, Participant, Researcher, Application
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
from maximatch.forms import ExperimentForm, ParticipantForm, UserForm, ResearcherForm, ParticipantFullForm

def encode_url(url):
    # Change underscores in the category name to spaces.
    return url.replace(' ', '_')

def decode_url(url):
    return url.replace('_', ' ')

def index(request):
    context = RequestContext(request)

    experiment_list = Experiment.objects.all()
    context_dict = {'experiments': experiment_list}

    for experiment in experiment_list:
        experiment.url = encode_url(experiment.title)

    return render_to_response('maximatch/index.html', context_dict, context)

def experiment(request, experiment_title_url):
    context = RequestContext(request)

    experiment_title = decode_url(experiment_title_url)

    context_dict = {'experiment_title': experiment_title}

    try:
        experiment = Experiment.objects.get(title=experiment_title)

        experiment.url = encode_url(experiment.title)

        context_dict['experiment'] = experiment

    except Experiment.DoesNotExist:
        pass

    return render_to_response('maximatch/experiment.html', context_dict, context)

def add_experiment(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = ExperimentForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = ExperimentForm()

    return render_to_response('maximatch/add_experiment.html', {'form': form}, context)

@login_required
def edit_experiment(request, experiment_title_url=None):
    context = RequestContext(request)

    experiment_title = decode_url(experiment_title_url)

    context_dict = {'experiment_title': experiment_title}

    try:
        experiment = Experiment.objects.get(title=experiment_title)
        experiment.url = encode_url(experiment.title)

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

    return render_to_response('maximatch/applied_experiment.html', context_dict, context)

def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        participant_form = ParticipantForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and participant_form.is_valid():
            user = user_form.save()

            # Once hashed, update the user object.
            user.set_password(user.password)
            user.save()

            # This delays saving the model until we're ready to avoid integrity problems.
            participant = participant_form.save(commit=False)
            participant.user = user

            participant.save()

            # Update our variable to tell the template registration was successful.
            registered = True

            user.password = user_form.cleaned_data['password']
            user = authenticate(username=user.username, password=user.password)
            login(request, user)
            return HttpResponseRedirect("/maximatch/")

        else:
            print user_form.errors, participant_form.errors

    else:
        user_form = UserForm()
        participant_form = ParticipantForm()

    return render_to_response(
            'maximatch/register.html', {
                        'user_form': user_form, 
                        'participant_form': participant_form, 
                        'registered': registered
                    },
                    context)


def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/maximatch/')

            else:
                context_dict = { 'error_message': 'Your Maxi-Match account is disabled.'}
                return render_to_response('maximatch/login.html', context_dict, context)

        else:
            # Bad login details were provided. So we can't log the user in.
            context_dict = { 'error_message': 'Invalid login details supplied.'}
            return render_to_response('maximatch/login.html', context_dict, context)

    else:
        return render_to_response('maximatch/login.html', {}, context)

@login_required
def user_logout(request):

    logout(request)

    return HttpResponseRedirect('/maximatch/')

@login_required
def settings(request):
    context = RequestContext(request)

    user_id = request.user.id
    updated = False

    context_dict = {'user_id': user_id}

    try:
        user = User.objects.get(id=user_id)
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
            participant_form = ParticipantFullForm(data=request.POST, instance=participant)
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
            participant_form = ParticipantFullForm(instance=participant)

        context_dict['user_form'] = user_form
        context_dict['participant_form'] = participant_form
        context_dict['updated'] = updated

        return render_to_response('maximatch/settings.html', context_dict, context)
