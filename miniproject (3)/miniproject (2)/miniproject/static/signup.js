// Select the form and the input fields
const form = document.getElementById('signup-form');
const firstNameInput = document.querySelector('input[name="first-name"]');
const lastNameInput = document.querySelector('input[name="last-name"]');
const emailInput = document.querySelector('input[name="email"]');
const phoneInput = document.querySelector('input[name="phone"]');
const passwordInput = document.querySelector('input[name="password"]');
const confirmPasswordInput = document.querySelector('input[name="confirm-password"]');

// Add event listener to form submission
form.addEventListener('submit', function(event) {
    // Prevent default form submission
    event.preventDefault();

    // Clear previous errors
    clearErrors();

    // Validate the form
    let isValid = true;

    // Check if any of the fields are empty
    if (!firstNameInput.value.trim() || !lastNameInput.value.trim() || !emailInput.value.trim() || !phoneInput.value.trim() || !passwordInput.value.trim() || !confirmPasswordInput.value.trim()) {
        showError('All fields are required.');
        isValid = false;
    }

    // Validate the email
    if (!validateEmail(emailInput.value)) {
        showError('Please enter a valid email address.');
        isValid = false;
    }

    // Validate the phone number (basic check for numeric characters)
    if (!/^\d+$/.test(phoneInput.value)) {
        showError('Please enter a valid phone number.');
        isValid = false;
    }

    // Check if passwords match
    if (passwordInput.value !== confirmPasswordInput.value) {
        showError('Passwords do not match.');
        isValid = false;
    }

    // If all validations pass, submit the form
    if (isValid) {
        // Here you would typically send the form data to a server
        // For demonstration purposes, we'll just log the values
        console.log('Form submitted successfully!');
        console.log({
            firstName: firstNameInput.value,
            lastName: lastNameInput.value,
            email: emailInput.value,
            phone: phoneInput.value,
            password: passwordInput.value
        });

        // You can add code here to send the data to your server if needed
        // e.g., fetch('/signup', { method: 'POST', body: formData });
    }
});

// Function to validate email address
function validateEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}

// Function to show error messages
function showError(message) {
    const errorMessages = document.getElementById('error-messages');
    errorMessages.innerText = message; // Display the message
}

// Function to clear previous error messages
function clearErrors() {
    const errorMessages = document.getElementById('error-messages');
    errorMessages.innerText = ''; // Clear previous messages
}
