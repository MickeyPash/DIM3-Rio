from django.conf.urls import patterns, url
from maximatch import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^add_experiment/$', views.add_experiment, name='add_experiment'),
        url(r'^apply_experiment/(?P<experiment_title_url>\w+)/$', views.apply_experiment, name='apply_experiment'),
        url(r'^view_participants/(?P<experiment_title_url>\w+)/$', views.view_participants, name='view_participants'),
        url(r'^experiment/(?P<experiment_title_url>\w+)/$', views.experiment, name='experiment'),
        url(r'^edit_experiment/(?P<experiment_title_url>\w+)/$', views.edit_experiment, name='edit_experiment'),
        url(r'^settings/$', views.settings, name='register'),
        url(r'^restricted/$', views.restricted, name='restricted'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
)
