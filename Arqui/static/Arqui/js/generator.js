document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("gastosForm");
  const montoInput = document.getElementById("monto");
  const periodoMesInput = document.getElementById("periodoMes");
  const periodoAnoInput = document.getElementById("periodoAno");
  const table = document
    .getElementById("gastosTable")
    .getElementsByTagName("tbody")[0];

  const csrfToken = getCookie("csrftoken");

  // Format monto input with dots
  montoInput.addEventListener("input", function (e) {
    let value = e.target.value.replace(/\D/g, "");
    if (value) {
      value = parseInt(value).toLocaleString("es-CL");
      e.target.value = value;
    }
  });

  // Only allow numbers in periodo inputs
  [periodoMesInput, periodoAnoInput].forEach((input) => {
    input.addEventListener("input", function (e) {
      e.target.value = e.target.value.replace(/\D/g, "");

      // Auto-advance to year field when month is complete
      if (input === periodoMesInput && e.target.value.length === 2) {
        if (parseInt(e.target.value) > 12) {
          e.target.value = "12";
        }
        periodoAnoInput.focus();
      }
    });
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const monto = montoInput.value;
    const mes = periodoMesInput.value.padStart(2, "0");
    const ano = periodoAnoInput.value;
    const periodo = `${mes}-${ano}`;

    // Clear existing table rows
    table.innerHTML = "";

    // Generate new rows
    /*     for (let i = 1; i <= 50; i++) {
      const row = table.insertRow();
      const deptCell = row.insertCell(0);
      const montoCell = row.insertCell(1);
      const periodoCell = row.insertCell(2);

      deptCell.textContent = `10${i}`;
      montoCell.textContent = `$${monto}`;
      periodoCell.textContent = periodo;
    } */

    const formData = new FormData();
    formData.append("monto", monto.replace(/\D/g, ""));
    formData.append("mes", mes);
    formData.append("anio", ano);

    fetch("/generar_gastos/", {
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
          data.generated.forEach((gasto) => {
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

  deptCell.textContent = data.depto;
  montoCell.textContent = `$${data.monto}`;
  periodoCell.textContent = data.fechaDeuda;
};
