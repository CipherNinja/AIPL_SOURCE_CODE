// JavaScript for navbar
document.addEventListener("DOMContentLoaded", function () {
  const hamburger = document.getElementById("hamburger");
  const option = document.querySelector(".option");
  const navbar = document.querySelector("nav");
  let isNavGrey = false;

  console.log("Document loaded and script initialized.");

  // Toggle hamburger and navigation options
  if (hamburger && option && navbar) {
    hamburger.addEventListener("click", () => {
      console.log("Hamburger menu clicked");
      hamburger.classList.toggle("active");
      option.classList.toggle("active");

      // Toggle navbar and option color
      if (isNavGrey) {
        navbar.classList.remove("scrolled");
        option.classList.remove("scrolled");
        isNavGrey = false;
        console.log("Navbar and option color reset");
      } else {
        navbar.classList.add("scrolled");
        option.classList.add("scrolled");
        isNavGrey = true;
        console.log("Navbar and option color changed");
      }
    });

    window.addEventListener("scroll", function () {
      const scrollableHeight =
        document.documentElement.scrollHeight - window.innerHeight;
      const scrolledPercentage = (window.scrollY / scrollableHeight) * 100;

      console.log(`Scrolled percentage: ${scrolledPercentage}`);

      if (scrolledPercentage >= 1 && !isNavGrey) {
        navbar.classList.add("scrolled");
        isNavGrey = true;
        console.log("Navbar color changed on scroll");
      } else if (scrolledPercentage < 1 && isNavGrey) {
        navbar.classList.remove("scrolled");
        isNavGrey = false;
        console.log("Navbar color reset on scroll");
      }
    });
  }

  // Handle clicks on main menu items to toggle submenus
  document.querySelectorAll(".nav-links > li > a").forEach(function (item) {
    item.addEventListener("click", function (event) {
      event.preventDefault();
      const allSubmenus = document.querySelectorAll(".submenu");
      const thisSubmenu = this.parentNode.querySelector(".submenu");

      // Close all other submenus
      allSubmenus.forEach((menu) => {
        if (menu !== thisSubmenu) {
          menu.classList.remove("show");
          menu.style.display = "none"; // Also hide any open inner submenus
          const arrow = menu.parentNode.querySelector(".arrow");
          if (arrow) arrow.classList.remove("down");
        }
      });

      // Toggle the current submenu
      thisSubmenu.classList.toggle("show");
      thisSubmenu.style.display =
        thisSubmenu.style.display === "none" ? "block" : "none";
      this.querySelector(".arrow").classList.toggle("down");
      console.log(
        `Submenu for '${this.textContent.trim()}' toggled: `,
        thisSubmenu.classList.contains("show")
      );
    });
  });

  // Initially hide all inner-submenus
  document.querySelectorAll(".inner-submenu").forEach(function (menu) {
    menu.style.display = "none";
  });

  // Handle clicks on submenu items to toggle inner-submenus
  document.querySelectorAll(".submenu > li").forEach(function (item) {
    const innerSubmenu = item.querySelector(".inner-submenu");
    item.addEventListener("click", function (event) {
      event.stopPropagation();

      // Close all other inner submenus except this one
      document.querySelectorAll(".inner-submenu").forEach(function (menu) {
        if (menu !== innerSubmenu) {
          menu.style.display = "none";
        }
      });

      // Toggle the display of this inner submenu
      innerSubmenu.style.display =
        innerSubmenu.style.display === "none" ? "block" : "none";
      console.log(
        `Inner-submenu for '${item.textContent.trim()}' toggled: `,
        innerSubmenu.style.display
      );
    });
  });

  // Close all menus when clicking outside of the navbar
  document.addEventListener("click", function (event) {
    if (!event.target.closest("nav")) {
      closeAllMenus();
      console.log("Clicked outside navbar, all menus closed.");
    }
  });

  function closeAllMenus() {
    document
      .querySelectorAll(".submenu, .inner-submenu")
      .forEach(function (menu) {
        menu.classList.remove("show");
        menu.style.display = "none";
      });
    document.querySelectorAll(".arrow.down").forEach(function (arrow) {
      arrow.classList.remove("down");
    });
    option.classList.remove("active");
    navbar.classList.remove("scrolled");
    hamburger.classList.remove("active");
    isNavGrey = false;
    console.log("All menus and submenu settings have been reset.");
  }

  // Additional listeners for address bar interactions
  const addressBarContainer = document.getElementById("address-bar-container");
  const closeBtn = document.getElementById("close-btn");
  const searchIcon = document.querySelector(".searchbar i");

  searchIcon.addEventListener("click", () => {
    addressBarContainer.style.display = "block";
    closeAllMenus();
    console.log("Search icon clicked, address bar displayed.");
  });

  closeBtn.addEventListener("click", () => {
    addressBarContainer.style.display = "none";
    console.log("Close button clicked, address bar hidden.");
  });
});
