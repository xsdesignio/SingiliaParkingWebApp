const deleteButtons = Array.from(document.getElementsByClassName('delete-button'));
const deleteForms = Array.from(document.getElementsByClassName('delete-form'));

deleteButtons.forEach((button, index) => {
    button.addEventListener('click', (event) => {
        event.preventDefault();
        const confirmation = confirm('¿Estás seguro que quieres eliminar este modelo de ticket?');
        if (confirmation) {
            deleteForms[index].submit();
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    let inputElement = document.getElementById("duration");
    inputElement.addEventListener("keyup", function() {
        toUppercase(inputElement);
    });
});

function toUppercase(inputElement) {
    inputElement.value = inputElement.value.toUpperCase();
}