new Vue({
    el: '#login-modal',
    template: "#LoginPopupTemplate",
    delimiters: ['[[', ']]'],
    data: {
        isShowPopup: false,
    },
    methods: {
        showPopupModal: function () {
            this.isShowPopup = true;
        },
        closeModal: function () {
            this.isShowPopup = false;
        },
        closePopupOnKey: function (e) {
            if (e.key === 'Escape') {
                this.isShowPopup = false;
            }
        },
    },
    mounted() {
        const t = this;
        $("a[href='#login']").each(function (index, el) {
            $(el).on('click', t.showPopupModal);
        });
        document.addEventListener('keydown', this.closePopupOnKey);
    }

})