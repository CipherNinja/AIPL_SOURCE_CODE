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

      // Check if the hamburger menu is active to change the navbar and menu color
      if (hamburger.classList.contains("active")) {
        navbar.classList.add("scrolled");
        option.classList.add("scrolled");
        isNavGrey = true;
        console.log("Navbar and menu color changed to grey when menu opened");
      } else {
        navbar.classList.remove("scrolled");
        option.classList.remove("scrolled");
        isNavGrey = false;
        console.log("Navbar and menu color reset when menu closed");
      }
    });

    window.addEventListener("scroll", function () {
      const scrollableHeight =
        document.documentElement.scrollHeight - window.innerHeight;
      const scrolledPercentage = (window.scrollY / scrollableHeight) * 100;

      console.log(`Scrolled percentage: ${scrolledPercentage}`);

      if (scrolledPercentage >= 1 && !isNavGrey) {
        navbar.classList.add("scrolled");
        option.classList.add("scrolled");
        isNavGrey = true;
        console.log("Navbar and menu color changed on scroll");
      } else if (
        scrolledPercentage < 1 &&
        isNavGrey &&
        !hamburger.classList.contains("active")
      ) {
        // Ensure the navbar and menu color reset only if the menu is not active
        navbar.classList.remove("scrolled");
        option.classList.remove("scrolled");
        isNavGrey = false;
        console.log("Navbar and menu color reset on scroll");
      }
    });
  }

  // Handle clicks on main menu items to toggle submenus
  document.querySelectorAll(".nav-links > li > a").forEach(function (item) {
    item.addEventListener("click", function (event) {
      event.preventDefault();
      const parentLi = this.parentNode;
      const thisSubmenu = parentLi.querySelector(".submenu");
      navbar.classList.add("scrolled");
      option.classList.add("scrolled");

      // Close all other submenus
      document.querySelectorAll(".submenu").forEach((submenu) => {
        if (submenu !== thisSubmenu) {
          submenu.classList.remove("show");
          submenu.style.maxHeight = null;
          submenu.style.opacity = 0;
          const arrow = submenu.previousElementSibling.querySelector(".arrow");
          if (arrow) arrow.classList.remove("down");
        }
      });

      // Toggle the current submenu
      const isSubmenuVisible = thisSubmenu.classList.toggle("show");
      thisSubmenu.style.maxHeight = isSubmenuVisible
        ? thisSubmenu.scrollHeight + "px"
        : 0;
      thisSubmenu.style.opacity = isSubmenuVisible ? 1 : 0;
      const arrow = thisSubmenu.previousElementSibling.querySelector(".arrow");
      if (arrow) arrow.classList.toggle("down", isSubmenuVisible);

      console.log(
        `Submenu for '${this.textContent.trim()}' toggled: `,
        isSubmenuVisible
      );
    });
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
      if (innerSubmenu) {
        innerSubmenu.style.display =
          innerSubmenu.style.display === "none" ? "block" : "none";
        console.log(
          `Inner-submenu for '${item.textContent.trim()}' toggled: `,
          innerSubmenu.style.display
        );

        // Toggle the icon from + to - and vice versa
        const icon = item.querySelector(".icon");
        if (icon) {
          icon.textContent = innerSubmenu.style.display === "block" ? "-" : "+";
        }
      }
    });
  });

  // Initially hide all inner-submenus
  document.querySelectorAll(".inner-submenu").forEach(function (menu) {
    menu.style.display = "none";
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
        const arrow = menu.previousElementSibling.querySelector(".arrow");
        if (arrow) arrow.classList.remove("down");
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

  // Toggle hamburger icon based on screen width
  function toggleMenuIcons() {
    const menuItems = document.querySelectorAll(".nav-links > li");

    menuItems.forEach((item) => {
      const submenu = item.querySelector(".submenu");

      if (submenu) {
        submenu.style.padding =
          window.innerWidth <= 768 ? "16px 20px 20px 20px" : "0% 50% 95% 50%";

        // Check if inner-submenu icons exist and remove them if screen size is >= 768px
        const innerSubmenuIcons = item.querySelectorAll(".icon");
        if (window.innerWidth >= 768 && innerSubmenuIcons.length > 0) {
          innerSubmenuIcons.forEach((icon) => {
            icon.remove();
          });
        }

        // Add inner-submenu icons if screen size is < 768px and icons don't already exist
        if (window.innerWidth < 768 && innerSubmenuIcons.length === 0) {
          // const icon = document.createElement("span");
          // icon.classList.add("icon");
          // icon.textContent = "+"; // Initial icon state
          // item.appendChild(icon);
        }

        // Set initial arrow state for closed submenus
        const arrow = item.querySelector(".arrow");
        if (arrow && !submenu.classList.contains("show")) {
          arrow.classList.remove("down");
        }
      }
    });
  }

  toggleMenuIcons(); // Initial call to set icons based on initial screen width
  window.addEventListener("resize", toggleMenuIcons); // Call on window resize
});
