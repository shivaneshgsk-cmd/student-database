
const API_URL = "/api/students";

const form = document.getElementById("studentForm");
const table = document.getElementById("studentTable");
const message = document.getElementById("message");

// DISPLAY MESSAGE
function showMessage(text) {
    message.textContent = text;
}

// FETCH AND DISPLAY STUDENTS
async function loadStudents() {

    try {
        const response = await fetch(API_URL);
        const students = await response.json();

        if (!response.ok) {
            throw new Error("Unable to load students");
        }

        table.innerHTML = "";

        students.forEach(student => {

            const row = document.createElement("tr");

            const values = [
                student.id,
                student.name,
                student.email,
                student.course
            ];

            values.forEach(value => {
                const cell = document.createElement("td");
                cell.textContent = value;
                row.appendChild(cell);
            });

            const actions = document.createElement("td");

            const editBtn = document.createElement("button");
            editBtn.textContent = "Edit";
            editBtn.onclick = () => editStudent(student);

            const deleteBtn = document.createElement("button");
            deleteBtn.textContent = "Delete";
            deleteBtn.onclick = () => deleteStudent(student.id);

            actions.append(editBtn, deleteBtn);
            row.appendChild(actions);

            table.appendChild(row);
        });

    } catch (error) {
        showMessage(error.message);
    }
}

// ADD OR UPDATE STUDENT
form.addEventListener("submit", async function(event) {

    event.preventDefault();

    const id = document.getElementById("studentId").value;

    const student = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        course: document.getElementById("course").value
    };

    const url = id ? `${API_URL}/${id}` : API_URL;
    const method = id ? "PUT" : "POST";

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(student)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Request failed");
        }

        showMessage(result.message);
        resetForm();
        loadStudents();

    } catch (error) {
        showMessage(error.message);
    }
});

// EDIT STUDENT
function editStudent(student) {

    document.getElementById("studentId").value = student.id;
    document.getElementById("name").value = student.name;
    document.getElementById("email").value = student.email;
    document.getElementById("course").value = student.course;

    document.getElementById("submitBtn").textContent = "Update Student";
    document.getElementById("cancelBtn").hidden = false;
}

// DELETE STUDENT
async function deleteStudent(id) {

    if (!confirm("Are you sure you want to delete this student?")) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: "DELETE"
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Delete failed");
        }

        showMessage(result.message);
        loadStudents();

    } catch (error) {
        showMessage(error.message);
    }
}

// RESET FORM
function resetForm() {

    form.reset();

    document.getElementById("studentId").value = "";
    document.getElementById("submitBtn").textContent = "Add Student";
    document.getElementById("cancelBtn").hidden = true;
}

// LOAD RECORDS WHEN PAGE OPENS
loadStudents();