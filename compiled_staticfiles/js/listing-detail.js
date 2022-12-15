
var detailPopupContact = new Vue({
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
        this.data.data.message = $('#detailContactForm input[name="message"]').val();
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

function setupViewMore(heightLimit, $itemsWrapper, $items, $viewMoreWrapper, $viewMoreLink){
    var isCollapse = false
    var itemHeight = $items.height()
    $itemsWrapper.css("box-sizing", "content-box")
    $viewMoreLink.click(function () {
      if(!isCollapse){
        showMore()
      }else{
        hide()
      }
    })

    function showMore(){
      isCollapse = true
      $viewMoreLink.html('Thu gọn<i class="zmdi zmdi-chevron-up zmdi-hc-fw"></i>')
      //$itemsWrapper.css('height', 'auto')
      $itemsWrapper.animate({height: itemHeight + "px"}, 500)
    }

    function hide(){
      isCollapse = false
      $viewMoreLink.html('Xem thêm<i class="zmdi zmdi-chevron-down zmdi-hc-fw"></i>')
      //$itemsWrapper.css('height', heightLimit + 'px')
      $itemsWrapper.animate({height: heightLimit + "px"}, 500)
    }

    if(itemHeight > heightLimit){
      $viewMoreWrapper.show()
    }else{
      $itemsWrapper.css('height', itemHeight + "px")
    }
  }

  var publicFacEle = {
    wrapper: $("#public-facilities .items"),
    items: $("#public-facilities .items ul"),
    viewMore: $("#public-facilities .view-more-wrapper"),
    viewMoreLink: $("#public-facilities .view-more-wrapper a")
  }
  $(document).ready(function(){
    setupViewMore(114, publicFacEle.wrapper, publicFacEle.items, publicFacEle.viewMore, publicFacEle.viewMoreLink)
  })

