import { replaceTable } from './table.js';
import { loadFormCategories, displayFormErrors, transactionFormTypeChange } from './transaction.js';

window.getUpdateTransactionForm = getUpdateTransactionForm;

export async function getUpdateTransactionForm(element){
    const transaction_id = element.closest('tr').id;
    
    await fetch(`http://127.0.0.1:8000/transactions/update?transaction_id=${transaction_id}`, {
        "method": "GET"
    })
    .then(response => {
        if ( !response.ok ){
            throw response.json();
        }
        return response.json()
    })
    .then(data => {
        const transaction = data['transaction']
        for (let key in transaction){
            if (transaction[key] != null){
                const inputElement = document.querySelector(`#update-transaction-form [name="${key}"]`);
                inputElement.value = transaction[key];
            }
        }
        
        document.querySelector("#update-transaction-form #category-name").innerHTML = '';
        loadFormCategories("update-transaction-form", data['categories']);
        
        transactionFormTypeChange(document.querySelector("#update-transaction-form #transaction-type"));
        if (transaction['transaction_type'] === 'EXPENSE'){
            document.querySelector("#update-transaction-form #category-name").value = transaction['category_name'];
        }

        document.getElementById("update-transaction-form").onsubmit = (event) => {
            postUpdateTransactionForm(event, document.getElementById("update-transaction-form"), transaction_id)
        };
    })
    .catch((error) => {
        error.then(data => {
            if ('field_errors' in data){
                const field_errors = data['field_errors'];
                displayFormErrors('create-transaction-form', field_errors);
            }
        });
    }  
    );
}

export async function postUpdateTransactionForm(event, updateTransactionForm, transaction_id){
    event.preventDefault();
    const formData = new FormData(updateTransactionForm);
    formData.append('transaction_id', transaction_id);

    // await fetch("http://127.0.0.1:8000/transactions/update",
    // {
    //     "method": "POST",
    //     "body": formData,
    //     "Content-Type": "application/x-www-form-urlencoded"
    // })
    // .then(response => {
    //     if (!response.ok ){
    //         throw response.json()
    //     }
    //     return response.json();
    // })
    // .then(async (data) => {
    //     replaceTable();
    // })
    // .catch(error => {
    //     error.then(data => {
    //         console.log(data)
    //         if ('field_errors' in data){
    //             const field_errors = data['field_errors'];
    //             displayFormErrors('update-transaction-form', field_errors);
    //         }
    //     });
    // }  
    // )

    event.target.closest('modal')
}

document.querySelector("#update-transaction-form").addEventListener("submit", (event) => {
    postUpdateTransactionForm(event, event.target);
})