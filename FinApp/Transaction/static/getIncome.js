export async function getIncome(){
    console.log("does it work");
    var queryParam = queryParam + `start_date=2023-03-01`;
    var queryParam = queryParam + `&end_date=2023-03-31`;
    
    return await fetch(`http://127.0.0.1:8000/transactions/get?${queryParam}`, {"method": "GET"})
    .then(response => {
        if (!response.ok ){
            throw response.json()
        }
        return response.json();
    })
    .then(data => {
        return data;
    })
    .catch(error => {
        throw error;
    });
}