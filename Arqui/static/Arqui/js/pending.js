addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("gastosForm");
  const montoInput = document.getElementById("monto");
  const periodoMesInput = document.getElementById("periodoMes");
  const periodoAnoInput = document.getElementById("periodoAno");
  const table = document
    .getElementById("gastosTable")
    .getElementsByTagName("tbody")[0];

  const csrfToken = getCookie("csrftoken");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const mes = periodoMesInput.value.padStart(2, "0");
    const ano = periodoAnoInput.value;
    const periodo = `${mes}-${ano}`;

    table.innerHTML = "";

    const formData = new FormData();
    formData.append("mes", mes);
    formData.append("anio", ano);

    fetch("/listar_pendientes/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if (data.complete) {
          data.pendientes.forEach((gasto) => {
            insertRow(table, gasto);
          });
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

const insertRow = (table, data) => {
  const row = table.insertRow();
  const deptCell = row.insertCell(0);
  const montoCell = row.insertCell(1);
  const periodoCell = row.insertCell(2);

  deptCell.textContent = data.departamento;
  montoCell.textContent = `$${data.monto}`;
  periodoCell.textContent = data.periodo;
};
