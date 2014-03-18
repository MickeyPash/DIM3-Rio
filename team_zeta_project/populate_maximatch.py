import os
from datetime import datetime

# Definig population script
def populate():
    #Adding a Researcher
    user_mickey = add_user(username='mick',
                first_name='Mickey',
				email='pashov.m@gmail.com',
				password='1234',
                is_active=True)

    mickey = add_researcher(matriculation_id='1005139',
                user=user_mickey)

    #another researcher

    user_goofy = add_user(username='goofy',
                        first_name='Goofy',
                        email='goofy@disney.com',
                        password='1234',
                        is_active=True)

    goofy = add_researcher(matriculation_id='222558879',
                           user=user_goofy)
    #another researcher

    user_don = add_user(username='don',
                        first_name='Vito Corleone',
                        email='donvito@littleitaly.com',
                        password='1234',
                        is_active=True)

    don = add_researcher(matriculation_id='19720324',
                         user=user_don)

    # Adding a Participant

    user_bruno = add_user(username = 'bruno',
            first_name = 'Bruno',
			email = 'bruno@developer.com',
			password = '1234',
            is_active=True)

    bruno = add_participant(
     		matriculation_id = '2105470',
     		nationality = 'BR',
     		date_of_birth = '1990-05-22',
	 		mobile_number = '08457642359',
	 		telephone_number = '5555555555',
	 		gender = 'M',
	 		first_language = 'Portuguese',
	 		education_level = 'Bachelor',
            user = user_bruno)

    # another participant

    user_vader = add_user(username='lord_vader',
                           first_name='Anakin Skywalker',
                           email='vadder@republic.sith.galaxy',
                           password='1234',
                           is_active=True)

    vadder = add_participant(
     		matriculation_id = '6631200',
     		nationality = 'BR',
     		date_of_birth = '1976-12-21',
	 		mobile_number = '08457642359',
	 		telephone_number = '5555555555',
	 		gender = 'M',
	 		first_language = 'English',
	 		education_level = 'Bachelor',
            user = user_vader)


    # Adding an Experiment
    test = add_experiment(title = 'Test Experiment',
			  short_description = 'We are currently running a behavioural study to examine how visual information associated to the self or others influences visual perception.',
			  description = "It will be used as a way of populating our database. Don't forget that models and the population scrip are tightly coupled",
     		  participants_needed = 20,
     		  status = 'Open to applicants',
     		  location = '58 Hillhead Street, Waiting Room',
      		  duration = '24 hours',
      		  payment_cash = 25.00,
      		  payment_credit = 2,
      		  payment_other = 'Ice cream',
      		  start_date = '2014-03-22',
      		  end_date = '2014-04-01',
      		  published = '2014-02-23 22:15:09',
      		  researcher = mickey)

    # experiment number 2

    experiment2 = add_experiment(title = 'Abnormal Psychology',
                                 short_description='',
                                 description=' In this experiment, you will be presented with a series of words in different colours. Your task is to indicate the colour of each word as quickly as possible. There will be a practice block, followed by the actual experiment.',
                                 participants_needed=12,
                                 status='Open to applicants',
                                 location='Lab 6',
                                 duration='5 minutes',
                                 payment_cash=0.0,
                                 payment_credit=0,
                                 payment_other='none',
                                 start_date='2014-04-01',
                                 end_date='2014-04-09',
                                 published='2014-02-28 10:40:32',
                                 researcher=mickey)

    experiment3 = add_experiment(title='CANNABIS QUESTIONNAIRE',
                                 short_description='',
                                 description='We hold some general information about you but the experimenter of this study requests some additional information. This is because the results of this study might be influenced by specific factors.',
                                 participants_needed=50,
                                 status='Open to applicants',
                                 location='Lab 11',
                                 duration='10 minutes',
                                 payment_cash=10.0,
                                 payment_credit=0,
                                 payment_other='none',
                                 start_date='2014-04-02',
                                 end_date='2014-04-12',
                                 published='2014-03-15 14:12:23',
                                 researcher=goofy)

    experiment4 = add_experiment(title='Mental Health Questionnaire',
                                 short_description='',
                                 description='This short questionnaire will be regarding your mental health. The information obtained is treated confidentially. Based on the results of the questionnaire, you may be requested to come to the University of Glasgow Psychology department in order to complete short tasks.',
                                 participants_needed=40,
                                 status='Open to applicants',
                                 location='Lab 4',
                                 duration='15 minutes',
                                 payment_cash=12.0,
                                 payment_credit=2,
                                 payment_other='Ipad',
                                 start_date='2014-04-02',
                                 end_date='2014-04-12',
                                 published='2014-03-15 14:12:23',
                                 researcher=don)

    experiment5 = add_experiment(title='Trustworthiness of Voices',
                                 short_description='',
                                 description='There are two blocks of voices. In each block you will hear a series of 9 voices. For each voice, please rate how trustworthy it sounds, that is, how much you would be ready to trust that person. The whole experiment should take no more than 3 minutes.',
                                 participants_needed=80,
                                 status='Open to applicants',
                                 location='Lab 1',
                                 duration='3 minutes',
                                 payment_cash=4.0,
                                 payment_credit=4,
                                 payment_other='none',
                                 start_date='2014-05-22',
                                 end_date='2014-05-22',
                                 published='2014-03-11 08:43:58',
                                 researcher=don)

    # Add application
    app = add_application(participant = bruno, experiment = test, status = 'Waiting for confirmation')


# Defining the add functions for our models
def add_user(username, first_name, email, password, is_active):

    u = User.objects.get_or_create(username = username, first_name = first_name, email = email, password = password, is_active = is_active)[0]
    u.set_password(password)
    u.save()
    return u

def add_researcher(matriculation_id, user):

    r = Researcher.objects.get_or_create(matriculation_id = matriculation_id, user = user)[0]
    return r

def add_participant(matriculation_id, nationality, date_of_birth,
	 mobile_number, telephone_number, gender, first_language, education_level, user):

     p = Participant.objects.get_or_create(matriculation_id = matriculation_id, nationality = nationality, date_of_birth = date_of_birth,
	 mobile_number = mobile_number, telephone_number = telephone_number, gender = gender, first_language = first_language, education_level = education_level, user = user)[0]
     return p

def add_experiment(title, short_description, description, participants_needed, status,
	 location, duration, payment_cash, payment_credit, payment_other, start_date, end_date, published, researcher):
    e = Experiment.objects.get_or_create(title = title, short_description = short_description, description = description,
    participants_needed = participants_needed, status = status, location = location,
    duration = duration, payment_cash = payment_cash, payment_credit = payment_credit, payment_other = payment_other,
    start_date = start_date, end_date = end_date, published = published, researcher = researcher)[0]
    return e

def add_application(participant, experiment, status):
    a = Application.objects.get_or_create(participant = participant, experiment = experiment, status = status, applied_on = datetime.now())[0]
    return a

# Start execution here!
if __name__ == '__main__':
    print "Starting MaxiMatch population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team_zeta_project.settings')
    from maximatch.models import Researcher, Participant, Experiment, Application
    from django.contrib.auth.models import User
    populate()
