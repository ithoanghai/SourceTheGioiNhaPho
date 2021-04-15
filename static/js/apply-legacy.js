!function (t, e) {
    "use strict";
    "function" == typeof define && define.amd ? define(e) : "object" == typeof exports ? module.exports = e() : t.returnExports = e()
}(this, function () {
    var t, e, r = Array.prototype, n = Object.prototype, o = Function.prototype, i = String.prototype,
        a = Number.prototype, c = r.slice, u = r.splice, f = r.push, l = r.unshift, p = o.call, s = n.toString,
        h = Array.isArray || function (t) {
            return "[object Array]" === s.call(t)
        }, y = "function" == typeof Symbol && "symbol" == typeof Symbol.toStringTag, b = Function.prototype.toString,
        d = function (t) {
            try {
                b.call(t);
                return !0
            } catch (t) {
                return !1
            }
        }, g = "[object Function]", v = "[object GeneratorFunction]";
    t = function (t) {
        if ("function" != typeof t) return !1;
        if (y) return d(t);
        var e = s.call(t);
        return e === g || e === v
    };
    var O, j = RegExp.prototype.exec, w = function (t) {
        try {
            j.call(t);
            return !0
        } catch (t) {
            return !1
        }
    }, m = "[object RegExp]";
    e = function (t) {
        return "object" == typeof t && (y ? w(t) : s.call(t) === m)
    };
    var x = String.prototype.valueOf, _ = function (t) {
        try {
            x.call(t);
            return !0
        } catch (t) {
            return !1
        }
    }, S = "[object String]";
    O = function (t) {
        return "string" == typeof t || "object" == typeof t && (y ? _(t) : s.call(t) === S)
    };
    var T = function (e) {
        var r = "[object Arguments]" === s.call(e);
        r || (r = !h(e) && null !== e && "object" == typeof e && "number" == typeof e.length && e.length >= 0 && t(e.callee));
        return r
    }, E = function (t) {
        var e, r = Object.defineProperty && function () {
            try {
                Object.defineProperty({}, "x", {});
                return !0
            } catch (t) {
                return !1
            }
        }();
        e = r ? function (t, e, r, n) {
            !n && e in t || Object.defineProperty(t, e, {configurable: !0, enumerable: !1, writable: !0, value: r})
        } : function (t, e, r, n) {
            !n && e in t || (t[e] = r)
        };
        return function (r, n, o) {
            for (var i in n) t.call(n, i) && e(r, i, n[i], o)
        }
    }(n.hasOwnProperty), N = function (t) {
        var e = typeof t;
        return null === t || "object" !== e && "function" !== e
    }, P = {
        ToInteger: function (t) {
            var e = +t;
            e != e ? e = 0 : 0 !== e && e !== 1 / 0 && e !== -1 / 0 && (e = (e > 0 || -1) * Math.floor(Math.abs(e)));
            return e
        }, ToPrimitive: function (e) {
            var r, n, o;
            if (N(e)) return e;
            n = e.valueOf;
            if (t(n)) {
                r = n.call(e);
                if (N(r)) return r
            }
            o = e.toString;
            if (t(o)) {
                r = o.call(e);
                if (N(r)) return r
            }
            throw new TypeError
        }, ToObject: function (t) {
            if (null == t) throw new TypeError("can't convert " + t + " to object");
            return Object(t)
        }, ToUint32: function (t) {
            return t >>> 0
        }
    }, I = function () {
    };
    E(o, {
        bind: function (e) {
            var r = this;
            if (!t(r)) throw new TypeError("Function.prototype.bind called on incompatible " + r);
            for (var n, o = c.call(arguments, 1), i = function () {
                if (this instanceof n) {
                    var t = r.apply(this, o.concat(c.call(arguments)));
                    return Object(t) === t ? t : this
                }
                return r.apply(e, o.concat(c.call(arguments)))
            }, a = Math.max(0, r.length - o.length), u = [], f = 0; f < a; f++) u.push("$" + f);
            n = Function("binder", "return function (" + u.join(",") + "){ return binder.apply(this, arguments); }")(i);
            if (r.prototype) {
                I.prototype = r.prototype;
                n.prototype = new I;
                I.prototype = null
            }
            return n
        }
    });
    var D, F, M = p.bind(n.hasOwnProperty), C = (F = (D = [1, 2]).splice(), 2 === D.length && h(F) && 0 === F.length);
    E(r, {
        splice: function (t, e) {
            return 0 === arguments.length ? [] : u.apply(this, arguments)
        }
    }, !C);
    var J = function () {
        var t = {};
        r.splice.call(t, 0, 0, 1);
        return 1 === t.length
    }();
    E(r, {
        splice: function (t, e) {
            if (0 === arguments.length) return [];
            var r = arguments;
            this.length = Math.max(P.ToInteger(this.length), 0);
            arguments.length > 0 && "number" != typeof e && ((r = c.call(arguments)).length < 2 ? r.push(this.length - t) : r[1] = P.ToInteger(e));
            return u.apply(this, r)
        }
    }, !J);
    var U = 1 !== [].unshift(0);
    E(r, {
        unshift: function () {
            l.apply(this, arguments);
            return this.length
        }
    }, U);
    E(Array, {isArray: h});
    var k = Object("a"), A = "a" !== k[0] || !(0 in k), R = function (t) {
        var e = !0, r = !0;
        if (t) {
            t.call("foo", function (t, r, n) {
                "object" != typeof n && (e = !1)
            });
            t.call([1], function () {
                "use strict";
                r = "string" == typeof this
            }, "x")
        }
        return !!t && e && r
    };
    E(r, {
        forEach: function (e) {
            var r = P.ToObject(this), n = A && O(this) ? this.split("") : r, o = arguments[1], i = -1,
                a = n.length >>> 0;
            if (!t(e)) throw new TypeError;
            for (; ++i < a;) i in n && e.call(o, n[i], i, r)
        }
    }, !R(r.forEach));
    E(r, {
        map: function (e) {
            var r = P.ToObject(this), n = A && O(this) ? this.split("") : r, o = n.length >>> 0, i = Array(o),
                a = arguments[1];
            if (!t(e)) throw new TypeError(e + " is not a function");
            for (var c = 0; c < o; c++) c in n && (i[c] = e.call(a, n[c], c, r));
            return i
        }
    }, !R(r.map));
    E(r, {
        filter: function (e) {
            var r, n = P.ToObject(this), o = A && O(this) ? this.split("") : n, i = o.length >>> 0, a = [],
                c = arguments[1];
            if (!t(e)) throw new TypeError(e + " is not a function");
            for (var u = 0; u < i; u++) if (u in o) {
                r = o[u];
                e.call(c, r, u, n) && a.push(r)
            }
            return a
        }
    }, !R(r.filter));
    E(r, {
        every: function (e) {
            var r = P.ToObject(this), n = A && O(this) ? this.split("") : r, o = n.length >>> 0, i = arguments[1];
            if (!t(e)) throw new TypeError(e + " is not a function");
            for (var a = 0; a < o; a++) if (a in n && !e.call(i, n[a], a, r)) return !1;
            return !0
        }
    }, !R(r.every));
    E(r, {
        some: function (e) {
            var r = P.ToObject(this), n = A && O(this) ? this.split("") : r, o = n.length >>> 0, i = arguments[1];
            if (!t(e)) throw new TypeError(e + " is not a function");
            for (var a = 0; a < o; a++) if (a in n && e.call(i, n[a], a, r)) return !0;
            return !1
        }
    }, !R(r.some));
    var z = !1;
    r.reduce && (z = "object" == typeof r.reduce.call("es5", function (t, e, r, n) {
        return n
    }));
    E(r, {
        reduce: function (e) {
            var r = P.ToObject(this), n = A && O(this) ? this.split("") : r, o = n.length >>> 0;
            if (!t(e)) throw new TypeError(e + " is not a function");
            if (!o && 1 === arguments.length) throw new TypeError("reduce of empty array with no initial value");
            var i, a = 0;
            if (arguments.length >= 2) i = arguments[1]; else for (; ;) {
                if (a in n) {
                    i = n[a++];
                    break
                }
                if (++a >= o) throw new TypeError("reduce of empty array with no initial value")
            }
            for (; a < o; a++) a in n && (i = e.call(void 0, i, n[a], a, r));
            return i
        }
    }, !z);
    var Z = !1;
    r.reduceRight && (Z = "object" == typeof r.reduceRight.call("es5", function (t, e, r, n) {
        return n
    }));
    E(r, {
        reduceRight: function (e) {
            var r = P.ToObject(this), n = A && O(this) ? this.split("") : r, o = n.length >>> 0;
            if (!t(e)) throw new TypeError(e + " is not a function");
            if (!o && 1 === arguments.length) throw new TypeError("reduceRight of empty array with no initial value");
            var i, a = o - 1;
            if (arguments.length >= 2) i = arguments[1]; else for (; ;) {
                if (a in n) {
                    i = n[a--];
                    break
                }
                if (--a < 0) throw new TypeError("reduceRight of empty array with no initial value")
            }
            if (a < 0) return i;
            do {
                a in n && (i = e.call(void 0, i, n[a], a, r))
            } while (a--);
            return i
        }
    }, !Z);
    var $ = Array.prototype.indexOf && -1 !== [0, 1].indexOf(1, 2);
    E(r, {
        indexOf: function (t) {
            var e = A && O(this) ? this.split("") : P.ToObject(this), r = e.length >>> 0;
            if (!r) return -1;
            var n = 0;
            arguments.length > 1 && (n = P.ToInteger(arguments[1]));
            n = n >= 0 ? n : Math.max(0, r + n);
            for (; n < r; n++) if (n in e && e[n] === t) return n;
            return -1
        }
    }, $);
    var q = Array.prototype.lastIndexOf && -1 !== [0, 1].lastIndexOf(0, -3);
    E(r, {
        lastIndexOf: function (t) {
            var e = A && O(this) ? this.split("") : P.ToObject(this), r = e.length >>> 0;
            if (!r) return -1;
            var n = r - 1;
            arguments.length > 1 && (n = Math.min(n, P.ToInteger(arguments[1])));
            n = n >= 0 ? n : r - Math.abs(n);
            for (; n >= 0; n--) if (n in e && t === e[n]) return n;
            return -1
        }
    }, q);
    var G = !{toString: null}.propertyIsEnumerable("toString"), B = function () {
        }.propertyIsEnumerable("prototype"), H = !M("x", "0"),
        L = ["toString", "toLocaleString", "valueOf", "hasOwnProperty", "isPrototypeOf", "propertyIsEnumerable", "constructor"],
        Y = L.length;
    E(Object, {
        keys: function (e) {
            var r = t(e), n = T(e), o = null !== e && "object" == typeof e, i = o && O(e);
            if (!o && !r && !n) throw new TypeError("Object.keys called on a non-object");
            var a = [], c = B && r;
            if (i && H || n) for (var u = 0; u < e.length; ++u) a.push(String(u));
            if (!n) for (var f in e) c && "prototype" === f || !M(e, f) || a.push(String(f));
            if (G) for (var l = e.constructor, p = l && l.prototype === e, s = 0; s < Y; s++) {
                var h = L[s];
                p && "constructor" === h || !M(e, h) || a.push(h)
            }
            return a
        }
    });
    var W = Object.keys && function () {
        return 2 === Object.keys(arguments).length
    }(1, 2), X = Object.keys;
    E(Object, {
        keys: function (t) {
            return T(t) ? X(r.slice.call(t)) : X(t)
        }
    }, !W);
    var K = -621987552e5, Q = "-000001", V = Date.prototype.toISOString && -1 === new Date(K).toISOString().indexOf(Q);
    E(Date.prototype, {
        toISOString: function () {
            var t, e, r, n, o;
            if (!isFinite(this)) throw new RangeError("Date.prototype.toISOString called on non-finite value.");
            n = this.getUTCFullYear();
            o = this.getUTCMonth();
            n += Math.floor(o / 12);
            t = [(o = (o % 12 + 12) % 12) + 1, this.getUTCDate(), this.getUTCHours(), this.getUTCMinutes(), this.getUTCSeconds()];
            n = (n < 0 ? "-" : n > 9999 ? "+" : "") + ("00000" + Math.abs(n)).slice(0 <= n && n <= 9999 ? -4 : -6);
            e = t.length;
            for (; e--;) (r = t[e]) < 10 && (t[e] = "0" + r);
            return n + "-" + t.slice(0, 2).join("-") + "T" + t.slice(2).join(":") + "." + ("000" + this.getUTCMilliseconds()).slice(-3) + "Z"
        }
    }, V);
    (function () {
        try {
            return Date.prototype.toJSON && null === new Date(NaN).toJSON() && -1 !== new Date(K).toJSON().indexOf(Q) && Date.prototype.toJSON.call({
                toISOString: function () {
                    return !0
                }
            })
        } catch (t) {
            return !1
        }
    })() || (Date.prototype.toJSON = function (e) {
        var r = Object(this), n = P.ToPrimitive(r);
        if ("number" == typeof n && !isFinite(n)) return null;
        var o = r.toISOString;
        if (!t(o)) throw new TypeError("toISOString property is not callable");
        return o.call(r)
    });
    var tt = 1e15 === Date.parse("+033658-09-27T01:46:40.000Z"),
        et = !isNaN(Date.parse("2012-04-04T24:00:00.500Z")) || !isNaN(Date.parse("2012-11-31T23:59:59.000Z")),
        rt = isNaN(Date.parse("2000-01-01T00:00:00.000Z"));
    Date.parse && !rt && !et && tt || (Date = function (t) {
        var e = function e(r, n, o, i, a, c, u) {
                var f = arguments.length;
                if (this instanceof t) {
                    var l = 1 === f && String(r) === r ? new t(e.parse(r)) : f >= 7 ? new t(r, n, o, i, a, c, u) : f >= 6 ? new t(r, n, o, i, a, c) : f >= 5 ? new t(r, n, o, i, a) : f >= 4 ? new t(r, n, o, i) : f >= 3 ? new t(r, n, o) : f >= 2 ? new t(r, n) : f >= 1 ? new t(r) : new t;
                    E(l, {constructor: e}, !0);
                    return l
                }
                return t.apply(this, arguments)
            },
            r = new RegExp("^(\\d{4}|[+-]\\d{6})(?:-(\\d{2})(?:-(\\d{2})(?:T(\\d{2}):(\\d{2})(?::(\\d{2})(?:(\\.\\d{1,}))?)?(Z|(?:([-+])(\\d{2}):(\\d{2})))?)?)?)?$"),
            n = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365], o = function (t, e) {
                var r = e > 1 ? 1 : 0;
                return n[e] + Math.floor((t - 1969 + r) / 4) - Math.floor((t - 1901 + r) / 100) + Math.floor((t - 1601 + r) / 400) + 365 * (t - 1970)
            }, i = function (e) {
                return Number(new t(1970, 0, 1, 0, 0, 0, e))
            };
        for (var a in t) e[a] = t[a];
        e.now = t.now;
        e.UTC = t.UTC;
        e.prototype = t.prototype;
        e.prototype.constructor = Date;
        e.parse = function (e) {
            var n = r.exec(e);
            if (n) {
                var a, c = Number(n[1]), u = Number(n[2] || 1) - 1, f = Number(n[3] || 1) - 1, l = Number(n[4] || 0),
                    p = Number(n[5] || 0), s = Number(n[6] || 0), h = Math.floor(1e3 * Number(n[7] || 0)),
                    y = Boolean(n[4] && !n[8]), b = "-" === n[9] ? 1 : -1, d = Number(n[10] || 0),
                    g = Number(n[11] || 0);
                if (l < (p > 0 || s > 0 || h > 0 ? 24 : 25) && p < 60 && s < 60 && h < 1e3 && u > -1 && u < 12 && d < 24 && g < 60 && f > -1 && f < o(c, u + 1) - o(c, u)) {
                    a = 1e3 * (60 * ((a = 60 * (24 * (o(c, u) + f) + l + d * b)) + p + g * b) + s) + h;
                    y && (a = i(a));
                    if (-864e13 <= a && a <= 864e13) return a
                }
                return NaN
            }
            return t.parse.apply(this, arguments)
        };
        return e
    }(Date));
    Date.now || (Date.now = function () {
        return (new Date).getTime()
    });
    var nt = a.toFixed && ("0.000" !== 8e-5.toFixed(3) || "1" !== .9.toFixed(0) || "1.25" !== 1.255.toFixed(2) || "1000000000000000128" !== (0xde0b6b3a7640080).toFixed(0)),
        ot = {
            base: 1e7, size: 6, data: [0, 0, 0, 0, 0, 0], multiply: function (t, e) {
                for (var r = -1, n = e; ++r < ot.size;) {
                    n += t * ot.data[r];
                    ot.data[r] = n % ot.base;
                    n = Math.floor(n / ot.base)
                }
            }, divide: function (t) {
                for (var e = ot.size, r = 0; --e >= 0;) {
                    r += ot.data[e];
                    ot.data[e] = Math.floor(r / t);
                    r = r % t * ot.base
                }
            }, numToString: function () {
                for (var t = ot.size, e = ""; --t >= 0;) if ("" !== e || 0 === t || 0 !== ot.data[t]) {
                    var r = String(ot.data[t]);
                    "" === e ? e = r : e += "0000000".slice(0, 7 - r.length) + r
                }
                return e
            }, pow: function t(e, r, n) {
                return 0 === r ? n : r % 2 == 1 ? t(e, r - 1, n * e) : t(e * e, r / 2, n)
            }, log: function (t) {
                for (var e = 0, r = t; r >= 4096;) {
                    e += 12;
                    r /= 4096
                }
                for (; r >= 2;) {
                    e += 1;
                    r /= 2
                }
                return e
            }
        };
    E(a, {
        toFixed: function (t) {
            var e, r, n, o, i, a, c, u;
            if ((e = (e = Number(t)) != e ? 0 : Math.floor(e)) < 0 || e > 20) throw new RangeError("Number.toFixed called with invalid number of decimals");
            if ((r = Number(this)) != r) return "NaN";
            if (r <= -1e21 || r >= 1e21) return String(r);
            n = "";
            if (r < 0) {
                n = "-";
                r = -r
            }
            o = "0";
            if (r > 1e-21) {
                a = (i = ot.log(r * ot.pow(2, 69, 1)) - 69) < 0 ? r * ot.pow(2, -i, 1) : r / ot.pow(2, i, 1);
                a *= 4503599627370496;
                if ((i = 52 - i) > 0) {
                    ot.multiply(0, a);
                    c = e;
                    for (; c >= 7;) {
                        ot.multiply(1e7, 0);
                        c -= 7
                    }
                    ot.multiply(ot.pow(10, c, 1), 0);
                    c = i - 1;
                    for (; c >= 23;) {
                        ot.divide(1 << 23);
                        c -= 23
                    }
                    ot.divide(1 << c);
                    ot.multiply(1, 1);
                    ot.divide(2);
                    o = ot.numToString()
                } else {
                    ot.multiply(0, a);
                    ot.multiply(1 << -i, 0);
                    o = ot.numToString() + "0.00000000000000000000".slice(2, 2 + e)
                }
            }
            return o = e > 0 ? (u = o.length) <= e ? n + "0.0000000000000000000".slice(0, e - u + 2) + o : n + o.slice(0, u - e) + "." + o.slice(u - e) : n + o
        }
    }, nt);
    var it, at = i.split;
    2 !== "ab".split(/(?:ab)*/).length || 4 !== ".".split(/(.?)(.?)/).length || "t" === "tesst".split(/(s)*/)[1] || 4 !== "test".split(/(?:)/, -1).length || "".split(/.?/).length || ".".split(/()()/).length > 1 ? (it = void 0 === /()??/.exec("")[1], i.split = function (t, r) {
        var n = this;
        if (void 0 === t && 0 === r) return [];
        if (!e(t)) return at.call(this, t, r);
        var o, i, a, c, u = [],
            l = (t.ignoreCase ? "i" : "") + (t.multiline ? "m" : "") + (t.extended ? "x" : "") + (t.sticky ? "y" : ""),
            p = 0, s = new RegExp(t.source, l + "g");
        n += "";
        it || (o = new RegExp("^" + s.source + "$(?!\\s)", l));
        var h = void 0 === r ? -1 >>> 0 : P.ToUint32(r);
        i = s.exec(n);
        for (; i;) {
            if ((a = i.index + i[0].length) > p) {
                u.push(n.slice(p, i.index));
                !it && i.length > 1 && i[0].replace(o, function () {
                    for (var t = 1; t < arguments.length - 2; t++) void 0 === arguments[t] && (i[t] = void 0)
                });
                i.length > 1 && i.index < n.length && f.apply(u, i.slice(1));
                c = i[0].length;
                p = a;
                if (u.length >= h) break
            }
            s.lastIndex === i.index && s.lastIndex++;
            i = s.exec(n)
        }
        p === n.length ? !c && s.test("") || u.push("") : u.push(n.slice(p));
        return u.length > h ? u.slice(0, h) : u
    }) : "0".split(void 0, 0).length && (i.split = function (t, e) {
        return void 0 === t && 0 === e ? [] : at.call(this, t, e)
    });
    var ct = i.replace;
    (function () {
        var t = [];
        "x".replace(/x(.)?/g, function (e, r) {
            t.push(r)
        });
        return 1 === t.length && void 0 === t[0]
    })() || (i.replace = function (r, n) {
        var o = t(n), i = e(r) && /\)[*?]/.test(r.source);
        if (o && i) {
            var a = function (t) {
                var e = arguments.length, o = r.lastIndex;
                r.lastIndex = 0;
                var i = r.exec(t) || [];
                r.lastIndex = o;
                i.push(arguments[e - 2], arguments[e - 1]);
                return n.apply(this, i)
            };
            return ct.call(this, r, a)
        }
        return ct.call(this, r, n)
    });
    var ut = i.substr, ft = "".substr && "b" !== "0b".substr(-1);
    E(i, {
        substr: function (t, e) {
            var r = t;
            t < 0 && (r = Math.max(this.length + t, 0));
            return ut.call(this, r, e)
        }
    }, ft);
    var lt, pt, st = "\t\n\v\f\r   ᠎             　\u2028\u2029\ufeff", ht = "​", yt = "[" + st + "]",
        bt = new RegExp("^" + yt + yt + "*"), dt = new RegExp(yt + yt + "*$"), gt = i.trim && (st.trim() || !ht.trim());
    E(i, {
        trim: function () {
            if (void 0 === this || null === this) throw new TypeError("can't convert " + this + " to object");
            return String(this).replace(bt, "").replace(dt, "")
        }
    }, gt);
    8 === parseInt(st + "08") && 22 === parseInt(st + "0x16") || (parseInt = (lt = parseInt, pt = /^0[xX]/, function (t, e) {
        var r = String(t).trim(), n = Number(e) || (pt.test(r) ? 16 : 10);
        return lt(r, n)
    }))
});
!function (t, e) {
    "use strict";
    "function" == typeof define && define.amd ? define(e) : "object" == typeof exports ? module.exports = e() : t.returnExports = e()
}(this, function () {
    var t, e, r, n, o = Function.prototype.call, i = Object.prototype, a = o.bind(i.hasOwnProperty),
        c = a(i, "__defineGetter__");
    if (c) {
        t = o.bind(i.__defineGetter__);
        e = o.bind(i.__defineSetter__);
        r = o.bind(i.__lookupGetter__);
        n = o.bind(i.__lookupSetter__)
    }
    Object.getPrototypeOf || (Object.getPrototypeOf = function (t) {
        var e = t.__proto__;
        return e || null === e ? e : t.constructor ? t.constructor.prototype : i
    });
    var u = function (t) {
        try {
            t.sentinel = 0;
            return 0 === Object.getOwnPropertyDescriptor(t, "sentinel").value
        } catch (t) {
            return !1
        }
    };
    if (Object.defineProperty) {
        var f = u({});
        if (!("undefined" == typeof document || u(document.createElement("div"))) || !f) var l = Object.getOwnPropertyDescriptor
    }
    if (!Object.getOwnPropertyDescriptor || l) {
        var p = "Object.getOwnPropertyDescriptor called on a non-object: ";
        Object.getOwnPropertyDescriptor = function (t, e) {
            if ("object" != typeof t && "function" != typeof t || null === t) throw new TypeError(p + t);
            if (l) try {
                return l.call(Object, t, e)
            } catch (t) {
            }
            var o;
            if (!a(t, e)) return o;
            o = {enumerable: !0, configurable: !0};
            if (c) {
                var u = t.__proto__, f = t !== i;
                f && (t.__proto__ = i);
                var s = r(t, e), h = n(t, e);
                f && (t.__proto__ = u);
                if (s || h) {
                    s && (o.get = s);
                    h && (o.set = h);
                    return o
                }
            }
            o.value = t[e];
            o.writable = !0;
            return o
        }
    }
    Object.getOwnPropertyNames || (Object.getOwnPropertyNames = function (t) {
        return Object.keys(t)
    });
    if (!Object.create) {
        var s, h = !({__proto__: null} instanceof Object);
        s = h || "undefined" == typeof document ? function () {
            return {__proto__: null}
        } : function () {
            var t = document.createElement("iframe"), e = document.body || document.documentElement;
            t.style.display = "none";
            e.appendChild(t);
            t.src = "javascript:";
            var r = t.contentWindow.Object.prototype;
            e.removeChild(t);
            t = null;
            delete r.constructor;
            delete r.hasOwnProperty;
            delete r.propertyIsEnumerable;
            delete r.isPrototypeOf;
            delete r.toLocaleString;
            delete r.toString;
            delete r.valueOf;
            r.__proto__ = null;
            var n = function () {
            };
            n.prototype = r;
            s = function () {
                return new n
            };
            return new n
        };
        Object.create = function (t, e) {
            var r, n = function () {
            };
            if (null === t) r = s(); else {
                if ("object" != typeof t && "function" != typeof t) throw new TypeError("Object prototype may only be an Object or null");
                n.prototype = t;
                (r = new n).__proto__ = t
            }
            void 0 !== e && Object.defineProperties(r, e);
            return r
        }
    }
    var y, b = function (t) {
        try {
            Object.defineProperty(t, "sentinel", {});
            return "sentinel" in t
        } catch (t) {
            return !1
        }
    };
    if (Object.defineProperty) {
        var d = b({}), g = "undefined" == typeof document || b(document.createElement("div"));
        if (!d || !g) var v = Object.defineProperty, O = Object.defineProperties
    }
    if (!Object.defineProperty || v) {
        var j = "Property description must be an object: ", w = "Object.defineProperty called on non-object: ",
            m = "getters & setters can not be defined on this javascript engine";
        Object.defineProperty = function (o, a, u) {
            if ("object" != typeof o && "function" != typeof o || null === o) throw new TypeError(w + o);
            if ("object" != typeof u && "function" != typeof u || null === u) throw new TypeError(j + u);
            if (v) try {
                return v.call(Object, o, a, u)
            } catch (t) {
            }
            if ("value" in u) if (c && (r(o, a) || n(o, a))) {
                var f = o.__proto__;
                o.__proto__ = i;
                delete o[a];
                o[a] = u.value;
                o.__proto__ = f
            } else o[a] = u.value; else {
                if (!c) throw new TypeError(m);
                "get" in u && t(o, a, u.get);
                "set" in u && e(o, a, u.set)
            }
            return o
        }
    }
    Object.defineProperties && !O || (Object.defineProperties = function (t, e) {
        if (O) try {
            return O.call(Object, t, e)
        } catch (t) {
        }
        for (var r in e) a(e, r) && "__proto__" !== r && Object.defineProperty(t, r, e[r]);
        return t
    });
    Object.seal || (Object.seal = function (t) {
        if (Object(t) !== t) throw new TypeError("Object.seal can only be called on Objects.");
        return t
    });
    Object.freeze || (Object.freeze = function (t) {
        if (Object(t) !== t) throw new TypeError("Object.freeze can only be called on Objects.");
        return t
    });
    try {
        Object.freeze(function () {
        })
    } catch (t) {
        Object.freeze = (y = Object.freeze, function (t) {
            return "function" == typeof t ? t : y(t)
        })
    }
    Object.preventExtensions || (Object.preventExtensions = function (t) {
        if (Object(t) !== t) throw new TypeError("Object.preventExtensions can only be called on Objects.");
        return t
    });
    Object.isSealed || (Object.isSealed = function (t) {
        if (Object(t) !== t) throw new TypeError("Object.isSealed can only be called on Objects.");
        return !1
    });
    Object.isFrozen || (Object.isFrozen = function (t) {
        if (Object(t) !== t) throw new TypeError("Object.isFrozen can only be called on Objects.");
        return !1
    });
    Object.isExtensible || (Object.isExtensible = function (t) {
        if (Object(t) !== t) throw new TypeError("Object.isExtensible can only be called on Objects.");
        for (var e = ""; a(t, e);) e += "?";
        t[e] = !0;
        var r = a(t, e);
        delete t[e];
        return r
    })
});
"object" != typeof JSON && (JSON = {});
!function () {
    "use strict";
    var rx_one = /^[\],:{}\s]*$/, rx_two = /\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g,
        rx_three = /"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, rx_four = /(?:^|:|,)(?:\s*\[)+/g,
        rx_escapable = /[\\\"\u0000-\u001f\u007f-\u009f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,
        rx_dangerous = /[\u0000\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,
        gap, indent, meta, rep;

    function f(t) {
        return t < 10 ? "0" + t : t
    }

    function this_value() {
        return this.valueOf()
    }

    if ("function" != typeof Date.prototype.toJSON) {
        Date.prototype.toJSON = function () {
            return isFinite(this.valueOf()) ? this.getUTCFullYear() + "-" + f(this.getUTCMonth() + 1) + "-" + f(this.getUTCDate()) + "T" + f(this.getUTCHours()) + ":" + f(this.getUTCMinutes()) + ":" + f(this.getUTCSeconds()) + "Z" : null
        };
        Boolean.prototype.toJSON = this_value;
        Number.prototype.toJSON = this_value;
        String.prototype.toJSON = this_value
    }

    function quote(t) {
        rx_escapable.lastIndex = 0;
        return rx_escapable.test(t) ? '"' + t.replace(rx_escapable, function (t) {
            var e = meta[t];
            return "string" == typeof e ? e : "\\u" + ("0000" + t.charCodeAt(0).toString(16)).slice(-4)
        }) + '"' : '"' + t + '"'
    }

    function str(t, e) {
        var r, n, o, i, a, c = gap, u = e[t];
        u && "object" == typeof u && "function" == typeof u.toJSON && (u = u.toJSON(t));
        "function" == typeof rep && (u = rep.call(e, t, u));
        switch (typeof u) {
            case"string":
                return quote(u);
            case"number":
                return isFinite(u) ? String(u) : "null";
            case"boolean":
            case"null":
                return String(u);
            case"object":
                if (!u) return "null";
                gap += indent;
                a = [];
                if ("[object Array]" === Object.prototype.toString.apply(u)) {
                    i = u.length;
                    for (r = 0; r < i; r += 1) a[r] = str(r, u) || "null";
                    o = 0 === a.length ? "[]" : gap ? "[\n" + gap + a.join(",\n" + gap) + "\n" + c + "]" : "[" + a.join(",") + "]";
                    gap = c;
                    return o
                }
                if (rep && "object" == typeof rep) {
                    i = rep.length;
                    for (r = 0; r < i; r += 1) "string" == typeof rep[r] && (o = str(n = rep[r], u)) && a.push(quote(n) + (gap ? ": " : ":") + o)
                } else for (n in u) Object.prototype.hasOwnProperty.call(u, n) && (o = str(n, u)) && a.push(quote(n) + (gap ? ": " : ":") + o);
                o = 0 === a.length ? "{}" : gap ? "{\n" + gap + a.join(",\n" + gap) + "\n" + c + "}" : "{" + a.join(",") + "}";
                gap = c;
                return o
        }
    }

    if ("function" != typeof JSON.stringify) {
        meta = {"\b": "\\b", "\t": "\\t", "\n": "\\n", "\f": "\\f", "\r": "\\r", '"': '\\"', "\\": "\\\\"};
        JSON.stringify = function (t, e, r) {
            var n;
            gap = "";
            indent = "";
            if ("number" == typeof r) for (n = 0; n < r; n += 1) indent += " "; else "string" == typeof r && (indent = r);
            rep = e;
            if (e && "function" != typeof e && ("object" != typeof e || "number" != typeof e.length)) throw new Error("JSON.stringify");
            return str("", {"": t})
        }
    }
    "function" != typeof JSON.parse && (JSON.parse = function (text, reviver) {
        var j;

        function walk(t, e) {
            var r, n, o = t[e];
            if (o && "object" == typeof o) for (r in o) Object.prototype.hasOwnProperty.call(o, r) && (void 0 !== (n = walk(o, r)) ? o[r] = n : delete o[r]);
            return reviver.call(t, e, o)
        }

        text = String(text);
        rx_dangerous.lastIndex = 0;
        rx_dangerous.test(text) && (text = text.replace(rx_dangerous, function (t) {
            return "\\u" + ("0000" + t.charCodeAt(0).toString(16)).slice(-4)
        }));
        if (rx_one.test(text.replace(rx_two, "@").replace(rx_three, "]").replace(rx_four, ""))) {
            j = eval("(" + text + ")");
            return "function" == typeof reviver ? walk({"": j}, "") : j
        }
        throw new SyntaxError("JSON.parse")
    })
}();