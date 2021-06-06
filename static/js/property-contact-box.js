const vnf_regex = /((09|03|07|08|05)+([0-9]{8})\b)/g;
const email_regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
new Vue({
    el: '#detailPopupContact',
    template: '#detailPopupContactTemplate',
    delimiters: ["[[", "]]"],
    data: {
        showContactPopup: false,
        data: {
            firstname: '',
            lastname: '',
            phone: '',
            email: '',
            message: ''
        },
        errors: {
            firstname: '',
            lastname: '',
            phone: '',
            email: '',
            message: ''
        }
    },
    beforeMount() {
        this.data.message = $('#detailContactForm input[name="message"]').val();
    },
    mounted() {
        const e = this;
        document.querySelectorAll(".btn-contact-me").forEach(function (t) {
            t.style.opacity = "1", t.addEventListener("click", e.onClickContactMe.bind(e))
        });
        document.addEventListener('keydown', this.closePopupOnKey);
    },
    methods: {

        onClickContactMe: function () {
            this.showContactPopup = true;
        },
        closePopup: function () {
            this.showContactPopup = false;
        },
        closePopupOnKey: function (e) {
            if (this.showContactPopup) {
                if (e.key === 'Escape') {
                    this.showContactPopup = false;
                }
            }
        },
        validateRequired(field) {
            if (!this.data[field]) {
                this.errors[field] = "Thông tin bắt buộc";
            }
        },
        validatePhone() {
            //Auto Input
            this.data.phone = $('#detailContactForm input[name="phone"]').val();
            if (this.data.phone) {
                if (vnf_regex.test(this.data.phone) === false) {
                    this.errors.phone = 'Số điện thoại không hợp lệ.'
                }
            } else {
                this.errors.phone = 'Vui lòng điền số điện thoại.'
            }
        },
        validateEmail() {
            this.data.phone = $('#detailContactForm input[name="email"]').val();
            if (this.data.email) {
                if (email_regex.test(this.data.email) === false) {
                    this.errors.email = 'Email không hợp lệ.'
                }
            }
        },
        handleInputChange(field, e) {
            this.errors[field] = '';
        },
        handleFormSubmit(e) {
            Object.values(this.errors).forEach((err) => {
                if (err) {
                    e.preventDefault()
                }
            })
        }
    },
    destroyed() {
        document.removeEventListener('keydown', this.closePopupOnKey)
    }
})