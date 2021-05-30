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

    let response = await fetch(`/search_results_11`);
    response = await response.json();
    console.log(response);

    if (response.status === 'ok') {
        document.getElementById('search_results').innerHTML = '';
        addItem('search_results', 'Результат пошуку:');
        addItem("search_results", response.orders.map(entry => `Місяць: ${entry.month}, кількість: ${entry.num_orders}`));
    } else {
        document.getElementById('search_results').innerHTML = '';
        addItem('search_results', ['За цими параметрами не було знайдено нічого.']);
    }
});
