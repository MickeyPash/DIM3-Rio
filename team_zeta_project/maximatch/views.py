from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from maximatch.models import Experiment

# Create your views here.

def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    experiment_list = Experiment.objects.all()
    context_dict = {'experiments': experiment_list}

    for experiment in experiment_list:
        experiment.url = experiment.title.replace(' ', '_')

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('maximatch/index.html', context_dict, context)

def experiment(request, experiment_title_url):
    context = RequestContext(request)

    # Change underscores in the category name to spaces.
    experiment_title = experiment_title_url.replace('_', ' ')

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
