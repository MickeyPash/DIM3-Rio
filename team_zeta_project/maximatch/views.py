from django.template import RequestContext
from django.shortcuts import render_to_response
from maximatch.models import Experiment, Participant, Researcher, Application
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from maximatch.forms import ExperimentForm, ParticipantForm, UserForm, \
    ResearcherForm, ParticipantFullForm, ApplicationForm

# Create your views here.


def encode_url(url):
    # Change underscores in the category name to spaces.
    return url.replace(' ', '_')


def decode_url(url):
    return url.replace('_', ' ')


def is_researcher(user_id=None):
    try:
        # If we can't find, the .get() method raises a DoesNotExist exception.
        user = User.objects.get(id=user_id)
        try:
            Researcher.objects.get(user=user)
            return True
        except Researcher.DoesNotExist:
            pass
    except:
        pass
    return False


def count_participants(experiment=None):
    try:
        num = Application.objects.filter(experiment=experiment).count()
    except:
        num = 0
    return num


def index(request):
    context = RequestContext(request)

    experiment_list = Experiment.objects.filter(status='Open to applicants',)
    context_dict = {'experiments': experiment_list}

    if experiment_list:
        for experiment in experiment_list:
            experiment.url = encode_url(experiment.title)
            experiment.num_participants = count_participants(experiment)

    if is_researcher(request.user.id):
        context_dict['is_researcher'] = True

    return render_to_response('maximatch/index.html', context_dict, context)


def restricted(request):
    context = RequestContext(request)
    return render_to_response('maximatch/restricted.html', {}, context)


def experiment(request, experiment_title_url):
    context = RequestContext(request)

    experiment_title = decode_url(experiment_title_url)

    context_dict = {'experiment_title': experiment_title}

    applied = False

    try:
        experiment = Experiment.objects.get(title=experiment_title)

        experiment.url = encode_url(experiment.title)
        experiment.num_participants = count_participants(experiment)

        context_dict['experiment'] = experiment

    except Experiment.DoesNotExist:
        experiment = None
        pass
    if not is_researcher(request.user.id) and experiment:
        try:
            user = User.objects.get(id=request.user.id)
            participant = Participant.objects.get(user=user)
            Application.objects.get(participant=participant,
                                    experiment=experiment)
            applied = True
        except (Application.DoesNotExist, Participant.DoesNotExist,
                User.DoesNotExist):
            applied = False

    context_dict['applied'] = applied

    return render_to_response('maximatch/experiment.html', context_dict,
                              context)


@login_required
def add_experiment(request):
    context = RequestContext(request)

    if not is_researcher(request.user.id):
        return restricted(request)

    if request.method == 'POST':
        form = ExperimentForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)
        else:
            # The supplied form contained errors - print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = ExperimentForm()

    context_dict = {'form': form}

    return render_to_response('maximatch/add_experiment.html', context_dict,
                              context)


@login_required
def edit_experiment(request, experiment_title_url=None):
    context = RequestContext(request)

    if not is_researcher(request.user.id):
        return restricted(request)

    experiment_title = decode_url(experiment_title_url)

    context_dict = {'experiment_title': experiment_title}

    try:
        experiment = Experiment.objects.get(title=experiment_title)
        experiment.url = encode_url(experiment.title)

        context_dict['experiment'] = experiment

    except Experiment.DoesNotExist:
        # We get here if we didn't find the specified experiment.
        return render_to_response('maximatch/edit_experiment.html',
                                  context_dict, context)

    if request.POST:
        form = ExperimentForm(request.POST, instance=experiment)
        if form.is_valid():
            form.save()

            # If the save was successful, redirect to the details page
            encoded_url = encode_url(form.cleaned_data['title'])
            return HttpResponseRedirect('/maximatch/experiment/' + encoded_url)

        else:
            print form.errors

    else:
        form = ExperimentForm(instance=experiment)

    context_dict['form'] = form

    return render_to_response('maximatch/edit_experiment.html', context_dict,
                              context)


@login_required
def apply_experiment(request, experiment_title_url=None):

    success = False
    context_dict = {'success': success}

    user_id = request.user.id

    try:
        user = User.objects.get(id=user_id)
        decoded_url = decode_url(experiment_title_url)
        experiment = Experiment.objects.get(title=decoded_url)
        experiment.url = encode_url(experiment.title)
        participant = Participant.objects.get(user=user)
    except (Experiment.DoesNotExist, User.DoesNotExist,
            Participant.DoesNotExist):
        context_dict['error_message'] = 'Participant or experiment does not '\
                                        'exist.'
        return HttpResponseRedirect('/maximatch/experiment/%s/' %
                                    experiment.url)

    try:
        application = Application.objects.get(participant=participant,
                                              experiment=experiment)
        context_dict['error_message'] = 'You have already applied to this '\
                                        'experiment.'
        context_dict['applied'] = True

        return HttpResponseRedirect('/maximatch/experiment/%s/' %
                                    experiment.url)

    except Application.DoesNotExist:
        pass

    application = Application(participant=participant, experiment=experiment,
                              status='Waiting for confirmation')
    application.save()

    success = True
    context_dict = {'success': success}

    return HttpResponseRedirect('/maximatch/experiment/%s/' % experiment.url)


@login_required
def update_application_status(request):

    application_id = None
    response = False
    if request.method == 'POST':
        application_id = request.POST['application_id']
        new_status = request.POST['status']

    if application_id:
        application = Application.objects.get(id=int(application_id))
        if application:
            application.status = new_status
            application.save()
            response = True

    return HttpResponse(response)


@login_required
def view_participants(request, experiment_title_url=None):
    context = RequestContext(request)

    if not is_researcher(request.user.id):
        return restricted(request)

    experiment_title = decode_url(experiment_title_url)

    context_dict = {'experiment_title': experiment_title}

    try:
        experiment = Experiment.objects.get(title=experiment_title)
        experiment.url = encode_url(experiment.title)
        applications = Application.objects.filter(experiment=experiment)

        context_dict['experiment'] = experiment
        context_dict['applications'] = applications
        update_application_form = ApplicationForm()
        update_application_form.choices = Application.STATUS_CHOICES
        context_dict['update_application_form'] = update_application_form

    except Experiment.DoesNotExist:
        # We get here if we didn't find the specified experiment.
        applications = None
        context_dict['error_message'] = 'Experiment does not exist'

    return render_to_response('maximatch/view_participants.html', context_dict,
                              context)

    if request.POST:
        form = ExperimentForm(request.POST, instance=experiment)
        if form.is_valid():
            form.save()

            # If the save was successful, redirect to the details page
            encoded_url = encode_url(form.cleaned_data['title'])
            return HttpResponseRedirect('/maximatch/experiment/' + encoded_url)

        else:
            print form.errors

    else:
        form = ExperimentForm(instance=experiment)

    context_dict['form'] = form

    return render_to_response('maximatch/view_participants.html', context_dict,
                              context)


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

            # Delays saving model until we're ready avoiding integrity issues
            participant = participant_form.save(commit=False)
            participant.user = user

            participant.save()

            # Tell the template registration was successful
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

    return render_to_response('maximatch/register.html', {
        'user_form': user_form, 'participant_form': participant_form,
        'registered': registered},
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
        # If None, no user
        # with matching credentials was found.
        if user is not None:
            if user.is_active:
                login(request, user)

                return HttpResponseRedirect('/maximatch/')

            else:
                context_dict = {'error_message': 'Your Maxi-Match account ' +
                                'is disabled.'}
                return render_to_response('maximatch/login.html', context_dict,
                                          context)

        else:
            # Bad login details were provided. So we can't log the user in.
            context_dict = {'error_message': 'Invalid login details supplied.'}
            return render_to_response('maximatch/login.html', context_dict,
                                      context)

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
        return render_to_response('maximatch/settings.html', context_dict,
                                  context)

    if participant is None:
        # Handling the case that the user is not a participant but a researcher
        if request.POST:
            user_form = UserForm(data=request.POST, instance=user)
            researcher_form = ResearcherForm(data=request.POST,
                                             instance=researcher)
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

                return render_to_response('maximatch/settings.html',
                                          context_dict, context)

            else:
                print user_form.errors, researcher_form.errors

        else:
            user_form = UserForm(instance=user)
            researcher_form = ResearcherForm(instance=researcher)

        context_dict['user_form'] = user_form
        context_dict['researcher_form'] = researcher_form
        context_dict['updated'] = updated

        return render_to_response('maximatch/settings.html', context_dict,
                                  context)

    elif researcher is None:
        if request.POST:
            user_form = UserForm(data=request.POST, instance=user)
            participant_form = ParticipantFullForm(data=request.POST,
                                                   instance=participant)
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

                return render_to_response('maximatch/settings.html',
                                          context_dict, context)

            else:
                print user_form.errors, participant_form.errors

        else:
            user_form = UserForm(instance=user)
            participant_form = ParticipantFullForm(instance=participant)

        context_dict['user_form'] = user_form
        context_dict['participant_form'] = participant_form
        context_dict['updated'] = updated

        return render_to_response('maximatch/settings.html', context_dict,
                                  context)
