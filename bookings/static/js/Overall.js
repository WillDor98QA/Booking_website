// auth.js
function checkAuth() {
    if (!localStorage.getItem('adminLoggedIn')) {
        window.location.href = 'login.html';
    }
}

document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.removeItem('adminLoggedIn');
    window.location.href = 'login.html';
});

function validatePassword(password) {
    // At least 8 characters, 1 uppercase, 1 lowercase, 1 number
    const hasMinLength = password.length >= 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumber = /\d/.test(password);
    
    if (hasMinLength && hasUpperCase && hasLowerCase && hasNumber) {
        return 'strong';
    } else if (hasMinLength && (hasUpperCase || hasLowerCase) && hasNumber) {
        return 'medium';
    } else {
        return 'weak';
    }
}

function updatePasswordStrength(password) {
    const strengthBar = document.querySelector('.password-strength-bar');
    const strength = validatePassword(password);
    
    strengthBar.classList.remove('strength-weak', 'strength-medium', 'strength-strong');
    if (password.length > 0) {
        strengthBar.classList.add(`strength-${strength}`);
    } else {
        strengthBar.style.width = '0';
    }
}

// Add these elements to the change password form in your HTML
const passwordForm = document.getElementById('changePasswordForm');
const newPasswordInput = document.getElementById('newPassword');
const errorMessage = document.createElement('div');
errorMessage.className = 'error-message';
const successMessage = document.createElement('div');
successMessage.className = 'success-message';
const strengthIndicator = document.createElement('div');
strengthIndicator.className = 'password-strength';
strengthIndicator.innerHTML = '<div class="password-strength-bar"></div>';

// Insert messages and strength indicator after the new password input
newPasswordInput.parentNode.appendChild(strengthIndicator);
newPasswordInput.parentNode.appendChild(errorMessage);
passwordForm.appendChild(successMessage);

newPasswordInput.addEventListener('input', (e) => {
    updatePasswordStrength(e.target.value);
});

passwordForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    errorMessage.classList.remove('show');
    successMessage.classList.remove('show');
    
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = newPasswordInput.value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (newPassword !== confirmPassword) {
        errorMessage.textContent = 'Passwords do not match';
        errorMessage.classList.add('show');
        return;
    }

    if (validatePassword(newPassword) === 'weak') {
        errorMessage.textContent = 'Password must be at least 8 characters with uppercase, lowercase, and numbers';
        errorMessage.classList.add('show');
        return;
    }

    try {
        // Replace with your actual API endpoint
        const response = await fetch('your-api-endpoint/change-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                currentPassword,
                newPassword
            })
        });

        if (response.ok) {
            successMessage.textContent = 'Password updated successfully!';
            successMessage.classList.add('show');
            setTimeout(() => {
                document.getElementById('passwordModal').style.display = 'none';
                passwordForm.reset();
            }, 2000);
        } else {
            errorMessage.textContent = 'Current password is incorrect';
            errorMessage.classList.add('show');
        }
    } catch (error) {
        errorMessage.textContent = 'An error occurred. Please try again.';
        errorMessage.classList.add('show');
    }
});

// Immediately check auth when script loads
checkAuth();

// Change password functionality
const passwordModal = document.getElementById('passwordModal');
const changePasswordBtn = document.getElementById('changePasswordBtn');
const closeBtn = document.querySelector('.close');

changePasswordBtn.addEventListener('click', () => {
    passwordModal.style.display = 'block';
});

closeBtn.addEventListener('click', () => {
    passwordModal.style.display = 'none';
});

document.getElementById('changePasswordForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (newPassword !== confirmPassword) {
        alert('New passwords do not match!');
        return;
    }

    // Add your password change logic here
    alert('Password updated successfully!');
    passwordModal.style.display = 'none';
});

// dashboard.js
async function fetchBookingCounts() {
    try {
        // Replace with your actual API endpoint
        const response = await fetch('your-api-endpoint/booking-counts');
        const data = await response.json();

        document.getElementById('pendingCount').textContent = data.pending || 0;
        document.getElementById('confirmedCount').textContent = data.confirmed || 0;
        document.getElementById('cancelledCount').textContent = data.cancelled || 0;
        document.getElementById('completedCount').textContent = data.completed || 0;
    } catch (error) {
        console.error('Error fetching booking counts:', error);
    }
}

// Call when page loads
fetchBookingCounts();

// bookings.js
async function fetchBookings(status) {
    try {
        // Replace with your actual API endpoint
        const response = await fetch(`your-api-endpoint/bookings?status=${status}`);
        const bookings = await response.json();
        return bookings;
    } catch (error) {
        console.error('Error fetching bookings:', error);
        return [];
    }
}

async function updateBookingStatus(bookingId, newStatus) {
    try {
        // Replace with your actual API endpoint
        const response = await fetch(`your-api-endpoint/bookings/${bookingId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status: newStatus }),
        });
        
        if (response.ok) {
            // Refresh the page to show updated data
            window.location.reload();
        } else {
            throw new Error('Failed to update booking');
        }
    } catch (error) {
        console.error('Error updating booking:', error);
        alert('Failed to update booking status');
    }
}

function renderBookingsTable(bookings, tableId, status) {
    const table = document.getElementById(tableId);
    const tbody = table.querySelector('tbody');
    tbody.innerHTML = '';

    bookings.forEach(booking => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${booking.firstName} ${booking.lastName}</td>
            <td>${booking.email}</td>
            <td>${booking.phone}</td>
            <td>${booking.service}</td>
            <td>${booking.size}</td>
            <td>${new Date(booking.preferredDate).toLocaleDateString()}</td>
            <td>${booking.preferredTime}</td>
            <td>${new Date(booking.createdAt).toLocaleDateString()}</td>
            ${status === 'pending' || status === 'confirmed' ? `
                <td class="action-buttons">
                    ${status === 'pending' ? `
                        <button class="confirm-btn" onclick="updateBookingStatus('${booking.id}', 'confirmed')">Confirm</button>
                    ` : ''}
                    ${status === 'confirmed' ? `
                        <button class="complete-btn" onclick="updateBookingStatus('${booking.id}', 'completed')">Complete</button>
                    ` : ''}
                    <button class="cancel-btn" onclick="updateBookingStatus('${booking.id}', 'cancelled')">Cancel</button>
                </td>
            ` : ''}
        `;
        tbody.appendChild(tr);
    });
}

// Add these functions to your Overall.js file

// Function to export table data to CSV
function exportToCSV() {
    const table = document.getElementById('bookingsTable');
    const rows = table.getElementsByTagName('tr');
    let csv = [];
    
    // Get headers
    const headers = [];
    const headerCells = rows[0].getElementsByTagName('th');
    for (let i = 0; i < headerCells.length - 1; i++) { // Exclude Action column
        headers.push(headerCells[i].textContent);
    }
    csv.push(headers.join(','));
    
    // Get data rows
    for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const cells = row.getElementsByTagName('td');
        const rowData = [];
        for (let j = 0; j < cells.length - 1; j++) { // Exclude Action column
            let cellData = cells[j].textContent.replace(/,/g, ';'); // Replace commas with semicolons
            rowData.push(cellData);
        }
        csv.push(rowData.join(','));
    }
    
    // Download CSV file
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', 'pending_bookings.csv');
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Function to export table data to Excel
function exportToExcel() {
    const table = document.getElementById('bookingsTable');
    const rows = table.getElementsByTagName('tr');
    const data = [];
    
    // Get headers
    const headers = [];
    const headerCells = rows[0].getElementsByTagName('th');
    for (let i = 0; i < headerCells.length - 1; i++) { // Exclude Action column
        headers.push(headerCells[i].textContent);
    }
    data.push(headers);
    
    // Get data rows
    for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const cells = row.getElementsByTagName('td');
        const rowData = [];
        for (let j = 0; j < cells.length - 1; j++) { // Exclude Action column
            rowData.push(cells[j].textContent);
        }
        data.push(rowData);
    }
    
    // Create workbook and worksheet
    const ws = XLSX.utils.aoa_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Pending Bookings");
    
    // Generate Excel file
    XLSX.writeFile(wb, "pending_bookings.xlsx");
}

// Add event listeners for export buttons
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('exportCSV').addEventListener('click', exportToCSV);
    document.getElementById('exportExcel').addEventListener('click', exportToExcel);
});

document.addEventListener('DOMContentLoaded', () => {
    const customAlert = document.getElementById('customAlert');
    const alertMessage = document.getElementById('alertMessage');
    const alertOkBtn = document.getElementById('alertOkBtn');
    const alertCancelBtn = document.getElementById('alertCancelBtn');

    // Function to show the custom alert
    function showAlert(message, isConfirmation = false) {
        alertMessage.textContent = message;
        alertCancelBtn.style.display = isConfirmation ? 'block' : 'none';
        customAlert.classList.remove('hidden');
    }

    // Function to hide the custom alert
    function hideAlert() {
        customAlert.classList.add('hidden');
    }

    // Handle "Confirm" button clicks
    document.querySelectorAll('.confirm-btn').forEach(button => {
        button.addEventListener('click', (event) => {
            const row = event.target.closest('tr'); // Get the closest table row
            showAlert(`Booking confirmed for ${row.cells[0].textContent}`);
            alertOkBtn.onclick = hideAlert; // Close the alert when OK is clicked
        });
    });

    // Handle "Cancel" button clicks
    document.querySelectorAll('.cancel-btn').forEach(button => {
        button.addEventListener('click', (event) => {
            const row = event.target.closest('tr'); // Get the closest table row
            showAlert(`Are you sure you want to cancel the booking for ${row.cells[0].textContent}?`, true);

            // Set up buttons for confirmation
            alertOkBtn.onclick = () => {
                row.remove(); // Remove the row from the table
                hideAlert(); // Hide the alert
                showAlert('Booking canceled successfully.');
                alertOkBtn.onclick = hideAlert; // Reset OK button behavior
            };

            alertCancelBtn.onclick = hideAlert; // Close the alert when Cancel is clicked
        });
    });
});

//for status changes
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".status").forEach(statusElement => {
        let status = statusElement.getAttribute("data-status"); // Get status from data attribute
        statusElement.classList.add(status); // Add the class dynamically
        statusElement.textContent = status.charAt(0).toUpperCase() + status.slice(1); // Capitalize first letter
    });
});

//pagination 
document.addEventListener("DOMContentLoaded", function () {
    let currentPage = 1;
    let itemsPerPage = parseInt(document.getElementById("itemsPerPage").value);
    let totalItems = 50; // Default, update dynamically when fetching data
    let totalPages = Math.ceil(totalItems / itemsPerPage);

    const tableBody = document.querySelector("#dataTable tbody"); // Adjust selector based on your table

    const startIndexSpan = document.getElementById("startIndex");
    const endIndexSpan = document.getElementById("endIndex");
    const totalItemsSpan = document.getElementById("totalItems");
    const currentPageSpan = document.getElementById("currentPage");
    const totalPagesSpan = document.getElementById("totalPages");

    const firstPageBtn = document.getElementById("firstPage");
    const prevPageBtn = document.getElementById("prevPage");
    const nextPageBtn = document.getElementById("nextPage");
    const lastPageBtn = document.getElementById("lastPage");
    const itemsPerPageSelect = document.getElementById("itemsPerPage");

    // Sample dataset (Replace this with real data from API)
    const data = Array.from({ length: totalItems }, (_, i) => ({
        name: `User ${i + 1}`,
        email: `user${i + 1}@example.com`,
        phone: `+12345678${i + 1}`,
        service: "Cleaning",
        size: ["Small", "Medium", "Large"][i % 3],
        preferredDate: `2025-02-${String((i % 28) + 1).padStart(2, "0")}`,
        preferredTime: `${(i % 12) + 1}:00 ${i % 2 === 0 ? "AM" : "PM"}`,
        createdAt: "2025-02-01 09:30 AM",
    }));

    function updatePaginationUI() {
        totalPages = Math.ceil(data.length / itemsPerPage); // Recalculate pages
        totalItems = data.length; // Update total items count

        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = Math.min(currentPage * itemsPerPage, totalItems);

        startIndexSpan.textContent = startIndex + 1;
        endIndexSpan.textContent = endIndex;
        currentPageSpan.textContent = currentPage;
        totalPagesSpan.textContent = totalPages;
        totalItemsSpan.textContent = totalItems;

        firstPageBtn.disabled = currentPage === 1;
        prevPageBtn.disabled = currentPage === 1;
        nextPageBtn.disabled = currentPage === totalPages;
        lastPageBtn.disabled = currentPage === totalPages;

        renderTable(startIndex, endIndex);
    }

    function renderTable(start, end) {
        tableBody.innerHTML = ""; // Clear previous rows
        data.slice(start, end).forEach((item) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${item.name}</td>
                <td>${item.email}</td>
                <td>${item.phone}</td>
                <td>${item.service}</td>
                <td>${item.size}</td>
                <td>${item.preferredDate}</td>
                <td>${item.preferredTime}</td>
                <td>${item.createdAt}</td>
            `;
            tableBody.appendChild(row);
        });
    }

    firstPageBtn.addEventListener("click", function () {
        currentPage = 1;
        updatePaginationUI();
    });

    prevPageBtn.addEventListener("click", function () {
        if (currentPage > 1) {
            currentPage--;
            updatePaginationUI();
        }
    });

    nextPageBtn.addEventListener("click", function () {
        if (currentPage < totalPages) {
            currentPage++;
            updatePaginationUI();
        }
    });

    lastPageBtn.addEventListener("click", function () {
        currentPage = totalPages;
        updatePaginationUI();
    });

    itemsPerPageSelect.addEventListener("change", function () {
        itemsPerPage = parseInt(this.value);
        currentPage = 1; // Reset to first page when items per page changes
        updatePaginationUI();
    });

    updatePaginationUI();
});