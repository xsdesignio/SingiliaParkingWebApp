
import getTickets from "./lazy_tickets.js";
import getBulletins from "./lazy_bulletins.js";



let url_split = window.location.pathname.split('/')
let user_id = url_split[url_split.length - 1]

let filter = { 
    'responsible_id': user_id
}

getTickets("tickets-record", filter)



function selectTickets() {
    document.getElementById("tickets-record-wrapper").classList.remove("hidden");
    document.getElementById("bulletins-record-wrapper").classList.add("hidden");

    document.getElementById("tickets-button").classList.add("selected");
    document.getElementById("bulletins-button").classList.remove("selected");

    getTickets("tickets-record", filter)
}

function selectBulletins() {
    document.getElementById("tickets-record-wrapper").classList.add("hidden");
    document.getElementById("bulletins-record-wrapper").classList.remove("hidden");
    console.log("This should be executed now")

    document.getElementById("tickets-button").classList.remove("selected");
    document.getElementById("bulletins-button").classList.add("selected");
    console.log("This should be executed now 2")
    getBulletins("bulletins-record", filter)
}



document.getElementById("tickets-button").addEventListener("click", selectTickets);
document.getElementById("bulletins-button").addEventListener("click", selectBulletins);
