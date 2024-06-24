document.addEventListener('DOMContentLoaded', function () {
  const dropdownToggles = document.querySelectorAll('.option > ul > li > a');
  const hamburger = document.getElementById('hamburger');
  const navOptions = document.querySelector('.option');
  const closeBtn = document.getElementById('close-btn');
  const searchIcon = document.querySelector('.searchbar img');
  const addressBarContainer = document.getElementById('address-bar-container');

  dropdownToggles.forEach(toggle => {
      toggle.addEventListener('click', function (e) {
          e.preventDefault();
          const submenu = this.nextElementSibling;
          const arrow = this.querySelector('.arrow');
          submenu.classList.toggle('show');
          arrow.classList.toggle('down');
      });
  });

  hamburger.addEventListener('click', function () {
      this.classList.toggle('active');
      navOptions.classList.toggle('active');
  });

  searchIcon.addEventListener('click', function () {
      addressBarContainer.style.display = 'block'; // Show the container
      setTimeout(() => {
          addressBarContainer.style.top = '0';
      }, 10);
  });

  closeBtn.addEventListener('click', function () {
      addressBarContainer.style.top = '100%';
      setTimeout(() => {
          addressBarContainer.style.display = 'none'; // Hide the container
      }, 300);
  });
});
