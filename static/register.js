function showPassword() {
    //function added to register.html
    //shows the element inputPassword in from

    //get the document by its
    passwordInput = document.getElementById("registerInputPassword1")
    // if its password change it to text
    if (passwordInput.type == "password") {
        passwordInput.type = "text";
    }
    // else change it to password
    else if (passwordInput.type == "text") {
        passwordInput = "password";
    }
}

function validateForm() {
    //check whether the form is valid
    //check all fields are filled

    let allAreFilled = true;

    document.getElementById("registerForm").querySelectorAll("[required]").forEach(function(i) {
        if (!allAreFilled) return;
            if (!i.value) allAreFilled = false;
            if (i.type === "radio") {
            let radioValueCheck = false;
            document.getElementById("myForm").querySelectorAll(`[name=${i.name}]`).forEach(function(r) {
                if (r.checked) radioValueCheck = true;
            })
            allAreFilled = radioValueCheck;
            }
        })
        if (!allAreFilled) {
            //send out alert if fields are empty
            alert('Fill all the fields');
        }

    //check whether passwords match
    if (document.getElementById("registerInputPassword1").value !=
    document.getElementById("reconfirmPassword").value) {
        //send out alert if passwords dont match
    alert("passwords do not match")
        return false
    }
    return true
}
