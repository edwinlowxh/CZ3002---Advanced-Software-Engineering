export function fillForm(form, data){
    for (let key in data){
        if (data[key] != null){
            const inputElement = document.querySelector(`${form} [name="${key}"]`);
            inputElement.value = data[key];
        }
    }
}