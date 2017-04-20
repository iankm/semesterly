from django.conf.urls import patterns, include, url
from django.http import HttpResponse
from django.conf import settings
from django.contrib import admin
from dashing.utils import router

from analytics.widgets import *

router.register(NumberTimetablesWidget, 'number_timetables_widget')
router.register(NumberCalendarExportsWidget, 'number_calendar_exports_widget')
router.register(NumberFinalExamViewsWidget, 'number_final_exam_views_widget')
router.register(NumberSignupsWidget, 'number_signups_widget')
router.register(NumberFacebookAlertsViewsWidget, 'number_facebook_alerts_views_widget')
router.register(NumberFacebookAlertsClicksWidget, 'number_facebook_alerts_clicks_widget')


admin.autodiscover()

urlpatterns = patterns('',
    # app urls
    url('', include('timetable.urls')),
    url('', include('authpipe.urls')),
    url('', include('courses.urls')),
    url('', include('integrations.urls')),
    url('', include('exams.urls')),
    url('', include('searches.urls')),
    url('', include('student.urls')),
    url('', include('analytics.urls')),

    # home
    url(r'^$', 'timetable.views.view_timetable'),

    # about page
    url(r'about/*', 'timetable.views.about'),

    # press page
    url(r'press/*', 'timetable.views.press'),

    # Automatic deployment endpoint
    url(r'deploy_staging/', 'semesterly.views.deploy_staging'),

    url(r'^sw(.*.js)$', 'timetable.views.sw_js', name='sw_js'),
    url(r'^manifest(.*.json)$', 'timetable.views.manifest_json', name='manifest_json'),

    # for testing 404, so i don't have to turn off debug
    url(r'^404testing/', 'timetable.views.custom_404'),
    url(r'^500testing/', 'timetable.views.custom_500'),

    # dashboard
    url(r'^dashboard/', include(router.urls), name='dashboard'),
)

# profiling
urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]

if getattr(settings, 'STAGING', False):
    urlpatterns += patterns('', url(r'^robots.txt$',
                                    lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")))
else:
    urlpatterns += patterns('', url(r'^robots.txt$',
                                    lambda r: HttpResponse("User-agent: *\nDisallow:", content_type="text/plain")))
