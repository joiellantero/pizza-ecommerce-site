function addToCart(data) {
  return new Promise(function(resolve, reject) {
    const request = new XMLHttpRequest();
    request.onload = function() {
      resolve(JSON.parse(this.responseText));
    };
    request.onerror = reject;
    request.open("POST", "add-to-cart");
    request.send(data);
  });
}

function compileModalTemplate(product_class, product_name, product_id, showModal) {
  let context = {
    "product_class": product_class,
    "product_class_hr": product_class,
    "product_name": product_name,
    "product_id": product_id,
    "size": false,
    "size_values": [],
    "subaddons": false,
    "subaddons_values": [],
    "toppings": false,
    "toppings_list": [],
    "toppings_count": []
  };

  if (product_class == "DinnerPlatterName") {
    getSizes(context.product_class, context.product_id)
      .then(function(result) {
        // Set context
        context.size = true;
        context.size_values = result;
        context.product_class_hr = "Dinner Platter";
      })
      .then(function(result) {
        // Compile modal window
        const template = document.querySelector("#modal-template").innerHTML;
        const templateScript = Handlebars.compile(template);
        const html = templateScript(context);
        document.querySelector("#modal-placeholder").innerHTML = html;
      })
      .then(function(result) {
        // Add onclick event
        document.querySelector("#add-to-cart").onclick = (e) => {
          data = new FormData(document.querySelector("#add-to-cart-form"));
          data.append("product_class", context.product_class);
          data.append("product_name", context.product_name);
          data.append("product_id", context.product_id);
          addToCart(data)
            .then(function(result) {
              // Close modal window
              $("#modalProduct").modal("hide");

              // Set price
              setOrderPrice(result.order_price);
            })
            .then(function(result) {
              // Remove modal window html content
              document.querySelector("#modal-placeholder").innerHTML = "";
            });
        };
      })
      .then(function(result) {
        $('#modalProduct').on('hidden.bs.modal', function (e) {
          document.querySelector("#modal-placeholder").innerHTML = "";
        });
      })
      .then(function(result) {
        // Show modal if specified
        if (showModal) {
          $("#modalProduct").modal("show");
        }
      });
  } else if (product_class == "Salad") {
      context.product_class_hr = "Salad";

      // Compile modal window
      const template = document.querySelector("#modal-template").innerHTML;
      const templateScript = Handlebars.compile(template);
      const html = templateScript(context);
      document.querySelector("#modal-placeholder").innerHTML = html;

      // Add onclick event
      document.querySelector("#add-to-cart").onclick = (e) => {
        data = new FormData(document.querySelector("#add-to-cart-form"));
        data.append("product_class", context.product_class);
        data.append("product_name", context.product_name);
        data.append("product_id", context.product_id);
        addToCart(data)
          .then(function(result) {
            // Close modal window
            $("#modalProduct").modal("hide");

            // Set price
            setOrderPrice(result.order_price);
          })
          .then(function(result) {
            // Remove modal window html content
            document.querySelector("#modal-placeholder").innerHTML = "";
          });
      };

      $('#modalProduct').on('hidden.bs.modal', function (e) {
        document.querySelector("#modal-placeholder").innerHTML = "";
      });

      // Show modal if specified
      if (showModal) {
        $("#modalProduct").modal("show");
      }
  } else if (product_class == "Pasta") {
    context.product_class_hr = "Pasta";

    // Compile modal window
    const template = document.querySelector("#modal-template").innerHTML;
    const templateScript = Handlebars.compile(template);
    const html = templateScript(context);
    document.querySelector("#modal-placeholder").innerHTML = html;

    // Add onclick event
    document.querySelector("#add-to-cart").onclick = (e) => {
      data = new FormData(document.querySelector("#add-to-cart-form"));
      data.append("product_class", context.product_class);
      data.append("product_name", context.product_name);
      data.append("product_id", context.product_id);
      addToCart(data)
        .then(function(result) {
          // Close modal window
          $("#modalProduct").modal("hide");

          // Set price
          setOrderPrice(result.order_price);
        })
        .then(function(result) {
          // Remove modal window html content
          document.querySelector("#modal-placeholder").innerHTML = "";
        });
    };

    $('#modalProduct').on('hidden.bs.modal', function (e) {
      document.querySelector("#modal-placeholder").innerHTML = "";
    });

    // Show modal if specified
    if (showModal) {
      $("#modalProduct").modal("show");
    }
  } else if (product_class == "Sub") {
    const promise1 = getSizes(context.product_class, context.product_id);
    const promise2 = getSubsAddons();

    Promise.all([promise1, promise2])
      .then(function(values) {
        // Set context
        context.product_class_hr = "Sub";
        context.size = true;
        context.size_values = values[0];
        context.subaddons = true;
        context.subaddons_values = values[1];
      })
      .then(function(result) {
        // Compile modal window
        const template = document.querySelector("#modal-template").innerHTML;
        const templateScript = Handlebars.compile(template);
        const html = templateScript(context);
        document.querySelector("#modal-placeholder").innerHTML = html;
      })
      .then(function(result) {
        // Add onclick event
        document.querySelector("#add-to-cart").onclick = (e) => {
          data = new FormData(document.querySelector("#add-to-cart-form"));
          data.append("product_class", context.product_class);
          data.append("product_name", context.product_name);
          data.append("product_id", context.product_id);
          data.append("subaddons", data.getAll("subaddons"));
          addToCart(data)
            .then(function(result) {
              // Close modal window
              $("#modalProduct").modal("hide");

              // Set price
              setOrderPrice(result.order_price);
            })
            .then(function(result) {
              // Remove modal window html content
              document.querySelector("#modal-placeholder").innerHTML = "";
            });
        };
      })
      .then(function(result) {
        $('#modalProduct').on('hidden.bs.modal', function (e) {
          document.querySelector("#modal-placeholder").innerHTML = "";
        })
      })
      .then(function(result) {
        // Show modal if specified
        if (showModal) {
          $("#modalProduct").modal("show");
        }
      });
  } else if (product_class == "PizzaName") {
    const promise1 = getSizes(context.product_class, context.product_id);
    const promise2 = getToppings();
    const promise3 = getToppingsCount(context.product_id);

    Promise.all([promise1, promise2, promise3])
      .then(function(values) {
        // Set context
        context.product_class_hr = "Pizza";
        context.size = true;
        context.size_values = values[0];
        context.toppings = true;
        context.toppings_list = values[1];
        values[2].forEach((item) => {
          context.toppings_count.push(item);
        });
      })
      .then(function(result) {
        // Compile modal window
        const template = document.querySelector("#modal-template").innerHTML;
        const templateScript = Handlebars.compile(template);
        const html = templateScript(context);
        document.querySelector("#modal-placeholder").innerHTML = html;
      })
      .then(function(result) {
        // Add onclick event
        document.querySelector("#add-to-cart").onclick = (e) => {
          data = new FormData(document.querySelector("#add-to-cart-form"));

          const tops_count = data.get("toppings_count");
          const tops = data.getAll("toppings").length;

          if (tops_count != tops) {
            alert("Your should choose selected amount of toppings");
            return false;
          }

          data.append("product_class", context.product_class);
          data.append("product_name", context.product_name);
          data.append("product_id", context.product_id);
          data.append("toppings", data.getAll("toppings"));
          addToCart(data)
            .then(function(result) {
              // Close modal window
              $("#modalProduct").modal("hide");

              // Set price
              setOrderPrice(result.order_price);
            })
            .then(function(result) {
              // Remove modal window html content
              document.querySelector("#modal-placeholder").innerHTML = "";
            });
        };
      })
      .then(function(result) {
        $('#modalProduct').on('hidden.bs.modal', function (e) {
          document.querySelector("#modal-placeholder").innerHTML = "";
        })
      })
      .then(function(result) {
        // Show modal if specified
        if (showModal) {
          $("#modalProduct").modal("show");
        }
      });
  }
}

function getSizes(product_class, product_id) {
  return new Promise(function(resolve, reject) {
    const request = new XMLHttpRequest();
    request.onload = function() {
      resolve(JSON.parse(this.responseText));
    };
    request.onerror = reject;
    request.open("POST", "get-sizes");

    const data = new FormData();
    data.append("product_class", product_class);
    data.append("product_id", product_id);
    request.send(data);
  });
}

function getSubsAddons() {
  return new Promise(function(resolve, reject) {
    const request = new XMLHttpRequest();
    request.onload = function() {
      resolve(JSON.parse(this.responseText));
    };
    request.onerror = reject;
    request.open("POST", "get-subs-addons");

    request.send();
  });
}

function getToppings() {
  return new Promise(function(resolve, reject) {
    const request = new XMLHttpRequest();
    request.onload = function() {
      resolve(JSON.parse(this.responseText));
    };
    request.onerror = reject;
    request.open("POST", "get-toppings");

    request.send();
  });
}

function getToppingsCount(product_id) {
  return new Promise(function(resolve, reject) {
    const request = new XMLHttpRequest();
    request.onload = function() {
      resolve(JSON.parse(this.responseText));
    };
    request.onerror = reject;
    request.open("POST", "get-toppings-count");

    const data = new FormData();
    data.append("product_id", product_id);
    request.send(data);
  });
}

function getOrderPrice() {
  return new Promise(function(resolve, reject) {
    const request = new XMLHttpRequest();
    request.onload = function() {
      resolve(JSON.parse(this.responseText));
    };
    request.onerror = reject;
    request.open("POST", "get-current-order-price");

    request.send();
  });
}

function setOrderPrice(order_price) {
  const span = document.querySelector("#order-price");
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
}

document.addEventListener("DOMContentLoaded", () => {
  // Get current order price
  getOrderPrice()
    .then(function(result) {
      setOrderPrice(result.order_price);
    });

  // Click "Add to cart"
  document.querySelectorAll(".add-to-order").forEach((element) => {
    element.onclick = (e) => {
      const product_class = e.target.dataset.productClass;
      const product_name = e.target.dataset.productName;
      const product_id = e.target.dataset.productId;

      compileModalTemplate(product_class, product_name, product_id, true);
      return false;
    };
  });
});
