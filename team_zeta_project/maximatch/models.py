from django.db import models

# Create your models here.
class Researcher(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=128, blank=False)
    matriculation_id = models.CharField(max_length=7)

    def __unicode__(self):
        return self.name

class Participant(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    NATIONALITY_CHOICES = (
        ('United Kingdom', 'United Kingdom'),
        )
    FIRST_LANGUAGE_CHOICES = (
        ('United Kingdom', 'United Kingdom'),
    )
    EDUCATION_LEVEL_CHOICES = (
        ('High school', 'High school'),
    )
    name = models.CharField(max_length=128)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=128, blank=False)
    matriculation_id = models.CharField(max_length=7)
    nationality = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=11)
    telephone_number = models.CharField(max_length=11)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    first_language = models.CharField(max_length=45, choices=FIRST_LANGUAGE_CHOICES)
    education_level = models.CharField(max_length=45, choices=EDUCATION_LEVEL_CHOICES)

    def __unicode__(self):
        return self.name

class Experiment(models.Model):
    STATUS_CHOICES = (
        ('Closed', 'Closed'),
        ('Open to applicants', 'Open to applicants'),
    )
    short_description = models.CharField(max_length=45, blank=False)
    description = models.CharField(max_length=1024)
    participants_needed = models.IntegerField()
    status = models.CharField(max_length=45, choices=STATUS_CHOICES)
    location = models.CharField(max_length=128)
    duration = models.CharField(max_length=20)
    payment_cash = models.DecimalField(decimal_places=2,max_digits=7)
    payment_credit = models.IntegerField()
    payment_other = models.CharField(max_length=128)
    start_date = models.DateField()
    end_date = models.DateField()
    published = models.DateTimeField()
    researcher = models.ForeignKey(Researcher)

    def __unicode__(self):
        return self.short_description
class Application(models.Model):
    STATUS_CHOICES = (
        ('Email sent', 'Email sent'),
        ('Waiting for confirmation', 'Waiting for confirmation'),
        ('Refused', 'Refused'),
        ('Experiment done', 'Experiment done'),
    )
    participant = models.ForeignKey(Participant)
    experiment = models.ForeignKey(Experiment)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES)
