(function () {
    var m = void 0, n = !0, r = null, A = !1;

    function B() {
        return function () {
        }
    }

    (function () {
        function W(a) {
            function b() {
                try {
                    a.D = a.D || {}, a.D.$__c = (a.D.$__c || 0) + 1, c.cookie.set("fap_" + d + "__c", a.D.$__c, 1, n)
                } catch (b) {
                    k.error(b)
                }
            }

            var d = a.d("name");
            a.D = a.D || {};
            a.D.$__c = parseInt(c.cookie.get("fap_" + d + "__c")) || 0;
            c.o(document, "submit", b);
            c.o(document, "change", b);
            var e = r;
            c.o(document, "mousedown", function (a) {
                e = a.target
            });
            c.o(document, "mouseup", function (a) {
                a.target === e && b()
            })
        }

        function X() {
            function a() {
                if (!a.Zc) R = a.Zc = n, S = A, c.a(y, function (a) {
                    a.mc()
                })
            }

            function b() {
                try {
                    document.documentElement.doScroll("left")
                } catch (d) {
                    setTimeout(b,
                        1);
                    return
                }
                a()
            }

            if (document.addEventListener) "complete" === document.readyState ? a() : document.addEventListener("DOMContentLoaded", a, A); else if (document.attachEvent) {
                document.attachEvent("onreadystatechange", a);
                var d = A;
                try {
                    d = window.frameElement === r
                } catch (e) {
                }
                document.documentElement.doScroll && d && b()
            }
            c.o(window, "load", a, n)
        }

        function Y() {
            s.init = function (a, b, d) {
                function e(a) {
                    "function" === typeof s.register_once && s.register_once(a)
                }

                if (d) return s[d] || (s[d] = y[d] = I(a, b, d), s[d].ta()), s[d];
                d = s;
                if (y.fap) d = y.fap; else if (a) d =
                    I(a, b, "fap"), d.ta(), y.fap = d;
                s = d;
                1 === M && (window.fap = s);
                Z();
                0 > document.referrer.indexOf(location.protocol + "//" + location.host) && (k.log("Init new session"), e({usid: c.N()}));
                e({psid: c.N(), trackid: c.N()})
            }
        }

        function Z() {
            c.a(y, function (a, b) {
                "fap" !== b && (s[b] = a)
            });
            s._ = c
        }

        function I(a, b, d) {
            var e, f = "fap" === d ? s : s[d];
            if (f && 0 === M) e = f; else {
                if (f && !c.isArray(f)) {
                    k.error("You have already initialized " + d);
                    return
                }
                e = new h
            }
            e.Na(a, b, d);
            e.people = new p;
            e.people.Na(e);
            e.cookie = c.cookie;
            e.utils = c;
            z = z || e.d("debug");
            e.__autotrack_enabled =
                e.d("autotrack");
            k.log(e.d("autotrack"));
            k.log(e);
            if (e.d("autotrack")) {
                E.$c(e.d("token"), 100, 100) ? E.ed() ? (E.T(e), k.log("Enable autotrack!")) : (e.__autotrack_enabled = A, k.log("Disabling Automatic Event Collection because this browser is not supported")) : (e.__autotrack_enabled = A, k.log("Not in active bucket: disabling Automatic Event Collection."));
                try {
                    W(e)
                } catch (i) {
                    k.error(i)
                }
            } else k.log("autotrack disabled");
            !c.c(f) && c.isArray(f) && (e.Ka.call(e.people, f.people), e.Ka(f));
            return e
        }

        function p() {
        }

        function h() {
        }

        function o(a) {
            this.props = {};
            this.Cb = A;
            this.name = a.persistence_name ? "f_" + a.persistence_name : "f_" + a.token + "_fap";
            var b = a.persistence;
            if ("cookie" !== b && "localStorage" !== b) k.ca("Unknown persistence type " + b + "; falling back to cookie"), b = a.persistence = "cookie";
            if (b = "localStorage" === b) {
                b = n;
                try {
                    c.localStorage.set("__mplssupport__", "xyz"), "xyz" !== c.localStorage.get("__mplssupport__") && (b = A), c.localStorage.remove("__mplssupport__")
                } catch (d) {
                    b = A
                }
                b || k.error("localStorage unsupported; falling back to cookie store")
            }
            this.u =
                b ? c.localStorage : c.cookie;
            this.load();
            this.ac(a);
            this.Gd(a);
            this.save()
        }

        function J() {
            this.Sb = "submit"
        }

        function F() {
            this.Sb = "click"
        }

        function x() {
        }

        var z = A, w;
        w = "undefined" === typeof window ? {navigator: {}} : window;
        var N = Array.prototype, T = Object.prototype, G = N.slice, H = T.toString, K = T.hasOwnProperty, u = w.console,
            C = w.navigator, v = w.document, t = C.userAgent, O = Function.prototype.bind, U = N.forEach, V = N.indexOf;
        w = Array.isArray;
        var P = {}, c = {
            trim: function (a) {
                return a.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, "")
            }
        }, k = {
            log: function () {
                if (z &&
                    !c.c(u) && u) try {
                    u.log.apply(u, arguments)
                } catch (a) {
                    c.a(arguments, function (a) {
                        u.log(a)
                    })
                }
            }, error: function () {
                if (z && !c.c(u) && u) {
                    var a = ["FAP error:"].concat(c.ka(arguments));
                    try {
                        u.error.apply(u, a)
                    } catch (b) {
                        c.a(a, function (a) {
                            u.error(a)
                        })
                    }
                }
            }, ca: function () {
                if (!c.c(u) && u) {
                    var a = ["FAP error:"].concat(c.ka(arguments));
                    try {
                        u.error.apply(u, a)
                    } catch (b) {
                        c.a(a, function (a) {
                            u.error(a)
                        })
                    }
                }
            }
        };
        c.bind = function (a, b) {
            var d, e;
            if (O && a.bind === O) return O.apply(a, G.call(arguments, 1));
            if (!c.ab(a)) throw new TypeError;
            d = G.call(arguments,
                2);
            return e = function () {
                if (!(this instanceof e)) return a.apply(b, d.concat(G.call(arguments)));
                var c = {};
                c.prototype = a.prototype;
                var i = new c;
                c.prototype = r;
                c = a.apply(i, d.concat(G.call(arguments)));
                return Object(c) === c ? c : i
            }
        };
        c.Ab = function (a) {
            for (var b in a) "function" === typeof a[b] && (a[b] = c.bind(a[b], a))
        };
        c.a = function (a, b, d) {
            if (!(a === r || a === m)) if (U && a.forEach === U) a.forEach(b, d); else if (a.length === +a.length) for (var c = 0, f = a.length; c < f && !(c in a && b.call(d, a[c], c, a) === P); c++) ; else for (c in a) if (K.call(a, c) &&
                b.call(d, a[c], c, a) === P) break
        };
        c.K = function (a) {
            a && c.bb(a) && (a = a.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;"));
            return a
        };
        c.extend = function (a) {
            c.a(G.call(arguments, 1), function (b) {
                for (var d in b) b[d] !== m && (a[d] = b[d])
            });
            return a
        };
        c.Od = function () {
            c.a()
        };
        c.isArray = w || function (a) {
            return "[object Array]" === H.call(a)
        };
        c.ab = function (a) {
            try {
                return /^\s*\bfunction\b/.test(a)
            } catch (b) {
                return A
            }
        };
        c.dd = function (a) {
            return !(!a || !K.call(a, "callee"))
        };
        c.ka =
            function (a) {
                return !a ? [] : a.ka ? a.ka() : c.isArray(a) || c.dd(a) ? G.call(a) : c.Id(a)
            };
        c.Id = function (a) {
            var b = [];
            if (a === r) return b;
            c.a(a, function (a) {
                b[b.length] = a
            });
            return b
        };
        c.Pd = function (a) {
            return a
        };
        c.Kb = function (a, b) {
            var d = A;
            if (a === r) return d;
            if (V && a.indexOf === V) return -1 != a.indexOf(b);
            c.a(a, function (a) {
                if (d || (d = a === b)) return P
            });
            return d
        };
        c.g = function (a, b) {
            return -1 !== a.indexOf(b)
        };
        c.Mb = function (a, b) {
            a.prototype = new b;
            a.Ad = b.prototype
        };
        c.j = function (a) {
            return a === Object(a) && !c.isArray(a)
        };
        c.U = function (a) {
            if (c.j(a)) {
                for (var b in a) if (K.call(a,
                    b)) return A;
                return n
            }
            return A
        };
        c.c = function (a) {
            return a === m
        };
        c.bb = function (a) {
            return "[object String]" == H.call(a)
        };
        c.fd = function (a) {
            return "[object Date]" == H.call(a)
        };
        c.hd = function (a) {
            return "[object Number]" == H.call(a)
        };
        c.gd = function (a) {
            return !!(a && 1 === a.nodeType)
        };
        c.Gb = function (a) {
            c.a(a, function (b, d) {
                c.fd(b) ? a[d] = c.ad(b) : c.j(b) && (a[d] = c.Gb(b))
            });
            return a
        };
        c.timestamp = function () {
            Date.now = Date.now || function () {
                return +new Date
            };
            return Date.now()
        };
        c.ad = function (a) {
            function b(a) {
                return 10 > a ? "0" + a : a
            }

            return a.getUTCFullYear() +
                "-" + b(a.getUTCMonth() + 1) + "-" + b(a.getUTCDate()) + "T" + b(a.getUTCHours()) + ":" + b(a.getUTCMinutes()) + ":" + b(a.getUTCSeconds())
        };
        c.l = function (a) {
            return function () {
                try {
                    return a.apply(this, arguments)
                } catch (b) {
                    k.ca("Implementation error. Please contact fap@rever.com.")
                }
            }
        };
        c.pd = function (a) {
            for (var b = ["identify", "_check_and_handle_notifications", "_show_notification"], d = 0; d < b.length; d++) a.prototype[b[d]] = c.l(a.prototype[b[d]])
        };
        c.qd = function (a) {
            for (var b in a) "function" === typeof a[b] && (a[b] = c.l(a[b]))
        };
        c.za = function (a) {
            var b =
                {};
            c.a(a, function (a, e) {
                c.bb(a) && 0 < a.length && (b[e] = a)
            });
            return b
        };
        c.truncate = function (a, b) {
            var d;
            "string" === typeof a ? d = a.slice(0, b) : c.isArray(a) ? (d = [], c.a(a, function (a) {
                d.push(c.truncate(a, b))
            })) : c.j(a) ? (d = {}, c.a(a, function (a, f) {
                d[f] = c.truncate(a, b)
            })) : d = a;
            return d
        };
        c.oa = function () {
            return function (a) {
                function b(a, f) {
                    var i = "", l = 0, j = l = "", j = 0, g = i, h = [], q = f[a];
                    q && "object" === typeof q && "function" === typeof q.toJSON && (q = q.toJSON(a));
                    switch (typeof q) {
                        case "string":
                            return c(q);
                        case "number":
                            return isFinite(q) ?
                                "" + q : "null";
                        case "boolean":
                        case "null":
                            return "" + q;
                        case "object":
                            if (!q) return "null";
                            i += "    ";
                            h = [];
                            if ("[object Array]" === H.apply(q)) {
                                j = q.length;
                                for (l = 0; l < j; l += 1) h[l] = b(l, q) || "null";
                                return j = 0 === h.length ? "[]" : i ? "[\n" + i + h.join(",\n" + i) + "\n" + g + "]" : "[" + h.join(",") + "]"
                            }
                            for (l in q) K.call(q, l) && (j = b(l, q)) && h.push(c(l) + (i ? ": " : ":") + j);
                            return j = 0 === h.length ? "{}" : i ? "{" + h.join(",") + "" + g + "}" : "{" + h.join(",") + "}"
                    }
                }

                function c(a) {
                    var b = /[\\"\x00-\x1f\x7f-\x9f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,
                        d = {
                            "\u0008": "\\b",
                            "\t": "\\t",
                            "\n": "\\n",
                            "\u000c": "\\f",
                            "\r": "\\r",
                            '"': '\\"',
                            "\\": "\\\\"
                        };
                    b.lastIndex = 0;
                    return b.test(a) ? '"' + a.replace(b, function (a) {
                        var b = d[a];
                        return "string" === typeof b ? b : "\\u" + ("0000" + a.charCodeAt(0).toString(16)).slice(-4)
                    }) + '"' : '"' + a + '"'
                }

                return b("", {"": a})
            }
        }();
        c.na = function () {
            function a() {
                switch (j) {
                    case "t":
                        return f("t"), f("r"), f("u"), f("e"), n;
                    case "f":
                        return f("f"), f("a"), f("l"), f("s"), f("e"), A;
                    case "n":
                        return f("n"), f("u"), f("l"), f("l"), r
                }
                i('Unexpected "' + j + '"')
            }

            function b() {
                for (; j &&
                       " " >= j;) f()
            }

            function c() {
                var a, b, d = "", e;
                if ('"' === j) for (; f();) {
                    if ('"' === j) return f(), d;
                    if ("\\" === j) if (f(), "u" === j) {
                        for (b = e = 0; 4 > b; b += 1) {
                            a = parseInt(f(), 16);
                            if (!isFinite(a)) break;
                            e = 16 * e + a
                        }
                        d += String.fromCharCode(e)
                    } else if ("string" === typeof g[j]) d += g[j]; else break; else d += j
                }
                i("Bad string")
            }

            function e() {
                var a;
                a = "";
                "-" === j && (a = "-", f("-"));
                for (; "0" <= j && "9" >= j;) a += j, f();
                if ("." === j) for (a += "."; f() && "0" <= j && "9" >= j;) a += j;
                if ("e" === j || "E" === j) {
                    a += j;
                    f();
                    if ("-" === j || "+" === j) a += j, f();
                    for (; "0" <= j && "9" >= j;) a += j, f()
                }
                a =
                    +a;
                if (isFinite(a)) return a;
                i("Bad number")
            }

            function f(a) {
                a && a !== j && i("Expected '" + a + "' instead of '" + j + "'");
                j = h.charAt(l);
                l += 1;
                return j
            }

            function i(a) {
                throw{name: "SyntaxError", message: a, Md: l, text: h};
            }

            var l, j, g = {'"': '"', "\\": "\\", "/": "/", b: "\u0008", f: "\u000c", n: "\n", r: "\r", t: "\t"}, h, q;
            q = function () {
                b();
                switch (j) {
                    case "{":
                        var l;
                        a:{
                            var g, h = {};
                            if ("{" === j) {
                                f("{");
                                b();
                                if ("}" === j) {
                                    f("}");
                                    l = h;
                                    break a
                                }
                                for (; j;) {
                                    g = c();
                                    b();
                                    f(":");
                                    Object.hasOwnProperty.call(h, g) && i('Duplicate key "' + g + '"');
                                    h[g] = q();
                                    b();
                                    if ("}" ===
                                        j) {
                                        f("}");
                                        l = h;
                                        break a
                                    }
                                    f(",");
                                    b()
                                }
                            }
                            i("Bad object")
                        }
                        return l;
                    case "[":
                        a:{
                            l = [];
                            if ("[" === j) {
                                f("[");
                                b();
                                if ("]" === j) {
                                    f("]");
                                    g = l;
                                    break a
                                }
                                for (; j;) {
                                    l.push(q());
                                    b();
                                    if ("]" === j) {
                                        f("]");
                                        g = l;
                                        break a
                                    }
                                    f(",");
                                    b()
                                }
                            }
                            i("Bad array")
                        }
                        return g;
                    case '"':
                        return c();
                    case "-":
                        return e();
                    default:
                        return "0" <= j && "9" >= j ? e() : a()
                }
            };
            return function (a) {
                h = a;
                l = 0;
                j = " ";
                a = q();
                b();
                j && i("Syntax error");
                return a
            }
        }();
        c.yb = function (a) {
            var b, d, e, f, i = 0, l = 0, j = "", j = [];
            if (!a) return a;
            a = c.Hd(a);
            do b = a.charCodeAt(i++), d = a.charCodeAt(i++), e = a.charCodeAt(i++),
                f = b << 16 | d << 8 | e, b = f >> 18 & 63, d = f >> 12 & 63, e = f >> 6 & 63, f &= 63, j[l++] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".charAt(b) + "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".charAt(d) + "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".charAt(e) + "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=".charAt(f); while (i < a.length);
            j = j.join("");
            switch (a.length % 3) {
                case 1:
                    j = j.slice(0, -2) + "==";
                    break;
                case 2:
                    j = j.slice(0, -1) + "="
            }
            return j
        };
        c.Hd = function (a) {
            var a =
                (a + "").replace(/\r\n/g, "\n").replace(/\r/g, "\n"), b = "", c, e, f = 0, i;
            c = e = 0;
            f = a.length;
            for (i = 0; i < f; i++) {
                var l = a.charCodeAt(i), j = r;
                128 > l ? e++ : j = 127 < l && 2048 > l ? String.fromCharCode(l >> 6 | 192, l & 63 | 128) : String.fromCharCode(l >> 12 | 224, l >> 6 & 63 | 128, l & 63 | 128);
                j !== r && (e > c && (b += a.substring(c, e)), b += j, c = e = i + 1)
            }
            e > c && (b += a.substring(c, a.length));
            return b
        };
        c.N = function () {
            function a() {
                function a(b, c) {
                    var d, e = 0;
                    for (d = 0; d < c.length; d++) e |= i[d] << 8 * d;
                    return b ^ e
                }

                var b, c, i = [], l = 0;
                for (b = 0; b < t.length; b++) c = t.charCodeAt(b), i.unshift(c &
                    255), 4 <= i.length && (l = a(l, i), i = []);
                0 < i.length && (l = a(l, i));
                return l.toString(16)
            }

            function b() {
                for (var a = 1 * new Date, b = 0; a == 1 * new Date;) b++;
                return a.toString(16) + b.toString(16)
            }

            return function () {
                var c = (screen.height * screen.width).toString(16);
                return b() + "-" + Math.random().toString(16).replace(".", "") + "-" + a() + "-" + c + "-" + b()
            }
        }();
        c.Nb = function (a) {
            return /(google web preview|baiduspider|yandexbot|bingbot|googlebot|yahoo! slurp)/i.test(a) ? n : A
        };
        c.gc = function (a) {
            var b, d, e, f = [];
            c.c(b) && (b = "&");
            c.a(a, function (a,
                             b) {
                d = encodeURIComponent(a.toString());
                e = encodeURIComponent(b);
                f[f.length] = e + "=" + d
            });
            return f.join(b)
        };
        c.Hb = function (a, b) {
            var b = b.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]"), c = RegExp("[\\?&]" + b + "=([^&#]*)").exec(a);
            return c === r || c && "string" !== typeof c[1] && c[1].length ? "" : decodeURIComponent(c[1]).replace(/\+/g, " ")
        };
        c.ea = function (a, b) {
            var c = a.match(RegExp(b + "=([^&]*)"));
            return c ? c[1] : r
        };
        c.cookie = {
            get: function (a) {
                for (var a = a + "=", b = v.cookie.split(";"), c = 0; c < b.length; c++) {
                    for (var e = b[c]; " " == e.charAt(0);) e =
                        e.substring(1, e.length);
                    if (0 === e.indexOf(a)) return decodeURIComponent(e.substring(a.length, e.length))
                }
                return r
            }, parse: function (a) {
                var b;
                try {
                    b = c.na(c.cookie.get(a)) || {}
                } catch (d) {
                }
                return b
            }, wd: function (a, b, c, e, f) {
                var d;
                var i = "", l = "", j = "";
                e && (d = (i = (i = v.location.hostname.match(/[a-z0-9][a-z0-9\-]+\.[a-z\.]{2,6}$/i)) ? i[0] : "") ? "; domain=." + i : "", i = d);
                c && (l = new Date, l.setTime(l.getTime() + 1E3 * c), l = "; expires=" + l.toGMTString());
                f && (j = "; secure");
                v.cookie = a + "=" + encodeURIComponent(b) + l + "; path=/" + i + j
            }, set: function (a,
                              b, c, e, f) {
                var d;
                var i = "", l = "", j = "";
                e && (d = (i = (i = v.location.hostname.match(/[a-z0-9][a-z0-9\-]+\.[a-z\.]{2,6}$/i)) ? i[0] : "") ? "; domain=." + i : "", i = d);
                c && (l = new Date, l.setTime(l.getTime() + 864E5 * c), l = "; expires=" + l.toGMTString());
                f && (j = "; secure");
                a = a + "=" + encodeURIComponent(b) + l + "; path=/" + i + j;
                return v.cookie = a
            }, remove: function (a, b) {
                c.cookie.set(a, "", -1, b)
            }
        };
        c.localStorage = {
            error: function (a) {
                k.error("localStorage error: " + a)
            }, get: function (a) {
                try {
                    return window.localStorage.getItem(a)
                } catch (b) {
                    c.localStorage.error(b)
                }
                return r
            },
            parse: function (a) {
                try {
                    return c.na(c.localStorage.get(a)) || {}
                } catch (b) {
                }
                return r
            }, set: function (a, b) {
                try {
                    window.localStorage.setItem(a, b)
                } catch (d) {
                    c.localStorage.error(d)
                }
            }, remove: function (a) {
                try {
                    window.localStorage.removeItem(a)
                } catch (b) {
                    c.localStorage.error(b)
                }
            }
        };
        c.o = function () {
            function a(a, e, f) {
                return function (i) {
                    if (i = i || b(window.event)) {
                        var l = n, j;
                        c.ab(f) && (j = f(i));
                        i = e.call(a, i);
                        if (A === j || A === i) l = A;
                        return l
                    }
                }
            }

            function b(a) {
                if (a) a.preventDefault = b.preventDefault, a.stopPropagation = b.stopPropagation;
                return a
            }

            b.preventDefault = function () {
                this.returnValue = A
            };
            b.stopPropagation = function () {
                this.cancelBubble = n
            };
            return function (b, c, f, i, l) {
                b ? b.addEventListener && !i ? b.addEventListener(c, f, !!l) : (c = "on" + c, b[c] = a(b, f, b[c])) : k.error("No valid element provided to register_event")
            }
        }();
        c.Yc = function () {
            function a(a, b) {
                return 0 <= (" " + a.className + " ").replace(d, " ").indexOf(" " + b + " ")
            }

            function b(b) {
                if (!v.getElementsByTagName) return [];
                var b = b.split(" "), d, i, l, j, g, h, q, k = [v];
                for (j = 0; j < b.length; j++) if (d = b[j].replace(/^\s+/,
                    "").replace(/\s+$/, ""), -1 < d.indexOf("#")) {
                    i = d.split("#");
                    d = i[0];
                    k = v.getElementById(i[1]);
                    if (!k || d && k.nodeName.toLowerCase() != d) return [];
                    k = [k]
                } else if (-1 < d.indexOf(".")) {
                    i = d.split(".");
                    d = i[0];
                    var o = i[1];
                    d || (d = "*");
                    i = [];
                    for (g = l = 0; g < k.length; g++) {
                        q = "*" == d ? k[g].all ? k[g].all : k[g].getElementsByTagName("*") : k[g].getElementsByTagName(d);
                        for (h = 0; h < q.length; h++) i[l++] = q[h]
                    }
                    k = [];
                    for (g = d = 0; g < i.length; g++) i[g].className && c.bb(i[g].className) && a(i[g], o) && (k[d++] = i[g])
                } else if (i = d.match(/^(\w*)\[(\w+)([=~\|\^\$\*]?)=?"?([^\]"]*)"?\]$/)) {
                    d =
                        i[1];
                    var p = i[2], o = i[3], D = i[4];
                    d || (d = "*");
                    i = [];
                    for (g = l = 0; g < k.length; g++) {
                        q = "*" == d ? k[g].all ? k[g].all : k[g].getElementsByTagName("*") : k[g].getElementsByTagName(d);
                        for (h = 0; h < q.length; h++) i[l++] = q[h]
                    }
                    k = [];
                    d = 0;
                    switch (o) {
                        case "=":
                            o = function (a) {
                                return a.getAttribute(p) == D
                            };
                            break;
                        case "~":
                            o = function (a) {
                                return a.getAttribute(p).match(RegExp("\\b" + D + "\\b"))
                            };
                            break;
                        case "|":
                            o = function (a) {
                                return a.getAttribute(p).match(RegExp("^" + D + "-?"))
                            };
                            break;
                        case "^":
                            o = function (a) {
                                return 0 === a.getAttribute(p).indexOf(D)
                            };
                            break;
                        case "$":
                            o = function (a) {
                                return a.getAttribute(p).lastIndexOf(D) == a.getAttribute(p).length - D.length
                            };
                            break;
                        case "*":
                            o = function (a) {
                                return -1 < a.getAttribute(p).indexOf(D)
                            };
                            break;
                        default:
                            o = function (a) {
                                return a.getAttribute(p)
                            }
                    }
                    k = [];
                    for (g = d = 0; g < i.length; g++) o(i[g]) && (k[d++] = i[g])
                } else {
                    i = [];
                    for (g = l = 0; g < k.length; g++) {
                        q = k[g].getElementsByTagName(d);
                        for (h = 0; h < q.length; h++) i[l++] = q[h]
                    }
                    k = i
                }
                return k
            }

            var d = /[\t\r\n]/g;
            return function (a) {
                return c.gd(a) ? [a] : c.j(a) && !c.c(a.length) ? a : b.call(this, a)
            }
        }();
        c.info = {
            Qc: function () {
                var a =
                    "", b = {};
                c.a("utm_source utm_medium utm_campaign utm_content utm_term".split(" "), function (d) {
                    a = c.Hb(v.URL, d);
                    a.length && (b[d] = a)
                });
                return b
            }, rd: function (a) {
                return 0 === a.search("https?://(.*)google.([^/?]*)") ? "google" : 0 === a.search("https?://(.*)bing.com") ? "bing" : 0 === a.search("https?://(.*)yahoo.com") ? "yahoo" : 0 === a.search("https?://(.*)duckduckgo.com") ? "duckduckgo" : r
            }, sd: function (a) {
                var b = c.info.rd(a), d = {};
                if (b !== r) d.$search_engine = b, a = c.Hb(a, "yahoo" != b ? "q" : "p"), a.length && (d.fap_keyword = a);
                return d
            },
            ba: function (a, b, d) {
                return d || c.g(a, " OPR/") ? c.g(a, "Mini") ? "Opera Mini" : "Opera" : /(BlackBerry|PlayBook|BB10)/i.test(a) ? "BlackBerry" : c.g(a, "IEMobile") || c.g(a, "WPDesktop") ? "Internet Explorer Mobile" : c.g(a, "Edge") ? "Microsoft Edge" : c.g(a, "FBIOS") ? "Facebook Mobile" : c.g(a, "Chrome") ? "Chrome" : c.g(a, "CriOS") ? "Chrome iOS" : c.g(a, "FxiOS") ? "Firefox iOS" : c.g(b || "", "Apple") ? c.g(a, "Mobile") ? "Mobile Safari" : "Safari" : c.g(a, "Android") ? "Android Mobile" : c.g(a, "Konqueror") ? "Konqueror" : c.g(a, "Firefox") ? "Firefox" : c.g(a, "MSIE") ||
                c.g(a, "Trident/") ? "Internet Explorer" : c.g(a, "Gecko") ? "Mozilla" : ""
            }, Bb: function (a, b, d) {
                b = {
                    "Internet Explorer Mobile": /rv:(\d+(\.\d+)?)/,
                    "Microsoft Edge": /Edge\/(\d+(\.\d+)?)/,
                    Chrome: /Chrome\/(\d+(\.\d+)?)/,
                    "Chrome iOS": /CriOS\/(\d+(\.\d+)?)/,
                    Safari: /Version\/(\d+(\.\d+)?)/,
                    "Mobile Safari": /Version\/(\d+(\.\d+)?)/,
                    Opera: /(Opera|OPR)\/(\d+(\.\d+)?)/,
                    Firefox: /Firefox\/(\d+(\.\d+)?)/,
                    "Firefox iOS": /FxiOS\/(\d+(\.\d+)?)/,
                    Konqueror: /Konqueror:(\d+(\.\d+)?)/,
                    BlackBerry: /BlackBerry (\d+(\.\d+)?)/,
                    "Android Mobile": /android\s(\d+(\.\d+)?)/,
                    "Internet Explorer": /(rv:|MSIE )(\d+(\.\d+)?)/,
                    Mozilla: /rv:(\d+(\.\d+)?)/
                }[c.info.ba(a, b, d)];
                if (b === m) return r;
                a = a.match(b);
                return !a ? r : parseFloat(a[a.length - 2])
            }, fb: function () {
                return /Windows/i.test(t) ? /Phone/.test(t) || /WPDesktop/.test(t) ? "Windows Phone" : "Windows" : /(iPhone|iPad|iPod)/.test(t) ? "iOS" : /Android/.test(t) ? "Android" : /(BlackBerry|PlayBook|BB10)/i.test(t) ? "BlackBerry" : /Mac/i.test(t) ? "Mac OS X" : /Linux/.test(t) ? "Linux" : ""
            }, Fb: function (a) {
                return /Windows Phone/i.test(a) || /WPDesktop/.test(a) ? "Windows Phone" :
                    /iPad/.test(a) ? "iPad" : /iPod/.test(a) ? "iPod Touch" : /iPhone/.test(a) ? "iPhone" : /(BlackBerry|PlayBook|BB10)/i.test(a) ? "BlackBerry" : /Android/.test(a) ? "Android" : ""
            }, nd: function (a) {
                a = a.split("/");
                return 3 <= a.length ? a[2] : ""
            }, ia: function () {
                return c.extend(c.za({
                    $os: c.info.fb(),
                    $browser: c.info.ba(t, C.vendor, window.opera),
                    $referrer: v.referrer,
                    $device: c.info.Fb(t)
                }), {
                    $current_url: window.location.href,
                    $browser_version: c.info.Bb(t, C.vendor, window.opera),
                    $screen_height: screen.height,
                    $screen_width: screen.width,
                    $title: v.title,
                    $user_agent: C.userAgent,
                    $timestamp: (new Date).getTime()
                })
            }, md: function () {
                return c.extend(c.za({
                    $os: c.info.fb(),
                    $browser: c.info.ba(t, C.vendor, window.opera)
                }), {$browser_version: c.info.Bb(t, C.vendor, window.opera)})
            }, ld: function (a) {
                return c.za({
                    fap_page: a,
                    fap_referrer: v.referrer,
                    fap_browser: c.info.ba(t, C.vendor, window.opera),
                    fap_platform: c.info.fb()
                })
            }
        };
        c.toArray = c.ka;
        c.isObject = c.j;
        c.JSONEncode = c.oa;
        c.JSONDecode = c.na;
        c.isBlockedUA = c.Nb;
        c.isEmptyObject = c.U;
        c.info = c.info;
        c.info.device = c.info.Fb;
        c.info.browser =
            c.info.ba;
        c.info.properties = c.info.ia;
        c.UUID = c.N;
        var E = {
            rb: [], Gc: function (a) {
                if (a.previousElementSibling) return a.previousElementSibling;
                do a = a.previousSibling; while (a && 1 !== a.nodeType);
                return a
            }, Dc: function (a, b) {
                var c = document.createElement("script");
                c.type = "text/javascript";
                c.src = a;
                c.onload = b;
                var e = document.getElementsByTagName("script");
                0 < e.length ? e[0].parentNode.insertBefore(c, e[0]) : document.body.appendChild(c)
            }, ra: function (a) {
                switch (typeof a.className) {
                    case "string":
                        return a.className;
                    case "object":
                        return a.className.Nd ||
                            a.getAttribute("class") || "";
                    default:
                        return ""
                }
            }, wc: function (a) {
                var b = {classes: this.ra(a).split(" "), tag_name: a.tagName.toLowerCase()};
                if (c.g(["input", "select", "textarea"], a.tagName.toLowerCase())) {
                    var d = this.ob(a);
                    this.Ma(a, d) && (b.value = d)
                }
                c.a(a.attributes, function (a) {
                    b["attr__" + a.name] = a.value
                });
                for (var e = d = 1, f = a; f = this.Gc(f);) d++, f.tagName === a.tagName && e++;
                b.nth_child = d;
                b.nth_of_type = e;
                return b
            }, Oa: function (a, b) {
                return a && a.tagName && a.tagName.toLowerCase() === b.toLowerCase()
            }, Ic: function (a, b) {
                if (!a ||
                    this.Oa(a, "html") || 1 !== a.nodeType) return A;
                switch (a.tagName.toLowerCase()) {
                    case "html":
                    case "div":
                        return A;
                    case "form":
                        return "submit" === b.type;
                    case "input":
                        return -1 === ["button", "submit"].indexOf(a.getAttribute("type")) ? "change" === b.type : "click" === b.type;
                    case "select":
                    case "textarea":
                        return "change" === b.type;
                    default:
                        return "click" === b.type
                }
            }, nb: function (a) {
                return {
                    $event_type: a,
                    $ce_version: 1,
                    $host: window.location.host,
                    $pathname: window.location.pathname
                }
            }, vc: function (a) {
                var b = r;
                switch (a.type.toLowerCase()) {
                    case "checkbox":
                        a.checked &&
                        (b = [a.value]);
                        break;
                    case "radio":
                        if (a.checked) b = a.value;
                        break;
                    default:
                        b = a.value
                }
                return b
            }, xc: function (a) {
                if (a.multiple) {
                    var b = [];
                    c.a(a.querySelectorAll("[selected]"), function (a) {
                        b.push(a.value)
                    });
                    a = b
                } else a = a.value;
                return a
            }, Ma: function (a, b) {
                for (var d = a; d.parentNode && !this.Oa(d, "body"); d = d.parentNode) {
                    var e = this.ra(d).split(" ");
                    if (c.g(e, "mp-sensitive") || c.g(e, "mp-no-track")) return A
                }
                if (c.g(this.ra(a).split(" "), "mp-include")) return n;
                if (b === r) return A;
                switch ((a.type || "").toLowerCase()) {
                    case "hidden":
                        return A;
                    case "password":
                        return A
                }
                return /^cc|cardnum|ccnum|creditcard|csc|cvc|cvv|exp|pass|seccode|securitycode|securitynum|socialsec|socsec|ssn/i.test((a.name || a.id || "").replace(/[^a-zA-Z0-9]/g, "")) || "string" === typeof b && (/^(?:(4[0-9]{12}(?:[0-9]{3})?)|(5[1-5][0-9]{14})|(6(?:011|5[0-9]{2})[0-9]{12})|(3[47][0-9]{13})|(3(?:0[0-5]|[68][0-9])[0-9]{11})|((?:2131|1800|35[0-9]{3})[0-9]{11}))$/.test((b || "").replace(/[\- ]/g, "")) || /(^\d{3}-?\d{2}-?\d{4}$)/.test(b)) ? A : n
            }, ob: function (a) {
                var b;
                switch (a.tagName.toLowerCase()) {
                    case "input":
                        b =
                            this.vc(a);
                        break;
                    case "select":
                        b = this.xc(a);
                        break;
                    default:
                        b = a.value || a.textContent
                }
                return this.Ma(a, b) ? b : r
            }, uc: function (a) {
                var b = {};
                c.a(a.elements, function (a) {
                    var c = a.getAttribute("name") || a.getAttribute("id");
                    if (c !== r) {
                        var c = "$form_field__" + c, f = this.ob(a);
                        this.Ma(a, f) && (a = b[c], b[c] = a !== m ? [].concat(a, f) : f)
                    }
                }, this);
                return b
            }, qc: function (a) {
                var b = [];
                c.a(document.querySelectorAll(a.css_selector), function (a) {
                    -1 < ["input", "select"].indexOf(a.tagName.toLowerCase()) ? b.push(a.value) : a.textContent && b.push(a.textContent)
                });
                return b.join(", ")
            }, sc: function (a) {
                var b = {};
                c.a(this.kb, function (d) {
                    c.a(d.event_selectors, function (e) {
                        e = document.querySelectorAll(e);
                        c.a(e, function (e) {
                            c.g(a, e) && (b[d.name] = this.qc(d))
                        }, this)
                    }, this)
                }, this);
                return b
            }, Rc: function (a) {
                a = parseInt(a.getResponseHeader("X-MP-CE-Backoff"));
                if (!isNaN(a) && 0 < a) {
                    var b = c.timestamp() + 1E3 * a;
                    console.log("disabling CE for " + a + " seconds (from " + c.timestamp() + " until " + b + ")");
                    c.cookie.wd("__mpced", n, a, n)
                }
            }, tc: function (a) {
                return "undefined" === typeof a.target ? a.srcElement :
                    a.target
            }, Lc: function (a, b) {
                var d = this.tc(a);
                if (3 === d.nodeType) d = d.parentNode;
                if (this.Ic(d, a)) {
                    for (var e = [d]; d.parentNode && !this.Oa(d, "body");) e.push(d.parentNode), d = d.parentNode;
                    var f = [], i, g, j, h = A, k = "", q = "";
                    c.a(e, function (a, b) {
                        "a" === a.tagName.toLowerCase() ? i = a.getAttribute("href") : "form" === a.tagName.toLowerCase() && (j = a);
                        if (!g && 5 > b && a.textContent) {
                            var d = c.trim(a.textContent);
                            d && (g = d.replace(/[\r\n]/g, " ").replace(/[ ]+/g, " ").substring(0, 255))
                        }
                        d = this.ra(a).split(" ");
                        c.g(d, "mp-no-track") && (h = n);
                        k =
                            a.id || m;
                        q = a.name || m;
                        f.push(this.wc(a))
                    }, this);
                    if (h) return A;
                    e = c.extend(this.nb(a.type), {$el_attr__href: i, $el_text: g, $el_id: k, $el_name: q}, this.sc(e));
                    j && ("submit" === a.type || "click" === a.type) && c.extend(e, this.uc(j));
                    b.I("auto_track", e);
                    return n
                }
            }, Ld: function (a) {
                window.location.href = a
            }, kc: function (a) {
                var b = c.bind(function (b) {
                    c.cookie.parse("__mpced") !== n && (b = b || window.event, this.Lc(b, a))
                }, this);
                c.o(document, "submit", b, A, n);
                c.o(document, "change", b, A, n);
                c.o(document, "click", b, A, n)
            }, kb: {}, T: function (a) {
                console.log("Init autotrack!");
                if (!document || !document.body) {
                    console.log("document not ready yet, trying again in 500 milliseconds...");
                    var b = this;
                    setTimeout(function () {
                        b.T(a)
                    }, 500)
                } else {
                    var d = a.d("token");
                    -1 < this.rb.indexOf(d) ? console.log('autotrack already initialized for token "' + d + '"') : (this.rb.push(d), this.Ec(a) || c.bind(function (b) {
                        if (b.custom_properties) this.kb = b.custom_properties;
                        a.I("$web_event", c.extend({}, this.nb("pageview")));
                        this.kc(a)
                    }, this)({}))
                }
            }, mb: function (a, b) {
                var d;
                try {
                    var e = c.ea(b, "state"), e = JSON.parse(decodeURIComponent(e)),
                        f = c.ea(b, "expires_in");
                    d = {
                        accessToken: c.ea(b, "access_token"),
                        accessTokenExpiresAt: (new Date).getTime() + 1E3 * Number(f),
                        bookmarkletMode: !!e.bookmarkletMode,
                        projectId: e.projectId,
                        projectOwnerId: e.projectOwnerId,
                        projectToken: e.token,
                        readOnly: e.readOnly,
                        userFlags: e.userFlags,
                        userId: e.userId
                    };
                    window.sessionStorage.setItem("editorParams", JSON.stringify(d));
                    e.desiredHash ? window.location.hash = e.desiredHash : window.history ? history.replaceState("", document.title, window.location.pathname + window.location.search) :
                        window.location.hash = ""
                } catch (i) {
                    console.error("Unable to parse data from hash", i)
                }
                return d
            }, Ec: function (a) {
                var b = A;
                c.ea(window.location.hash, "state") && (b = c.ea(window.location.hash, "state"), b = JSON.parse(decodeURIComponent(b)), b = "mpeditor" === b.action);
                var d = !!window.sessionStorage.getItem("_mpcehash");
                b ? b = this.mb(a, window.location.hash) : d ? (b = this.mb(a, window.sessionStorage.getItem("_mpcehash")), window.sessionStorage.removeItem("_mpcehash")) : b = JSON.parse(window.sessionStorage.getItem("editorParams") ||
                    "{}");
                return b.projectToken && a.d("token") === b.projectToken ? (this.Cc(a, b), n) : A
            }, lb: A, Cc: function (a, b) {
                if (!this.lb) {
                    this.lb = n;
                    var c = "?_ts=" + (new Date).getTime(), e = a.d("app_host") + "/site_media";
                    this.Dc(z ? e + "/compiled/reports/collect-everything/editor.js" + c : e + "/bundle-webpack/reports/collect-everything/editor.min.js" + c, function () {
                        window.mp_load_editor(b)
                    });
                    return n
                }
                return A
            }, $c: function (a, b, d) {
                for (var b = !c.c(b) ? b : 10, d = !c.c(d) ? d : 10, e = 0, f = 0; f < a.length; f++) e += a.charCodeAt(f);
                return e % b < d
            }, ed: function () {
                return c.ab(document.querySelectorAll)
            }
        };
        c.Ab(E);
        c.qd(E);
        var M, s, $ = "__faps,__fapso,__fapa,__fapap,__fapu,$people_distinct_id,__alias,__cmpns,__timers".split(",");
        w = "https:" === document.location.protocol ? "https://" : "http://";
        var L = window.XMLHttpRequest && "withCredentials" in new XMLHttpRequest,
            S = !L && -1 === t.indexOf("MSIE") && -1 === t.indexOf("Mozilla"), Q = {
                api_host: w + "client.thegioinhaphovietnam.com.vn",
                app_host: w + "client.thegioinhaphovietnam.com.vn",
                autotrack: n,
                cdn: w + "client.thegioinhaphovietnam.com.vn",
                cross_subdomain_cookie: n,
                persistence: "cookie",
                persistence_name: "persistence.thegioinhaphovietnam.com.vn",
                cookie_name: ".thegioinhaphovietnam.com.vn",
                loaded: B(),
                store_google: n,
                save_referrer: n,
                test: A,
                verbose: A,
                img: A,
                track_pageview: n,
                debug: n,
                track_links_timeout: 300,
                cookie_expiration: 365,
                upgrade: A,
                disable_persistence: A,
                disable_cookie: A,
                secure_cookie: A,
                ip: n,
                property_blacklist: []
            };
        Q.decide_host = Q.api_host;
        var R = A;
        x.prototype.wa = B();
        x.prototype.Wa = B();
        x.prototype.Sa = B();
        x.prototype.T = function (a) {
            this.Qb = a;
            return this
        };
        x.prototype.I = function (a, b, d, e) {
            var f = this, i = c.Yc(a);
            if (0 === i.length) k.error("The DOM query (" + a + ") returned 0 elements"); else return c.a(i,
                function (a) {
                    c.o(a, this.Sb, function (a) {
                        var c = {}, i = f.wa(d, this), g = f.Qb.d("track_links_timeout");
                        f.Wa(a, this, c);
                        window.setTimeout(f.Yb(e, i, c, n), g);
                        f.Qb.I(b, i, f.Yb(e, i, c))
                    })
                }, this), n
        };
        x.prototype.Yb = function (a, b, c, e) {
            var e = e || A, f = this;
            return function () {
                if (!c.Pc) c.Pc = n, a && a(e, b) === A || f.Sa(b, c, e)
            }
        };
        x.prototype.wa = function (a, b) {
            return "function" === typeof a ? a(b) : c.extend({}, a)
        };
        c.Mb(F, x);
        F.prototype.wa = function (a, b) {
            var c = F.Ad.wa.apply(this, arguments);
            if (b.href) c.url = b.href;
            return c
        };
        F.prototype.Wa = function (a,
                                   b, c) {
            c.Rb = 2 === a.which || a.metaKey || a.ctrlKey || "_blank" === b.target;
            c.href = b.href;
            c.Rb || a.preventDefault()
        };
        F.prototype.Sa = function (a, b) {
            b.Rb || setTimeout(function () {
                window.location = b.href
            }, 0)
        };
        c.Mb(J, x);
        J.prototype.Wa = function (a, b, c) {
            c.element = b;
            a.preventDefault()
        };
        J.prototype.Sa = function (a, b) {
            setTimeout(function () {
                b.element.submit()
            }, 0)
        };
        o.prototype.ia = function () {
            var a = {};
            c.a(this.props, function (b, d) {
                c.Kb($, d) || (a[d] = b)
            });
            return a
        };
        o.prototype.load = function () {
            if (!this.disabled) {
                var a = this.u.parse(this.name);
                a && (this.props = c.extend({}, a))
            }
        };
        o.prototype.Gd = function (a) {
            var b = a.upgrade, d;
            if (b) d = "fap_super_properties", "string" === typeof b && (d = b), b = this.u.parse(d), this.u.remove(d), this.u.remove(d, n), b && (this.props = c.extend(this.props, b.all, b.events));
            if (!a.cookie_name && "mixpanel" !== a.name && (d = "fap_" + a.token + "_" + a.name, b = this.u.parse(d))) this.u.remove(d), this.u.remove(d, n), this.F(b);
            this.u === c.localStorage && (b = c.cookie.parse(this.name), c.cookie.remove(this.name), c.cookie.remove(this.name, n), b && this.F(b))
        };
        o.prototype.save =
            function () {
                this.disabled || (this.pc(), this.u.set(this.name, c.oa(this.props), this.Xa, this.Ua, this.Tb))
            };
        o.prototype.remove = function () {
            this.u.remove(this.name, A);
            this.u.remove(this.name, n)
        };
        o.prototype.clear = function () {
            this.remove();
            this.props = {}
        };
        o.prototype.F = function (a, b, d) {
            return c.j(a) ? ("undefined" === typeof b && (b = "None"), this.Xa = "undefined" === typeof d ? this.Eb : d, c.a(a, function (a, c) {
                if (!this.props[c] || this.props[c] === b) this.props[c] = a
            }, this), this.save(), n) : A
        };
        o.prototype.ja = function (a, b) {
            return c.j(a) ?
                (this.Xa = "undefined" === typeof b ? this.Eb : b, c.extend(this.props, a), this.save(), n) : A
        };
        o.prototype.Ca = function (a) {
            a in this.props && (delete this.props[a], this.save())
        };
        o.prototype.pc = c.l(function () {
            var a = this.props.__cmpns, b = z ? 6E4 : 36E5;
            if (a) {
                for (var d in a) 1 * new Date - a[d] > b && delete a[d];
                c.U(a) && delete this.props.__cmpns
            }
        });
        o.prototype.Fd = function () {
            if (!this.Cb) this.F(c.info.Qc()), this.Cb = n
        };
        o.prototype.bc = function (a) {
            this.ja(c.info.sd(a))
        };
        o.prototype.ib = function (a) {
            this.F({
                $initial_referrer: a || "$direct",
                $initial_referring_domain: c.info.nd(a) || "$direct"
            }, "")
        };
        o.prototype.cd = function () {
            return c.za({
                $initial_referrer: this.props.$initial_referrer,
                $initial_referring_domain: this.props.$initial_referring_domain
            })
        };
        o.prototype.ac = function (a) {
            this.Eb = this.Xa = a.cookie_expiration;
            this.ud(a.disable_persistence);
            this.td(a.cross_subdomain_cookie);
            this.xd(a.secure_cookie)
        };
        o.prototype.ud = function (a) {
            (this.disabled = a) && this.remove()
        };
        o.prototype.td = function (a) {
            if (a !== this.Ua) this.Ua = a, this.remove(), this.save()
        };
        o.prototype.bd = function () {
            return this.Ua
        };
        o.prototype.xd = function (a) {
            if (a !== this.Tb) this.Tb = a ? n : A, this.remove(), this.save()
        };
        o.prototype.z = function (a, b) {
            var d = this.La(a), e = b[a], f = this.Z("$set"), i = this.Z("$set_once"), g = this.Z("$add"),
                j = this.Z("$union"), h = this.Z("$append", []);
            "__faps" === d ? (c.extend(f, e), this.S("$add", e), this.S("$union", e)) : "__fapso" === d ? c.a(e, function (a, b) {
                b in i || (i[b] = a)
            }) : "__fapa" === d ? c.a(e, function (a, b) {
                b in f ? f[b] += a : (b in g || (g[b] = 0), g[b] += a)
            }, this) : "__fapu" === d ? c.a(e, function (a,
                                                         b) {
                c.isArray(a) && (b in j || (j[b] = []), j[b] = j[b].concat(a))
            }) : "__fapap" === d && h.push(e);
            k.log("FAP PEOPLE REQUEST (QUEUED, PENDING IDENTIFY):");
            k.log(b);
            this.save()
        };
        o.prototype.S = function (a, b) {
            var d = this.R(a);
            c.c(d) || (c.a(b, function (a, b) {
                delete d[b]
            }, this), this.save())
        };
        o.prototype.La = function (a) {
            if ("$set" === a) return "__faps";
            if ("$set_once" === a) return "__fapso";
            if ("$add" === a) return "__fapa";
            if ("$append" === a) return "__fapap";
            if ("$union" === a) return "__fapu";
            k.error("Invalid queue:", a)
        };
        o.prototype.R = function (a) {
            return this.props[this.La(a)]
        };
        o.prototype.Z = function (a, b) {
            var d = this.La(a), b = c.c(b) ? {} : b;
            return this.props[d] || (this.props[d] = b)
        };
        o.prototype.vd = function (a) {
            var b = this.props.__timers || {};
            b[a] = (new Date).getTime();
            this.props.__timers = b;
            this.save()
        };
        o.prototype.od = function (a) {
            var b = (this.props.__timers || {})[a];
            c.c(b) || (delete this.props.__timers[a], this.save());
            return b
        };
        var g;
        h.prototype.T = function (a, b, d) {
            if (c.c(d)) k.error("You must name your new library: init(token, config, name)"); else if ("fap" === d) k.error("You must initialize the main fap object right after you include the FAP js snippet");
            else return a = I(a, b, d), s[d] = a, a.ta(), a
        };
        h.prototype.Na = function (a, b, d) {
            k.log("_init mix lib!");
            this.__loaded = n;
            this.config = {};
            this.Ub(c.extend({}, Q, b, {name: d, token: a, callback_fn: ("fap" === d ? d : "fap." + d) + "._jsc"}));
            this._jsc = B();
            this.Ia = [];
            this.Ja = [];
            this.Ha = [];
            this.Y = {disable_all_events: A, identify_called: A};
            this.persistence = this.cookie = new o(this.config);
            this.F({uuid: c.N()}, "")
        };
        h.prototype.ta = function () {
            this.d("loaded")(this);
            this.d("track_pageview") && this.Zb()
        };
        h.prototype.mc = function () {
            c.a(this.Ia,
                function (a) {
                    this.Qa.apply(this, a)
                }, this);
            c.a(this.Ja, function (a) {
                this.A.apply(this, a)
            }, this);
            delete this.Ia;
            delete this.Ja
        };
        h.prototype.Qa = function (a, b) {
            if (this.d("img")) return k.error("You can't use DOM tracking functions with img = true."), A;
            if (!R) return this.Ia.push([a, b]), A;
            var c = (new a).T(this);
            return c.I.apply(c, b)
        };
        h.prototype.ub = function (a, b) {
            if (c.c(a)) return r;
            if (L) return function (c) {
                a(c, b)
            };
            var d = this._jsc, e = "" + Math.floor(1E8 * Math.random()), f = this.d("callback_fn") + "[" + e + "]";
            d[e] = function (c) {
                delete d[e];
                a(c, b)
            };
            return f
        };
        h.prototype.A = function (a, b, d) {
            if (S) this.Ja.push(arguments); else {
                var e = this.d("verbose");
                b.verbose && (e = n);
                this.d("test") && (b.test = 1);
                e && (b.verbose = 1);
                this.d("img") && (b.img = 1);
                if (!L) if (d) b.callback = d; else if (e || this.d("test")) b.callback = "(function(){})";
                b._ = (new Date).getTime().toString();
                a += "?" + c.gc(b);
                if ("img" in b) {
                    var f = document.createElement("img");
                    f.src = a;
                    document.body.appendChild(f)
                } else if (L) try {
                    var i = new XMLHttpRequest;
                    i.open("GET", a, n);
                    i.withCredentials = n;
                    i.onreadystatechange =
                        function () {
                            if (4 === i.readyState) if (-1 !== a.indexOf("api.fap.vn/track") && E.Rc(i), 200 === i.status) d && (e ? d(c.na(i.responseText)) : d(Number(i.responseText))); else {
                                var b = "Bad HTTP status: " + i.status + " " + i.statusText;
                                k.error(b);
                                d && (e ? d({status: 0, error: b}) : d(0))
                            }
                        };
                    i.send(r)
                } catch (g) {
                    k.error(g)
                } else {
                    f = document.createElement("script");
                    f.type = "text/javascript";
                    f.async = n;
                    f.defer = n;
                    f.src = a;
                    var j = document.getElementsByTagName("script")[0];
                    j.parentNode.insertBefore(f, j)
                }
            }
        };
        h.prototype.Ka = function (a) {
            function b(a, b) {
                c.a(a,
                    function (a) {
                        this[a[0]].apply(this, a.slice(1))
                    }, b)
            }

            var d, e = [], f = [], i = [];
            c.a(a, function (a) {
                a && (d = a[0], "function" === typeof a ? a.call(this) : c.isArray(a) && "alias" === d ? e.push(a) : c.isArray(a) && -1 !== d.indexOf("track") && "function" === typeof this[d] ? i.push(a) : f.push(a))
            }, this);
            b(e, this);
            b(f, this);
            b(i, this)
        };
        h.prototype.push = function (a) {
            this.Ka([a])
        };
        h.prototype.disable = function (a) {
            "undefined" === typeof a ? this.Y.Vc = n : this.Ha = this.Ha.concat(a)
        };
        h.prototype.I = function (a, b, d) {
            "function" !== typeof d && (d = B());
            if (c.c(a)) k.error("No event name provided to fap.track");
            else {
                var b = b || {}, e = this.persistence.od(a);
                c.c(e) || (b.duration = parseFloat((((new Date).getTime() - e) / 1E3).toFixed(3)));
                this.persistence.bc(document.referrer);
                this.d("store_google") && this.persistence.Fd();
                this.d("save_referrer") && this.persistence.ib(document.referrer);
                b = c.extend({}, c.info.ia(), this.persistence.ia(), b);
                try {
                    if (this.d("autotrack") && "fap_page_view" !== a && "$create_alias" !== a) b = c.extend({}, b, this.D), this.D = {$__c: 0}, c.cookie.set("fap_" + this.d("name") + "__c", 0, 1, n)
                } catch (f) {
                    k.error(f)
                }
                e = this.d("property_blacklist");
                c.isArray(e) ? c.a(e, function (a) {
                    delete b[a]
                }) : k.error("Invalid value for property_blacklist config: " + e);
                var e = c.truncate(b, 255), i = c.oa(e), i = c.yb(i);
                k.log("FAP REQUEST:");
                k.log(e);
                this.A(this.d("api_host") + "/track", {topic: a, data: i, version: "1"}, this.ub(d, e));
                return e
            }
        };
        h.prototype.Zb = function (a) {
            if (c.c(a)) a = document.location.href;
            this.I("fap_page_view", c.info.ld(a))
        };
        h.prototype.Ed = function () {
            return this.Qa.call(this, F, arguments)
        };
        h.prototype.Dd = function () {
            return this.Qa.call(this, J, arguments)
        };
        h.prototype.Bd =
            function (a) {
                c.c(a) ? k.error("No event name provided to fap.time_event") : this.oc(a) || this.persistence.vd(a)
            };
        h.prototype.ja = function (a, b) {
            this.persistence.ja(a, b)
        };
        h.prototype.F = function (a, b, c) {
            this.persistence.F(a, b, c)
        };
        h.prototype.Ca = function (a) {
            this.persistence.Ca(a)
        };
        h.prototype.Pa = function (a, b) {
            var c = {};
            c[a] = b;
            this.ja(c)
        };
        h.prototype.Za = function (a, b, c, e, f, i) {
            a !== this.fa() && a !== this.xa("__alias") && (this.Ca("__alias"), this.Pa("uuid", a));
            this.jb();
            this.Y.Ib = n;
            this.people.rc(b, c, e, f, i)
        };
        h.prototype.reset =
            function () {
                this.persistence.clear();
                this.Y.Ib = A;
                this.F({uuid: c.N()}, "")
            };
        h.prototype.fa = function () {
            return this.xa("uuid")
        };
        h.prototype.Nc = function (a, b) {
            if (a === this.xa("$people_distinct_id")) return k.ca("Attempting to create alias for existing People user - aborting."), -2;
            var d = this;
            c.c(b) && (b = this.fa());
            if (a !== b) return this.Pa("__alias", a), this.I("$create_alias", {alias: a, uuid: b}, function () {
                d.Za(a)
            });
            k.error("alias matches current distinct_id - skipping api call.");
            this.Za(a);
            return -1
        };
        h.prototype.jd =
            function (a) {
                this.Pa("fap_name_tag", a)
            };
        h.prototype.Ub = function (a) {
            if (c.j(a)) c.extend(this.config, a), this.d("persistence_name") || (this.config.persistence_name = this.config.cookie_name), this.d("disable_persistence") || (this.config.disable_persistence = this.config.disable_cookie), this.persistence && this.persistence.ac(this.config), z = z || this.d("debug")
        };
        h.prototype.d = function (a) {
            return this.config[a]
        };
        h.prototype.xa = function (a) {
            return this.persistence.props[a]
        };
        h.prototype.toString = function () {
            var a = this.d("name");
            "fap" !== a && (a = "fap." + a);
            return a
        };
        h.prototype.oc = function (a) {
            return c.Nb(t) || this.Y.Vc || c.Kb(this.Ha, a)
        };
        h.prototype.jb = B();
        h.prototype.Jc = function (a) {
            (new g(a, this)).show()
        };
        p.prototype.Na = function (a) {
            this.e = a
        };
        p.prototype.set = function (a, b, d) {
            var e = {}, f = {};
            c.j(a) ? (c.a(a, function (a, b) {
                this.$(b) || (f[b] = a)
            }, this), d = b) : f[a] = b;
            this.sa("save_referrer") && this.e.persistence.ib(document.referrer);
            f = c.extend({}, c.info.md(), this.e.persistence.cd(), f);
            e.$set = f;
            return this.A(e, d)
        };
        p.prototype.Vb = function (a, b,
                                   d) {
            var e = {}, f = {};
            c.j(a) ? (c.a(a, function (a, b) {
                this.$(b) || (f[b] = a)
            }, this), d = b) : f[a] = b;
            e.$set_once = f;
            return this.A(e, d)
        };
        p.prototype.Lb = function (a, b, d) {
            var e = {}, f = {};
            c.j(a) ? (c.a(a, function (a, b) {
                this.$(b) || (isNaN(parseFloat(a)) ? k.error("Invalid increment value passed to fap.people.increment - must be a number") : f[b] = a)
            }, this), d = b) : (c.c(b) && (b = 1), f[a] = b);
            e.$add = f;
            return this.A(e, d)
        };
        p.prototype.append = function (a, b, d) {
            var e = {}, f = {};
            c.j(a) ? (c.a(a, function (a, b) {
                this.$(b) || (f[b] = a)
            }, this), d = b) : f[a] = b;
            e.$append =
                f;
            return this.A(e, d)
        };
        p.prototype.$b = function (a, b, d) {
            var e = {}, f = {};
            c.j(a) ? (c.a(a, function (a, b) {
                this.$(b) || (f[b] = c.isArray(a) ? a : [a])
            }, this), d = b) : f[a] = c.isArray(b) ? b : [b];
            e.$union = f;
            return this.A(e, d)
        };
        p.prototype.Cd = function (a, b, d) {
            if (!c.hd(a) && (a = parseFloat(a), isNaN(a))) {
                k.error("Invalid value passed to fap.people.track_charge - must be a number");
                return
            }
            return this.append("$transactions", c.extend({$amount: a}, b), d)
        };
        p.prototype.Sc = function (a) {
            return this.set("$transactions", [], a)
        };
        p.prototype.Uc = function () {
            if (this.qb()) return this.A({$delete: this.e.fa()});
            k.error("fap.people.delete_user() requires you to call identify() first")
        };
        p.prototype.toString = function () {
            return this.e.toString() + ".people"
        };
        p.prototype.A = function (a, b) {
            a.$token = this.sa("token");
            a.$distinct_id = this.e.fa();
            var d = c.Gb(a), e = c.truncate(d, 255), d = c.oa(d), d = c.yb(d);
            if (!this.qb()) return this.nc(a), c.c(b) || (this.sa("verbose") ? b({status: -1, error: r}) : b(-1)), e;
            k.log("FAP PEOPLE REQUEST:");
            k.log(e);
            this.e.A(this.sa("api_host") + "/engage/", {data: d}, this.e.ub(b, e));
            return e
        };
        p.prototype.sa = function (a) {
            return this.e.d(a)
        };
        p.prototype.qb = function () {
            return this.e.Y.Ib === n
        };
        p.prototype.nc = function (a) {
            "$set" in a ? this.e.persistence.z("$set", a) : "$set_once" in a ? this.e.persistence.z("$set_once", a) : "$add" in a ? this.e.persistence.z("$add", a) : "$append" in a ? this.e.persistence.z("$append", a) : "$union" in a ? this.e.persistence.z("$union", a) : k.error("Invalid call to _enqueue():", a)
        };
        p.prototype.rc = function (a, b, d, e, f) {
            var i = this, g = c.extend({}, this.e.persistence.R("$set")),
                j = c.extend({}, this.e.persistence.R("$set_once")), h = c.extend({},
                this.e.persistence.R("$add")), k = this.e.persistence.R("$append"),
                o = c.extend({}, this.e.persistence.R("$union"));
            !c.c(g) && c.j(g) && !c.U(g) && (i.e.persistence.S("$set", g), this.set(g, function (b, d) {
                0 === b && i.e.persistence.z("$set", g);
                c.c(a) || a(b, d)
            }));
            !c.c(j) && c.j(j) && !c.U(j) && (i.e.persistence.S("$set_once", j), this.Vb(j, function (a, b) {
                0 === a && i.e.persistence.z("$set_once", j);
                c.c(e) || e(a, b)
            }));
            !c.c(h) && c.j(h) && !c.U(h) && (i.e.persistence.S("$add", h), this.Lb(h, function (a, d) {
                0 === a && i.e.persistence.z("$add", h);
                c.c(b) ||
                b(a, d)
            }));
            !c.c(o) && c.j(o) && !c.U(o) && (i.e.persistence.S("$union", o), this.$b(o, function (a, b) {
                0 === a && i.e.persistence.z("$union", o);
                c.c(f) || f(a, b)
            }));
            if (!c.c(k) && c.isArray(k) && k.length) {
                for (var p, s = function (a, b) {
                    0 === a && i.e.persistence.z("$append", p);
                    c.c(d) || d(a, b)
                }, t = k.length - 1; 0 <= t; t--) p = k.pop(), i.append(p, s);
                i.e.persistence.save()
            }
        };
        p.prototype.$ = function (a) {
            return "$distinct_id" === a || "$token" === a
        };
        h.jc = function (a, b) {
            c.Ab(this);
            this.eb = b;
            this.gb = this.eb.persistence;
            this.C = c.K(a.id);
            this.Pb = c.K(a.message_id);
            this.body = (c.K(a.body) || "").replace(/\n/g, "<br/>");
            this.Tc = c.K(a.cta) || "Close";
            this.ga = c.K(a.type) || "takeover";
            this.style = c.K(a.style) || "light";
            this.title = c.K(a.title) || "";
            this.la = g.ic;
            this.W = g.hc;
            this.da = a.cta_url || r;
            this.$a = a.image_url || r;
            this.L = a.thumb_image_url || r;
            this.Da = a.video_url || r;
            this.va = n;
            if (!this.da) this.da = "#dismiss", this.va = A;
            this.s = "mini" === this.ga;
            if (!this.s) this.ga = "takeover";
            this.kd = !this.s ? g.X : g.Ea;
            this.wb();
            this.ya = this.yc();
            this.Bc()
        };
        g = h.jc;
        g.M = 200;
        g.v = "mixpanel-notification";
        g.ma = 0.6;
        g.H = 25;
        g.pa = 200;
        g.X = 388;
        g.Ea = 420;
        g.w = 85;
        g.Fa = 5;
        g.J = 60;
        g.Ga = Math.round(g.J / 2);
        g.ic = 595;
        g.hc = 334;
        g.prototype.show = function () {
            var a = this;
            this.wb();
            this.p ? (this.Ac(), this.zc(), this.Fc(this.lc)) : setTimeout(function () {
                a.show()
            }, 300)
        };
        g.prototype.Va = c.l(function () {
            this.Ob || this.tb({invisible: n});
            var a = this.yd ? this.i("video") : this.Q();
            if (this.cc) this.Hc("bg", "visible"), this.O(a, "exiting"), setTimeout(this.vb, g.M); else {
                var b, c, e;
                this.s ? (b = "right", c = 20, e = -100) : (b = "top", c = g.H, e = g.pa + g.H);
                this.qa([{
                    q: this.i("bg"),
                    m: "opacity", start: g.ma, k: 0
                }, {q: a, m: "opacity", start: 1, k: 0}, {q: a, m: b, start: c, k: e}], g.M, this.vb)
            }
        });
        g.prototype.O = c.l(function (a, b) {
            b = g.v + "-" + b;
            "string" === typeof a && (a = this.i(a));
            a.className ? ~(" " + a.className + " ").indexOf(" " + b + " ") || (a.className += " " + b) : a.className = b
        });
        g.prototype.Hc = c.l(function (a, b) {
            b = g.v + "-" + b;
            "string" === typeof a && (a = this.i(a));
            if (a.className) a.className = (" " + a.className + " ").replace(" " + b + " ", "").replace(/^[\s\xA0]+/, "").replace(/[\s\xA0]+$/, "")
        });
        g.prototype.qa = c.l(function (a,
                                       b, c, e) {
            var f = this, g = A, h, j;
            h = 1 * new Date;
            var k, e = e || h;
            k = h - e;
            for (h = 0; h < a.length; h++) {
                j = a[h];
                if ("undefined" === typeof j.G) j.G = j.start;
                if (j.G !== j.k) {
                    var g = n, o = j.k >= j.start ? 1 : -1;
                    j.G = j.start + (j.k - j.start) * k / b;
                    if ("opacity" !== j.m) j.G = Math.round(j.G);
                    if (0 < o && j.G >= j.k || 0 > o && j.G <= j.k) j.G = j.k
                }
            }
            if (g) {
                for (h = 0; h < a.length; h++) j = a[h], j.q && (j.q.style[j.m] = "" + j.G + ("opacity" === j.m ? "" : "px"));
                setTimeout(function () {
                    f.qa(a, b, c, e)
                }, 10)
            } else c && c()
        });
        g.prototype.lc = c.l(function () {
            var a = this;
            if (!this.zd && !this.pb()[this.C]) this.zd =
                n, this.p.appendChild(this.ha), setTimeout(function () {
                var b = a.Q();
                if (a.cc) a.s || a.O("bg", "visible"), a.O(b, "visible"), a.sb(); else {
                    var c, e, f;
                    a.s ? (c = "right", e = -100, f = 20) : (c = "top", e = g.pa + g.H, f = g.H);
                    a.qa([{q: a.i("bg"), m: "opacity", start: 0, k: g.ma}, {q: b, m: "opacity", start: 0, k: 1}, {
                        q: b,
                        m: c,
                        start: e,
                        k: f
                    }], g.M, a.sb)
                }
            }, 100), c.o(a.i("cancel"), "click", function (b) {
                b.preventDefault();
                a.Va()
            }), c.o(a.i("button") || a.i("mini-content"), "click", function (b) {
                b.preventDefault();
                a.V ? (a.Ra("$campaign_open", {$resource_type: "video"}),
                    a.Kc()) : (a.Va(), a.va && a.Ra("$campaign_open", {$resource_type: "link"}, function () {
                    window.location.href = a.da
                }))
            })
        });
        g.prototype.i = function (a) {
            return document.getElementById(g.v + "-" + a)
        };
        g.prototype.Q = function () {
            return this.i(this.ga)
        };
        g.prototype.pb = function () {
            return this.gb.props.__cmpns || (this.gb.props.__cmpns = {})
        };
        g.prototype.P = function (a, b) {
            return this.B[a] && this.B[a] <= b
        };
        g.prototype.yc = function () {
            var a = [];
            this.s ? (this.L = this.L || "//cdn.mxpnl.com/site_media/images/icons/notifications/mini-news-dark.png",
                a.push(this.L)) : (this.$a ? (a.push(this.$a), this.Jb = '<img id="img" src="' + this.$a + '"/>') : this.Jb = "", this.L ? (a.push(this.L), this.Xb = '<div id="thumbborder-wrapper"><div id="thumbborder"></div></div><img id="thumbnail" src="' + this.L + '" width="' + g.J + '" height="' + g.J + '"/><div id="thumbspacer"></div>') : this.Xb = "");
            return a
        };
        g.prototype.zc = function () {
            var a = "", b = "", c = "";
            this.ha = document.createElement("div");
            this.ha.id = g.v + "-wrapper";
            if (this.s) a = '<div id="mini"><div id="mainbox"><div id="cancel"><div id="cancel-icon"></div></div><div id="mini-content"><div id="mini-icon"><div id="mini-icon-img"></div></div><div id="body"><div id="body-text"><div>' +
                this.body + '</div></div></div></div></div><div id="mini-border"></div></div>'; else {
                var a = this.va || this.V ? "" : '<div id="button-close"></div>',
                    e = this.V ? '<div id="button-play"></div>' : "";
                this.P("ie", 7) && (e = a = "");
                a = '<div id="takeover">' + this.Xb + '<div id="mainbox"><div id="cancel"><div id="cancel-icon"></div></div><div id="content">' + this.Jb + '<div id="title">' + this.title + '</div><div id="body">' + this.body + '</div><div id="tagline"><a href="http://fap.com?from=inapp" target="_blank">POWERED BY MIXPANEL</a></div></div><div id="button">' +
                    a + '<a id="button-link" href="' + this.da + '">' + this.Tc + "</a>" + e + "</div></div></div>"
            }
            this.ec ? (b = "//www.youtube.com/embed/" + this.ec + "?wmode=transparent&showinfo=0&modestbranding=0&rel=0&autoplay=1&loop=0&vq=hd1080", this.fc && (b += "&enablejsapi=1&html5=1&controls=0", c = '<div id="video-controls"><div id="video-progress" class="video-progress-el"><div id="video-progress-total" class="video-progress-el"></div><div id="video-elapsed" class="video-progress-el"></div></div><div id="video-time" class="video-progress-el"></div></div>')) :
                this.dc && (b = "//player.vimeo.com/video/" + this.dc + "?autoplay=1&title=0&byline=0&portrait=0");
            if (this.V) this.Jd = '<iframe id="' + g.v + '-video-frame" width="' + this.la + '" height="' + this.W + '"  src="' + b + '" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen="1" scrolling="no"></iframe>', c = '<div id="video-' + (this.Ya ? "" : "no") + 'flip"><div id="video"><div id="video-holder"></div>' + c + "</div></div>";
            b = c + a;
            this.Ya && (b = (this.s ? a : "") + '<div id="flipcontainer"><div id="flipper">' + (this.s ? c : b) + "</div></div>");
            this.ha.innerHTML = ('<div id="overlay" class="' + this.ga + '"><div id="campaignid-' + this.C + '"><div id="bgwrapper"><div id="bg"></div>' + b + "</div></div></div>").replace(/class=\"/g, 'class="' + g.v + "-").replace(/id=\"/g, 'id="' + g.v + "-")
        };
        g.prototype.Ac = function () {
            this.h = "dark" === this.style ? {
                Ta: "#1d1f25",
                aa: "#282b32",
                ua: "#3a4147",
                zb: "#4a5157",
                Oc: "#32353c",
                Db: "0.4",
                cb: "#2a3137",
                Ba: "#fff",
                hb: "#9498a3",
                Wb: "#464851",
                Aa: "#ddd"
            } : {
                Ta: "#fff", aa: "#e7eaee", ua: "#eceff3", zb: "#f5f5f5", Oc: "#e4ecf2", Db: "1.0", cb: "#fafafa",
                Ba: "#5c6578", hb: "#8b949b", Wb: "#ced9e6", Aa: "#7c8598"
            };
            var a = "0px 0px 35px 0px rgba(45, 49, 56, 0.7)", b = a, d = a, e = g.J + 2 * g.Fa, f = g.M / 1E3 + "s";
            this.s && (a = "none");
            var i = {};
            i["@media only screen and (max-width: " + (g.Ea + 20 - 1) + "px)"] = {"#overlay": {display: "none"}};
            a = {
                ".flipped": {transform: "rotateY(180deg)"},
                "#overlay": {
                    position: "fixed",
                    top: "0",
                    left: "0",
                    width: "100%",
                    height: "100%",
                    overflow: "auto",
                    "text-align": "center",
                    "z-index": "10000",
                    "font-family": '"Helvetica", "Arial", sans-serif',
                    "-webkit-font-smoothing": "antialiased",
                    "-moz-osx-font-smoothing": "grayscale"
                },
                "#overlay.mini": {height: "0", overflow: "visible"},
                "#overlay a": {
                    width: "initial",
                    padding: "0",
                    "text-decoration": "none",
                    "text-transform": "none",
                    color: "inherit"
                },
                "#bgwrapper": {position: "relative", width: "100%", height: "100%"},
                "#bg": {
                    position: "fixed",
                    top: "0",
                    left: "0",
                    width: "100%",
                    height: "100%",
                    "min-width": 4 * this.Xc + "px",
                    "min-height": 4 * this.Wc + "px",
                    "background-color": "black",
                    opacity: "0.0",
                    "-ms-filter": "progid:DXImageTransform.Microsoft.Alpha(Opacity=60)",
                    filter: "alpha(opacity=60)",
                    transition: "opacity " + f
                },
                "#bg.visible": {opacity: g.ma},
                ".mini #bg": {width: "0", height: "0", "min-width": "0"},
                "#flipcontainer": {perspective: "1000px", position: "absolute", width: "100%"},
                "#flipper": {position: "relative", "transform-style": "preserve-3d", transition: "0.3s"},
                "#takeover": {
                    position: "absolute",
                    left: "50%",
                    width: g.X + "px",
                    "margin-left": Math.round(-g.X / 2) + "px",
                    "backface-visibility": "hidden",
                    transform: "rotateY(0deg)",
                    opacity: "0.0",
                    top: g.pa + "px",
                    transition: "opacity " + f + ", top " + f
                },
                "#takeover.visible": {
                    opacity: "1.0",
                    top: g.H + "px"
                },
                "#takeover.exiting": {opacity: "0.0", top: g.pa + "px"},
                "#thumbspacer": {height: g.Ga + "px"},
                "#thumbborder-wrapper": {
                    position: "absolute",
                    top: -g.Fa + "px",
                    left: g.X / 2 - g.Ga - g.Fa + "px",
                    width: e + "px",
                    height: e / 2 + "px",
                    overflow: "hidden"
                },
                "#thumbborder": {
                    position: "absolute",
                    width: e + "px",
                    height: e + "px",
                    "border-radius": e + "px",
                    "background-color": this.h.aa,
                    opacity: "0.5"
                },
                "#thumbnail": {
                    position: "absolute",
                    top: "0px",
                    left: g.X / 2 - g.Ga + "px",
                    width: g.J + "px",
                    height: g.J + "px",
                    overflow: "hidden",
                    "z-index": "100",
                    "border-radius": g.J +
                        "px"
                },
                "#mini": {
                    position: "absolute",
                    right: "20px",
                    top: g.H + "px",
                    width: this.kd + "px",
                    height: 2 * g.w + "px",
                    "margin-top": 20 - g.w + "px",
                    "backface-visibility": "hidden",
                    opacity: "0.0",
                    transform: "rotateX(90deg)",
                    transition: "opacity 0.3s, transform 0.3s, right 0.3s"
                },
                "#mini.visible": {opacity: "1.0", transform: "rotateX(0deg)"},
                "#mini.exiting": {opacity: "0.0", right: "-150px"},
                "#mainbox": {
                    "border-radius": "4px",
                    "box-shadow": a,
                    "text-align": "center",
                    "background-color": this.h.Ta,
                    "font-size": "14px",
                    color: this.h.hb
                },
                "#mini #mainbox": {
                    height: g.w +
                        "px", "margin-top": g.w + "px", "border-radius": "3px", transition: "background-color " + f
                },
                "#mini-border": {
                    height: g.w + 6 + "px",
                    width: g.Ea + 6 + "px",
                    position: "absolute",
                    top: "-3px",
                    left: "-3px",
                    "margin-top": g.w + "px",
                    "border-radius": "6px",
                    opacity: "0.25",
                    "background-color": "#fff",
                    "z-index": "-1",
                    "box-shadow": d
                },
                "#mini-icon": {
                    position: "relative",
                    display: "inline-block",
                    width: "75px",
                    height: g.w + "px",
                    "border-radius": "3px 0 0 3px",
                    "background-color": this.h.aa,
                    background: "linear-gradient(135deg, " + this.h.zb + " 0%, " + this.h.aa +
                        " 100%)",
                    transition: "background-color " + f
                },
                "#mini:hover #mini-icon": {"background-color": this.h.cb},
                "#mini:hover #mainbox": {"background-color": this.h.cb},
                "#mini-icon-img": {
                    position: "absolute",
                    "background-image": "url(" + this.L + ")",
                    width: "48px",
                    height: "48px",
                    top: "20px",
                    left: "12px"
                },
                "#content": {padding: "30px 20px 0px 20px"},
                "#mini-content": {"text-align": "left", height: g.w + "px", cursor: "pointer"},
                "#img": {width: "328px", "margin-top": "30px", "border-radius": "5px"},
                "#title": {
                    "max-height": "600px",
                    overflow: "hidden",
                    "word-wrap": "break-word",
                    padding: "25px 0px 20px 0px",
                    "font-size": "19px",
                    "font-weight": "bold",
                    color: this.h.Ba
                },
                "#body": {
                    "max-height": "600px",
                    "margin-bottom": "25px",
                    overflow: "hidden",
                    "word-wrap": "break-word",
                    "line-height": "21px",
                    "font-size": "15px",
                    "font-weight": "normal",
                    "text-align": "left"
                },
                "#mini #body": {
                    display: "inline-block",
                    "max-width": "250px",
                    margin: "0 0 0 30px",
                    height: g.w + "px",
                    "font-size": "16px",
                    "letter-spacing": "0.8px",
                    color: this.h.Ba
                },
                "#mini #body-text": {display: "table", height: g.w + "px"},
                "#mini #body-text div": {
                    display: "table-cell",
                    "vertical-align": "middle"
                },
                "#tagline": {
                    "margin-bottom": "15px",
                    "font-size": "10px",
                    "font-weight": "600",
                    "letter-spacing": "0.8px",
                    color: "#ccd7e0",
                    "text-align": "left"
                },
                "#tagline a": {color: this.h.Wb, transition: "color " + f},
                "#tagline a:hover": {color: this.h.Aa},
                "#cancel": {
                    position: "absolute",
                    right: "0",
                    width: "8px",
                    height: "8px",
                    padding: "10px",
                    "border-radius": "20px",
                    margin: "12px 12px 0 0",
                    "box-sizing": "content-box",
                    cursor: "pointer",
                    transition: "background-color " + f
                },
                "#mini #cancel": {margin: "7px 7px 0 0"},
                "#cancel-icon": {
                    width: "8px",
                    height: "8px",
                    overflow: "hidden",
                    "background-image": "url(//cdn.mxpnl.com/site_media/images/icons/notifications/cancel-x.png)",
                    opacity: this.h.Db
                },
                "#cancel:hover": {"background-color": this.h.ua},
                "#button": {
                    display: "block",
                    height: "60px",
                    "line-height": "60px",
                    "text-align": "center",
                    "background-color": this.h.aa,
                    "border-radius": "0 0 4px 4px",
                    overflow: "hidden",
                    cursor: "pointer",
                    transition: "background-color " + f
                },
                "#button-close": {
                    display: "inline-block",
                    width: "9px",
                    height: "60px",
                    "margin-right": "8px",
                    "vertical-align": "top",
                    "background-image": "url(//cdn.mxpnl.com/site_media/images/icons/notifications/close-x-" + this.style + ".png)",
                    "background-repeat": "no-repeat",
                    "background-position": "0px 25px"
                },
                "#button-play": {
                    display: "inline-block",
                    width: "30px",
                    height: "60px",
                    "margin-left": "15px",
                    "background-image": "url(//cdn.mxpnl.com/site_media/images/icons/notifications/play-" + this.style + "-small.png)",
                    "background-repeat": "no-repeat",
                    "background-position": "0px 15px"
                },
                "a#button-link": {
                    display: "inline-block",
                    "vertical-align": "top",
                    "text-align": "center",
                    "font-size": "17px",
                    "font-weight": "bold",
                    overflow: "hidden",
                    "word-wrap": "break-word",
                    color: this.h.Ba,
                    transition: "color " + f
                },
                "#button:hover": {"background-color": this.h.ua, color: this.h.Aa},
                "#button:hover a": {color: this.h.Aa},
                "#video-noflip": {position: "relative", top: 2 * -this.W + "px"},
                "#video-flip": {"backface-visibility": "hidden", transform: "rotateY(180deg)"},
                "#video": {
                    position: "absolute",
                    width: this.la - 1 + "px",
                    height: this.W + "px",
                    top: g.H + "px",
                    "margin-top": "100px",
                    left: "50%",
                    "margin-left": Math.round(-this.la /
                        2) + "px",
                    overflow: "hidden",
                    "border-radius": "5px",
                    "box-shadow": b,
                    transform: "translateZ(1px)",
                    transition: "opacity " + f + ", top " + f
                },
                "#video.exiting": {opacity: "0.0", top: this.W + "px"},
                "#video-holder": {
                    position: "absolute",
                    width: this.la - 1 + "px",
                    height: this.W + "px",
                    overflow: "hidden",
                    "border-radius": "5px"
                },
                "#video-frame": {"margin-left": "-1px", width: this.la + "px"},
                "#video-controls": {opacity: "0", transition: "opacity 0.5s"},
                "#video:hover #video-controls": {opacity: "1.0"},
                "#video .video-progress-el": {
                    position: "absolute",
                    bottom: "0", height: "25px", "border-radius": "0 0 0 5px"
                },
                "#video-progress": {width: "90%"},
                "#video-progress-total": {width: "100%", "background-color": this.h.Ta, opacity: "0.7"},
                "#video-elapsed": {width: "0", "background-color": "#6cb6f5", opacity: "0.9"},
                "#video #video-time": {
                    width: "10%",
                    right: "0",
                    "font-size": "11px",
                    "line-height": "25px",
                    color: this.h.hb,
                    "background-color": "#666",
                    "border-radius": "0 0 5px 0"
                }
            };
            this.P("ie", 8) && c.extend(a, {
                "* html #overlay": {position: "absolute"},
                "* html #bg": {position: "absolute"},
                "html, body": {height: "100%"}
            });
            this.P("ie", 7) && c.extend(a, {
                "#mini #body": {
                    display: "inline",
                    zoom: "1",
                    border: "1px solid " + this.h.ua
                }, "#mini #body-text": {padding: "20px"}, "#mini #mini-icon": {display: "none"}
            });
            var b = "backface-visibility,border-radius,box-shadow,opacity,perspective,transform,transform-style,transition".split(","),
                d = ["khtml", "moz", "ms", "o", "webkit"], h;
            for (h in a) for (e = 0; e < b.length; e++) if (f = b[e], f in a[h]) for (var j = a[h][f], k = 0; k < d.length; k++) a[h]["-" + d[k] + "-" + f] = j;
            (function (a, b) {
                function c(a) {
                    var b = "", d;
                    for (d in a) {
                        var e =
                                d.replace(/#/g, "#" + g.v + "-").replace(/\./g, "." + g.v + "-"), b = b + ("\n" + e + " {"),
                            e = a[d], f;
                        for (f in e) b += f + ":" + e[f] + ";";
                        b += "}"
                    }
                    return b
                }

                var d = c(a) + function (a) {
                        var b = "", d;
                        for (d in a) b += "\n" + d + " {" + c(a[d]) + "\n}";
                        return b
                    }(b), e = document.head || document.getElementsByTagName("head")[0] || document.documentElement,
                    f = document.createElement("style");
                e.appendChild(f);
                f.setAttribute("type", "text/css");
                f.styleSheet ? f.styleSheet.cssText = d : f.textContent = d
            })(a, i)
        };
        g.prototype.Bc = c.l(function () {
            if (this.Da) {
                var a = this;
                a.fc =
                    "postMessage" in window;
                a.da = a.Da;
                var b = a.Da.match(/(?:youtube(?:-nocookie)?\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/ ]{11})/i),
                    c = a.Da.match(/vimeo\.com\/.*?(\d+)/i);
                if (b) {
                    if (a.V = n, a.ec = b[1], a.fc) window.onYouTubeIframeAPIReady = function () {
                        a.i("video-frame") && a.xb()
                    }, b = document.createElement("script"), b.src = "//www.youtube.com/iframe_api", c = document.getElementsByTagName("script")[0], c.parentNode.insertBefore(b, c)
                } else if (c) a.V = n, a.dc = c[1];
                if (a.P("ie", 7) || a.P("firefox", 3)) a.V =
                    A, a.va = n
            }
        });
        g.prototype.sb = c.l(function () {
            function a(a, b) {
                var c = {};
                if (document.defaultView && document.defaultView.getComputedStyle) c = document.defaultView.getComputedStyle(a, r); else if (a.currentStyle) c = a.currentStyle;
                return c[b]
            }

            var b = this;
            c.o(b.i("bg"), "click", function () {
                b.Va()
            });
            if (this.C) {
                var d = this.i("overlay");
                d && "hidden" !== a(d, "visibility") && "none" !== a(d, "display") && this.tb()
            }
        });
        g.prototype.tb = c.l(function (a) {
            if (!this.Ob) this.Ob = n, this.C && (this.pb()[this.C] = 1 * new Date, this.gb.save()), this.Ra("$campaign_delivery",
                a), this.eb.people.append({
                $campaigns: this.C,
                $notifications: {campaign_id: this.C, message_id: this.Pb, type: "web", time: new Date}
            })
        });
        g.prototype.Fc = function (a) {
            var b = this;
            if (0 === this.ya.length) a(); else {
                for (var c = 0, e = [], f = function () {
                    c++;
                    c === b.ya.length && a && (a(), a = r)
                }, g = 0; g < this.ya.length; g++) {
                    var h = new Image;
                    h.onload = f;
                    h.src = this.ya[g];
                    h.complete && f();
                    e.push(h)
                }
                this.P("ie", 7) && setTimeout(function () {
                    var b = n;
                    for (g = 0; g < e.length; g++) e[g].complete || (b = A);
                    b && a && (a(), a = r)
                }, 500)
            }
        };
        g.prototype.vb = c.l(function () {
            window.clearInterval(this.Mc);
            this.ha.style.visibility = "hidden";
            this.p.removeChild(this.ha)
        });
        g.prototype.wb = function () {
            function a(a) {
                if (a in e) return n;
                if (!c) for (var a = a[0].toUpperCase() + a.slice(1), a = ["O" + a, "Webkit" + a, "Moz" + a], b = 0; b < a.length; b++) if (a[b] in e) return n;
                return A
            }

            function b(a) {
                return (a = navigator.userAgent.match(a)) && a[1]
            }

            this.B = {};
            this.B.chrome = b(/Chrome\/(\d+)/);
            this.B.firefox = b(/Firefox\/(\d+)/);
            this.B.ie = b(/MSIE (\d+).+/);
            !this.B.ie && !window.ActiveXObject && "ActiveXObject" in window && (this.B.ie = 11);
            if (this.p = document.body ||
                document.getElementsByTagName("body")[0]) this.Xc = Math.max(this.p.scrollWidth, document.documentElement.scrollWidth, this.p.offsetWidth, document.documentElement.offsetWidth, this.p.clientWidth, document.documentElement.clientWidth), this.Wc = Math.max(this.p.scrollHeight, document.documentElement.scrollHeight, this.p.offsetHeight, document.documentElement.offsetHeight, this.p.clientHeight, document.documentElement.clientHeight);
            var c = this.B.ie, e = document.createElement("div").style;
            this.cc = this.p && a("transition") &&
                a("transform");
            this.Ya = (33 <= this.B.chrome || 15 <= this.B.firefox) && this.p && a("backfaceVisibility") && a("perspective") && a("transform")
        };
        g.prototype.Kc = c.l(function () {
            function a() {
                window.YT && window.YT.loaded && b.xb();
                b.yd = n;
                b.Q().style.visibility = "hidden"
            }

            var b = this, c = [{q: b.Q(), m: "opacity", start: 1, k: 0}, {
                q: b.Q(),
                m: "top",
                start: g.H,
                k: -500
            }, {q: b.i("video-noflip"), m: "opacity", start: 0, k: 1}, {
                q: b.i("video-noflip"),
                m: "top",
                start: 2 * -b.W,
                k: 0
            }];
            if (b.s) {
                var e = b.i("bg"), f = b.i("overlay");
                e.style.width = "100%";
                e.style.height =
                    "100%";
                f.style.width = "100%";
                b.O(b.Q(), "exiting");
                b.O(e, "visible");
                c.push({q: b.i("bg"), m: "opacity", start: 0, k: g.ma})
            }
            b.i("video-holder").innerHTML = b.Jd;
            b.Ya ? (b.O("flipper", "flipped"), setTimeout(a, g.M)) : b.qa(c, g.M, a)
        });
        g.prototype.Ra = function (a, b, d) {
            this.C ? (b = b || {}, b = c.extend(b, {
                campaign_id: this.C,
                message_id: this.Pb,
                message_type: "web_inapp",
                message_subtype: this.ga
            }), this.eb.track(a, b, d)) : d && d.call()
        };
        g.prototype.xb = c.l(function () {
            var a = this;
            if (!a.Kd) {
                a.Kd = n;
                var b = a.i("video-elapsed"), d = a.i("video-time"),
                    e = a.i("video-progress");
                new window.YT.Player(g.v + "-video-frame", {
                    events: {
                        onReady: function (f) {
                            function g(a) {
                                var a = Math.round(j - a), b = Math.floor(a / 60), c = Math.floor(b / 60),
                                    a = a - 60 * b;
                                d.innerHTML = "-" + (c ? c + ":" : "") + ("00" + (b - 60 * c)).slice(-2) + ":" + ("00" + a).slice(-2)
                            }

                            var h = f.target, j = h.getDuration();
                            g(0);
                            a.Mc = window.setInterval(function () {
                                var a = h.getCurrentTime();
                                b.style.width = 100 * (a / j) + "%";
                                g(a)
                            }, 250);
                            c.o(e, "click", function (a) {
                                a = Math.max(0, a.pageX - e.getBoundingClientRect().left);
                                h.seekTo(j * a / e.clientWidth, n)
                            })
                        }
                    }
                })
            }
        });
        h.prototype.init = h.prototype.T;
        h.prototype.reset = h.prototype.reset;
        h.prototype.disable = h.prototype.disable;
        h.prototype.time_event = h.prototype.Bd;
        h.prototype.track = h.prototype.I;
        h.prototype.track_links = h.prototype.Ed;
        h.prototype.track_forms = h.prototype.Dd;
        h.prototype.track_pageview = h.prototype.Zb;
        h.prototype.register = h.prototype.ja;
        h.prototype.register_once = h.prototype.F;
        h.prototype.unregister = h.prototype.Ca;
        h.prototype.identify = h.prototype.Za;
        h.prototype.alias = h.prototype.Nc;
        h.prototype.name_tag =
            h.prototype.jd;
        h.prototype.set_config = h.prototype.Ub;
        h.prototype.get_config = h.prototype.d;
        h.prototype.get_property = h.prototype.xa;
        h.prototype.get_distinct_id = h.prototype.fa;
        h.prototype.toString = h.prototype.toString;
        h.prototype._check_and_handle_notifications = h.prototype.jb;
        h.prototype._show_notification = h.prototype.Jc;
        o.prototype.properties = o.prototype.ia;
        o.prototype.update_search_keyword = o.prototype.bc;
        o.prototype.update_referrer_info = o.prototype.ib;
        o.prototype.get_cross_subdomain = o.prototype.bd;
        o.prototype.clear = o.prototype.clear;
        p.prototype.set = p.prototype.set;
        p.prototype.set_once = p.prototype.Vb;
        p.prototype.increment = p.prototype.Lb;
        p.prototype.append = p.prototype.append;
        p.prototype.union = p.prototype.$b;
        p.prototype.track_charge = p.prototype.Cd;
        p.prototype.clear_charges = p.prototype.Sc;
        p.prototype.delete_user = p.prototype.Uc;
        p.prototype.toString = p.prototype.toString;
        c.pd(h);
        var y = {};
        (function () {
            M = 1;
            s = window.fap;
            c.c(s) ? k.ca('"fap" object not initialized. Ensure you are using the latest version of the FAP JS Library along with the snippet we provide.') :
                s.__loaded || s.config && s.persistence ? k.error("FAP library has already been downloaded at least once.") : 1.1 > (s.__SV || 0) ? k.ca("Version mismatch; please ensure you're using the latest version of the FAP code snippet.") : (c.a(s._i, function (a) {
                    a && c.isArray(a) && (y[a[a.length - 1]] = I.apply(this, a))
                }), Y(), s.init(), c.a(y, function (a) {
                    a.ta()
                }), X())
        })()
    })();
})();