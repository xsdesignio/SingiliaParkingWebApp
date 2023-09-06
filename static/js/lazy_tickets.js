// Here is the script to show the printed tickets into a lazy loading way
// We get the tickets from the server and we show them when the user scrolls down
// We use the IntersectionObserver API to detect when the user is at the bottom of the page
// and we show the tickets
// We use the IntersectionObserver API because it is more performant than the scroll event



const PAYMENT_METHODS = {
    CARD: 'Tarjeta',
    CASH: 'Efectivo',
    DEFAULT: 'Efectivo'
};



// ------------------------------------------------------------------------
// CREATING CLASES FOR MANAGE SUCH TICKETS AND BULLETINS FOR THE LAZY LOADING
// ------------------------------------------------------------------------

export class TicketsManager {
    constructor(element, record_wrapper_id, extra_filters = {}) {
        this.page = 0
        this.url = '/tickets/get-tickets/'
        this.record_wrapper_id = record_wrapper_id
        this.filter = {...extra_filters}
        this.ticketsLoadingElement = element

        this.initializeDOMElements()
    }

    initializeDOMElements() {
        this.ticket = this.ticketTemplate()

        let start_date = document.getElementById('start_date').value
        if(start_date != undefined && start_date != '')
            this.filter['start_date'] = start_date

        let end_date = document.getElementById('end_date').value
        if(end_date != undefined && end_date != '')
            this.filter['end_date'] = end_date

        let zone = document.getElementById('zone')?.value
        if(zone != undefined && zone != '')
            this.filter['zone'] = zone
    }


    showTicketsLot() {

        fetch(`/tickets/get-tickets/${this.page}`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify(this.filter)
            })
            .then(response => response.json())
            .then(data => {
                
                if(data != undefined && data.length > 0)
                    data.forEach(ticket => {
                        
                        let ticket_element = this.format_ticket(ticket)
                        document.getElementById(this.record_wrapper_id).insertAdjacentHTML('beforeend', ticket_element)
                    })
                else {
                    this.stopLoading()
                }
            })
        this.page += 1
    }

    ticketTemplate() {
        return `
            <div class="ticket [box_class]">
                <p>Fecha: <strong>[creation_date]</strong></p>
                <p>Hora: <strong>[creation_time]</strong></p>
                <p>Responsable: <strong>[responsible]</strong></p>
                <p>Duración: <strong>[duration] min</strong></p>
                <p>Precio: <strong>[price] €</strong></p>
                <p>
                    Método de pago: 
                    <strong> 
                        <payment-method>
                    </strong>
                </p>
                <p>Matrícula: <strong>[registration]</strong></p>
                <p>Zona: <strong>[zone_name]</strong></p>
                        
            </div>
        `
    }


    format_ticket(data) {

        switch (data.duration) {
            case 30:
                data.box_class = 'yellow-box'
                break;
            case 60:
                data.box_class = 'green-box'
                break;
            case 90:
                data.box_class = 'orange-box'
                break;
            case 120:
                data.box_class = 'pink-box'
                break;
        }


        //Extract the date and the time from the created_at field
        let creation_date = data.created_at.split(' ')[0]
        let creation_time = data.created_at.split(' ')[1]

        let payment_method = PAYMENT_METHODS[data.payment_method] || PAYMENT_METHODS.DEFAULT;

        return this.ticket.replace('[box_class]', data.box_class)
                    .replace('[creation_date]', creation_date)
                    .replace('[creation_time]', creation_time)
                    .replace('[responsible]', data.responsible)
                    .replace('[duration]', data.duration)
                    .replace('[price]', data.price)
                    .replace('[payment_method]', payment_method)
                    .replace('[registration]', data.registration)
                    .replace('[zone_name]', data.zone)
    }

    stopLoading() {
        this.ticketsLoadingElement.remove()
    }

}


export default function getTickets(record_wrapper_id, extra_filters = {}) {
    const loaderTrigger = document.getElementById("loadMoreTicketsTrigger");

    if(loaderTrigger != undefined) {
        const ticketsManager = new TicketsManager(loaderTrigger, record_wrapper_id, extra_filters);
        const observer = new IntersectionObserver((entries) => {
                
            if (entries[0].isIntersecting === true) {
                setTimeout(() => {
                    ticketsManager.showTicketsLot();
                }, 2000); 
            }
        }, { threshold: [1] });

        observer.observe(loaderTrigger);
    }
}



const isMainScript = [...document.scripts].some(script => 
    script.src.includes("lazy_tickets.js") && script.hasAttribute("data-main")
);

if (isMainScript) {
    getTickets("record");
}

