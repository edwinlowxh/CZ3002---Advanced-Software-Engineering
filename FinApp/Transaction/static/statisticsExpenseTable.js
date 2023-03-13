import { getExpense } from "./getExpense.js";

export async function replaceTable(){
    try{
        console.log("in expense");
        var data = await getExpense();
    }
    catch(error){
        error.then(data => {
            // Display Error
        })
        return;
    }

    const newTable = generateTransactionTable(data);
    const existingTable = document.querySelector('#expense-table');

    if (existingTable){
        existingTable.replaceWith(newTable);
    }
    else{
        document.querySelector('#expense-table-div').appendChild(newTable);
    }
}

export function generateTransactionTable(data){
    var tableHeader = data['expense_table_header'];
    console.log(tableHeader)
    // document.querySelector("body").style.backgroundImage = "url('/static/nav/assets/img/expenses2.jpeg')";
    
    const table = document.createElement("table");
    table.id = "expense-table";
    table.classList.add("table", "table-hover", "table-dark");
    table.style = "width:100%; border-collapse: collapse; border-radius: 1em; overflow: hidden; padding: 5px;";

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
    // theadTr.appendChild(document.createElement("th"));
    thead.append(theadTr);

    const tbody = document.createElement("tbody");

    if ('transactions' in data){
        const transactions = data['transactions'];
        transactions.forEach((transaction) => {
            if (transaction['type'] === 'EXPENSE'){
                const tr = document.createElement("tr");
                tr.id = transaction["id"];
                
                Object.keys(tableHeader).forEach((header) => {
                    const td = document.createElement("td");
                    td.textContent = transaction[header];
                    tr.append(td);
                })
                
                // const lastTd = document.createElement("td");
                // lastTd.style = "text-align:right;";
                // lastTd.appendChild(editIcon());
                // lastTd.appendChild(deleteIcon());
                
    
                // tr.append(lastTd);
                tbody.append(tr);
            }
        })
    }
    
    table.append(tbody);

    return table;
}
