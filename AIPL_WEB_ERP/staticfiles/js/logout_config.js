// this code is necessary else the padding of other forms will overlap
logout_button=document.getElementsByClassName("logout")[0].style
if (window.innerWidth < 768) {
    logout_button.marginBottom = "0px"
    logout_button.marginRight = "0px"
}
else{
    logout_button.padding = "0px"
}