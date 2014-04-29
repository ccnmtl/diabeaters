from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
import os.path
admin.autodiscover()


site_media_root = os.path.join(os.path.dirname(__file__), "../media")

urlpatterns = patterns(
    '',
    (r'^$', 'diabeaters.main.views.index'),
    url(r'^_impersonate/', include('impersonate.urls')),
    (r'^export/$', 'diabeaters.main.views.export'),
    (r'^import/$', 'diabeaters.main.views.import_'),
    (r'^about/$', 'diabeaters.main.views.flatpage_hack'),
    (r'^credits/$', 'diabeaters.main.views.flatpage_hack'),
    (r'^contact/$', 'diabeaters.main.views.flatpage_hack'),

    (r'^home/$', 'diabeaters.main.views.home'),
    (r'^logout/$', 'django.contrib.auth.views.logout',
     {'next_page': '/home/'}),
    ('^accounts/', include('djangowind.urls')),
    (r'^smoketest/', include('smoketest.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^pagetree/', include('pagetree.urls')),
    (r'^quiz/', include('diabeaters.quiz.urls')),
    (r'^health-habit-plan/', include('diabeaters.healthhabitplan.urls')),
    (r'^site_media/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': site_media_root}),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^_stats/', TemplateView.as_view(template_name="main/stats.html")),
    # very important that these three stay last and in this order
    (r'^edit/(?P<path>.*)$', 'diabeaters.main.views.edit_page'),
    (r'^instructor/(?P<path>.*)$', 'diabeaters.main.views.instructor_page'),
    (r'^(?P<path>.*)$', 'diabeaters.main.views.page'),
)
