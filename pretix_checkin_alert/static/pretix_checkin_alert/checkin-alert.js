$(function() {
    "use strict";
    
    if (!$('#checkin-alert-settings-form').length) {
        return;  // Only run on our settings page
    }
    
    console.log('Check-in Alert JS loaded');
    
    // Handle placeholder button clicks
    $(document).on('click', '.placeholder-btn', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        var placeholder = $(this).data('placeholder');
        var target = $(this).data('target');
        
        console.log('Placeholder clicked:', placeholder, 'Target:', target);
        
        // Find the body field for this target
        var bodyField;
        if (target === 'redflag') {
            bodyField = document.getElementById('id_checkin_alert_redflag_body');
        } else if (target === 'blocked') {
            bodyField = document.getElementById('id_checkin_alert_blocked_body');
        }
        
        if (bodyField) {
            // Insert at cursor position
            if (bodyField.setSelectionRange) {
                var startPos = bodyField.selectionStart;
                var endPos = bodyField.selectionEnd;
                bodyField.value = bodyField.value.substring(0, startPos) + placeholder + bodyField.value.substring(endPos);
                bodyField.setSelectionRange(startPos + placeholder.length, startPos + placeholder.length);
            } else {
                bodyField.value += placeholder;
            }
            bodyField.focus();
        }
        return false;
    });
    
    // Handle preview tab clicks
    $(document).on('shown.bs.tab', 'a.preview-tab', function(e) {
        var templateType = $(this).data('template-type');
        var previewContainer = templateType === 'redflag' ? '#redflag-preview' : '#blocked-preview';
        var $container = $(previewContainer);
        
        console.log('Preview tab shown, type:', templateType);
        
        // Show loading
        $container.find('.preview-loading').removeClass('hidden');
        $container.find('.preview-content').addClass('hidden');
        
        // Gather form data
        var parentForm = $(this).closest('form');
        var previewUrl = parentForm.attr('mail-preview-url') || parentForm.attr('action');
        var token = parentForm.find('input[name=csrfmiddlewaretoken]').val();
        var dataString = 'action=preview&template_type=' + templateType + '&csrfmiddlewaretoken=' + token;
        
        // Add form fields
        parentForm.find('input[type=text], textarea').each(function() {
            if ($(this).attr('name')) {
                dataString += '&' + $(this).serialize();
            }
        });
        
        console.log('Sending preview request to:', previewUrl);
        
        // Send AJAX request
        $.ajax({
            type: 'POST',
            url: previewUrl,
            data: dataString,
            dataType: 'json',
            success: function(response) {
                console.log('Preview response:', response);
                
                $container.find('.preview-subject-text').text(response.subject || 'No subject');
                $container.find('.preview-body-html').html(response.body_html || '<pre>' + (response.body || 'No content') + '</pre>');
                
                $container.find('.preview-loading').addClass('hidden');
                $container.find('.preview-content').removeClass('hidden');
            },
            error: function(xhr) {
                console.error('Preview error:', xhr);
                
                $container.find('.preview-subject-text').text('Error generating preview');
                $container.find('.preview-body-html').html('<p class="text-danger">Failed to generate preview</p>');
                
                $container.find('.preview-loading').addClass('hidden');
                $container.find('.preview-content').removeClass('hidden');
            }
        });
    });
});