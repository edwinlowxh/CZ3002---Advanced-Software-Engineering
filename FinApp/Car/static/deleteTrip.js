window.deleteTrip = deleteTrip

export async function deleteTrip(event){
    event.preventDefault();
    const trip_id = event.target.closest('tr').id;
    const formData = new FormData();
    formData.append('trip_id', trip_id);
    await fetch("http://127.0.0.1:8000/car/delete_trip/",
    {
        "method": "POST",
        "body": formData,
        "Content-Type": "application/x-www-form-urlencoded"
    })
    .then(response => {
        if (!response.ok ){
            throw response.json();
        }
        return response.json();
    })
    .then(() => {
        // event.target.closest('tr').remove();
        location.reload();
    })
    .catch(error => {
        console.error(error);
        error.then(data => {
            alert(data);
        });
    }  
    )    
}