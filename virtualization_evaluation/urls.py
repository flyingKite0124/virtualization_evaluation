from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from virtualization_evaluation import views


urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'virtualization_evaluation.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^ves_ihep/', include('ves_ihep.urls')),
                       url(r'^$', views.redirect, name='redirect'),
                       )

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
         'serve',
         {'document_root': settings.MEDIA_ROOT}),)
