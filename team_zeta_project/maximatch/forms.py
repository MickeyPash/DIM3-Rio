from django import forms
from maximatch.models import Experiment, Researcher, Participant, Application
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget


class ExperimentForm(forms.ModelForm):
    title = forms.CharField(max_length=70)
    description = forms.CharField(max_length=1024, widget=forms.Textarea)
    participants_needed = forms.IntegerField()
    short_description = forms.CharField(max_length=145)
    status = forms.ChoiceField(choices=Experiment.STATUS_CHOICES)
    location = forms.CharField(max_length=128)
    duration = forms.CharField(max_length=20)
    payment_cash = forms.DecimalField(decimal_places=2, max_digits=7)
    payment_credit = forms.IntegerField()
    payment_other = forms.CharField(max_length=128)
    start_date = forms.DateField(widget=SelectDateWidget())
    end_date = forms.DateField(widget=SelectDateWidget())
    researcher = forms.ModelChoiceField(queryset=Researcher.objects.all())

    class Meta:
        model = Experiment
        # Removes the published field
        fields = ('title', 'short_description', 'description',
                  'participants_needed', 'status', 'location', 'duration',
                  'payment_cash', 'payment_credit', 'payment_other',
                  'start_date', 'end_date', 'researcher')


class ResearcherForm(forms.ModelForm):
    class Meta:
        model = Researcher
        fields = ('matriculation_id',)


class ApplicationForm(forms.ModelForm):
    status = Application.STATUS_CHOICES

    class Meta:
        model = Application
        fields = ('status',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ()


class ParticipantFullForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ('matriculation_id', 'nationality', 'date_of_birth',
                  'mobile_number', 'telephone_number', 'gender',
                  'first_language', 'education_level')
