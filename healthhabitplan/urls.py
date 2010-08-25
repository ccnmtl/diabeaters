from django.conf.urls.defaults import patterns


urlpatterns = patterns('healthhabitplan.views',
                       (r'^$', 'index',{},'health-habit-plan-index'),
)
