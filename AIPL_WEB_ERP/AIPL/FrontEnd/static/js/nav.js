// function toggleMenu() {
//     const navLinks = document.querySelector('.nav-links');
//     navLinks.classList.toggle('active');
// }
console.log("Hello world");

document.addEventListener("DOMContentLoaded", function () {
  const hamburger = document.getElementById("hamburger");
  const option = document.querySelector(".option");
  const navbar = document.querySelector("nav");
  let isNavGrey = false;

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

    document.querySelectorAll(".nav-links > li").forEach(function (item) {
      const link = item.querySelector("a");
      const submenu = item.querySelector(".submenu");
      const arrow = item.querySelector(".arrow");

      if (link && submenu && arrow) {
        item.addEventListener("click", function (event) {
          console.log(`Clicked on nav item: ${link.textContent}`);

          if (submenu) {
            event.preventDefault();

            // Close any other open submenus
            document
              .querySelectorAll(".submenu.show")
              .forEach(function (openSubmenu) {
                if (openSubmenu !== submenu) {
                  openSubmenu.classList.remove("show");
                  openSubmenu
                    .closest("li")
                    .querySelector(".arrow")
                    .classList.remove("down");
                  console.log("Closed other open submenu");
                }
              });

            submenu.classList.toggle("show");
            arrow.classList.toggle("down");

            if (submenu.classList.contains("show")) {
              console.log("Opened submenu");
            } else {
              console.log("Closed submenu");
            }

            navbar.classList.add("scrolled");
          } else {
            navbar.classList.remove("scrolled");
          }
        });

        // Stop click event from propagating up when clicking on submenu
        submenu.addEventListener("click", function (event) {
          event.stopPropagation();
        });
      }
    });

    document.addEventListener("click", function (event) {
      const target = event.target;
      const isClickInsideNav =
        navbar.contains(target) || target.closest(".submenu");

      if (!isClickInsideNav) {
        console.log("Clicked outside the menu");
        document.querySelectorAll(".submenu.show").forEach(function (submenu) {
          submenu.classList.remove("show");
          submenu
            .closest("li")
            .querySelector(".arrow")
            .classList.remove("down");
        });

        navbar.classList.remove("scrolled");
        option.classList.remove("active");
        hamburger.classList.remove("active");
        isNavGrey = false;
        console.log("Menu closed");
      }
    });
  }

  const addressBarContainer = document.getElementById("address-bar-container");
  const closeBtn = document.getElementById("close-btn");
  const searchIcon = document.querySelector(".searchbar img");

  if (addressBarContainer && closeBtn && searchIcon) {
    addressBarContainer.style.display = "none";

    searchIcon.addEventListener("click", () => {
      console.log("Search icon clicked");
      addressBarContainer.style.display = "flex";

      // Close any open menus or submenus
      document.querySelectorAll(".submenu.show").forEach(function (submenu) {
        submenu.classList.remove("show");
        submenu.closest("li").querySelector(".arrow").classList.remove("down");
      });
      navbar.classList.remove("scrolled");
      option.classList.remove("active");
      hamburger.classList.remove("active");
      isNavGrey = false;
      console.log("Menu closed");
    });

    closeBtn.addEventListener("click", () => {
      console.log("Close button clicked");
      addressBarContainer.style.display = "none";
    });
  }
});
