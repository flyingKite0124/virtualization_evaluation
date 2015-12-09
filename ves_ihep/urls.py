from django.conf.urls import patterns, url
from ves_ihep import views

urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		url(r'^add_new_scene/$', views.add_new_scene, name='add_new_scene'),
		url(r'^delete_scene/$', views.delete_scene, name='delete_scene'),
		url(r'^show_scenes/$', views.show_scenes, name='show_scenes'),
		url(r'^hostpool/$', views.hostpool, name='hostpool'),
		url(r'^add_host/$', views.add_host, name='add_host'),
		url(r'^get_status/$', views.get_status, name='get_status'),
		url(r'^delete_host/$', views.delete_host, name='delete_host'),
		url(r'^scriptpool/$', views.scriptpool, name='scriptpool'),
		url(r'^add_script/$', views.add_script, name='add_script'),
		url(r'^delete_script/$', views.delete_script, name='delete_script'),
		url(r'^add_activity/$', views.add_activity, name='add_activity'),
		url(r'^view_activity/$', views.view_activity, name='view_activity'),
		url(r'^delete_activity/$', views.delete_activity, name='delete_activity'),
		url(r'^rename_activity/$', views.rename_activity, name='rename_activity'),
		url(r'^get_activity/$', views.get_activity, name='get_activity'),
		url(r'^deploy/$', views.deploy, name='deploy'),
		url(r'^view_result/$', views.view_result, name='view_result'),
		url(r'^evaresult/$', views.evaresult, name='evaresult'),
		)
