/*Footer*/
let footerContent = $("#footer .info-container li")

toggleFooterContent()

footerContent.click(function (e) {
  if (window.matchMedia("(max-width: 640px)").matches) {
    // don't slideUp when click <a>
    if (e.target.tagName === 'A')
      return

    footerContent.find("ul").slideUp(300)
    footerContent.find(".zmdi").removeClass("zmdi-chevron-up").addClass("zmdi-chevron-down")
    if (!$(this).find("ul").is(":visible")) {
      $(this).find("ul").slideDown(300)
      $(this).find(".zmdi").removeClass("zmdi-chevron-down").addClass("zmdi-chevron-up")
    }
  }
});

$(window).resize(function () {
  toggleFooterContent()
})

/**
 * show/hide footer content depend on max-width
 */
function toggleFooterContent() {
  if (window.matchMedia("(max-width: 640px)").matches) {
    footerContent.find("ul").hide()
    footerContent.find(".zmdi").removeClass("zmdi-chevron-up").addClass("zmdi-chevron-down")
  } else {
    footerContent.find("ul").show()
  }
}

/*Footer - END*/