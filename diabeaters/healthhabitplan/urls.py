from django.conf.urls.defaults import patterns


urlpatterns = patterns(
    'diabeaters.healthhabitplan.views',
    (r'^$', 'index', {}, 'health-habit-plan-index'),
    (r'^new_session/$', 'new_session', {}, 'health-habit-plan-new-session'),
    (r'^del_session/(?P<id>\d+)/$', 'del_session', {},
     'health-habit-plan-del-session'),
    (r'^all_sessions/$', 'all_sessions', {}, 'health-habit-plan-all-sessions'),
    (r'^session/(?P<id>\d+)/$', 'session', {}, 'health-habit-plan-session'),
    (r'^session/(?P<id>\d+)/save_magnet/$', 'save_magnet', {},
     'health-habit-plan-save-magnet'),
    (r'^session/(?P<id>\d+)/delete_magnet/$', 'delete_magnet', {},
     'health-habit-plan-delete-magnet'),
)
