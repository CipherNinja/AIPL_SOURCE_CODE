document.addEventListener('DOMContentLoaded', function() {
    const closeButtons = document.querySelectorAll('.closebtn');

    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const alert = this.parentElement;
            alert.style.display = 'none';
        });
    });
});
