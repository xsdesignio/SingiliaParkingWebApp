

const PAYMENT_METHODS = {
    CARD: 'Tarjeta',
    CASH: 'Efectivo',
    DEFAULT: 'Efectivo'
};


export class BulletinsManager {
    constructor(element, record_wrapper_id = "record", extra_filters = {}) {
        this.page = 0
        this.record_wrapper_id = record_wrapper_id
        this.filter = extra_filters
        
        this.bulletinsLoadingElement = element

        this.initializeDOMElements()
    }

    initializeDOMElements() {

        this.bulletin = this.bulletinTemplate()

        let start_date = document.getElementById('start_date').value
        if(start_date != undefined && start_date != '')
            this.filter['start_date'] = start_date

        let end_date = document.getElementById('end_date').value
        if(end_date != undefined && end_date != '')
            this.filter['end_date'] = end_date

        let zone = document.getElementById('zone')?.value
        if(zone != undefined && zone != '')
            this.filter['zone_name'] = zone
    }


    bulletinTemplate() {
        return `
            <div class="ticket bulletin-box">
                <p>Fecha: <strong>[creation_date]</strong></p>
                <p>Hora: <strong>[creation_time]</strong></p>
                <p>Responsable: <strong>[responsible]</strong></p>
                <p>Duración: <strong>[duration] min</strong></p>
                <p>Precio: <strong>[price] €</strong></p>
                <p>
                    Método de pago: 
                    <strong> 
                        [payment_method]
                    </strong>
                </p>
                <p>Matrícula: <strong>[registration]</strong></p>
                <p>Zona: <strong>[zone_name]</strong></p>
            </div>
        `
    }


    showBulletinsLot() {
        fetch(`/bulletins/get-bulletins/${this.page}`,
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
                
                if(data != undefined && data.length > 0) {

                    data.forEach(bulletin => {
                        let bulletin_element = this.format_bulletin(bulletin)
                        document.getElementById(this.record_wrapper_id).insertAdjacentHTML('beforeend', bulletin_element)
            
                    })
                }
                else {
                    this.stopLoading()
                }

            })

        this.page += 1
    }

    format_bulletin(data) {

        let payment_method = PAYMENT_METHODS[data.payment_method] || PAYMENT_METHODS.DEFAULT;
        
        //Extract the date and the time from the created_at field
        let creation_date = data.created_at.split(' ')[0]
        let creation_time = data.created_at.split(' ')[1]

        let formatted_bulletin = this.bulletin.replace('[creation_date]', creation_date)
                    .replace('[creation_time]', creation_time)
                    .replace('[responsible]', data.responsible)
                    .replace('[duration]', data.duration)
                    .replace('[price]', data.price)
                    .replace('[payment_method]', payment_method)
                    .replace('[registration]', data.registration)
                    .replace('[zone_name]', data.zone)

        let car_data = this.format_bulletin_car_info(data) 
        let formatted_element = formatted_bulletin.replace('</div>', car_data + '</div>')
        
        return formatted_element
        
    }

    format_bulletin_car_info(data) {
        let car_data = "";

        if(
            (data.model != null && data.model != "") || 
            (data.brand != null && data.brand != "") || 
            (data.color != null && data.color != "")
        ) {
            car_data = `<span class="divider"></span>`

            if(data.brand != null && data.brand != "")
                car_data += `<p>Marca: <strong>${data.brand}</strong></p>`
            if(data.model != null && data.model != "") 
                car_data += `<p>Modelo: <strong>${data.model}</strong></p>`
            if(data.color != null && data.color != "")
                car_data += `<p>Color: <strong>${data.color}</strong></p>`
        }

        return car_data
    }


    stopLoading() {
        this.bulletinsLoadingElement.remove()

    }

}


// Create the observer to observe if the user is during more than 3 seconds at the bottom of the page
// If the user is during more than 3 seconds at the bottom of the page, we load more tickets
export default function getBulletins(record_wrapper_id, extra_filters = {}) {
    const loaderTrigger = document.getElementById("loadMoreBulletinsTrigger");

    if(loaderTrigger != undefined) {
        const bulletinsManager = new BulletinsManager(loaderTrigger, record_wrapper_id, extra_filters);
        const observer = new IntersectionObserver((entries) => {
                
            if (entries[0].isIntersecting === true) {
                
                setTimeout(() => {
                    bulletinsManager.showBulletinsLot();
                }, 2000); // Change to 3 seconds based on the comment
            } 
        }, { threshold: [1] });

        observer.observe(loaderTrigger);
    }
}



const isMainScript = [...document.scripts].some(script => 
    script.src.includes("lazy_bulletins.js") && script.hasAttribute("data-main")
);

if (isMainScript) {
    getBulletins("record");
}
