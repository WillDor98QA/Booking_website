// Mobile menu functionality
const menuButton = document.getElementById('menuButton');
const mobileMenu = document.getElementById('mobileMenu');

menuButton.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        target.scrollIntoView({
            behavior: 'smooth'
        });
        // Close mobile menu if open
        mobileMenu.classList.add('hidden');
    });
});

// Form handling
const bookingForm = document.getElementById('bookingForm');
const toast = document.getElementById('toast');

bookingForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Show loading state
    const submitButton = bookingForm.querySelector('button[type="submit"]');
    const buttonText = submitButton.querySelector('span');
    const spinner = submitButton.querySelector('.spinner');
    
    buttonText.classList.add('hidden');
    spinner.classList.remove('hidden');
    submitButton.disabled = true;

    // Collect form data
    const formData = new FormData(bookingForm);
    const bookingData = Object.fromEntries(formData.entries());

    try {
        // Simulate API call with timeout
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Show success message
        showToast('Booking submitted successfully! We will contact you shortly.', 'success');
        bookingForm.reset();
    } catch (error) {
        showToast('There was an error submitting your booking. Please try again.', 'error');
    } finally {
        // Reset button state
        buttonText.classList.remove('hidden');
        spinner.classList.add('hidden');
        submitButton.disabled = false;
    }
});

// Toast notification function
function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast ${type === 'success' ? 'bg-purple-900' : 'bg-red-600'}`;
    
    // Show toast
    setTimeout(() => toast.classList.add('show'), 100);
    
    // Hide toast after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Date input validation
const dateInput = bookingForm.querySelector('input[name="date"]');
dateInput.min = new Date().toISOString().split('T')[0];

// Time input validation
const timeInput = bookingForm.querySelector('input[name="time"]');
timeInput.addEventListener('change', (e) => {
    const time = e.target.value;
    const [hours, minutes] = time.split(':').map(Number);
    
    // Validate business hours (9 AM - 7 PM)
    if (hours < 9 || hours >= 19) {
        showToast('Please select a time between 9:00 AM and 7:00 PM', 'error');
        e.target.value = '';
    }
});