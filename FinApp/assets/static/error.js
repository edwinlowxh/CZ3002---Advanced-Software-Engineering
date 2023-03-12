export function displayFormErrors(formSelector, fieldErrors){
    for (const key in fieldErrors){
        const inputElement = document.querySelector(`${formSelector} [name="${key}"]`);
        inputElement.classList.add("is-invalid");
        if (Array.isArray(fieldErrors[key])){
            const ulElement = document.createElement('ul');
            fieldErrors[key].forEach(e => {
                const liElement = document.createElement('li');
                liElement.innerHTML = e;
                ulElement.appendChild(liElement);
            });
            inputElement.parentNode.querySelector(".invalid-feedback").innerHTML = '';
            inputElement.parentNode.querySelector(".invalid-feedback").appendChild(ulElement);
        }
        else{
            inputElement.parentNode.querySelector(".invalid-feedback").innerHTML = fieldErrors[key];
        }                                      
    }
}