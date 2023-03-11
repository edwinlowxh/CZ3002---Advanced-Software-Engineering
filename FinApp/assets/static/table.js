export function newTableRow(tableId, data, deleteCallback, updateCallback, updateFormModal){
    const table = document.querySelector(`${tableId}`);
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
    if (updateCallback){
        lastCol.appendChild(editIcon(updateCallback, updateFormModal));
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
    span.textContent = "delete";
    attribute.appendChild(
        span
    )

    return attribute;
}

function editIcon(updateCallback, updateFormModal){
    const attribute = document.createElement("a");
    attribute.style = "margin-right: 20px;";
    const span = document.createElement("span");
    span.classList.add("material-icons");
    span.setAttribute("data-toggle", "modal");
    span.setAttribute("data-target", `${updateFormModal}`);
    span.addEventListener("click", (event) => {
        updateCallback(event);
    })
    span.textContent = "edit";
    attribute.appendChild(
        span
    )

    return attribute;
}