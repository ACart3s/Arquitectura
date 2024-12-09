addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("gastosForm");
  const departament = document.getElementById("department");
  const periodoMesInput = document.getElementById("periodoMes");
  const periodoAnoInput = document.getElementById("periodoAno");

  const csrfToken = getCookie("csrftoken");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const mes = periodoMesInput.value.padStart(2, "0");
    const ano = periodoAnoInput.value;
    const departament = document.getElementById("departament");

    const formData = new FormData();
    formData.append("mes", mes);
    formData.append("anio", ano);
    formData.append("departament", departament.value);

    fetch("/realizar_pago/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.complete) {
          showAlert(data.status, "success");
          return;
        }

        showAlert(data.message, "error");
      });
  });
});

const showAlert = (message, type) => {
  const alert = document.createElement("div");
  alert.className = `alert alert-${type}`;
  alert.textContent = message;
  document.body.insertAdjacentElement("afterbegin", alert);
  setTimeout(() => alert.remove(), 5000);
};
