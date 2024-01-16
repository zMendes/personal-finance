function getData() {

    cardsDiv.innerHTML = "";
    fetch(`http://localhost:8080/dashboard/movement_by_month_year/${accountSelect.value}/${yearSelect.value}/${monthSelect.value}`)
        .then(response => response.json())
        .then(data => createView(data))
}

function createView(data) {

    console.log(data);

    let container = document.getElementById("table")

    if (hot != null) {
        hot.updateSettings({
            data: data,
        });
    }
    else {
        hot = new Handsontable(container, {
            data: data,
            colHeaders: ["Item", "Payment", "Type", "Value"],
            columns: function (column) {
                let columnMeta = {};
                if (column == 0) {
                    columnMeta.data = "fields.description"
                } else if (column == 1) {
                    columnMeta.data = "fields.payment_type"
                } else if (column == 2) {
                    columnMeta.data = "fields.transaction_type"
                } else if (column == 3) {
                    columnMeta.data = "fields.value"
                } else {
                    columnMeta = null;
                }
                return columnMeta;
            },
            licenseKey: 'non-commercial-and-evaluation',


        });
    }
    let totals = { "expenses": 0, "debit": 0, "credit": 0, "investment": 0 }
    for (let i = 0; i < data.length; i++) {
        if (data[i].fields.transaction_type == "expenses") {
            totals.expenses += data[i].fields.value;
        }
        if (data[i].fields.payment_type == "credit") {
            totals.credit += data[i].fields.value;
        }
        if (data[i].fields.payment_type == "debit") {
            totals.debit += data[i].fields.value;
        }
        if (data[i].fields.transaction_type == "investment") {
            totals.investment += data[i].fields.value;
        }
    }
    for (const [key, value] of Object.entries(totals)) {
        createCard(key, value)
    }
}

function createCard(key, value) {
    var cardContainer = document.createElement('div');
    cardContainer.className = 'card text-bg-light mb-3';
    cardContainer.style.maxWidth = '18rem';
    cardContainer.id = "card";

    // Create card header
    var cardHeader = document.createElement('div');
    cardHeader.className = 'card-header';
    cardHeader.textContent = 'Total';
    cardContainer.appendChild(cardHeader);

    // Create card body
    var cardBody = document.createElement('div');
    cardBody.className = 'card-body';

    // Create card title
    var cardTitle = document.createElement('h5');
    cardTitle.className = 'card-title';
    cardTitle.textContent = key;
    cardBody.appendChild(cardTitle);

    // Create card text
    var cardText = document.createElement('p');
    cardText.className = 'card-text';
    cardText.textContent = value;
    cardBody.appendChild(cardText);

    // Append card body to card container
    cardContainer.appendChild(cardBody);


    // Append the card container to the body or any other desired element
    cardsDiv.appendChild(cardContainer);
}

let monthSelect = document.getElementById("month-select");
let yearSelect = document.getElementById("year-select");
let accountSelect = document.getElementById("account-select");
let dataDiv = document.getElementById("data");
let cardsDiv = document.getElementById("cards");
let container = document.getElementById("table");
var hot = null;

getData();


