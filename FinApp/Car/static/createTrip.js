import { displayFormErrors } from "./error.js";
import { newTableRow } from "./table.js";
import { deleteTrip } from "./deleteTrip.js";


async function postCreateTripForm(event){
    event.preventDefault();
    const formData = new FormData(event.target);
    formData.append('create_trip', '')
    console.log(formData)

    await fetch(window.location.href,
    {
        "method": "POST",
        "body": formData,
        "Content-Type": "application/x-www-form-urlencoded"
    })
    .then(response => {
        if (!response.ok ){
            throw response.json()
        }
        return response.json();
    })
    .then((data) => {
        // document.querySelector('#createTripFormModal .close').click();
        // const newTr = newTableRow("#trip-table", data, deleteTrip);
        // document.querySelector("#trip-table tbody").appendChild(newTr);
        location.reload();
    })
    .catch((error) => {
        error.then(data => {
            if ('field_errors' in data){
                const field_errors = data['field_errors'];
                displayFormErrors('#create-category-form', field_errors);
            }
        });
    }  
    )
}

document.querySelector("#create-trip-form").addEventListener("submit", (event) => {
    postCreateTripForm(event);
})