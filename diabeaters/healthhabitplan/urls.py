from django.conf.urls import url
from .views import (
    index, new_session, del_session, session, save_magnet, delete_magnet,
    all_sessions
)

urlpatterns = [
    url(r'^$', index, {}, 'health-habit-plan-index'),
    url(r'^new_session/$', new_session, {},
        'health-habit-plan-new-session'),
    url(r'^del_session/(?P<id>\d+)/$', del_session, {},
        'health-habit-plan-del-session'),
    url(r'^all_sessions/$', all_sessions, {},
        'health-habit-plan-all-sessions'),
    url(r'^session/(?P<id>\d+)/$', session, {}, 'health-habit-plan-session'),
    url(r'^session/(?P<id>\d+)/save_magnet/$', save_magnet, {},
        'health-habit-plan-save-magnet'),
    url(r'^session/(?P<id>\d+)/delete_magnet/$', delete_magnet, {},
        'health-habit-plan-delete-magnet'),
]
