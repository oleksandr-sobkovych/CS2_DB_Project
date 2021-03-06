document.addEventListener("DOMContentLoaded", async function() {
    const x = document.getElementById("select");
    const response = await fetch('/customers');
    const data = await response.json();

    const promise = new Promise((resolve, reject) => {
        resolve(data)
    });

    data["customers"].forEach(customer => {
        var option = document.createElement("option");
        option.text = customer.name;
        option.setAttribute('id', customer.customer_id);
        x.add(option);
    });
});

function addItem(containerID, data) {
    let container = document.getElementById(containerID);
    if (Array.isArray(data)) {
        if (data.length === 0) {
            data = ['За цими параметрами не було знайдено нічого.'];
        }
        data.forEach((item) => {
            var elem = document.createElement('li');
            elem.innerHTML = `${item}`;
            container.appendChild(elem)
        });
    }
}

document.getElementById('search').addEventListener('click', async function(evt){
    evt.preventDefault();
    document.getElementById('parameters').classList = 'width-50';
    const select = document.getElementById('select');
    const customerID = select.options[select.selectedIndex].getAttribute('id');

    let response = await fetch(`/search_results_7?customer_id=${customerID}`);
    response = await response.json();
    console.log(response);

    if (response.status === 'ok') {
        document.getElementById('search_results').innerHTML = '';
        addItem('search_results', 'Результат пошуку:');
        addItem("search_results", response.users.map(user => user.first_name + " "+ user.last_name));
    } else {
        document.getElementById('search_results').innerHTML = '';
        addItem('search_results', ['За цими параметрами не було знайдено нічого.']);
    }
});
