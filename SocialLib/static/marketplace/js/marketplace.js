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