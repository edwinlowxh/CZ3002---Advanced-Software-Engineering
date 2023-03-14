export function newTableHeader(headers, extraCol){
    const thead = document.createElement("thead");

    const tr = document.createElement("tr");
    Object.entries(headers).forEach(([key, header]) => {
        const td = document.createElement("td");
        td.innerText = header;
        td.id = key;
        tr.appendChild(td);
    })

    if (extraCol){
        const td = document.createElement("td");
        td.style = "width: 30%;";
        tr.appendChild(document.createElement("td"));
    }

    thead.appendChild(tr);
    return thead;
}

export function newTableRow(tableSelector, data, deleteCallback, updateCallback, updateFormModalSelector){
    const table = document.querySelector(`${tableSelector}`);
    const tableHeader = table.querySelector('thead tr');
    const columnOrder = Array.from(tableHeader.children).map((th) => th.id);
    columnOrder.pop();

    const newTr = document.createElement('tr')

    if ('id' in data){
        newTr.id = data['id'];
    }

    for (let column of columnOrder) {
        const td = document.createElement('td');
        td.textContent = data[column];
        newTr.appendChild(td);
    }

    const lastCol = document.createElement('td');
    lastCol.style = "text-align:right;";
    if (updateCallback){
        lastCol.appendChild(editIcon(updateCallback, updateFormModalSelector));
    }

    if (deleteCallback){
        lastCol.appendChild(deleteIcon(deleteCallback));
    }

    if (lastCol.childElementCount > 0){
        newTr.appendChild(lastCol);
    }

    return newTr;
}

function deleteIcon(deleteCallback){
    const attribute = document.createElement("a");
    attribute.style = "margin-right: 20px;";
    const span = document.createElement("span");
    span.classList.add("material-icons");
    span.addEventListener("click", (event) => {
        deleteCallback(event);
    })
    span.addEventListener("mouseover", func, false);
    span.addEventListener("mouseout", func1, false);

    function func()
    {  
    span.setAttribute("style", "color:red;")
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

function editIcon(updateCallback, updateFormModalSelector){
    const attribute = document.createElement("a");
    attribute.style = "margin-right: 20px;";
    const span = document.createElement("span");
    span.classList.add("material-icons");
    span.setAttribute("data-toggle", "modal");
    span.setAttribute("data-target", `${updateFormModalSelector}`);
    span.addEventListener("click", (event) => {
        updateCallback(event);
    })
    span.addEventListener("mouseover", func, false);
    span.addEventListener("mouseout", func1, false);

    function func()
    {  
    span.setAttribute("style", "color:#f6b26b;")
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