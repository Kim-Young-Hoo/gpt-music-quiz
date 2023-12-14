function login() {
    var username = document.getElementById('login-username').value;
    var password = document.getElementById('login-password').value;

    // Add your login logic here (communicate with your backend)
    console.log('Login:', username, password);
}

function signup() {
    var username = document.getElementById('signup-username').value;
    var password = document.getElementById('signup-password').value;

    // Add your signup logic here (communicate with your backend)
    console.log('Sign Up:', username, password);
}

// Toggle between login and signup forms
document.getElementById('signup-heading').addEventListener('click', function () {
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('signup-form').style.display = 'block';
});
