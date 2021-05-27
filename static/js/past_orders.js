class Salutation extends HTMLElement {
    connectedCallback() {
        var userName = this.attributes.username.value
        this.innerHTML = `Hello ${userName}...`
    }
}

customElements.define('salutation-element', Salutation);

// window.onload = function() {
//     myFunction(param1, param2);
//   };



document.addEventListener("DOMContentLoaded", async function() {
    var x = document.getElementById("mySelect");
    var option = document.createElement("option");
    option.text = "OOOO";
    // for (let item in departments.json()["authors"]) {
    //     x.add(item["name"]);
    // }
    x.add(option);
  });
    



(function($) {
$(document).ready(  
$.getJSON("http://localhost:8888/test.json", function(data){
    document.write(data);
}))
}); 