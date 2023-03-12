import { getUpdateTransactionForm } from "./updateTransaction.js";
import { getTransaction } from "./getTransaction.js";
import { deleteTransaction } from "./deleteTransaction.js";

export async function replaceTable(){
    try{
        var data = await getTransaction();
    }
    catch(error){
        error.then(data => {
            // Display Error
        })
        return;
    }

    const newTable = generateTransactionTable(data);
    const existingTable = document.querySelector('#transaction-table');

    if (existingTable){
        existingTable.replaceWith(newTable);
    }
    else{
        document.querySelector('#table-div').appendChild(newTable);
    }
}

export function generateTransactionTable(data){
    const transactionType = sessionStorage.getItem('transactionTableType');

    console.log("HELLLOOO")
    console.log(transactionType)
    if (transactionType === 'INCOME'){
        var tableHeader = data['income_table_header'];
        document.querySelector("body").style.backgroundImage = "url('/static/nav/assets/img/income.jpeg')";
    }
    else{
        var tableHeader = data['expense_table_header'];
        document.querySelector("body").style.backgroundImage = "url('/static/nav/assets/img/expenses2.jpeg')";
    }

    const table = document.createElement("table");
    table.id = "transaction-table";
    table.classList.add("table", "table-hover", "table-dark");
    table.style = "margin-top: 80px; width:100%; margin:80px auto;border-collapse: collapse; border-radius: 1em; overflow: hidden; padding: 5px;";

    const thead = document.createElement("thead");
    table.appendChild(thead);
    const theadTr = document.createElement("tr");
    Object.entries(tableHeader).forEach(([id, header]) => {
        console.log("hello");
        const th = document.createElement("th");
        th.id = id;
        th.textContent = header;
        theadTr.appendChild(th);
    })
    theadTr.appendChild(document.createElement("th"));
    thead.append(theadTr);

    const tbody = document.createElement("tbody");

    if ('transactions' in data){
        const transactions = data['transactions'];
        transactions.forEach((transaction) => {
            if (transaction['type'] === transactionType){
                const tr = document.createElement("tr");
                tr.id = transaction["id"];
                
                Object.keys(tableHeader).forEach((header) => {
                    const td = document.createElement("td");
                    td.textContent = transaction[header];
                    tr.append(td);
                })
                
                const lastTd = document.createElement("td");
                lastTd.appendChild(editIcon());
                lastTd.appendChild(deleteIcon());
                
    
                tr.append(lastTd);
                tbody.append(tr);
            }
        })
    }
    
    table.append(tbody);

    return table;
}

function deleteIcon(){
    const attribute = document.createElement("a");
    attribute.style = "margin-right: 20px;";
    const span = document.createElement("span");
    span.classList.add("material-icons");
    span.addEventListener("click", (event) => {
        deleteTransaction(event, event.target);
    })
    span.addEventListener("mouseover", func, false);
    span.addEventListener("mouseout", func1, false);

    function func()
    {  
    span.setAttribute("style", "color:#3AEDCC;")
    }

    function func1()
    {  
    span.setAttribute("style", "color:white;")
    }
    span.textContent = "delete";
    attribute.appendChild(
        span
    )

    return attribute;
}

function editIcon(){
    const attribute = document.createElement("a");
    attribute.style = "margin-right: 20px;";
    const span = document.createElement("span");
    span.classList.add("material-icons");
    span.setAttribute("data-toggle", "modal");
    span.setAttribute("data-target", "#updateTransactionFormModal");
    span.addEventListener("click", (event) => {
        getUpdateTransactionForm(event.target);
    })
    span.addEventListener("mouseover", func, false);
    span.addEventListener("mouseout", func1, false);

    function func()
    {  
    span.setAttribute("style", "color:#3AEDCC;")
    }

    function func1()
    {  
    span.setAttribute("style", "color:white;")
    }
    span.textContent = "edit";
    attribute.appendChild(
        span
    )

    return attribute;
}