import getTickets from './lazy_tickets.js'
import getBulletins from './lazy_bulletins.js'

let url_split = window.location.pathname.split('/')
let zone_id = url_split[url_split.length - 1]
    
filter = { 'zone_id': zone_id}

getTickets(filter)



function selectTickets() {
    document.getElementById("tickets-record").classList.remove("hidden");
    document.getElementById("bulletins-record").classList.add("hidden");

    document.getElementById("tickets-button").classList.add("selected");
    document.getElementById("bulletins-button").classList.remove("selected");

    getTickets(filter)
}
function selectBulletins() {
    document.getElementById("tickets-record").classList.add("hidden");
    document.getElementById("bulletins-record").classList.remove("hidden");

    document.getElementById("tickets-button").classList.remove("selected");
    document.getElementById("bulletins-button").classList.add("selected");

    getBulletins(filter)
}