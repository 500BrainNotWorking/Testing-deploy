document.addEventListener("DOMContentLoaded", function () {
    var el = document.querySelector('.more');
    var btn = el.querySelector('.more-btn');
    var menu = el.querySelector('.more-menu');
    var visible = false;

    //  Function to Show Menu
    function showMenu(e) {
        e.preventDefault();
        if (!visible) {
            visible = true;
            el.classList.add('show-more-menu');
            menu.setAttribute('aria-hidden', false);
            document.addEventListener('mousedown', hideMenu, false);
        }
    }

    //  Function to Hide Menu When Clicking Outside
    function hideMenu(e) {
        if (btn.contains(e.target) || menu.contains(e.target)) {
            return; // Don't close if clicking inside the menu
        }
        if (visible) {
            visible = false;
            el.classList.remove('show-more-menu');
            menu.setAttribute('aria-hidden', true);
            document.removeEventListener('mousedown', hideMenu);
        }
    }

    // Ensure Click Works for Profile Link
    document.querySelector(".more-menu a").addEventListener("click", function () {
        console.log("Profile link clicked! Navigating...");
        document.querySelector('.more-menu').classList.remove('show-more-menu');
        window.location.href = "/staff-profile";
    });

    btn.addEventListener('click', showMenu, false);

    //  Function to Open Sidebar Menu
    function openNav() {
        document.getElementById("mySidenav").style.width = "250px";
        document.getElementById("main-content").style.marginLeft = "250px";
    }

    //  Function to Close Sidebar Menu
    function closeNav() {
        document.getElementById("mySidenav").style.width = "0";
        document.getElementById("main-content").style.marginLeft = "0";
    }

    // Function to Filter Reviews in Search Bar
    function filterReviews() {
        let input, filter, reviews, studentName, i, txtValue;
        input = document.getElementById("myInput");
        filter = input.value.toUpperCase();
        reviews = document.getElementById("reviewsList").getElementsByClassName("review-card");

        for (i = 0; i < reviews.length; i++) {
            studentName = reviews[i].querySelector("h4");
            
            if (studentName) {
                txtValue = studentName.textContent || studentName.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    reviews[i].style.display = "";
                } else {
                    reviews[i].style.display = "none";
                }
            }
        }
    }

    //  Function to Search for Students
    function searchStudents() {
        const query = document.getElementById("searchQuery").value;

        fetch(`/searchStudent?query=${query}`)
        .then(response => response.json())
        .then(data => {
            const studentList = document.getElementById("student-list");
            const noStudentsMsg = document.getElementById("no-students");

            studentList.innerHTML = ""; // Clear existing students

            if (data.students.length > 0) {
                noStudentsMsg.style.display = "none";

                data.students.forEach(student => {
                    const card = document.createElement("div");
                    card.classList.add("student-card");
                    card.innerHTML = `
                        <h3>${student.firstname} ${student.lastname}</h3>
                        <p><strong>Student ID:</strong> ${student.UniId}</p>
                        <p><strong>Degree:</strong> ${student.degree ? student.degree : "Not assigned"}</p>
                        <a href="/getStudentProfile/${student.UniId}">
                            <button class="profile-button">View Profile</button>
                        </a>
                    `;
                    studentList.appendChild(card);
                });
            } else {
                noStudentsMsg.style.display = "block";
            }
        })
        .catch(error => console.error("Error fetching students:", error));
    }

    //  Attach Filter Function to Input Field
    document.getElementById("myInput").addEventListener("keyup", filterReviews);
});

//for navbar
function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("main-content").style.marginLeft = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main-content").style.marginLeft = "0";
}

function searchStudents() {
    const query = document.getElementById("searchQuery").value;

    fetch(`/searchStudent?query=${query}`)
    .then(response => response.json())
    .then(data => {
        const studentList = document.getElementById("student-list");
        const noStudentsMsg = document.getElementById("no-students");

        studentList.innerHTML = ""; // Clear existing students

        if (data.students.length > 0) {
            noStudentsMsg.style.display = "none";

            data.students.forEach(student => {
                const card = document.createElement("div");
                card.classList.add("student-card");
                card.innerHTML = `
                    <h3>${student.firstname} ${student.lastname}</h3>
                    <p><strong>Student ID:</strong> ${student.UniId}</p>
                    <p><strong>Degree:</strong> ${student.degree ? student.degree : "Not assigned"}</p>
                    <a href="/getStudentProfile/${student.UniId}">
                        <button class="profile-button">View Profile</button>
                    </a>
                `;
                studentList.appendChild(card);
            });
        } else {
            noStudentsMsg.style.display = "block";
        }
    })
    .catch(error => console.error("Error fetching students:", error));
}