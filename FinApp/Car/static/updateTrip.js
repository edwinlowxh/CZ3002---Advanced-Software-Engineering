import { fillForm } from "./form.js";
import { newTableRow } from "./table.js";
import { deleteTrip } from "./deleteTrip.js";


window.getUpdateTripForm = getUpdateTripForm;

export async function getUpdateTripForm(event){
    const trip_id = event.target.closest('tr').id;
    const formData = new FormData();
    formData.append('trip_id', trip_id);
    
    await fetch(`http://127.0.0.1:8000/car/get_trip/`, {
        "method": "POST",
        "body": formData,
        "Content-Type": "application/x-www-form-urlencoded"
    })
    .then(response => {
        if ( !response.ok ){
            throw response.json();
        }
        return response.json()
    })
    .then(data => {
        fillForm("#update-trip-form", data['trip']);
        document.getElementById("update-trip-form").onsubmit = (event) => {
            postUpdateTripForm(event, trip_id);
        };
    })
    .catch((error) => {
        console.log(error);
    });
}

export async function postUpdateTripForm(event, trip_id){
    event.preventDefault();
    const formData = new FormData(event.target);
    formData.append('trip_id', trip_id);

    await fetch("http://127.0.0.1:8000/car/update_trip/",
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
        // const newTr = newTableRow("#trip-table", data, deleteTrip, getUpdateTripForm, "#updateTripFormModal");
        // document.querySelector(`#trip-table tbody [id="${trip_id}"]`).replaceWith(newTr);
        // document.querySelector('#updateTripFormModal .close').click();
        location.reload();
    })
    .catch(error => {
        console.log(error);
        error.then(data => {
            console.log(data)
            if ('field_errors' in data){
                const field_errors = data['field_errors'];
                displayFormErrors('#update-trip-form', field_errors);
            }
        });
    });
}