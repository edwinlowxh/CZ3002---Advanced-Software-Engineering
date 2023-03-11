import { replaceTable } from "./transactionTable.js";

export async function deleteTransaction(event, element){
    const transaction_id = element.closest('tr').id;
    const formData = new FormData();
    formData.append('transaction_id', transaction_id);
    await fetch("http://127.0.0.1:8000/transactions/delete",
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
    .then(async () => {
        await replaceTable();
    })
    .catch(error => {
        error.then(data => {
            console.log(data)
            if ('non_field_errors' in data){
                alert(data['non_field_errors'])
            }
        });
    }  
    )    
}