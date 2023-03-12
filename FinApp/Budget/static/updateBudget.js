import { newTableRow } from "./table.js";
import { displayFormErrors } from "./error.js"

export async function postUpdateBudgetForm(event, budget_id, category_name){
    event.preventDefault();
    const month = document.querySelector("#inputMonth").selectedIndex;
    const year = document.querySelector("#inputYear").value;

    const formData = new FormData(event.target);
    formData.append('year', year);
    formData.append('month', month + 1);
    formData.append('budget_id', budget_id);
    formData.append('category_name', category_name);

    return await fetch(`http://127.0.0.1:8000/budgets/update_budget`, {
        "method": "POST",
        "body": formData
    })
    .then(response => {
        if (!response.ok ){
            throw response.json()
        }
        return response.json();
    })
    .then(data => {
        const newTr = newTableRow("#budget-table", data, null, getUpdateBudgetForm, '#updateBudgetFormModal');
        document.querySelector(`#budget-table tbody [id="${budget_id}"]`).replaceWith(newTr);
        document.querySelector('#updateBudgetFormModal .close').click();
    })
    .catch(error => {
        error.then(data => {
            if ('field_errors' in data){
                console.error(data['field_errors'])
                displayFormErrors('#update-budget-form', data['field_errors'])
            }
        })
    });
}

export async function getUpdateBudgetForm(event){
    const budget_id = event.target.closest('tr').id;
    const budget_name = event.target.closest('tr').querySelector('td').textContent;
    
    document.querySelector("#updateBudgetFormModal .modal-title").textContent = `Update ${budget_name}'s limit`
    document.querySelector("#update-budget-form").addEventListener("submit", async (event) => {
        await postUpdateBudgetForm(event, budget_id, budget_name);
    })
}