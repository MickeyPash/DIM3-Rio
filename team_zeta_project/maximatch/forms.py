from django import forms
from maximatch.models import Experiment, Researcher, Participant, Application
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from multiselectfield import MultiSelectField


class ExperimentForm(forms.ModelForm):
    title = forms.CharField(max_length=70)
    description = forms.CharField(max_length=1024, widget=forms.Textarea)
    participants_needed = forms.IntegerField()
    short_description = forms.CharField(max_length=145)
    status = forms.ChoiceField(choices=Experiment.STATUS_CHOICES)
    location = forms.CharField(max_length=128)
    duration = forms.CharField(max_length=20)
    payment_cash = forms.DecimalField(decimal_places=2, max_digits=7, required=False)
    payment_credit = forms.IntegerField(required=False)
    payment_other = forms.CharField(max_length=128, required=False)
    start_date = forms.DateField(widget=SelectDateWidget())
    end_date = forms.DateField(widget=SelectDateWidget())
    researcher = forms.ModelChoiceField(queryset=Researcher.objects.all())
    # Requirements
    required_nationalities = MultiSelectField(max_length=45, null=True,
                                            choices=Participant.NATIONALITY_CHOICES)
    minimum_age = forms.IntegerField(required=False, widget=forms.TextInput(
                                attrs={'placeholder': 'Leave empty for not required'}))
    required_gender = MultiSelectField(choices=Participant.GENDER_CHOICES)
    required_first_language = forms.ChoiceField(required=True,
                                                choices=Participant.FIRST_LANGUAGE_CHOICES)
    required_education_level = MultiSelectField(
                                       choices=Participant.EDUCATION_LEVEL_CHOICES)

    class Meta:
        model = Experiment
        # Removes the published field
        fields = ('title', 'short_description', 'description',
                  'participants_needed', 'status', 'location', 'duration',
                  'payment_cash', 'payment_credit', 'payment_other',
                  'start_date', 'end_date', 'researcher',
                  'required_nationalities', 'minimum_age', 'required_gender',
                  'required_first_language', 'required_education_level')


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
        fields = ('date_of_birth',)


class ParticipantFullForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=SelectDateWidget(years=range(1920, 2014)))
    matriculation_id = forms.CharField(required=False, max_length=7)
    nationality = forms.ChoiceField(choices=Participant.NATIONALITY_CHOICES, required=False)
    mobile_number = forms.CharField(max_length=11, required=False)
    telephone_number = forms.CharField(max_length=11, required=False)
    gender = forms.ChoiceField(choices=Participant.GENDER_CHOICES, required=False)
    first_language = forms.ChoiceField(choices=Participant.FIRST_LANGUAGE_CHOICES, required=False)
    education_level = forms.ChoiceField(choices=Participant.EDUCATION_LEVEL_CHOICES, required=False)


    class Meta:
        model = Participant
        fields = ('matriculation_id', 'nationality', 'date_of_birth',
                  'mobile_number', 'telephone_number', 'gender',
                  'first_language', 'education_level')
