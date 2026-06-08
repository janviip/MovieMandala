document
.getElementById("loginForm")
.addEventListener("submit", function(e){

    e.preventDefault();

    alert("Login Successful");

    window.location.href = "result.html";

});