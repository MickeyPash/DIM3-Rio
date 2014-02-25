import os

# Definig population script
def populate():
    #Adding a Researcher
    mickey = add_researcher(name = 'Mickey',
				email = 'pashov.m@gmail.com',
				password = '123456',
				matriculation_id = '1005139')

    # Adding a Participant
    bruno = add_participant(name = 'Bruno',
			email = 'bruno@developer.com',
			password = 'coolbeans',
     			matriculation_id = '2105470',
     			nationality = 'BR',
     			date_of_birth = '1990-05-22',
	 		mobile_number = '08457642359',
	 		telephone_number = '5555555555',
	 		gender = 'M',
	 		first_language = 'Portuguese',
	 		education_level = 'Bachelor')

    # Adding an Experiment
    test = add_experiment(title = 'Test Experiment',
			  short_description = 'This is a test experiment.',
			  description = "It will be used as a way of populating our database. Don't forget that models and the population scrip are tightly coupled",
     			  participants_needed = 20,
     			  status = 'Closed',
     			  location = '58 Hillhead Street, Waiting Room',
      			  duration = '24 hours',
      			  payment_cash = 25.00,
      		     	  payment_credit = 2,
      			  payment_other = 'Ice cream',
      			  start_date = '2014-03-22',
      			  end_date = '2014-04-01',
      			  published = '2014-02-23 22:15:09',
      			  researcher = mickey)
    # Add application
    app = add_application(participant = bruno, experiment = test, status = 'Email sent')

# Defining the add functions for our models
def add_researcher(name, email, password, matriculation_id):

    r = Researcher.objects.get_or_create(name = name, email = email, password = password, matriculation_id = matriculation_id)[0]
    return r

def add_participant(name, email, password, matriculation_id, nationality, date_of_birth,
	 mobile_number, telephone_number, gender, first_language, education_level):

     p = Participant.objects.get_or_create(name = name, email = email, password = password,
     matriculation_id = matriculation_id, nationality = nationality, date_of_birth = date_of_birth,
	 mobile_number = mobile_number, telephone_number = telephone_number, gender = gender, first_language = first_language, education_level = education_level)[0]
     return p

def add_experiment(title, short_description, description, participants_needed, status,
	 location, duration, payment_cash, payment_credit, payment_other, start_date, end_date, published, researcher):
    e = Experiment.objects.get_or_create(title = title, short_description = short_description, description = description,
    participants_needed = participants_needed, status = status, location = location,
    duration = duration, payment_cash = payment_cash, payment_credit = payment_credit, payment_other = payment_other,
    start_date = start_date, end_date = end_date, published = published, researcher = researcher)[0]
    return e

def add_application(participant, experiment, status):
    a = Application.objects.get_or_create(participant = participant, experiment = experiment, status = status)[0]
    return a

# Start execution here!
if __name__ == '__main__':
    print "Starting MaxiMatch population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team_zeta_project.settings')
    from maximatch.models import Researcher, Participant, Experiment, Application
    populate()
