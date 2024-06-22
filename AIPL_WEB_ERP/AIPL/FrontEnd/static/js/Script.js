console.log("Hello world");

document.addEventListener("DOMContentLoaded", function () {
  const hamburger = document.getElementById("hamburger");
  const option = document.querySelector(".option");
  const navbar = document.querySelector("nav");
  let isNavGrey = false;

  hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("active");
    option.classList.toggle("active");

    // Toggle navbar and option color
    if (isNavGrey) {
      navbar.classList.remove("scrolled");
      option.classList.remove("scrolled");
      isNavGrey = false;
    } else {
      navbar.classList.add("scrolled");
      option.classList.add("scrolled");
      isNavGrey = true;
    }
  });

  window.addEventListener("scroll", function () {
    const scrollableHeight =
      document.documentElement.scrollHeight - window.innerHeight;
    const scrolledPercentage = (window.scrollY / scrollableHeight) * 100;

    if (scrolledPercentage >= 1 && !isNavGrey) {
      navbar.classList.add("scrolled");
      isNavGrey = true;
    } else if (scrolledPercentage < 1 && isNavGrey) {
      navbar.classList.remove("scrolled");
      isNavGrey = false;
    }
  });

  document.querySelectorAll(".nav-links > li").forEach(function (item) {
    const link = item.querySelector("a");
    const submenu = item.querySelector(".submenu");
    const arrow = item.querySelector(".arrow");

    item.addEventListener("click", function (event) {
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
            }
          });

        submenu.classList.toggle("show");
        arrow.classList.toggle("down");

        navbar.classList.add("scrolled");
      } else {
        navbar.classList.remove("scrolled");
      }
    });
  });

  const addressBarContainer = document.getElementById("address-bar-container");
  const closeBtn = document.getElementById("close-btn");
  const searchIcon = document.querySelector(".searchbar img");

  addressBarContainer.style.display = "none";

  searchIcon.addEventListener("click", () => {});

  closeBtn.addEventListener("click", () => {
    addressBarContainer.style.display = "none";
  });
});
