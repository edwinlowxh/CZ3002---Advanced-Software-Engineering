import { displayFormErrors } from "./error.js";
import { newTableRow } from "./table.js";
import { deleteCategory } from "./deleteCategory.js";
import { getUpdateCategoryForm } from "./updateCategory.js";

async function postCreateCategoryForm(event){
    event.preventDefault();
    const formData = new FormData(event.target);

    await fetch("http://127.0.0.1:8000/budget/create_category",
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
        document.querySelector('#createCategoryFormModal .close').click();
        const newTr = newTableRow("#category-table", data, deleteCategory, getUpdateCategoryForm, "#updateCategoryFormModal");
        document.querySelector("#category-table tbody").appendChild(newTr);
    })
    .catch((error) => {
        console.error(error);
        error.then(data => {
            if ('field_errors' in data){
                const field_errors = data['field_errors'];
                displayFormErrors('#create-category-form', field_errors);
            }
        });
    }  
    )
}

document.querySelector("#create-category-form").addEventListener("submit", (event) => {
    postCreateCategoryForm(event);
})