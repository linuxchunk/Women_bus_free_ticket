document.getElementById('generateTicket').addEventListener('click', function () {
    const startPoint = document.getElementById('startPoint').value;
    const destination = document.getElementById('destination').value;
    const mobileNumber = document.getElementById('mobileNumber').value;
    
    // Make an AJAX request to the server to generate the ticket.
    // You can use fetch or other AJAX libraries for this.
    fetch('/generate_ticket', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ startPoint, destination, mobileNumber })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('ticketQRCode').innerHTML = `<img src="${data.qrCode}" alt="QR Code">`;
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
