

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

