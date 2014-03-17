from django.db import models
from django.contrib.auth.models import User

# Researcher - Participant - Experiment - Application


class Researcher(models.Model):
    # Name, email, first, last name and password fiels are used from
    # User built-in model, from the authentication app.
    matriculation_id = models.CharField(max_length=7)
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.username


class Participant(models.Model):
    # Name, email, first, last name and password fiels are used from
    # User built-in model, from the authentication app.
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    NATIONALITY_CHOICES = (
        ('GB', 'British'),
        ('BR', 'Brazilian'),
        ('BG', 'Bulgarian'),
    )
    FIRST_LANGUAGE_CHOICES = (
        ('English', 'English'),
        ('Portuguese', 'Portuguese'),
    )
    EDUCATION_LEVEL_CHOICES = (
        ('High school', 'High school'),
        ('Bachelor', 'Bachelor'),
    )
    matriculation_id = models.CharField(max_length=7)
    nationality = models.CharField(max_length=2, choices=NATIONALITY_CHOICES)
    date_of_birth = models.DateField(null=True)
    mobile_number = models.CharField(max_length=11)
    telephone_number = models.CharField(max_length=11)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    first_language = models.CharField(max_length=45,
                                      choices=FIRST_LANGUAGE_CHOICES)
    education_level = models.CharField(max_length=45,
                                       choices=EDUCATION_LEVEL_CHOICES)
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.username


class Experiment(models.Model):
    STATUS_CHOICES = (
        ('Closed', 'Closed'),
        ('Open to applicants', 'Open to applicants'),
    )
    title = models.CharField(max_length=128, blank=False)
    short_description = models.CharField(max_length=45, blank=False)
    description = models.CharField(max_length=1024)
    participants_needed = models.IntegerField()
    status = models.CharField(max_length=45, choices=STATUS_CHOICES)
    location = models.CharField(max_length=128)
    duration = models.CharField(max_length=20)
    payment_cash = models.DecimalField(decimal_places=2, max_digits=7)
    payment_credit = models.IntegerField()
    payment_other = models.CharField(max_length=128)
    start_date = models.DateField(null=True, blank=False)
    end_date = models.DateField(null=True, blank=False)
    # Having problems with this field, tried this format 2014-12-22 15:12:13
    # Changed on server side
    published = models.DateTimeField(null=True, blank=False)
    researcher = models.ForeignKey(Researcher)

    def __unicode__(self):
        return self.title


class Application(models.Model):
    STATUS_CHOICES = (
        ('Accepted ', 'Accepted'),
        ('Waiting for confirmation', 'Waiting for confirmation'),
        ('Refused', 'Refused'),
        ('Experiment done', 'Experiment done'),
    )
    participant = models.ForeignKey(Participant)
    experiment = models.ForeignKey(Experiment)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES)

    def __unicode__(self):
        return '\"' + self.participant.user.username + '\"' + \
               ' applied for \"' + self.experiment.short_description + '\"'
