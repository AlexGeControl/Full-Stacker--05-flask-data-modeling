const descInput = document.getElementById('description');

document.getElementById('form').onsubmit = function(e) {
    e.preventDefault();
    // get description:
    const desc = descInput.value;
    descInput.value = '';

    fetch(
        '/todos/create', 
        {
            headers: {
                'Content-Type': 'application/json',
            },
            method: 'POST',
            body: JSON.stringify(
                {
                    'description': desc,
                }
            )
        }
    )
    .then(response => response.json())
    .then(
        jsonResponse => {
            console.log('response', jsonResponse);
            
            document.getElementById('error').className = 'hidden';

            location.reload()
        }
    )
    .catch(
        function() {
            document.getElementById('error').className = '';
        }
    )
}

function updateTodo(element) {
    // parse todo status:
    const id = element.getAttribute('data-id');

    // toggle
    const completed = element.checked;

    fetch(
        `/todos/${id}/edit`, 
        {
            headers: {
                'Content-Type': 'application/json',
            },
            method: 'PUT',
            body: JSON.stringify(
                {
                    'completed': completed,
                }
            )
        }
    )
    .then(response => response.json())
    .then(
        jsonResponse => {
            console.log('response', jsonResponse);

            document.getElementById('error').className = 'hidden';
        }
    )
    .catch(
        function() {
            document.getElementById('error').className = '';
        }
    )
}

function deleteTodo(element) {
    // parse todo status:
    const id = element.getAttribute('data-id');

    fetch(
        `/todos/${id}`, 
        {
            method: 'DELETE'
        }
    )
    .then(
        jsonResponse => {
            console.log('response', jsonResponse);

            // remove from list:
            document.getElementById('error').className = 'hidden';

            location.reload()
        }
    )
    .catch(
        function() {
            document.getElementById('error').className = '';
        }
    )
}