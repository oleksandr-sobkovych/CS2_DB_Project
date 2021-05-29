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
    
    const numCustomer = document.getElementById('numCustomer');

    // const authorID = select.options[select.selectedIndex].getAttribute('id');
    // const num = document.getElementById('maxNum').value;
    const dateStart = document.getElementById('dateStart').value;
    const dateEnd = document.getElementById('dateEnd').value;

    let response = await fetch(`/search_results_3?numCustomer=${numCustomer}&date_start=${dateStart}&date_end=${dateEnd}`);
    response = await response.json();
    console.log(response);

    if (response.status === 'ok') {
        document.getElementById('search_results').innerHTML = '';
        addItem('search_results', 'Результат пошуку:');
        addItem("search_results", response.users.map(user => user.name));
    } else {
        document.getElementById('search_results').innerHTML = '';
        addItem('search_results', ['За цими параметрами не було знайдено нічого.']);
    }
});
