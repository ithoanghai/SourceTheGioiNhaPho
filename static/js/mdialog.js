window.$dialog = function () {
    var e = {
        bodyClassSpecs: "mdialog-body",
        bodyLoadingClass: "mdialog-loading",
        cachedBodyStyle: null,
        default: {zindex: 99999, width: 300, minHeight: 100, background: "rgba(0,0,0,.5)", opacity: .5},
        key: {cachedStyle: "cached-style"}
    };
    return e.show = function (t, n, i, o) {
        (n = $.extend(!0, {outSideClick: !0}, n || {})).maxWidth = "100%";
        var a, d = document.body.getAttribute("style");
        document.body.setAttribute(e.key.cachedStyle, d), (a = t && "string" == typeof t ? $(document.getElementById(t)) : t).css("opacity", 0), a.css("overflow-y", "auto"), a.css("overflow-x", "hidden"), a.addClass("opened");
        var s = (n ? n.body : "") || ".body";
        return a.find(s).css(n), a.find(s).addClass(e.bodyClassSpecs), a[0] && (a[0].$dialogCallback = i), a[0] && (a[0].$dialogInitTime = +new Date), n && n.close && a.find(s + " " + n.close).off().click(function (n) {
            n.preventDefault(), e.hide(t, i)
        }), n && n.outSideClick && a.off().click(function () {
            e.hide(t, i)
        }), a.find(s).click(function (e) {
            e.stopPropagation()
        }), e.animation(a, 0, 0, 1, function () {
            o && o()
        }), e.loadingEnd(a), a
    }, e.animation = function (t, n, i, o, a) {
        t.css("opacity", n), o > 0 && n > 1 || o < 0 && n < 0 ? a && a() : setTimeout(function () {
            n += o * (.05 * i + 1e-4 * i * i), e.animation(t, n, i + 1, o, a)
        }, 10)
    }, e.hide = function (t, n) {
        var i;
        i = t ? "string" == typeof t ? $(document.getElementById(t)) : t : $(".mdialog.opened"), e.animation(i, 1, 0, -1, function () {
            i.removeClass("opened"), n && n(i)
        })
    }, e.loadingStart = function (t) {
        (t ? "string" == typeof t ? $(document.getElementById(t)) : t : $(".mdialog.opened")).find("." + e.bodyClassSpecs).addClass(e.bodyLoadingClass)
    }, e.loadingEnd = function (t) {
        (t ? "string" == typeof t ? $(document.getElementById(t)) : t : $(".mdialog.opened")).find("." + e.bodyClassSpecs + "." + e.bodyLoadingClass).removeClass(e.bodyLoadingClass)
    }, $(window).keydown(function (t) {
        var n = $(".mdialog.opened");
        if (n.length && 27 == t.keyCode) {
            var i = [];
            i.length = n.length;
            for (var o = 0; o < n.length; o++) for (var a = o; a < n.length; a++) n[o].$dialogInitTime > n[a].$dialogInitTime ? (i[a] = n[o], i[o] = n[a]) : (i[o] = n[o], i[a] = n[a]);
            var d = i[i.length - 1];
            d && e.hide($(d), d ? d.$dialogCallback : null)
        }
    }), e.initStyles = function () {
        var e = document.createElement("STYLE"), t = document.head || document.getElementsByTagName("head")[0];
        e.type = "text/css", e.styleSheet ? e.styleSheet.cssText = "" : e.appendChild(document.createTextNode(this.getCss())), t.appendChild(e)
    }, e.getCss = function () {
        var t = e.default, n = "",
            i = {display: "none", position: "fixed", top: "0", height: "100%", left: "0", width: "100%"};
        i["z-index"] = t.zindex, i.background = t.background, n += e.assignStyle(".mdialog", i), n += ".mdialog.opened{display: block;}";
        var o = {};
        o.width = t.width + "px", o["min-height"] = t.minHeight + "px", o.background = "#fff", o.margin = "60px auto 140px auto", n += e.assignStyle(".mdialog .body", o);
        var a = {position: "relative"};
        n += e.assignStyle("." + e.bodyLoadingClass, a);
        var d = {
            content: "' '",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            position: "absolute",
            background: "#fff",
            opacity: .4,
            "z-index": 1
        };
        n += e.assignStyle("." + e.bodyLoadingClass + ":before", d);
        var s = {
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
        };
        return n += e.assignStyle("." + e.bodyLoadingClass + ":after", s), n += "@-webkit-keyframes spin { 0% { -webkit-transform: rotate(0deg); } 100% { -webkit-transform: rotate(360deg); } } @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }"
    }, e.assignStyle = function (e, t) {
        var n = e + "{";
        for (var i in t) {
            n += i + ":" + t[i] + ";"
        }
        return n += "}"
    }, e.initStyles(), e
}();