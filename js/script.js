$('option').mousedown(function(e) {
    /*
        Avoid the need for ctrl-click in a multi-select box.
    */

    e.preventDefault();
    $(this).toggleClass('selected');
    $(this).prop('selected', !$(this).prop('selected'));
    return false;
});


$(document).ready(function(){

    const username = document.getElementById("id_username")
    const password = document.getElementById("id_password")

    const password1 = document.getElementById("id_password1")
    const password2 = document.getElementById("id_password2")

    if (username && password){
        username.setAttribute('class','form-control');
        password.setAttribute('class','form-control');
    }
    else if(password1 && password2){
        username.setAttribute('class','form-control');
        password1.setAttribute('class','form-control');
        password2.setAttribute('class','form-control');
    }

});