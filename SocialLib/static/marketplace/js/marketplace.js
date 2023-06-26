
function userAvatarImgPreview(input) {
    console.log("Catalog image selected!")
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#user_avatar_preview')
                .attr('src', e.target.result)
                .css({'height': '130px', 'width': '130px'});
        };
        $('#avatar_img_load_btn_block').css({'display': 'none'});

        reader.readAsDataURL(input.files[0]);
    }
}


function pswToggle() {
    const togglePassword = document.querySelector('#togglePassword');
    const password = document.querySelector('#password');

    // toggle the type attribute
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    // toggle the eye slash icon
    togglePassword.classList.toggle('fa-eye-slash');
}