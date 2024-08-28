document.getElementById('csv-file').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const reader = new FileReader();
    
    reader.onload = function(e) {
        const text = e.target.result;
        const rows = text.split('\n').map(row => row.split(',').map(cell => cell.trim().replace(/"/g, '')));
        const tableHeader = document.getElementById('table-header');
        const tableBody = document.getElementById('table-body');
        
        tableHeader.innerHTML = '';
        tableBody.innerHTML = '';
        
        // Create table header
        if (rows.length > 0) {
            const headerRow = rows[0];
            headerRow.forEach(header => {
                const th = document.createElement('th');
                th.textContent = header;
                tableHeader.appendChild(th);
            });
        }
        
        // Create table body
        for (let i = 1; i < rows.length; i++) {
            const tr = document.createElement('tr');
            rows[i].forEach(cell => {
                const td = document.createElement('td');
                td.textContent = cell;
                tr.appendChild(td);
            });
            tableBody.appendChild(tr);
        }
    };
    
    reader.readAsText(file);
});

document.getElementById('meeting-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const meetingTime = document.getElementById('meeting-time').value;
    const meetingReason = document.getElementById('meeting-reason').value;

    // Display alert with entered data for demonstration
    alert(`Meeting Scheduled!\nTime: ${meetingTime}\nReason: ${meetingReason}`);
});
