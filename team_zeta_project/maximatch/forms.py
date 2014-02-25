from django import forms
from maximatch.models import Experiment, Researcher

class ExperimentForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Title")
    short_description = forms.CharField(max_length=45, help_text="Short decription")
    description = forms.CharField(max_length=1024, help_text="Full description")
    participants_needed = forms.IntegerField(help_text="Participants needed")
    status = forms.ChoiceField(help_text="Status", choices=Experiment.STATUS_CHOICES)
    location = forms.CharField(max_length=128, help_text="Location")
    duration = forms.CharField(max_length=20, help_text="Duration")
    payment_cash = forms.DecimalField(decimal_places=2,max_digits=7, help_text="Payment cash")
    payment_credit = forms.IntegerField(help_text="Payment credits")
    payment_other = forms.CharField(max_length=128, help_text="Payment (other)")
    start_date = forms.DateField(help_text="Start date")
    end_date = forms.DateField(help_text="End date")
    published = forms.DateTimeField(help_text="Published")
    researcher = forms.ModelChoiceField(help_text="Researcher", queryset=Researcher.objects.all())

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Experiment
