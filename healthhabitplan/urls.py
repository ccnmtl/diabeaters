from django.conf.urls.defaults import patterns


urlpatterns = patterns('healthhabitplan.views',
                       (r'^$', 'index',{},'health-habit-plan-index'),
                       (r'^new_session/$','new_session',{},'health-habit-plan-new-session'),
                       (r'^session/(?P<id>\d+)/$','session',{},'health-habit-plan-session'),
)
