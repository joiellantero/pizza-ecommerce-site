function removeFromCart(order_class, order_id) {
  return new Promise(function(resolve, reject) {
    const request = new XMLHttpRequest();
    request.onload = function() {
      resolve(JSON.parse(this.responseText));
    };
    request.onerror = reject;
    request.open("POST", "remove-from-cart");

    const data = new FormData();
    data.append("order_class", order_class);
    data.append("order_id", order_id);
    request.send(data);
  });
}

function setOrderPrice(order_price) {
  const span = document.querySelector("#order-price");
  if ((span === null) || (span === undefined)) {
      return
  }
  span.innerText = "$" + order_price;

  const a = span.closest("a");
  if (order_price == 0) {
    if (!a.classList.contains("disabled")) {
      a.classList.add("disabled");
    }

    // Disable clicking
    a.href = "#";
    a.onclick = () => {
      return false;
    };

  } else {
    if (a.classList.contains("disabled")) {
      a.classList.remove("disabled");
    }
  }

  const strong = document.querySelector("#overall-price");
  if (strong !== null) {
    strong.innerText = "$" + order_price;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  // Remove item from order
  document.querySelectorAll(".remove-item").forEach((el) => {
    el.onclick = (e) => {
      const order_class = e.target.dataset.orderClass;
      const order_id = e.target.dataset.orderId;

      removeFromCart(order_class, order_id)
        .then(function(result) {
          // Renew order price
          setOrderPrice(result.order_price);
        })
        .then(function(result) {
          // Remove tr
          const tr = e.target.closest("tr");

          const tbody = tr.closest("tbody");
          const table = tbody.closest("table");
          const header = table.previousElementSibling;

          tr.style.animationPlayState = 'running';
          tr.addEventListener('animationend', () =>  {
              tr.remove();

              // Remove table and h3 if needed
              if (tbody.childElementCount == 0) {
                table.remove();
                header.remove();
              }
          });
        });
    };
  });
});
