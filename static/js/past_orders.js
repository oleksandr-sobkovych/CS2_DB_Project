class Salutation extends HTMLElement {
    connectedCallback() {
        var userName = this.attributes.username.value
        this.innerHTML = `Hello ${userName}...`
    }
}

customElements.define('salutation-element', Salutation);


document.addEventListener("DOMContentLoaded", async function() {
    var x = document.getElementById("mySelect");
    var option = document.createElement("option");

    const response = await fetch('/authors')

    const data = await response.json()
    // const data = response

    const promise = new Promise((resolve, reject) => {
        resolve(data)
    })


    for (let item in data["authors"]){
        var option = document.createElement("option");
        option.text = data["authors"][item]["name"];
        x.add(option);

    }
    // })

   
    });

function addRow(tableID, data) {
    let tableRef = document.getElementById(tableID);
    for (let item in data){
        // console.log(item)
        let newRow = tableRef.insertRow(-1);
        let newCell = newRow.insertCell(0);
    
        let newText = document.createTextNode(data[item].name+" "+data[item].dateStart+" "+data[item].dateEnd);
    
        newCell.appendChild(newText);
    }
    
    }

document.getElementById('formmm').addEventListener('submit', function(evt){
    evt.preventDefault();
    // console.log(document.getElementById("formmm").submit());
    console.log(document.getElementById('mySelect').value)
    console.log(document.getElementById('maxNum').value)
    console.log(document.getElementById('dateStart').value)
    console.log(document.getElementById('dateEnd').value)


    // var url = new URL("/search_1"),
    // params = {author_id:document.getElementById('mySelect'),
    //     mess_num: document.getElementById('maxNum').value,
    //     date_start: document.getElementById('dateStart').value,
    //     date_end: document.getElementById('dateEnd').value}
    // Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
    // // fetch(url).then(...)
    // const response = await fetch(url)


    let users = [{name: "Maria Garcia",
                dateStart: "10-02-2020",
                dateEnd: "12-02-2020",
    },
    {name: "James Smith",
                dateStart: "10-02-2020",
                dateEnd: "12-02-2020",
    }]

    response = {'status': 'ok', 'users': users}
    
    addRow("result_table", users)


    // document.getElementById('dateEnd').style.display = 'none'
    // document.getElementById('topMessage').style.display = 'none';
})
