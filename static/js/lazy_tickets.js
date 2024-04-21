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

        const urlParams = new URLSearchParams(window.location.search);

        let start_date = urlParams.get('start_date')
        
        if(start_date != undefined && start_date != '')
            this.filter['start_date'] = start_date

        let end_date = urlParams.get('end_date')
        
        if(end_date != undefined && end_date != '')
            this.filter['end_date'] = end_date

        let zone = urlParams.get('zone')
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
            <div class="ticket green-box">
                <p>[id]</p>
                <p class="capital-letter">[responsible]</p>
                <p>[registration]</p>
                <p>[zone_name]</p>
                <p>[creation_date] [creation_time]</p>
                <p>[duration]</p>
                <p>[price] €</p>
                <p>[payment_method]</p>
                        
            </div>
        `
    }


    format_ticket(data) {

        //Extract the date and the time from the created_at field
        let creation_date = data.created_at.split(' ')[0]
        let creation_time = data.created_at.split(' ')[1]

        // Modifying creation_date to set in format of day-month-year
        creation_date = creation_date.split('-').reverse().join('-')

        let payment_method = PAYMENT_METHODS[data.payment_method] || PAYMENT_METHODS.DEFAULT;

        return this.ticket.replace('[id]', data.id)
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

