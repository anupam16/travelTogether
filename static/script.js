document.getElementById('travellerForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = {
        full_name: formData.get('full_name'),
        phone_number: formData.get('phone_number'),
        place_from: formData.get('place_from'),
        place_to: formData.get('place_to'),
        date: formData.get('date')
    };

    fetch('http://127.0.0.1:5000/travellers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 200) {
            populateTable(result.details);
            openPopup();
        } else {
            alert(result.details);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

  
});

function populateTable(details) {
    const tbody = document.querySelector('#resultsTable tbody');
    tbody.innerHTML = '';

    if (!details) {
        const row = document.createElement('tr');
        const cell = document.createElement('td');
        cell.colSpan = 5;
        cell.textContent = 'No matching travellers found.';
        row.appendChild(cell);
        tbody.appendChild(row);
    } else {
        details.forEach(traveller => {
            const row = document.createElement('tr');
            Object.values(traveller).forEach(text => {
                const cell = document.createElement('td');
                cell.textContent = text;
                row.appendChild(cell);
            });
            tbody.appendChild(row);
        });

      
    }
}

function openPopup() {
    document.getElementById('popup').style.display = 'block';
}

function closePopup() {
    document.getElementById('popup').style.display = 'none';
}
