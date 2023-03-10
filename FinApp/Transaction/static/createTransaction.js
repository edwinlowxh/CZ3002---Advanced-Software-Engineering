import { replaceTable } from './table.js';
import { loadFormCategories, displayFormErrors } from './transaction.js';


window.getCreateTransactionForm = getCreateTransactionForm;

async function getCreateTransactionForm(){
    await fetch("http://127.0.0.1:8000/transactions/create", {"method": "GET"})
    .then(response => response.json())
    .then(data => {
        document.querySelector("#create-transaction-form #category-name").innerHTML = '';
        loadFormCategories("create-transaction-form", data['categories']);
    })
    .catch(error => console.error(error));
}

async function postCreateTransactionForm(event, createTransactionForm){
    event.preventDefault();
    const formData = new FormData(createTransactionForm);

    await fetch("http://127.0.0.1:8000/transactions/create",
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
    .then(async (data) => {
        await replaceTable();
    })
    .catch(error => {
        error.then(data => {
            console.log(data)
            if ('field_errors' in data){
                const field_errors = data['field_errors'];
                displayFormErrors('create-transaction-form', field_errors);
            }
        });
    }  
    )
}

document.querySelector("#create-transaction-form").addEventListener("submit", (event) => {
    postCreateTransactionForm(event, event.target);
})