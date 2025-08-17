from django.utils.translation import gettext_lazy as _

from . import __version__, PretixPluginMeta

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")


class PluginApp(PluginConfig):
    default = True
    name = "pretix_checkin_alert"
    verbose_name = "Check-in Alert System"

    class PretixPluginMeta:
        name = _("Check-in Alert System")
        author = "River Creative"
        description = _("Send real-time email alerts for security-sensitive check-in events, including red-flagged attendees and blocked ticket attempts")
        visible = True
        version = __version__
        category = "FEATURE"
        compatibility = "pretix>=4.0.0"
        
    def ready(self):
        from . import signals  # NOQA
        
    def installed(self, event):
        # Called when plugin is activated for an event
        pass
