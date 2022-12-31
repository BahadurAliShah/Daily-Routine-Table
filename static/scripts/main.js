function displayModal(id) {
    var sesctions = [];
    fetch('/api/dailies', {method: 'GET'})
        .then(response => response.json())
        .then(res => {
            sesctions = res['sections'];
            console.log(sesctions);
            const formSection = document.getElementById('FormSection');
            formSection.innerHTML = '';

            sesctions.forEach((section, sectionIndex) => {
                const option = document.createElement('option');
                option.setAttribute('value', section.type);
                option.innerHTML = section.type;
                formSection.appendChild(option);
            });
            document.getElementById(id).style.display='block';
        });
}

function toggleCheckbox(day, index, id, value) {
    const settings = {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            taskId: id,
            day: day,
            index: index,
            isChecked: value == '0'
        })
    };
    fetch('/api/dailies', settings)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            getDailies();
        });
}

function createCheckBox(day, array, id) {
    return array.map((value, index) => {
        return [array.length > 1 ? `<span>&nbsp;|&nbsp;</span>` : ``, `<a class="" onclick="toggleCheckbox(day='${day}', index=${index}, id=${id}, value='${value}')"><i class="bi ${value == '1' ? 'bi-check2-square' : 'bi-app'}"></i></a>`, array.length > 1 && index == array.length - 1 ? `<span>&nbsp;|</span>` : ``].join('')
    }).join('');
}

function getDailies() {
    fetch('/api/dailies', {method: 'GET'})
        .then(response => response.json())
        .then(res => {
            console.log(res);
            SetDailies(res);
        })
}

function SetDailies(res) {
    const tableBody = document.getElementById('dailiesBody');
    tableBody.innerHTML = '';
    res['sections'].forEach((section, sectionIndex) => {
        if (section.type != 'default'){
            const sectionRow = document.createElement('tr');
            const sectionTitle = document.createElement('td');
            sectionTitle.setAttribute('colspan', 9);
            sectionTitle.style.textAlign = 'center';
            sectionTitle.style.fontWeight = 'bold';
            sectionRow.style.backgroundColor = '#f9bb03';
            sectionRow.classList.add('table-border');
            sectionTitle.innerHTML = section.type;
            sectionRow.appendChild(sectionTitle);
            tableBody.appendChild(sectionRow);
        }
        const tableData = res['todos'].filter(todo => todo.type == section.type);
        const notes = res['notes'].filter(note => note.id == section.notesID);
        tableData.forEach((row, rowIndex) => {
        const tableRow = document.createElement('tr');
        tableRow.setAttribute('data-task-id', row.id);
        tableRow.innerHTML = `
                <td class="table-border titleColumn">${row.title}</td>
                <td class="table-border mondayColumn">
                ${createCheckBox(day = 'monday', array = row.monday, id = row.id)}
                </td>
                <td class="table-border tuesdayColumn">
                ${createCheckBox(day = 'tuesday', array = row.tuesday, id = row.id)}
                </td>
                <td class="table-border wednesdayColumn">
                ${createCheckBox(day = 'wednesday', array = row.wednesday, id = row.id)}
                </td>
                <td class="table-border thursdayColumn">
                ${createCheckBox(day = 'thursday', array = row.thursday, id = row.id)}
                </td>
                <td class="table-border fridayColumn">
                ${createCheckBox(day = 'friday', array = row.friday, id = row.id)}
                </td>
                <td class="table-border saturdayColumn">
                ${createCheckBox(day = 'saturday', array = row.saturday, id = row.id)}
                </td>
                <td class="table-border sundayColumn">
                ${createCheckBox(day = 'sunday', array = row.sunday, id = row.id)}
                </td>

                <td class="table-border btn-danger" onclick="deleteTask(${row.id})">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3-fill" viewBox="0 0 16 16">
                          <path d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5Zm-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5ZM4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06Zm6.53-.528a.5.5 0 0 0-.528.47l-.5 8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528ZM8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5Z"></path>
                      </svg>
                </td>
            `;
        tableBody.appendChild(tableRow);
    });
        const NotesRow = document.createElement('tr');
        NotesRow.setAttribute('data-task-type', notes[0].type);
        NotesRow.innerHTML = `
                  <td class="table-border titleColumn">Notes</td>
                  <td class="table-border mondayColumn"><textarea type="text" class="form-control" style="padding: 0px">${notes[0].monday}</textarea></td>
                    <td class="table-border tuesdayColumn"><textarea type="text" class="form-control" style="padding: 0px">${notes[0].tuesday}</textarea></td>
                    <td class="table-border wednesdayColumn"><textarea type="text" class="form-control" style="padding: 0px">${notes[0].wednesday}</textarea></td>
                    <td class="table-border thursdayColumn"><textarea type="text" class="form-control" style="padding: 0px">${notes[0].thursday}</textarea></td>
                    <td class="table-border fridayColumn"><textarea type="text" class="form-control" style="padding: 0px">${notes[0].friday}</textarea></td>
                    <td class="table-border saturdayColumn"><textarea type="text" class="form-control" style="padding: 0px">${notes[0].saturday}</textarea></td>
                    <td class="table-border sundayColumn"><textarea type="text" class="form-control" style="padding: 0px">${notes[0].sunday}</textarea></td>
                  <td class="table-border btn-primary" onclick="updateNotes(type='${section.type}', rowID='${notes[0].id}')"><i class="bi bi-cloud-arrow-up-fill"></i></td>
                `;
        tableBody.appendChild(NotesRow);
    });
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', toggleCheckbox);
    });
}

function deleteTask(id) {
    const settings = {
        method: 'DELETE',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            taskId: id
        })
    };
    console.log(settings);
    fetch('/api/dailies', settings)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            getDailies();
        });
}

function AddTask() {
    document.getElementById('DailiesForm').style.display = 'none';

    const title = document.getElementById('FormTitle').value;
    document.getElementById('FormTitle').value = '';
    const section = document.getElementById('FormSection').value;
    const monday = document.getElementById('FormMonday').value;
    const tuesday = document.getElementById('FormTuesday').value;
    const wednesday = document.getElementById('FormWednesday').value;
    const thursday = document.getElementById('FormThursday').value;
    const friday = document.getElementById('FormFriday').value;
    const saturday = document.getElementById('FormSaturday').value;
    const sunday = document.getElementById('FormSunday').value;

    const settings = {
        method: 'PUT',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            title: title,
            section: section,
            monday: monday,
            tuesday: tuesday,
            wednesday: wednesday,
            thursday: thursday,
            friday: friday,
            saturday: saturday,
            sunday: sunday
        })
    };

    fetch('/api/dailies', settings)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            getDailies();
        });
}

function addNewSection() {
    const section = document.getElementById('SectionName').value;
    document.getElementById('SectionName').value = '';
    const settings = {
        method: 'PUT',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            section: section
        })
    };

    fetch('/api/sections', settings).then(
        response => response.json()
    ).then(data => {
        console.log(data);
        getDailies();
    });
}

function RemoveSection(){
    const section = document.getElementById('SectionName').value;
    document.getElementById('SectionName').value = '';
    const settings = {
        method: 'DELETE',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            section: section
        })
    };

    fetch('/api/sections', settings).then(
        response => response.json()
    ).then(data => {
        console.log(data);
        getDailies();
    });
}

function updateNotes(type, rowID) {
    const row = document.querySelector(`tr[data-task-type="${type}"]`);
    const monday = row.querySelector('.mondayColumn textarea').value
    const tuesday = row.querySelector('.tuesdayColumn textarea').value
    const wednesday = row.querySelector('.wednesdayColumn textarea').value
    const thursday = row.querySelector('.thursdayColumn textarea').value
    const friday = row.querySelector('.fridayColumn textarea').value
    const saturday = row.querySelector('.saturdayColumn textarea').value
    const sunday = row.querySelector('.sundayColumn textarea').value

    const settings = {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            type: type,
            id: rowID,
            monday: monday,
            tuesday: tuesday,
            wednesday: wednesday,
            thursday: thursday,
            friday: friday,
            saturday: saturday,
            sunday: sunday
        })
    };
    fetch('/api/notes', settings).then(
        response => response.json()
    ).then(data => {
        console.log(data);
        getDailies();
    });
}


getDailies();
