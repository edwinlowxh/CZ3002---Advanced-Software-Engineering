export async function getTransaction(){
    const startDate = document.querySelector("#transaction-start-date").value;
    const endDate = document.querySelector("#transaction-end-date").value;

    var queryParam = '';
    if (startDate.length > 0){
        var queryParam = queryParam + `start_date=${startDate}`;
    }

    if (endDate.length > 0){
        var queryParam = queryParam + `&end_date=${endDate}`;
    }

    const data = await fetch(`http://127.0.0.1:8000/transactions/get?${queryParam}`, {"method": "GET"})
    .then(response => response.json())
    .then(data => {
        return data;
    })
    .catch(error => console.error(error));

    return data;
}