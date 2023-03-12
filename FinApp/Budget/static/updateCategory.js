import { fillForm } from "./form.js";
import { newTableRow } from "./table.js";
import { deleteCategory } from "./deleteCategory.js";


window.getUpdateCategoryForm = getUpdateCategoryForm;

export async function getUpdateCategoryForm(event){
    const category_id = event.target.closest('tr').id;
    
    await fetch(`http://127.0.0.1:8000/budget/update_category?category_id=${category_id}`, {
        "method": "GET"
    })
    .then(response => {
        if ( !response.ok ){
            throw response.json();
        }
        return response.json()
    })
    .then(data => {
        fillForm("#update-category-form", data['category']);
        document.getElementById("update-category-form").onsubmit = (event) => {
            postUpdateCategoryForm(event, category_id);
        };
    })
    .catch((error) => {
        console.log(error)
        error.then(data => {
            if ('field_errors' in data){
                const field_errors = data['field_errors'];
                displayFormErrors('#update-category-form', field_errors);
            }
        });
    }  
    );
}

export async function postUpdateCategoryForm(event, category_id){
    event.preventDefault();
    const formData = new FormData(event.target);
    formData.append('category_id', category_id);

    await fetch("http://127.0.0.1:8000/budget/update_category",
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
        const newTr = newTableRow("#category-table", data, deleteCategory, getUpdateCategoryForm, "#updateCategoryFormModal");
        document.querySelector(`#category-table tbody [id="${category_id}"]`).replaceWith(newTr);
        document.querySelector('#updateCategoryFormModal .close').click();
    })
    .catch(error => {
        console.log(error);
        error.then(data => {
            console.log(data)
            if ('field_errors' in data){
                const field_errors = data['field_errors'];
                displayFormErrors('#update-transaction-form', field_errors);
            }
        });
    }  
    )
}