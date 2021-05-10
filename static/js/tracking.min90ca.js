!function (e, t, a) {
    if (!t.__SV) {
        var n = window;
        try {
            var o, i, r, s = n.location, p = s.hash;
            o = function (e, t) {
                return (i = e.match(new RegExp(t + "=([^&]*)"))) ? i[1] : null
            }, p && o(p, "state") && "mpeditor" === (r = JSON.parse(decodeURIComponent(o(p, "state")))).action && (n.sessionStorage.setItem("_mpcehash", p), history.replaceState(r.desiredHash || "", e.title, s.pathname + s.search))
        } catch (e) {
        }
        var c, l, g, u;
        window.fap = t, t._i = [], t.init = function (e, a, n) {
            var o = t;

            function i(e, t) {
                var a = t.split(".");
                2 == a.length && (e = e[a[0]], t = a[1]), e[t] = function () {
                    e.push([t].concat(Array.prototype.slice.call(arguments, 0)))
                }
            }

            for (void 0 !== n ? o = t[n] = [] : n = "fap", o.people = o.people || [], o.toString = function (e) {
                var t = "fap";
                return "fap" !== n && (t += "." + n), e || (t += " (stub)"), t
            }, o.people.toString = function () {
                return o.toString(1) + ".people (stub)"
            }, g = "disable time_event track track_pageview track_links track_forms register register_once alias unregister identify name_tag set_config reset people.set people.set_once people.increment people.append people.union people.track_charge people.clear_charges people.delete_user".split(" "), u = 0; u < g.length; u++) i(o, g[u]);
            t._i.push([e, a, n])
        }, t.integrateWithGA = function () {
            var e, t, a = "sendHitTask";
            e = "remoteHitSender", "function" == typeof (t = window[window.GoogleAnalyticsObject || "ga"]) && t("provide", e, function (e, t) {
                var n = e.get(a);
                e.set(a, function (e) {
                    var a = e.get("hitPayload");
                    n(e);
                    var o = new XMLHttpRequest;
                    o.open("get", t.url + "?" + a, !0), o.send()
                })
            })
        }, t.__SV = 1.2, t.init("", {
            api_host: window["fap.server"] || "//google-analytics.vn/mixpanel",
            persistence: "localStorage",
            persistence_name: "__.thegioinhaphovietnam.com.vn",
            autotrack: !1,
            track_pageview: !1,
            debug: !1,
            img: !0
        }), (c = e.createElement("script")).type = "text/javascript", c.async = !0, c.src = a, (l = e.getElementsByTagName("script")[0]).parentNode.insertBefore(c, l)
    }
}(document, window.fap || [], window.fap_url || "/static/js/fap.min.js"), function (e, t, a, n, o, i, r) {
    e.GoogleAnalyticsObject = o, e.ga = e.ga || function () {
        (e.ga.q = e.ga.q || []).push(arguments)
    }, e.ga.l = 1 * new Date, i = t.createElement(a), r = t.getElementsByTagName(a)[0], i.async = 1, i.src = "https://www.google-analytics.com/analytics.js", r.parentNode.insertBefore(i, r)
}(window, document, "script", 0, "ga"), ga("create", "UA-77196470-1", "auto");