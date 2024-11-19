document.addEventListener("DOMContentLoaded", function () {
  const hamburger = document.getElementById("hamburger");
  const option = document.querySelector(".option");
  const navbar = document.querySelector("nav");
  const submenus = document.querySelectorAll(".submenu");
  const innerSubmenus = document.querySelectorAll(".inner-submenu");

  // Close all submenus
  function closeAllSubmenus() {
    submenus.forEach((submenu) => {
      submenu.classList.remove("show");
      submenu.style.maxHeight = null;
      const arrow = submenu.previousElementSibling.querySelector(".arrow");
      if (arrow) arrow.classList.remove("down");
    });
    innerSubmenus.forEach((innerSubmenu) => {
      innerSubmenu.style.display = "none";
    });
  }

  // Toggle specific submenu
  function toggleSubmenu(menuLink) {
    const parentLi = menuLink.parentElement;
    const submenu = parentLi.querySelector(".submenu");

    // Close all other submenus
    submenus.forEach((otherSubmenu) => {
      if (otherSubmenu !== submenu) {
        otherSubmenu.classList.remove("show");
        otherSubmenu.style.maxHeight = null;
        const arrow = otherSubmenu.previousElementSibling.querySelector(".arrow");
        if (arrow) arrow.classList.remove("down");
      }
    });

    // Toggle the current submenu
    if (submenu) {
      const isSubmenuVisible = submenu.classList.toggle("show");
      submenu.style.maxHeight = isSubmenuVisible ? submenu.scrollHeight + "px" : null;
      const arrow = menuLink.querySelector(".arrow");
      if (arrow) arrow.classList.toggle("down", isSubmenuVisible);
    }
  }

  // Event listener for menu links
  document.querySelectorAll(".nav-links > li > a").forEach((menuLink) => {
    menuLink.addEventListener("click", function (event) {
      event.preventDefault();
      toggleSubmenu(this);
    });
  });

  // Handle clicks on inner submenus
  document.querySelectorAll(".submenu > li").forEach((menuItem) => {
    const innerSubmenu = menuItem.querySelector(".inner-submenu");

    menuItem.addEventListener("click", function (event) {
      event.stopPropagation(); // Prevent bubbling up to parent submenu

      // Toggle the display of this inner submenu
      if (innerSubmenu) {
        innerSubmenu.style.display =
          innerSubmenu.style.display === "block" ? "none" : "block";
      }
    });
  });

  // Close menus when clicking outside
  document.addEventListener("click", function (event) {
    if (!event.target.closest("nav")) {
      closeAllSubmenus();
    }
  });

  // Hamburger menu toggle for mobile
  if (hamburger && option) {
    hamburger.addEventListener("click", () => {
      hamburger.classList.toggle("active");
      option.classList.toggle("active");

      // Close all submenus when the hamburger menu is toggled off
      if (!hamburger.classList.contains("active")) {
        closeAllSubmenus();
      }
    });
  }

  // Reset menus on window resize
  window.addEventListener("resize", function () {
    if (window.innerWidth > 768) {
      option.classList.remove("active");
      hamburger.classList.remove("active");
      closeAllSubmenus();
    }
  });
});
