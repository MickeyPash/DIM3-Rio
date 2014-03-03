from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from maximatch.models import Experiment

# Create your views here.
from maximatch.forms import ExperimentForm

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