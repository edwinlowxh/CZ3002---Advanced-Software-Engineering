import { newTableRow } from "./table.js";
import { newTableHeader } from "./table.js";
import { getUpdateBudgetForm } from "./updateBudget.js";

export async function getBudget(){
    const month = document.querySelector("#inputMonth").selectedIndex;
    const year = document.querySelector("#inputYear").value;

    const formData = new FormData();
    formData.append('year', year);
    formData.append('month', month + 1);

    return await fetch(`http://127.0.0.1:8000/budgets/get`, {
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
        const thead = newTableHeader(data['budget_table_header'], true);
        document.querySelector("#budget-table").appendChild(thead);
        
        const tbody = document.createElement('tbody');
        document.querySelector("#budget-table").appendChild(tbody);
        const budgets = data["budgets"];
        budgets.forEach(budget => {
            const tr = newTableRow("#budget-table", budget, null, getUpdateBudgetForm, '#updateBudgetFormModal');
            tbody.appendChild(tr);
        })
    })
    .catch(error => {
        error.then(data => {
            console.error(data);
        })
    });
}

window.addEventListener('DOMContentLoaded', async() => {
    const now = new Date();
    document.querySelector("#inputMonth").selectedIndex = now.getMonth();
    document.querySelector("#inputYear").value = now.getFullYear();
    await(getBudget());
})

document.getElementById("inputMonth").addEventListener("change", async () => {
    Array.from(document.getElementById("budget-table").children).forEach(element => {
        element.remove();
    })
    await getBudget();
})

document.getElementById("inputYear").addEventListener("change", async () => {
    document.getElementById("budget-table").children.forEach(element => {
        element.remove();
    })
    await getBudget();
})