async function getCreateTransactionForm(){
    await fetch("http://127.0.0.1:8000/transactions/create", {"method": "GET"})
    .then(response => response.json())
    .then(data => {
        data['categories'].forEach(category => {
            var option = document.createElement('option');
            option.value = category
            option.innerHTML = category
            document.getElementById('transaction-category').appendChild(
                option
            )
        });
    })
    .catch(error => console.error(error));
}

async function postCreateTransactionForm(event, transactionForm){
    event.preventDefault();
    const formData = new FormData(transactionForm);
    for (let [key, value] of formData.entries()){
        console.log(`${key}: ${value}`);
    }
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
    .then(data => {
    })
    .catch(error => {
        error.then(data => {
            console.log(data)
            if ('field_errors' in data){
                const field_errors = data['field_errors'];
                
                for (const key in field_errors){
                    const inputElement = document.querySelector(`#transaction-form [name="${key}"]`);
                    inputElement.classList.add("is-invalid");
                    if (Array.isArray(field_errors[key])){
                        const ulElement = document.createElement('ul');
                        field_errors[key].forEach(e => {
                            const liElement = document.createElement('li');
                            liElement.innerHTML = e;
                            ulElement.appendChild(liElement);
                        });
                        inputElement.parentNode.querySelector(".invalid-feedback").appendChild(ulElement);
                    }
                    else{
                        inputElement.parentNode.querySelector(".invalid-feedback").innerHTML = field_errors[key];
                    }                                      
                }
            }
        });
    }  
    )
}

async function getUpdateTransactionForm(element){
    const transaction_id = element.closest('tr').id;
    
    await fetch(`http://127.0.0.1:8000/transactions/update?transaction_id=${transaction_id}`, {
        "method": "GET"
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => console.error(error));
}

function transactionTypeChange(e){
    selectedOption = e.options[e.selectedIndex].value;

    if (selectedOption === 'INCOME'){
        document.getElementById("transaction-category").parentElement.style.display = "none";
    }
    else {
        document.getElementById("transaction-category").parentElement.style.display = "block";
    }
}


