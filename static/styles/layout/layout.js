document.addEventListener('DOMContentLoaded', initialize);


function initialize() {
  const button = document.querySelector(".hamburguer-button");
  const cellphoneMenu = document.querySelector(".navbar-navigation");

  button.addEventListener('click', () => {  
    cellphoneMenu.classList.contains("custom-visible") ? cellphoneMenu.classList.remove("custom-visible") : cellphoneMenu.classList.add("custom-visible");
  })

  window.addEventListener("resize", () => {
    window.innerWidth > 768 && cellphoneMenu.classList.remove("custom-visible");
  })

  const userButton = document.getElementById("user-button");
  const userMenu = document.querySelector(".user-menu");

  if (userButton) {
    userButton.addEventListener('click', () => {
      userMenu.classList.contains("shown") ? userMenu.classList.remove("shown") : userMenu.classList.add("shown");
    });
  }
}
