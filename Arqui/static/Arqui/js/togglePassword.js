addEventListener("DOMContentLoaded", () => {
  const $passwordToggle = document.querySelector(".toggle-password");
  const $password = document.querySelector("#password");

  $passwordToggle.addEventListener("click", () => {
    if ($password.type === "password") {
      $password.type = "text";
      $passwordToggle.querySelector("i").classList.remove("bx-show");
      $passwordToggle.querySelector("i").classList.add("bx-hide");
    } else {
      $password.type = "password";
      $passwordToggle.querySelector("i").classList.add("bx-show");
      $passwordToggle.querySelector("i").classList.remove("bx-hide");
    }
  });
});
