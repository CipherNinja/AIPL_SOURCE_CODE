function openTab(tabNumber, element) {
    var i;
    var x = document.getElementsByClassName("tab__inside");

    // Remove active class from all tabs
    for (i = 0; i < x.length; i++) {
        x[i].classList.remove("tab__inside-active");
    }

    // Add active class to the selected tab
    document.getElementById(tabNumber).classList.add("tab__inside-active");

    // Remove active class from all buttons
    var buttons = document.getElementsByClassName("tab__button");
    for (i = 0; i < buttons.length; i++) {
        buttons[i].classList.remove("tab_button-active");
    }

    // Add active class to the clicked button
    element.classList.add("tab_button-active");
}
