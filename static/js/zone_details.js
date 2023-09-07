import getTickets from './lazy_tickets.js'
import getBulletins from './lazy_bulletins.js'

let url_split = window.location.pathname.split('/')
let zone_id = url_split[url_split.length - 1]

    
let filter = { 'zone_id': zone_id }

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

    document.getElementById("tickets-button").classList.remove("selected");
    document.getElementById("bulletins-button").classList.add("selected");

    getBulletins("bulletins-record", filter)
}


document.getElementById("tickets-button").addEventListener("click", selectTickets);
document.getElementById("bulletins-button").addEventListener("click", selectBulletins);



const deleteButton = document.getElementById('delete-zone-button');
const deleteForm = document.getElementById('delete-zone')

deleteButton.addEventListener('click', (event) => {
    event.preventDefault();
    const confirmation = confirm('¿Estás seguro que quieres eliminar este usuario?');
    if (confirmation) {
        deleteForm.submit();
    }
});