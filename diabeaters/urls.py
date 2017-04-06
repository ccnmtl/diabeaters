import django.contrib.auth.views
import django.views.static
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from diabeaters.main.views import (
    index, export, import_, flatpage_hack, home, edit_page,
    instructor_page, page,
)
admin.autodiscover()


urlpatterns = [
    url(r'^$', index),
    url(r'^_impersonate/', include('impersonate.urls')),
    url(r'^export/$', export),
    url(r'^import/$', import_),
    url(r'^about/$', flatpage_hack),
    url(r'^credits/$', flatpage_hack),
    url(r'^contact/$', flatpage_hack),

    url(r'^home/$', home),
    url(r'^logout/$', django.contrib.auth.views.logout,
        {'next_page': '/home/'}),
    url('^accounts/', include('djangowind.urls')),
    url(r'^smoketest/', include('smoketest.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pagetree/', include('pagetree.urls')),
    url(r'^quiz/', include('diabeaters.quiz.urls')),
    url(r'^health-habit-plan/', include('diabeaters.healthhabitplan.urls')),
    url(r'^uploads/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^_stats/', TemplateView.as_view(template_name="main/stats.html")),
    # very important that these three stay last and in this order
    url(r'^edit/(?P<path>.*)$', edit_page),
    url(r'^instructor/(?P<path>.*)$', instructor_page),
    url(r'^(?P<path>.*)$', page),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
