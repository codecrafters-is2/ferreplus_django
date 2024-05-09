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
}
