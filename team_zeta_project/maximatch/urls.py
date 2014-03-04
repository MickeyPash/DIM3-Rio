from django.conf.urls import patterns, url
from maximatch import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^add_experiment/$', views.add_experiment, name='add_experiment'),
        url(r'^experiment/(?P<experiment_title_url>\w+)/$', views.experiment, name='experiment'),
        url(r'^register/$', views.register, name='register'),
)
