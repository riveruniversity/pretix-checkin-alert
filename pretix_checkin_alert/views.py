from django import forms
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.template.loader import render_to_string
from pretix.base.forms import SettingsForm
from pretix.base.models import Event
from pretix.control.views.event import EventSettingsViewMixin, EventSettingsFormView
from pretix.base.templatetags.rich_text import markdown_compile_email


class CheckinAlertSettingsForm(SettingsForm):
    checkin_alert_enabled = forms.BooleanField(
        label=_("Enable check-in alert notifications"),
        help_text=_("Send email notifications when flagged attendees check in or blocked tickets attempt check-in"),
        required=False,
    )
    
    checkin_alert_notification_email = forms.CharField(
        label=_("Notification email address(es)"),
        help_text=_("Email address(es) to receive check-in alerts. Separate multiple addresses with commas."),
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "security@example.com, admin@example.com"
        })
    )
    
    checkin_alert_from_name = forms.CharField(
        label=_("From name"),
        help_text=_("The name that will appear in the From field of notification emails"),
        required=False,
        initial="Security Alert System",
        widget=forms.TextInput(attrs={
            "placeholder": "Security Alert System"
        })
    )
    
    # Red Flag Templates
    checkin_alert_redflag_subject = forms.CharField(
        label=_("Subject"),
        required=False,
        initial="[RED FLAG] Check-in Alert: {attendee_name} - {event_name}",
        widget=forms.TextInput(attrs={
            "placeholder": "[RED FLAG] {attendee_name} at {event_name}",
            "data-display-dependency": "#id_checkin_alert_enabled"
        })
    )
    
    checkin_alert_redflag_body = forms.CharField(
        label=_("Body"),
        required=False,
        widget=forms.Textarea(attrs={
            "rows": 10,
            "placeholder": "Use Markdown formatting...",
            "data-display-dependency": "#id_checkin_alert_enabled"
        }),
        initial="""# RED FLAG CHECK-IN ALERT

## Event Information
- **Event:** {event_name}
- **Check-in Time:** {checkin_time}
- **Check-in List:** {checkin_list}

## Attendee Information
- **Name:** {attendee_name}
- **Email:** {attendee_email}
- **Order:** {order_code}
- **Product:** {product}
- **Variation:** {variation}

## Alert Reasons
{flag_reasons}

---
*Please take appropriate action as per your event protocols.*"""
    )
    
    # Blocked Ticket Templates
    checkin_alert_blocked_subject = forms.CharField(
        label=_("Subject"),
        required=False,
        initial="[BLOCKED] Check-in DENIED: {attendee_name} - {event_name}",
        widget=forms.TextInput(attrs={
            "placeholder": "[BLOCKED] {attendee_name} at {event_name}",
            "data-display-dependency": "#id_checkin_alert_enabled"
        })
    )
    
    checkin_alert_blocked_body = forms.CharField(
        label=_("Body"),
        required=False,
        widget=forms.Textarea(attrs={
            "rows": 10,
            "placeholder": "Use Markdown formatting...",
            "data-display-dependency": "#id_checkin_alert_enabled"
        }),
        initial="""# ⚠️ BLOCKED CHECK-IN ATTEMPT ⚠️

**CHECK-IN WAS DENIED - BLOCKED TICKET**

## Event Information
- **Event:** {event_name}
- **Attempted Check-in Time:** {checkin_time}
- **Check-in List:** {checkin_list}

## Blocked Attendee Information
- **Name:** {attendee_name}
- **Email:** {attendee_email}
- **Order:** {order_code}
- **Product:** {product}
- **Variation:** {variation}

## Blocking Reasons
{flag_reasons}

---
**IMMEDIATE ACTION REQUIRED:** Security personnel should be aware of this denied entry attempt."""
    )
    
    def clean_checkin_alert_notification_email(self):
        value = self.cleaned_data.get("checkin_alert_notification_email", "")
        if value:
            emails = [email.strip() for email in value.split(",")]
            for email in emails:
                if "@" not in email or "." not in email:
                    raise forms.ValidationError(
                        _("Please enter valid email addresses separated by commas")
                    )
        return value


class CheckinAlertSettings(EventSettingsViewMixin, EventSettingsFormView):
    model = Event
    form_class = CheckinAlertSettingsForm
    template_name = "pretix_checkin_alert/settings.html"
    permission = "can_change_settings"
    
    def get_success_url(self):
        return reverse("plugins:pretix_checkin_alert:settings", kwargs={
            "organizer": self.request.event.organizer.slug,
            "event": self.request.event.slug
        })
    
    def post(self, request, *args, **kwargs):
        # Handle preview requests
        if request.POST.get("action") == "preview":
            return self.preview_email(request)
        return super().post(request, *args, **kwargs)
    
    def preview_email(self, request):
        """Generate email preview"""
        template_type = request.POST.get("template_type", "redflag")
        
        # Sample data for preview
        preview_data = {
            "event_name": self.request.event.name,
            "attendee_name": "John Doe",
            "attendee_email": "john.doe@example.com",
            "order_code": "ABC123",
            "product": "General Admission",
            "variation": "Early Bird",
            "checkin_time": "2024-01-15 14:30:00",
            "checkin_list": "Main Entrance",
            "flag_reasons": "- Red flag in hidden answer: Security concern noted\n- Previous incident reported"
        }
        
        if template_type == "blocked":
            subject = request.POST.get("checkin_alert_blocked_subject", "")
            body = request.POST.get("checkin_alert_blocked_body", "")
            preview_data["flag_reasons"] = "- BLOCKED TICKET - Check-in was DENIED\n- Ticket has been manually blocked by administrator"
        else:
            subject = request.POST.get("checkin_alert_redflag_subject", "")
            body = request.POST.get("checkin_alert_redflag_body", "")
        
        try:
            subject_preview = subject.format(**preview_data)
        except:
            subject_preview = "Error in template variables"
        
        try:
            body_preview = body.format(**preview_data)
            body_html = markdown_compile_email(body_preview)
        except:
            body_preview = "Error in template variables"
            body_html = "<p>Error in template variables</p>"
        
        return JsonResponse({
            "subject": subject_preview,
            "body": body_preview,
            "body_html": body_html
        })