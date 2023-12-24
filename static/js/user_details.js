
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

    document.getElementById("tickets-button").classList.remove("selected");
    document.getElementById("bulletins-button").classList.add("selected");

    getBulletins("bulletins-record", filter)
}



document.getElementById("tickets-button").addEventListener("click", selectTickets);
document.getElementById("bulletins-button").addEventListener("click", selectBulletins);



const deleteButton = document.getElementById('delete-user-button');
const deleteForm = document.getElementById('delete-user')

deleteButton.addEventListener('click', (event) => {
    event.preventDefault();
    const confirmation = confirm('¿Estás seguro que quieres eliminar este usuario?');
    if (confirmation) {
        deleteForm.submit();
    }
});




const payWitheldAmountButton = document.getElementById('pay-witheld-amount-button');
const payWitheldAmountForm = document.getElementById('pay-witheld-amount')

payWitheldAmountButton.addEventListener('click', (event) => {
    event.preventDefault();
    const confirmation = confirm('Pagar ingresos retenidos');
    if (confirmation) {
        payWitheldAmountForm.submit();
    }
});



const payWitheldButton = document.getElementById('pay-witheld-button');
const payWitheldForm = document.getElementById('pay-witheld')

payWitheldButton.addEventListener('click', (event) => {
    event.preventDefault();
    const confirmation = confirm('Pagar Todos los ingresos retenidos');
    if (confirmation) {
        payWitheldForm.submit();
    }
});

