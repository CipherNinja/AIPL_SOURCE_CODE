document.addEventListener('DOMContentLoaded', function() {
    const today = new Date().toISOString().split('T')[0];
    const dateInput = document.getElementById('date');
    const timeInput = document.getElementById('time');

    // Set the minimum date to today in dd-mm-yyyy format
    const todayFormatted = `${today.split('-')[2]}-${today.split('-')[1]}-${today.split('-')[0]}`;
    dateInput.setAttribute('placeholder', 'dd-mm-yyyy');
    
    // Set working hours from 9 AM to 5 PM
    timeInput.setAttribute('min', '09:00');
    timeInput.setAttribute('max', '17:00');
});