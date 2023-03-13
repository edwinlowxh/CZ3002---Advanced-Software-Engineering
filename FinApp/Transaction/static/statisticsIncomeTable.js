import { getIncome } from "./getIncome.js";

export async function replaceTable(){
    try{
        var data = await getIncome();
    }
    catch(error){
        error.then(data => {
            // Display Error
        })
        return;
    }

    const newTable = generateTransactionTable(data);
    const existingTable = document.querySelector('#income-table');

    if (existingTable){
        existingTable.replaceWith(newTable);
    }
    else{
        document.querySelector('#income-table-div').appendChild(newTable);
    }
}

export function generateTransactionTable(data){
    var tableHeader = data['income_table_header'];
    // document.querySelector("body").style.backgroundImage = "url('/static/nav/assets/img/income.jpeg')";
    
    const table = document.createElement("table");
    table.id = "income-table";
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
            if (transaction['type'] === 'INCOME'){
                const tr = document.createElement("tr");
                tr.id = transaction["id"];
                
                Object.keys(tableHeader).forEach((header) => {
                    const td = document.createElement("td");
                    td.textContent = transaction[header];
                    tr.append(td);
                })
                
                tbody.append(tr);
            }
        })
    }
    
    table.append(tbody);

    return table;
}

