window.deleteCategory = deleteCategory

export async function deleteCategory(event){
    const category_id = event.target.closest('tr').id;
    const formData = new FormData();
    formData.append('category_id', category_id);
    await fetch("http://127.0.0.1:8000/budget/delete_category",
    {
        "method": "POST",
        "body": formData,
        "Content-Type": "application/x-www-form-urlencoded"
    })
    .then(response => {
        if (!response.ok ){
            throw response.json();
        }
        return response.json();
    })
    .then(() => {
        event.target.closest('tr').remove();
    })
    .catch(error => {
        console.error(error);
        error.then(data => {
            alert(data);
        });
    }  
    )    
}