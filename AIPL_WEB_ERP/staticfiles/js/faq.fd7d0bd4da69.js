
function gsapAccordion() {
    let menus = document.querySelectorAll(".accordion-menu");

    menus.forEach(menu => {
        menu.addEventListener("click", () => {
            let content = menu.nextElementSibling;
            content.classList.toggle("expanded");

            // Close other accordions
            let allContents = document.querySelectorAll(".accordion-content");
            allContents.forEach(item => {
                if (item !== content && item.classList.contains("expanded")) {
                    item.classList.remove("expanded");
                }
            });

            // Toggle plus/minus icon
            let plusMinus = menu.querySelector(".accordion-plus");
            plusMinus.textContent = content.classList.contains("expanded") ? "-" : "+";

            // Smooth scroll to expanded content
            if (content.classList.contains("expanded")) {
                gsap.to(window, {
                    duration: 1,
                    scrollTo: {
                        y: content.offsetTop - 50,
                        autoKill: true
                    }
                });
            }
        });
    });
}

// Run GSAP accordion function on page load
gsapAccordion();
