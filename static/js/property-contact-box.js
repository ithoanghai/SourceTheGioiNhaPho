const vnf_regex = /((09|03|07|08|05)+([0-9]{8})\b)/g;
const email_regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
const houseTypes = [
    {type: 'town_house', text: 'Nhà phố'},
    {type: 'shop_house', text: 'Cửa hàng'},
    {type: 'apartment', text: 'Căn hộ'},
    {type: 'land', text: 'Đất nền'},
    {type: 'land_business', text: 'Mặt bằng kinh doanh'},
    {type: 'villa', text: 'Biệt thự'}
];

new Vue({
    el: '#withUs_PopupContact',
    template: '#withUs_ContactPopupTemplate',
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
        this.data.message = $('#contact-now-form input[name="message"]').val();
    },
    mounted() {
        const e = this;
        document.querySelectorAll(".btn-contact").forEach(function (t) {
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

        shouldFocusedClass(field) {
            return this.focusedField === field || this.data[field] !== '';
        },
        onFocusField(field) {
            this.focusedField = field;
        },
        toggleFocusField(field) {
            if (this.focusedField == field) {
                this.focusedField = ''
            } else {
                this.focusedField = field;
            }
        },
        onBlur(field) {
            this.focusedField = '';
            switch (field) {
                case 'phone':
                    this.validatePhone();
                    break;
                case 'email':
                    this.validateEmail();
                    break;
                case 'requestPrice':
                    this.validatePrice();
                    break;
                default:
                    this.validateRequired(field);
                    break;
            }
        },
        onSelectHouseType(type) {
            this.data.houseType = type;
            this.onBlur('houseType');
        },
        getSelectedHouseTypeText() {
            return (this.houseTypes.find(item => item.type === this.data.houseType)).text;
        },
        onSelectDistrict(district) {
            this.data.district = district
        },
        handleInputChange(field, e) {
            this.errors[field] = '';
        },
        validateRequired(field) {
            if (!this.data[field]) {
                this.errors[field] = "Thông tin bắt buộc";
            }
        },
        validatePhone() {
            //Auto Input
            const phone = $('#contact-now-form input[name="phone"]').val();
            if (phone) {
                const isValid = vnf_regex.test(phone.trim());
                if (!isValid) {
                    this.errors.phone = 'Số điện thoại không hợp lệ.'
                    return;
                }
                this.errors.phone = '';
                this.data.phone = phone;
            } else {
                this.errors.phone = 'Vui lòng điền số điện thoại.'
            }
        },
        validateEmail() {
            this.data.email = $('#contact-now-form input[name="email"]').val();
            if (this.data.email) {
                const isValid = email_regex.test(this.data.email);
                 if (!isValid) {
                    this.errors.email = 'Email không hợp lệ.'
                    return this.errors.email;
                }
            }
        },
        validatePrice() {
            if (!this.data.requestPrice) {
                this.errors.requestPrice = '';
                return;
            }
            const price = parseFloat(this.data.requestPrice);
            if (isNaN(price)) {
                this.errors.requestPrice = 'Xin điền số hợp lệ';
            } else {
                this.errors.requestPrice = '';
            }
        },
        handleFormSubmit(e) {
            e.preventDefault();
            let hasError = false;
            for (let field of Object.keys(this.errors)) {
                this.onBlur(field);
                if (this.errors[field]) {
                    hasError = true;
                }
            }
            if (hasError) {
                return;
            }
            // const data = this.data;
            const $form = $('#contact-now-form form');
            const formData = $form.serialize();
            $.ajax({
                method: $form.attr('method'),
                url: $form.attr('action'),
                data: formData,
                beforeSend: () => {
                    $form.find('button').attr('disabled', 'disabled').addClass('running');
                }
            }).fail(() => {
            }).done((resp) => {
                setTimeout(() => {
                    $('#search-content').prepend(`<div style="text-align: center;padding-bottom: 0;" class="alert alert-success">
                    <p class="blink">${resp.message}</p>
                </div>`)
                    this.closePopup();
                    hideAlert(8000);
                }, 2000)
            }).always(() => {
                setTimeout(() => {
                    $form.find('button').removeClass('running').removeAttr('disabled');
                }, 1500)
            })
        }
    },
    destroyed() {
        document.removeEventListener('keydown', this.closePopupOnKey)
    }
})

const ContactPopUpComponent = Vue.extend({
    template: '#contactPopupTemplate',
    delimiters: ["[[", "]]"],
    props: {
        showContactPopup: {
            type: Boolean,
            default: true
        },
        closePopup: Function
    },
    data() {
        return {
            data: {
                firstname: '',
                lastname: '',
                phone: '',
                email: '',
                district: {
                    code: '',
                    text: ''
                },
                houseType: 'apartment',
                requestPrice: '',
                message: ''
            },
            errors: {
                firstname: '',
                lastname: '',
                phone: '',
                email: '',
                district: '',
                houseType: '',
                requestPrice: '',
                message: ''
            },
            focusedField: '',
            houseTypes: houseTypes,
            districtData: districts,
        }
    },
    computed: {},
    methods: {
        shouldFocusedClass(field) {
            return this.focusedField === field || this.data[field] !== '';
        },
        onFocusField(field) {
            this.focusedField = field;
        },
        toggleFocusField(field) {
            if (this.focusedField == field) {
                this.focusedField = ''
            } else {
                this.focusedField = field;
            }
        },
        onBlur(field) {
            this.focusedField = '';
            switch (field) {
                case 'phone':
                    this.validatePhone();
                    break;
                case 'email':
                    this.validateEmail();
                    break;
                case 'requestPrice':
                    this.validatePrice();
                    break;
                default:
                    this.validateRequired(field);
                    break;
            }
        },
        onSelectHouseType(type) {
            this.data.houseType = type;
            this.onBlur('houseType');
        },
        getSelectedHouseTypeText() {
            return (this.houseTypes.find(item => item.type === this.data.houseType)).text;
        },
        onSelectDistrict(district) {
            this.data.district = district
        },
        handleInputChange(field, e) {
            this.errors[field] = '';
        },
        validateRequired(field) {
            if (!this.data[field]) {
                this.errors[field] = "Thông tin bắt buộc";
            }
        },
        validatePhone() {
            //Auto Input
            const phone = $('#contact-now-form-body input[name="phone"]').val();
            if (phone) {
                const isValid = vnf_regex.test(phone.trim());
                if (!isValid) {
                    this.errors.phone = 'Số điện thoại không hợp lệ.'
                    return;
                }
                this.errors.phone = '';
                this.data.phone = phone;
            } else {
                this.errors.phone = 'Vui lòng điền số điện thoại.'
            }
        },
        validateEmail() {
            this.data.email = $('#contact-now-form-body input[name="email"]').val();
            if (this.data.email) {
                if (email_regex.test(this.data.email) === false) {
                    this.errors.email = 'Email không hợp lệ.'
                }
            }
        },
        validatePrice() {
            if (!this.data.requestPrice) {
                this.errors.requestPrice = '';
                return;
            }
            const price = parseFloat(this.data.requestPrice);
            if (isNaN(price)) {
                this.errors.requestPrice = 'Xin điền số hợp lệ';
            } else {
                this.errors.requestPrice = '';
            }
        },
        handleFormSubmit(e) {
            e.preventDefault();
            let hasError = false;
            for (let field of Object.keys(this.errors)) {
                this.onBlur(field);
                if (this.errors[field]) {
                    hasError = true;
                }
            }
            if (hasError) {
                return;
            }
            // const data = this.data;
            const $form = $('#contact-now-form form');
            const formData = $form.serialize();
            $.ajax({
                method: $form.attr('method'),
                url: $form.attr('action'),
                data: formData,
                beforeSend: () => {
                    $form.find('button').attr('disabled', 'disabled').addClass('running');
                }
            }).fail(() => {
            }).done((resp) => {
                setTimeout(() => {
                    $('#search-content').prepend(`<div style="text-align: center;padding-bottom: 0;" class="alert alert-success">
                    <p class="blink">${resp.message}</p>
                </div>`)
                    this.closePopup();
                    hideAlert(8000);
                }, 2000)
            }).always(() => {
                setTimeout(() => {
                    $form.find('button').removeClass('running').removeAttr('disabled');
                }, 1500)
            })
        }
    }
})
Vue.component('contact-popup', ContactPopUpComponent);
