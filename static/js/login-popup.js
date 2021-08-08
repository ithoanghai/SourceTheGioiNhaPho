new Vue({
    el: '#login-modal',
    template: "#LoginPopupTemplate",
    delimiters: ['[[', ']]'],
    data: {
        isShowPopup: false,
    },
    methods: {
        showPopupModal: function () {
            console.log('click show popup modal')
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

$(document).ready(function () {
    // const secondaryBar$ = $('.secondaryBar');
    // const actionBar$ = $('.actionBar');
    // $('.menu-humber').click(() => {
    //     secondaryBar$.css('position', 'static');
    //     actionBar$.css('position', 'static');
    // });
    //
    // $(".main-nav-menu__overlay").click(() => {
    //     secondaryBar$.css('position', '');
    //     actionBar$.css('position', '');
    // });
    //
    // $(".close__main-menu").click(() => {
    //     secondaryBar$.css('position', '');
    //     actionBar$.css('position', '');
    // });
})