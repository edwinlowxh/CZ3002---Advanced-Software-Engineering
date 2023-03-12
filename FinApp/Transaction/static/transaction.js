import { replaceTable } from './transactionTable.js';

window.addEventListener("DOMContentLoaded", async (event) => {
    sessionStorage.setItem("transactionTableType", "EXPENSE");
    await replaceTable();
})

export function transactionFormTypeChange(element){
    const selectedOption = element.options[element.selectedIndex].value;
    const categoryInput = document.querySelector(`#${element.closest('form').id} #category-name`);
    console.log("HELLLOOO")
    console.log(selectedOption)
    if (selectedOption === 'INCOME'){
        categoryInput.parentElement.style.display = "none";
        document.querySelector("body").style.backgroundImage = url('/static/nav/assets/img/income.jpeg')
    }
    else {
        categoryInput.parentElement.style.display = "block";
        document.querySelector("body").style.backgroundImage = url('/static/nav/assets/img/expenses.jpeg')
    }
}

export function displayFormErrors(formId, fieldErrors){
    for (const key in fieldErrors){
        const inputElement = document.querySelector(`#${formId} [name="${key}"]`);
        inputElement.classList.add("is-invalid");
        if (Array.isArray(fieldErrors[key])){
            const ulElement = document.createElement('ul');
            fieldErrors[key].forEach(e => {
                const liElement = document.createElement('li');
                liElement.innerHTML = e;
                ulElement.appendChild(liElement);
            });
            inputElement.parentNode.querySelector(".invalid-feedback").appendChild(ulElement);
        }
        else{
            inputElement.parentNode.querySelector(".invalid-feedback").innerHTML = fieldErrors[key];
        }                                      
    }
}

export function loadFormCategories(formId, categories){
    categories.forEach(category => {
        var option = document.createElement('option');
        option.value = category
        option.innerHTML = category
        document.querySelector(`#${formId} #category-name`).appendChild(
            option
        )
    });
}

document.querySelectorAll("#transaction-type").forEach((element) => {
    element.addEventListener("change", ()=> {
        transactionFormTypeChange(element);
    })
})

document.querySelectorAll("#transaction-type-radio-group input").forEach((element) => {
    element.addEventListener("click", async (event) => {
        document.querySelector("#table-title").textContent = event.target.id.toUpperCase();
        sessionStorage.setItem("transactionTableType", event.target.id.toUpperCase());
        await replaceTable();
    })
})

document.querySelectorAll(".date-filter").forEach((element) => {
    element.querySelector("input").addEventListener("change", async () => {
        await replaceTable();
    })
})



