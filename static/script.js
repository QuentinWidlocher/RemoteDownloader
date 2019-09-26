var inputField = document.querySelector('input#input-url');
var tableField = document.querySelector('tbody#table');
var baseRow = document.querySelector('tr#base-row');

function addURL() {
    let inputValue = inputField.value;

    console.log(inputValue);
    

    fetch('/add-url', { method: 'POST', body: JSON.stringify({ url: inputValue }) }).then((result) => {        
        if (result.status === 200) {
            console.log(baseRow);
            
            let newRow = baseRow.cloneNode(true);
            newRow.removeAttribute('hidden');

            newRow.querySelector('td.url').innerHTML = inputValue;

            tableField.append(newRow);

            inputField.value = '';
        }
    });
}