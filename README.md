# Pretix Check-in Alert Plugin

Real-time email alerts for security-sensitive check-in events in pretix.

## Features

- **Red Flag Alerts**: Automatically send email notifications when attendees with red flags check in
- **Blocked Ticket Alerts**: Immediate notifications when someone attempts to check in with a blocked ticket
- **Customizable Email Templates**: Full control over email content with markdown support
- **Multiple Recipients**: Send alerts to multiple email addresses
- **Live Preview**: Preview emails before saving with actual placeholder data

## Installation

1. Install the plugin:
```bash
pip install pretix-checkin-alert
```

2. Enable the plugin in your pretix event settings:
   - Go to Settings → Plugins
   - Enable "Check-in Alert System"

## Configuration

1. Navigate to your event settings → Check-in Alerts
2. Enable check-in alert notifications
3. Configure notification recipients (comma-separated email addresses)
4. Customize email templates for:
   - Red flag check-ins
   - Blocked ticket attempts

### Red Flag Setup

To use red flag functionality:
1. Create a question with identifier `red_flags` 
2. Mark it as hidden (admin-only)
3. Add notes to attendees who need special attention

### Available Placeholders

- `{event_name}` - Event name
- `{attendee_name}` - Attendee name  
- `{attendee_email}` - Attendee email
- `{order_code}` - Order code
- `{product}` - Product/ticket name
- `{variation}` - Product variation
- `{checkin_time}` - Check-in timestamp
- `{checkin_list}` - Check-in list name
- `{flag_reasons}` - List of alert reasons

## Development

### Setup

```bash
git clone https://github.com/river-creative/pretix-checkin-alert.git
cd pretix-checkin-alert
pip install -e .
```

### Running Tests

```bash
pytest
```

## License

Apache License 2.0

## Support

For issues and feature requests, please use the [GitHub issue tracker](https://github.com/river-creative/pretix-checkin-alert/issues).

## Author

River Creative - creative@revival.com