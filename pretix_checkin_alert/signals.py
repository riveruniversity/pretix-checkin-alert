from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from pretix.control.signals import nav_event_settings


@receiver(nav_event_settings, dispatch_uid='checkin_alert_nav_settings')
def add_settings_nav_item(sender, request, **kwargs):
    """Add Check-in Alert settings to the event settings navigation"""
    url = reverse('plugins:pretix_checkin_alert:settings', kwargs={
        'organizer': request.event.organizer.slug,
        'event': request.event.slug
    })
    return [{
        'label': _('Check-in Alerts'),
        'icon': 'bell',
        'url': url,
        'active': request.resolver_match.url_name == 'settings' and 
                  request.resolver_match.namespace == 'plugins:pretix_checkin_alert',
    }]
