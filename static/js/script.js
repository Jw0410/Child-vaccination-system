function validateForm() {
    var username = document.getElementById("username").value.trim();
    var password = document.getElementById("password").value.trim();

    // Add your conditions to check for wrong values
    if (username === "") {
        alert("Please enter a valid username.");
        return false; // Prevent form submission
    }

    if (password === "") {
        alert("Please enter a valid password.");
        return false; // Prevent form submission
    }

    return true; // Allow form submission
}