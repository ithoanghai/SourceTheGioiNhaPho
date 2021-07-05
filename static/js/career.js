!function () {
    var c = $("#list-career");
    $("a[href=#list-career]").click(function (e) {
        e.preventDefault(), $("html, body").animate({scrollTop: c.offset().top}, 400)
    })
}(), function () {
    $(".career-form").on("click", ".hs_upload_cv .hs-field-desc", function () {
        $(".career-form").find(".hs_upload_cv input[type=file]").click()
    })
}();