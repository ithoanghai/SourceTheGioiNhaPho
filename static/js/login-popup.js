new Vue({
    el: "#login-modal",
    template: "#LoginPopupTemplate",
    delimiters: [ "[[", "]]" ],
    data: {
        isShowPopup: !1
    },
    methods: {
        showPopupModal: function() {
            this.isShowPopup = !0;
        },
        closeModal: function() {
            this.isShowPopup = !1;
        },
        closePopupOnKey: function(t) {
            "Escape" === t.key && (this.isShowPopup = !1);
        }
    },
    mounted: function() {
        const t = this;
        $("a[href='#login']").each(function(e, n) {
            $(n).on("click", t.showPopupModal);
        }), document.addEventListener("keydown", this.closePopupOnKey);
    }
});