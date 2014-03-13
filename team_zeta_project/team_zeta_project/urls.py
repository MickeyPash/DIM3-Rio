from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'team_zeta_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('maximatch.urls')), 
<<<<<<< HEAD
=======
    url(r'^maximatch/', include('maximatch.urls')), 
>>>>>>> 77ebf8de27e4a1cc2214868b7542fb7b1248ff96
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
