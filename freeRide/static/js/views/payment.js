const pay_options = document.querySelectorAll('#option');
const modal_body = document.getElementById('modal-body');
const modal_header = document.getElementById('modal-header');

$(document).ready(function () {
    // Click event for PayPal option
    $('.paypal').click(function () {
        // Hide the current modal
        $('#staticBackdrop').modal('hide');
        // Show the PayPal form modal
        // Replace 'paypalFormModal' with the ID of your PayPal form modal
        $('#paypalFormModal').modal('show');

    });

    // Click event for Voucher option
    $('.voucher').click(function () {
        // Hide the current modal
        $('#staticBackdrop').modal('hide');
        // Show the voucher form modal
        // Replace 'voucherFormModal' with the ID of your voucher form modal
        $('#voucherFormModal').modal('show');
    });

    // Click event for Credit/Debit card option
    $('.credit').click(function () {
        // Hide the current modal
        $('#staticBackdrop').modal('hide');
        // Show the credit/debit card form modal
        // Replace 'cardFormModal' with the ID of your card form modal
        $('#creditFormModal').modal('show');
    });

    // Click event for back option
    $('.back').click(function () {
        // Hide the current modal
        $('#paypalFormModal').modal('hide');
        $('#voucherFormModal').modal('hide');
        $('#creditFormModal').modal('hide');
        // Show the credit/debit card form modal
        // Replace 'cardFormModal' with the ID of your card form modal
        $('#staticBackdrop').modal('show');
    });
});

function submitVoucherForm() {

    const code = document.getElementById('code').value
    const dataToSend = {
        'payment_method': 'voucher',
        'payment_details': code,
    };

    fetch('/add_payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    })
    .then(response => {
        if (response.ok) {
            return response.json(); // Parse the response body as JSON
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        // Redirect to the new page using JavaScript after successful request
        window.location.href = `/payment`; // Replace with the URL you want to redirect to
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error scenarios here
    });
}

function submitCreditForm() {

    const card_no = document.getElementById('card-number').value
    const exp_date = document.getElementById('expiry').value
    const cvv = document.getElementById('cvv').value
    const card_holder = document.getElementById('card-holder').value

    const dataToSend = {
        'payment_method': 'credit',
        'payment_details': {
            'card_no': card_no,
            'exp_date': exp_date,
            'cvv': cvv,
            'card_holder': card_holder,
        }
    };

    fetch('/add_payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    })
    .then(response => {
        if (response.ok) {
            return response.json(); // Parse the response body as JSON
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        // Redirect to the new page using JavaScript after successful request
        window.location.href = `/payment`; // Replace with the URL you want to redirect to
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error scenarios here
    });
}