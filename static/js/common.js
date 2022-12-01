function createHSForm(t) {
    var e = t.onFormSubmit, n = Object.create(t);
    return n.onFormSubmit = function() {
        var t = $("[name=ga_client_id]");
        t[0] && t.val(function() {
            try {
                return ga.getAll()[0].get("clientId");
            } catch (t) {
                return "";
            }
        }()), "function" == typeof e && e.apply(this, arguments);
    }, hbspt.forms.create(n);
}

function toggleFooterContent() {
    window.matchMedia("(max-width: 640px)").matches ? (footerContent.find("ul").hide(),
    footerContent.find(".zmdi").removeClass("zmdi-chevron-up").addClass("zmdi-chevron-down")) : footerContent.find("ul").show();
}

var dialogManager, footerContent, chatbox = document.getElementById("fb-customer-chat");

chatbox.setAttribute("page_id", "108470991299693"), chatbox.setAttribute("attribution", "biz_inbox"),
window.fbAsyncInit = function() {
    FB.init({
        xfbml: !0,
        version: "v11.0"
    });
}, function(t, e, n) {
    var i, o = t.getElementsByTagName(e)[0];
    t.getElementById(n) || ((i = t.createElement(e)).id = n, i.src = "https://connect.facebook.net/vi_VN/sdk/xfbml.customerchat.js",
    o.parentNode.insertBefore(i, o));
}(document, "script", "facebook-jssdk"), !function(t, e, n, i, o, r, a) {
    t.fbq || (o = t.fbq = function() {
        o.callMethod ? o.callMethod.apply(o, arguments) : o.queue.push(arguments);
    }, t._fbq || (t._fbq = o), (o.push = o).loaded = !0, o.version = "2.0", o.queue = [],
    (r = e.createElement(n)).async = !0, r.src = "https://connect.facebook.net/en_US/fbevents.js",
    (a = e.getElementsByTagName(n)[0]).parentNode.insertBefore(r, a));
}(window, document, "script"), fbq("init", "425964015350296"), fbq("track", "PageView"),
window._au_api = "", window.fap_url = "",
window["fap.server"] = "", window.favorite_api = "api/favorite",
window.googleClientId = "539423642927.apps.googleusercontent.com", window.staticUrl = "",
window.isLoggedIn = !1, window.hsConversationsSettings = {
    loadImmediately: !1
}, window.RFeedback = {
    API: "https://thegioinhaphovietnam.com.vn/mapi",
    email: "",
    name: "",
    phone: "",
    ip: "10.244.0.0"
}, !function() {
    var t = [], e = 0, n = function() {
        n.called = !0, t && hbspt && hbspt.forms && hbspt.forms.deps ? (t.forEach(function(t) {
            hbspt.forms.create(t);
        }), clearTimeout(e), delete t) : e = setTimeout(n, 500);
    };
    window.hbspt = {
        forms: {
            create: function(e) {
                n.called || n(), function(e) {
                    !t || hbspt && hbspt.forms && hbspt.forms.deps || t.push(e);
                }(e);
            }
        }
    };
}(), dialogManager = function() {
    var t = this;
    return t.bodyClassSpecs = "mdialog-body", t.bodyLoadingClass = "mdialog-loading",
    t.cachedBodyStyle = null, t.styleOptions = {
        zindex: 99999,
        width: 300,
        minHeight: 100,
        background: "rgba(0,0,0,.5)",
        opacity: .5
    }, t.key = {
        cachedStyle: "cached-style"
    }, t.show = function(e, n, i, o) {
        var r, a, s;
        return (n = $.extend(!0, {
            outSideClick: !0
        }, n || {})).maxWidth = "100%", a = document.body.getAttribute("style"), document.body.setAttribute(t.key.cachedStyle, a),
        (r = e && "string" == typeof e ? $(document.getElementById(e)) : e).css("opacity", 0),
        r.css("overflow-y", "auto"), r.css("overflow-x", "hidden"), r.addClass("opened"),
        s = (n ? n.body : "") || ".body", r.find(s).css(n), r.find(s).addClass(t.bodyClassSpecs),
        r[0] && (r[0].$dialogCallback = i), r[0] && (r[0].$dialogInitTime = +new Date()),
        n && n.close && r.find(s + " " + n.close).off().click(function(n) {
            n.preventDefault(), t.hide(e, i);
        }), n && n.outSideClick && r.off().click(function() {
            t.hide(e, i);
        }), r.find(s).click(function(t) {
            t.stopPropagation();
        }), t.animation(r, 0, 0, 1, function() {
            o && o();
        }), t.loadingEnd(r), r;
    }, t.animation = function(e, n, i, o, r) {
        e.css("opacity", n), o > 0 && n > 1 || 0 > o && 0 > n ? r && r() : setTimeout(function() {
            n += o * (.05 * i + 1e-4 * i * i), t.animation(e, n, i + 1, o, r);
        }, 10);
    }, t.hide = function(e, n) {
        var i;
        i = e ? "string" == typeof e ? $(document.getElementById(e)) : e : $(".mdialog.opened"),
        t.animation(i, 1, 0, -1, function() {
            i.removeClass("opened"), n && n(i);
        });
    }, t.loadingStart = function(e) {
        (e ? "string" == typeof e ? $(document.getElementById(e)) : e : $(".mdialog.opened")).find("." + t.bodyClassSpecs).addClass(t.bodyLoadingClass);
    }, t.loadingEnd = function(e) {
        (e ? "string" == typeof e ? $(document.getElementById(e)) : e : $(".mdialog.opened")).find("." + t.bodyClassSpecs + "." + t.bodyLoadingClass).removeClass(t.bodyLoadingClass);
    }, $(window).keydown(function(e) {
        var n, i, o, r, a = $(".mdialog.opened");
        if (a.length && 27 == e.keyCode) {
            for (n = [], n.length = a.length, i = 0; i < a.length; i++) for (o = i; o < a.length; o++) a[i].$dialogInitTime > a[o].$dialogInitTime ? (n[o] = a[i],
            n[i] = a[o]) : (n[i] = a[i], n[o] = a[o]);
            r = n[n.length - 1], r && t.hide($(r), r ? r.$dialogCallback : null);
        }
    }), t.initStyles = function() {
        var t = document.createElement("STYLE"), e = document.head || document.getElementsByTagName("head")[0];
        t.type = "text/css", t.styleSheet ? t.styleSheet.cssText = "" : t.appendChild(document.createTextNode(this.getCss())),
        e.appendChild(t);
    }, t.getCss = function() {
        var e, n, i, o, r = t.styleOptions, a = "", s = {
            display: "none",
            position: "fixed",
            top: "0",
            height: "100%",
            left: "0",
            width: "100%"
        };
        return s["z-index"] = r.zindex, s.background = r.background, a += t.assignStyle(".mdialog", s),
        a += ".mdialog.opened{display: block;}", e = {}, e.width = r.width + "px", e["min-height"] = r.minHeight + "px",
        e.background = "#fff", e.margin = "60px auto 140px auto", a += t.assignStyle(".mdialog .body", e),
        n = {
            position: "relative"
        }, a += t.assignStyle("." + t.bodyLoadingClass, n), i = {
            content: "' '",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            position: "absolute",
            background: "#fff",
            opacity: .4,
            "z-index": 1
        }, a += t.assignStyle("." + t.bodyLoadingClass + ":before", i), o = {
            content: "' '",
            border: "2px solid #303339",
            "border-top": "2px solid #fff;",
            "border-radius": "50%",
            width: "30px",
            height: "30px",
            position: "absolute",
            top: "calc(50% - 15px)",
            left: "calc(50% - 15px)",
            "-webkit-animation": "spin 2s linear infinite",
            animation: "spin 2s linear infinite",
            "z-index": 1
        }, a += t.assignStyle("." + t.bodyLoadingClass + ":after", o), a += "@-webkit-keyframes spin { 0% { -webkit-transform: rotate(0deg); } 100% { -webkit-transform: rotate(360deg); } } @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }";
    }, t.assignStyle = function(t, e) {
        var n, i = t + "{";
        for (n in e) i += n + ":" + e[n] + ";";
        return i += "}";
    }, t.initStyles(), t;
}(), window.showDialog || (window.showDialog = function(t, e, n) {
    dialogManager.show("contact-now", {
        close: e,
        body: n
    }, function() {}, function(e) {
        $("#" + t).find("input").first().focus(), $(n).css("max-width", "").css("width", "100%").find(".popup-contact").scrollTop(0);
    });
}), createHSForm({
    css: "",
    target: "#sell-now-form-body",
    portalId: "2775524",
    formId: "9cc2fa2e-59d1-410a-a910-217a24437963",
    onFormReady: function(t) {
        t.on("submit", function(t) {
            goog_report_conversion ? goog_report_conversion() : null;
        });
    }
}), footerContent = $("#footer .info-container li"), toggleFooterContent(), footerContent.click(function(t) {
    if (window.matchMedia("(max-width: 640px)").matches) {
        if ("A" === t.target.tagName) return;
        footerContent.find("ul").slideUp(300), footerContent.find(".zmdi").removeClass("zmdi-chevron-up").addClass("zmdi-chevron-down"),
        $(this).find("ul").is(":visible") || ($(this).find("ul").slideDown(300), $(this).find(".zmdi").removeClass("zmdi-chevron-down").addClass("zmdi-chevron-up"));
    }
}), $(window).resize(function() {
    toggleFooterContent();
}), Defer.dom("img.lazy", 200, "loaded"), $(document).ready(function() {
    $("*").bind("cut copy paste contextmenu", function(t) {
        t.preventDefault();
    });
});

window.addEventListener("message", function(t) {
	if (t.data && t.data.cmd == "zchat_widget_toggle_sticker") {
		const f = document.getElementById("chatiframe");
		if (t.data.width) {
			f.style.width = t.data.width;
			f.style.height = t.data.height;
		} else {
			f.style.width = "440px";
			f.style.height = "85vh";
		}
	}
});