

const PAYMENT_METHODS = {
    CARD: 'Tarjeta',
    CASH: 'Efectivo',
    DEFAULT: 'Efectivo'
};


// Modificar this.bulletin para que no haya ninguno definido, ya que el template varía según se haya pagado o aún no

export class BulletinsManager {
    constructor(element, record_wrapper_id = "record", extra_filters = {}) {
        this.page = 0
        this.record_wrapper_id = record_wrapper_id
        this.filter = extra_filters
        
        this.bulletinsLoadingElement = element

        this.initializeDOMElements()
    }

    initializeDOMElements() {
        const urlParams = new URLSearchParams(window.location.search);

        let start_date = urlParams.get('start_date')
        if(start_date != undefined && start_date != '')
            this.filter['start_date'] = start_date

        let end_date = urlParams.get('end_date')
        if(end_date != undefined && end_date != '')
            this.filter['end_date'] = end_date

        let zone = urlParams.get('zone')
        if(zone != undefined && zone != '')
            this.filter['zone_name'] = zone
    }


    bulletinTemplate(paid) {

        let template =  `
            <div class="bulletin bulletin-box">
                <p class="capital-letter">[id]</p>
                <p class="capital-letter">[responsible]</p>
                <p><strong>[registration]</strong></p>
                <p><strong>[zone_name]</strong></p>
                <p>[creation_date] [creation_time]</p>
                <p><strong>[paid]</strong></p>
        `

        if(paid)
            template+=`
                <p><strong>[price] €</strong></p>
                <p>Duración: <strong>[duration]</strong></p>
                <p style="width:100px"><strong>[precept]</strong></p>
                <p>
                    <strong> 
                        [payment_method]
                    </strong>
                </p>`
        else 
            template+=`
                <p></p>
                <p></p>
                <p style="width:100px"></p>
                <p></p>
            `

        template += '</div>'

        return template
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

    format_bulletin(bulletin) {

        let payment_method = PAYMENT_METHODS[bulletin.payment_method] || "Aún no ha sido pagado";
        //Extract the date and the time from the created_at field
        let creation_date = bulletin.created_at.split(' ')[0]
        let creation_time = bulletin.created_at.split(' ')[1]

        // Modifying creation_date to set in format of day-month-year
        creation_date = creation_date.split('-').reverse().join('-')

        let bulletin_template = this.bulletinTemplate(bulletin.paid)
        let formatted_bulletin = bulletin_template.replace('[id]', bulletin.id)
                    .replace('[creation_date]', creation_date)
                    .replace('[creation_time]', creation_time)
                    .replace('[responsible]', bulletin.responsible)
                    .replace('[registration]', bulletin.registration)
                    .replace('[zone_name]', bulletin.zone)
                    .replace('[paid]', bulletin.paid ? 'Pagado' : 'No pagado')

        console.log(formatted_bulletin)
        if(bulletin.paid == true)
            formatted_bulletin = formatted_bulletin.replace('[duration]', bulletin.duration)
                    .replace('[price]', bulletin.price)
                    .replace('[payment_method]', payment_method)
                    .replace('[precept]', bulletin.precept)

        let car_data = this.format_bulletin_car_info(bulletin) 
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
            if(data.brand != null && data.brand != "")
                car_data += `<p>${data.brand}</p>`
            if(data.model != null && data.model != "") 
                car_data += `<p>${data.model}</p>`
            if(data.color != null && data.color != "")
                car_data += `<p>${data.color}</p>`
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
