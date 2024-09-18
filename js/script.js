jQuery(document).ready(function($) {
    $('#cmp-save-button').on('click', function() {
        var data = [];
        $('.cmp-data-table tbody tr').each(function() {
            var index = $(this).find('.cmp-called-checkbox').data('index');
            var phoneNumber = $(this).find('td:eq(0)').text();
            var called = $(this).find('.cmp-called-checkbox').is(':checked');
            var notes = $(this).find('.cmp-notes-input').val();
            data.push({ 'Phone Number': phoneNumber, 'Called': called, 'Notes': notes });
        });
        $.ajax({
            url: ajaxurl,
            type: 'POST',
            data: {
                action: 'cmp_save_changes',
                cmp_data: JSON.stringify(data)
            },
            success: function(response) {
                alert('Data saved successfully.');
            },
            error: function() {
                alert('Error saving data.');
            }
        });
    });
});
