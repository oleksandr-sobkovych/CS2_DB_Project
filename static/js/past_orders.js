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
document.getElementById('formmm').addEventListener('submit', function(evt){
    evt.preventDefault();
    console.log("KJJK")
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


    // response = {'status': 'ok', 'users': users}
    
    // document.getElementById('dateEnd').style.display = 'none'
    // document.getElementById('topMessage').style.display = 'none';
})
