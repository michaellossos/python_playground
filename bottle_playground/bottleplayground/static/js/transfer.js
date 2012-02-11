// Closure avoids polluting the global namespace
(function(window) {

    var log = ML.log;

    var setMessage = function(message) {
        // TODO Allow changing message colour
        $(".message_panel").html(message);
    };

    // returns: true if valid, false otherwise
    var validateFormData = function(formData) {
        if(ML.isUndefined(formData)) {
            throw 'Invalid parameter: formData was undefined.'
        }
        var message = '';
        $.each(formData, function(k, v) {
            if(ML.isUndefined(v) || ML.isEmpty(v)) {
                // TODO Nice error messages
                message = 'Please correct the invalid value in ' + k + '.';
                return false;
            }
        });
        // TODO Additional validation (amount > 0, from acct != to)
        setMessage(message);
        return ML.isEmpty(message);
    };

    var transferSuccess = function(data, textStatus, jqXHR) {
        setMessage('Transfer success.');
        var from_account = data['from_account'];
        var divId = '#acct_bal_' + from_account;
        var div = $(divId);
        var newBalance = data['new_balances'][from_account];
        div.text('$' + newBalance);
//        div.innerHTML(newBalance);
    };

    var createTransferUrl = function() {
        return '/api/v1/transfer/';
    };

    var transferFailure = function(jqXHR, textStatus, errorThrown) {
        // TODO Better error message
        setMessage('Transfer failed.');
    };

    var transferFunds = function(formData) {
        setMessage('Making transfer... please wait.');

//        var data = $.toJSON(formData);
//        $.post(createTransferUrl(), data, transferSuccess, 'json').error(transferFailure);

        var data = JSON.stringify(formData);
        $.ajax({
            type: 'POST',
            url: createTransferUrl(),
            data: data,
            success: transferSuccess,
            dataType: 'json',
            contentType: 'application/json'
        });
    };

    var init = function() {
        $('#submit_button').click(function() {
            var formData = {
                from_account: $('#from_account').val(),
                to_account: $('#to_account').val(),
                amount: $('#amount').val()
            };
            log('Submit requested:');
            log(formData);
            if(validateFormData(formData)) {
                transferFunds(formData);
            }
        });
    };

    $(document).ready(function() {
        init();
    });


})(window);
