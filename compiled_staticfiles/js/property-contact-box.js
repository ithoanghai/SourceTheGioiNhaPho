const setupContactBox = function() {
    const t = (new Vue({
        "el": "#withUs_PopupContact",
        "template": "#withUs_ContactPopupTemplate",
        "delimiters": [ "[[", "]]" ],
        "data": {
            "showContactPopup": !1,
            "data": {
                "firstname": "",
                "lastname": "",
                "phone": "",
                "email": "",
                "message": ""
            },
            "errors": {
                "firstname": "",
                "lastname": "",
                "phone": "",
                "email": "",
                "message": ""
            }
        },
        "beforeMount": function() {
            this.data.message = $('#contact-now-form input[name="message"]').val();
        },
        "mounted": function() {
            const t = this;
            document.querySelectorAll(".btn-contact").forEach(function(e) {
                e.style.opacity = "1", e.addEventListener("click", t.onClickContactMe.bind(t));
            }), document.addEventListener("keydown", this.closePopupOnKey);
        },
        "methods": {
            "onClickContactMe": function() {
                this.showContactPopup = !0;
            },
            "closePopup": function() {
                this.showContactPopup = !1;
            },
            "closePopupOnKey": function(t) {
                this.showContactPopup && "Escape" === t.key && (this.showContactPopup = !1);
            },
            "shouldFocusedClass": function(t) {
                return this.focusedField === t || "" !== this.data[t];
            },
            "onFocusField": function(t) {
                this.focusedField = t;
            },
            "toggleFocusField": function(t) {
                this.focusedField == t ? this.focusedField = "" : this.focusedField = t;
            },
            "onBlur": function(t) {
                switch (this.focusedField = "", t) {
                  case "phone":
                    this.validatePhone();
                    break;

                  case "email":
                    this.validateEmail();
                    break;

                  case "requestPrice":
                    this.validatePrice();
                    break;

                  default:
                    this.validateRequired(t);
                }
            },
            "onSelectHouseType": function(t) {
                this.data.houseType = t, this.onBlur("houseType");
            },
            "getSelectedHouseTypeText": function(t) {
                return this.houseTypes.find(t.type === this.data.houseType).text;
            },
            "onSelectDistrict": function(t) {
                this.data.district = t;
            },
            "handleInputChange": function(t, e) {
                this.errors[t] = "";
            },
            "validateRequired": function(t) {
                this.data[t] || (this.errors[t] = "Thông tin bắt buộc");
            },
            "validatePhone": function() {
                const t = $('#contact-now-form input[name="phone"]').val();
                if (t) {
                    const e = vnf_regex.test(t.trim());
                    if (!e) return void (this.errors.phone = "Số điện thoại không hợp lệ.");
                    this.errors.phone = "", this.data.phone = t;
                } else this.errors.phone = "Vui lòng điền số điện thoại.";
            },
            "validateEmail": function() {
                if (this.data.email = $('#contact-now-form input[name="email"]').val(), this.data.email) {
                    const t = email_regex.test(this.data.email);
                    if (!t) return this.errors.email = "Email không hợp lệ.", this.errors.email;
                }
            },
            "validatePrice": function() {
                if (!this.data.requestPrice) return void (this.errors.requestPrice = "");
                const t = parseFloat(this.data.requestPrice);
                isNaN(t) ? this.errors.requestPrice = "Xin điền số hợp lệ" : this.errors.requestPrice = "";
            },
            "handleFormSubmit": function(t) {
                var e, n;
                t.preventDefault(), e = !1;
                for (n in Object.keys(this.errors)) this.onBlur(n), this.errors[n] && (e = !0);
                if (!e) {
                    const r = $("#contact-now-form form"), i = r.serialize();
                    $.ajax({
                        "method": r.attr("method"),
                        "url": r.attr("action"),
                        "data": i,
                        "beforeSend": function() {
                            r.find("button").attr("disabled", "disabled").addClass("running");
                        }
                    }).fail(function() {}).done(function(t) {
                        setTimeout(function() {
                            $("#search-content").prepend('<div style="text-align: center;padding-bottom: 0;" class="alert alert-success">\n                    <p class="blink">${resp.message}</p>\n                </div>'),
                            this.closePopup(), hideAlert(8e3);
                        }, 2e3);
                    }).always(function() {
                        setTimeout(function() {
                            r.find("button").removeClass("running").removeAttr("disabled");
                        }, 1500);
                    });
                }
            }
        },
        "destroyed": function() {
            document.removeEventListener("keydown", this.closePopupOnKey);
        }
    }), Vue.extend({
        "template": "#contactPopupTemplate",
        "delimiters": [ "[[", "]]" ],
        "props": {
            "showContactPopup": {
                "type": Boolean,
                "default": !0
            },
            "closePopup": Function
        },
        "data": {
            "data": {
                "firstname": "",
                "lastname": "",
                "phone": "",
                "email": "",
                "district": {
                    "code": "",
                    "text": ""
                },
                "houseType": "apartment",
                "requestPrice": "",
                "message": ""
            },
            "errors": {
                "firstname": "",
                "lastname": "",
                "phone": "",
                "email": "",
                "district": "",
                "houseType": "",
                "requestPrice": "",
                "message": ""
            },
            "focusedField": "",
            "houseTypes": houseTypes,
            "districtData": districts,
        },
        "computed": {},
        "methods": {
            "shouldFocusedClass": function(t) {
                return this.focusedField === t || "" !== this.data[t];
            },
            "onFocusField": function(t) {
                this.focusedField = t;
            },
            "toggleFocusField": function(t) {
                this.focusedField == t ? this.focusedField = "" : this.focusedField = t;
            },
            "onBlur": function(t) {
                switch (this.focusedField = "", t) {
                  case "phone":
                    this.validatePhone();
                    break;

                  case "email":
                    this.validateEmail();
                    break;

                  case "requestPrice":
                    this.validatePrice();
                    break;

                  default:
                    this.validateRequired(t);
                }
            },
            "onSelectHouseType": function(t) {
                this.data.houseType = t, this.onBlur("houseType");
            },
            "getSelectedHouseTypeText": function(t) {
                return this.houseTypes.find(t.type === this.data.houseType).text;
            },
            "onSelectDistrict": function(t) {
                this.data.district = t;
            },
            "handleInputChange": function(t, e) {
                this.errors[t] = "";
            },
            "validateRequired": function(t) {
                this.data[t] || (this.errors[t] = "Thông tin bắt buộc");
            },
            "validatePhone": function() {
                const t = $('#contact-now-form-body input[name="phone"]').val();
                if (t) {
                    const e = vnf_regex.test(t.trim());
                    if (!e) return void (this.errors.phone = "Số điện thoại không hợp lệ.");
                    this.errors.phone = "", this.data.phone = t;
                } else this.errors.phone = "Vui lòng điền số điện thoại.";
            },
            "validateEmail": function() {
                this.data.email = $('#contact-now-form-body input[name="email"]').val(), this.data.email && email_regex.test(this.data.email) === !1 && (this.errors.email = "Email không hợp lệ.");
            },
            "validatePrice": function() {
                if (!this.data.requestPrice) return void (this.errors.requestPrice = "");
                const t = parseFloat(this.data.requestPrice);
                isNaN(t) ? this.errors.requestPrice = "Xin điền số hợp lệ" : this.errors.requestPrice = "";
            },
            "handleFormSubmit": function(t) {
                var e, n;
                t.preventDefault(), e = !1;
                for (n in Object.keys(this.errors)) this.onBlur(n), this.errors[n] && (e = !0);
                if (!e) {
                    const r = $("#contact-now-form form"), i = r.serialize();
                    $.ajax({
                        "method": r.attr("method"),
                        "url": r.attr("action"),
                        "data": i,
                        "beforeSend": function() {
                            r.find("button").attr("disabled", "disabled").addClass("running");
                        }
                    }).fail(function() {}).done(function(t) {
                        setTimeout(function() {
                            $("#search-content").prepend('<div style="text-align: center;padding-bottom: 0;" class="alert alert-success">\n                    <p class="blink">${resp.message}</p>\n</div>'),
                            this.closePopup(), hideAlert(8e3);
                        }, 2e3);
                    }).always(function() {
                        setTimeout(function() {
                            r.find("button").removeClass("running").removeAttr("disabled");
                        }, 1500);
                    });
                }
            }
        }
    }));
    Vue.component("contact-popup", t);
};

waitFor("Vue", setupContactBox);