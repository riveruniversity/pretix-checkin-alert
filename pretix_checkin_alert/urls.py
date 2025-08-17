from django.urls import re_path

from .views import CheckinAlertSettings

urlpatterns = [
    re_path(
        r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/settings/checkin-alert/$',
        CheckinAlertSettings.as_view(),
        name='settings',
    ),
]