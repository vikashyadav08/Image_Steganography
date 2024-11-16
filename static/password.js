const strength = { 
    1: "Very Weak", 
    2: "Weak", 
    3: "Medium", 
    4: "Strong", 
}; 
function checkStrength(pass) { 
    if (pass.length > 15) 
        return  " Password is too lengthy"
    else if (pass.length < 8) 
        return  " Password is too short"

    let regex = 
/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@.#$!%*?&])[A-Za-z\d@.#$!^%*?&]{8,15}$/; 
    if (regex.test(pass)) { 
        return  " Password is Strong"
    } 
    let count = 0; 
    let regex1 = /[a-z]/; 
    if (regex1.test(pass)) count++; 
    let regex2 = /[A-Z]/; 
    if (regex2.test(pass)) count++; 
    let regex3 = /[\d]/; 
    if (regex3.test(pass)) count++; 
    let regex4 = /[!@#$%^&*.?]/; 
    if (regex4.test(pass)) count++; 

    return strength[count];
}

// Get a reference to the input element
const enc_pass = document.getElementById('encodePassword');
const enc_password_type = document.getElementById('enc_password_type')
const dec_password_type = document.getElementById('dec_password_type')


// Add an event listener to the input element to detect changes
enc_pass.addEventListener('input', function(event) {
// When the input value changes, update the output element with the input value
if(event.target.value == '')
    {
        enc_password_type.textContent = ""
    }
    else
    {
        enc_password_type.textContent = checkStrength(event.target.value)
    }

});

const dec_pass = document.getElementById('decodePassword')
dec_pass.addEventListener('input', function(event) {
    // When the input value changes, update the output element with the input value
    if(event.target.value == '')
        {
            dec_password_type.textContent = ""
        }
        else
        {
            dec_password_type.textContent = checkStrength(event.target.value)
        }
    
    });
