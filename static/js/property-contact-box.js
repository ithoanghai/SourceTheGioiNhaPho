new Vue({
    el: '#detailPopupContact',
    template: '#detailPopupContactTemplate',
    delimiters: ["[[", "]]"],
    data: {
        showContactPopup: false
    },
    mounted() {
        const e = this;
        document.querySelectorAll(".btn-contact-me").forEach(function (t) {
            t.style.opacity = "1", t.addEventListener("click", e.onClickContactMe.bind(e))
        })
    },
    methods: {
       onClickContactMe: function () {
           this.showContactPopup = true;
       },
        closePopup: function () {
           this.showContactPopup = false;
        }
    }
})