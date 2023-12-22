

function login() {
    let form_element = document.getElementById("login-form");
    let formData = new FormData(form_element);

    let form = {
        "email": formData.get("email"),
        "password": formData.get("password")
    };

    
    let json = JSON.stringify(form);
    fetch("/auth/login", {
        method: "POST",
        body: json,
        headers: {
            "Content-Type": "application/json"
        }
    }).then((response) => {
        if (response.status == 200) {
            return response.json();
        } else
            alert("Usuario o contraseña incorrectos");
    }).then((data) => {
        localStorage.setItem("name", data.name);
        localStorage.setItem("email", data.email);
        localStorage.setItem("role", data.role);
        window.location.href = "/";
    }).catch((error) => {
        console.log(error);
    });
}




function signup() {
    let form_element = document.getElementById("signup-form");
    let formData = new FormData(form_element);

    let form = {
        "name": formData.get("name"),
        "role": formData.get("role"),
        "email": formData.get("email"),
        "password": formData.get("password"),
        "security_code": formData.get("security_code")
    };

    
    let json = JSON.stringify(form);
    fetch("/auth/signup", {
        method: "POST",
        body: json,
        headers: {
            "Content-Type": "application/json"
        }
    }).then((response) => {
        if (response.status == 200) {
            return response.json();
        } else
            alert("Ha ocurrido un error, puede que el usuario ya se encuentre dentro del sistema");
    }).then((data) => {
        localStorage.setItem("name", data.name);
        localStorage.setItem("email", data.email);
        localStorage.setItem("role", data.role);
        window.location.href = "/";
    }).catch((error) => {
        console.log(error);
    });
}

