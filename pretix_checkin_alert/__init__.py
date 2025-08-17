from django.utils.translation import gettext_lazy as _

__version__ = "0.0.1"

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")


class PretixPluginMeta:
    name = _("Check-in Alert System")
    author = "River Creative"
    description = _("Send real-time email alerts for security-sensitive check-in events, including red-flagged attendees and blocked ticket attempts")
    visible = True
    version = __version__
    category = "FEATURE"
    compatibility = "pretix>=4.0.0"
