document.addEventListener('DOMContentLoaded', initialize);


function initialize() {
  const button = document.querySelector(".hamburguer-button");
  const cellphoneMenu = document.querySelector(".navbar-nav");

  button.addEventListener('click', () => {  
    cellphoneMenu.classList.contains("visible") ? cellphoneMenu.classList.remove("visible") : cellphoneMenu.classList.add("visible");
  })

  window.addEventListener("resize", () => {
    window.innerWidth > 768 && cellphoneMenu.classList.remove("visible");
  })

  const userButton = document.getElementById("user-button");
  const userMenu = document.querySelector(".user-menu");

  userButton.addEventListener('click', () => {
    userMenu.classList.contains("shown") ? userMenu.classList.remove("shown") : userMenu.classList.add("shown");
  })

}
