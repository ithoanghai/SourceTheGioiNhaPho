try{!function(t,e){"object"==typeof exports&&"object"==typeof module?module.exports=e():"function"==typeof define&&define.amd?define("ZaloSocialSDK",[],e):"object"==typeof exports?exports.ZaloSocialSDK=e():t.ZaloSocialSDK=e()}(window,function(){return function(t){function e(i){if(n[i])return n[i].exports
var r=n[i]={i:i,l:!1,exports:{}}
return t[i].call(r.exports,r,r.exports,e),r.l=!0,r.exports}var n={}
return e.m=t,e.c=n,e.d=function(t,n,i){e.o(t,n)||Object.defineProperty(t,n,{enumerable:!0,get:i})},e.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},e.t=function(t,n){if(1&n&&(t=e(t)),8&n)return t
if(4&n&&"object"==typeof t&&t&&t.__esModule)return t
var i=Object.create(null)
if(e.r(i),Object.defineProperty(i,"default",{enumerable:!0,value:t}),2&n&&"string"!=typeof t)for(var r in t)e.d(i,r,function(e){return t[e]}.bind(null,r))
return i},e.n=function(t){var n=t&&t.__esModule?function(){return t["default"]}:function(){return t}
return e.d(n,"a",n),n},e.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},e.p="./",e(e.s=47)}([function(t,e,n){t.exports={"default":n(85),__esModule:!0}},function(t,e){var n=t.exports="undefined"!=typeof window&&window.Math==Math?window:"undefined"!=typeof self&&self.Math==Math?self:Function("return this")()
"number"==typeof __g&&(__g=n)},function(t,e){var n=t.exports={version:"2.5.3"}
"number"==typeof __e&&(__e=n)},function(t,e,n){var i=n(32)("wks"),r=n(33),o=n(1).Symbol,a="function"==typeof o;(t.exports=function(t){return i[t]||(i[t]=a&&o[t]||(a?o:r)("Symbol."+t))}).store=i},function(t,e,n){var i=n(1),r=n(2),o=n(10),a=n(6),s="prototype",l=function(t,e,n){var u,c,h,f=t&l.F,d=t&l.G,p=t&l.S,m=t&l.P,g=t&l.B,y=t&l.W,v=d?r:r[e]||(r[e]={}),w=v[s],x=d?i:p?i[e]:(i[e]||{})[s]
for(u in d&&(n=e),n)(c=!f&&x&&void 0!==x[u])&&u in v||(h=c?x[u]:n[u],v[u]=d&&"function"!=typeof x[u]?n[u]:g&&c?o(h,i):y&&x[u]==h?function(t){var e=function(e,n,i){if(this instanceof t){switch(arguments.length){case 0:return new t
case 1:return new t(e)
case 2:return new t(e,n)}return new t(e,n,i)}return t.apply(this,arguments)}
return e[s]=t[s],e}(h):m&&"function"==typeof h?o(Function.call,h):h,m&&((v.virtual||(v.virtual={}))[u]=h,t&l.R&&w&&!w[u]&&a(w,u,h)))}
l.F=1,l.G=2,l.S=4,l.P=8,l.B=16,l.W=32,l.U=64,l.R=128,t.exports=l},function(t,e,n){var i=n(11)
t.exports=function(t){if(!i(t))throw TypeError(t+" is not an object!")
return t}},function(t,e,n){var i=n(7),r=n(21)
t.exports=n(8)?function(t,e,n){return i.f(t,e,r(1,n))}:function(t,e,n){return t[e]=n,t}},function(t,e,n){var i=n(5),r=n(53),o=n(54),a=Object.defineProperty
e.f=n(8)?Object.defineProperty:function(t,e,n){if(i(t),e=o(e,!0),i(n),r)try{return a(t,e,n)}catch(t){}if("get"in n||"set"in n)throw TypeError("Accessors not supported!")
return"value"in n&&(t[e]=n.value),t}},function(t,e,n){t.exports=!n(19)(function(){return 7!=Object.defineProperty({},"a",{get:function(){return 7}}).a})},function(t,e,n){"use strict"
function i(t){return t&&t.__esModule?t:{"default":t}}Object.defineProperty(e,"__esModule",{value:!0})
var r=i(n(0)),o=i(n(89)),a=function(){function t(t,e){for(var n=0;n<e.length;n++){var i=e[n]
i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),(0,r["default"])(t,i.key,i)}}return function(e,n,i){return n&&t(e.prototype,n),i&&t(e,i),e}}(),s=function(){function t(){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t)}return a(t,null,[{key:"jsonToQueryString",value:function(t){return"?"+(0,o["default"])(t).map(function(e){return encodeURIComponent(e)+"="+encodeURIComponent(t[e])}).join("&")}}]),t}()
e["default"]=s},function(t,e,n){var i=n(13)
t.exports=function(t,e,n){if(i(t),void 0===e)return t
switch(n){case 1:return function(n){return t.call(e,n)}
case 2:return function(n,i){return t.call(e,n,i)}
case 3:return function(n,i,r){return t.call(e,n,i,r)}}return function(){return t.apply(e,arguments)}}},function(t,e){t.exports=function(t){return"object"==typeof t?null!==t:"function"==typeof t}},function(t,e){t.exports={}},function(t,e){t.exports=function(t){if("function"!=typeof t)throw TypeError(t+" is not a function!")
return t}},function(t,e){var n={}.hasOwnProperty
t.exports=function(t,e){return n.call(t,e)}},function(t,e){var n={}.toString
t.exports=function(t){return n.call(t).slice(8,-1)}},function(t,e,n){"use strict"
Object.defineProperty(e,"__esModule",{value:!0})
var i,r=n(0),o=(i=r)&&i.__esModule?i:{"default":i},a=function(){function t(t,e){for(var n=0;n<e.length;n++){var i=e[n]
i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),(0,o["default"])(t,i.key,i)}}return function(e,n,i){return n&&t(e.prototype,n),i&&t(e,i),e}}(),s=function(){function t(){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t)}return a(t,null,[{key:"isAndroid",value:function(){var t=navigator.userAgent||navigator.vendor||window.opera
return!!/android/i.test(t)}},{key:"isIOS",value:function(){var t=navigator.userAgent||navigator.vendor||window.opera
return!(!/iPad|iPhone|iPod/.test(t)||window.MSStream)}},{key:"isMobile",value:function(){var t,e=!1
return t=navigator.userAgent||navigator.vendor||window.opera,(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(t)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(t.substr(0,4)))&&(e=!0),e}}]),t}()
e["default"]=s},function(t,e){var n=Math.ceil,i=Math.floor
t.exports=function(t){return isNaN(t=+t)?0:(t>0?i:n)(t)}},function(t,e){t.exports=function(t){if(null==t)throw TypeError("Can't call method on  "+t)
return t}},function(t,e){t.exports=function(t){try{return!!t()}catch(t){return!0}}},function(t,e,n){var i=n(11),r=n(1).document,o=i(r)&&i(r.createElement)
t.exports=function(t){return o?r.createElement(t):{}}},function(t,e){t.exports=function(t,e){return{enumerable:!(1&t),configurable:!(2&t),writable:!(4&t),value:e}}},function(t,e,n){var i=n(60),r=n(18)
t.exports=function(t){return i(r(t))}},function(t,e,n){var i=n(17),r=Math.min
t.exports=function(t){return t>0?r(i(t),9007199254740991):0}},function(t,e,n){var i=n(32)("keys"),r=n(33)
t.exports=function(t){return i[t]||(i[t]=r(t))}},function(t,e,n){var i=n(7).f,r=n(14),o=n(3)("toStringTag")
t.exports=function(t,e,n){t&&!r(t=n?t:t.prototype,o)&&i(t,o,{configurable:!0,value:e})}},function(t,e,n){var i=n(18)
t.exports=function(t){return Object(i(t))}},function(t,e,n){"use strict"
var i=n(13)
t.exports.f=function(t){return new function(t){var e,n
this.promise=new t(function(t,i){if(void 0!==e||void 0!==n)throw TypeError("Bad Promise constructor")
e=t,n=i}),this.resolve=i(e),this.reject=i(n)}(t)}},function(t,e,n){"use strict"
var i=n(52)(!0)
n(29)(String,"String",function(t){this._t=t+"",this._i=0},function(){var t,e=this._t,n=this._i
return n>=e.length?{value:void 0,done:!0}:(t=i(e,n),this._i+=t.length,{value:t,done:!1})})},function(t,e,n){"use strict"
var i=n(30),r=n(4),o=n(55),a=n(6),s=n(14),l=n(12),u=n(56),c=n(25),h=n(63),f=n(3)("iterator"),d=!([].keys&&"next"in[].keys()),p="values",m=function(){return this}
t.exports=function(t,e,n,g,y,v,w){u(n,e,g)
var x,b,_,B=function(t){if(!d&&t in S)return S[t]
switch(t){case"keys":case p:return function(){return new n(this,t)}}return function(){return new n(this,t)}},k=e+" Iterator",E=y==p,T=!1,S=t.prototype,P=S[f]||S["@@iterator"]||y&&S[y],A=!d&&P||B(y),R=y?E?B("entries"):A:void 0,z="Array"==e&&S.entries||P
if(z&&(_=h(z.call(new t)))!==Object.prototype&&_.next&&(c(_,k,!0),i||s(_,f)||a(_,f,m)),E&&P&&P.name!==p&&(T=!0,A=function(){return P.call(this)}),i&&!w||!d&&!T&&S[f]||a(S,f,A),l[e]=A,l[k]=m,y)if(x={values:E?A:B(p),keys:v?A:B("keys"),entries:R},w)for(b in x)b in S||o(S,b,x[b])
else r(r.P+r.F*(d||T),e,x)
return x}},function(t,e){t.exports=!0},function(t,e,n){var i=n(59),r=n(34)
t.exports=Object.keys||function(t){return i(t,r)}},function(t,e,n){var i=n(1),r="__core-js_shared__",o=i[r]||(i[r]={})
t.exports=function(t){return o[t]||(o[t]={})}},function(t,e){var n=0,i=Math.random()
t.exports=function(t){return"Symbol(".concat(void 0===t?"":t,")_",(++n+i).toString(36))}},function(t,e){t.exports="constructor,hasOwnProperty,isPrototypeOf,propertyIsEnumerable,toLocaleString,toString,valueOf".split(",")},function(t,e,n){var i=n(1).document
t.exports=i&&i.documentElement},function(t,e,n){var i=n(15),r=n(3)("toStringTag"),o="Arguments"==i(function(){return arguments}())
t.exports=function(t){var e,n,a
return void 0===t?"Undefined":null===t?"Null":"string"==typeof(n=function(t,e){try{return t[e]}catch(t){}}(e=Object(t),r))?n:o?i(e):"Object"==(a=i(e))&&"function"==typeof e.callee?"Arguments":a}},function(t,e,n){var i=n(5)
t.exports=function(t,e,n,r){try{return r?e(i(n)[0],n[1]):e(n)}catch(e){var o=t["return"]
throw void 0!==o&&i(o.call(t)),e}}},function(t,e,n){var i=n(12),r=n(3)("iterator"),o=Array.prototype
t.exports=function(t){return void 0!==t&&(i.Array===t||o[r]===t)}},function(t,e,n){var i=n(36),r=n(3)("iterator"),o=n(12)
t.exports=n(2).getIteratorMethod=function(t){return null!=t?t[r]||t["@@iterator"]||o[i(t)]:void 0}},function(t,e,n){var i=n(5),r=n(13),o=n(3)("species")
t.exports=function(t,e){var n,a=i(t).constructor
return void 0===a||null==(n=i(a)[o])?e:r(n)}},function(t,e,n){var i,r,o,a=n(10),s=n(71),l=n(35),u=n(20),c=n(1),h=c.process,f=c.setImmediate,d=c.clearImmediate,p=c.MessageChannel,m=c.Dispatch,g=0,y={},v="onreadystatechange",w=function(){var t=+this
if(y.hasOwnProperty(t)){var e=y[t]
delete y[t],e()}},x=function(t){w.call(t.data)}
f&&d||(f=function(t){for(var e=[],n=1;arguments.length>n;)e.push(arguments[n++])
return y[++g]=function(){s("function"==typeof t?t:Function(t),e)},i(g),g},d=function(t){delete y[t]},"process"==n(15)(h)?i=function(t){h.nextTick(a(w,t,1))}:m&&m.now?i=function(t){m.now(a(w,t,1))}:p?(o=(r=new p).port2,r.port1.onmessage=x,i=a(o.postMessage,o,1)):c.addEventListener&&"function"==typeof postMessage&&!c.importScripts?(i=function(t){c.postMessage(t+"","*")},c.addEventListener("message",x,!1)):i=v in u("script")?function(t){l.appendChild(u("script"))[v]=function(){l.removeChild(this),w.call(t)}}:function(t){setTimeout(a(w,t,1),0)}),t.exports={set:f,clear:d}},function(t,e){t.exports=function(t){try{return{e:!1,v:t()}}catch(t){return{e:!0,v:t}}}},function(t,e,n){var i=n(5),r=n(11),o=n(27)
t.exports=function(t,e){if(i(t),r(e)&&e.constructor===t)return e
var n=o.f(t)
return(0,n.resolve)(e),n.promise}},function(t,e,n){var i=n(3)("iterator"),r=!1
try{var o=[7][i]()
o["return"]=function(){r=!0},Array.from(o,function(){throw 2})}catch(t){}t.exports=function(t,e){if(!e&&!r)return!1
var n=!1
try{var o=[7],a=o[i]()
a.next=function(){return{done:n=!0}},o[i]=function(){return a},t(o)}catch(t){}return n}},function(t,e,n){t.exports={"default":n(87),__esModule:!0}},function(t,e){var n
n=function(){return this}()
try{n=n||Function("return this")()}catch(t){"object"==typeof window&&(n=window)}t.exports=n},function(t,e,n){t.exports=n(48)},function(t,e,n){"use strict"
function i(t){return t&&t.__esModule?t:{"default":t}}Object.defineProperty(e,"__esModule",{value:!0})
var r=i(n(49)),o=i(n(77))
e.init=function(){l.init()},e.reload=function(){c&&clearInterval(c),l.reload()},e.openChatWidget=function(){l.openChatWidget()},e.closeChatWidget=function(){l.closeChatWidget()}
var a=i(n(80)),s=i(n(107)),l=new a["default"]
l.init()
var u,c=void 0;(u=o["default"].mark(function h(){return o["default"].wrap(function(t){for(;;)switch(t.prev=t.next){case 0:c=setInterval(function(){l.retry()},1e3),setTimeout(function(){c&&clearInterval(c)},5e3)
case 2:case"end":return t.stop()}},h,this)}),function(){return u.apply(this,arguments),new r["default"](function(t,e){return function n(i,o){try{var a=l[i](o),s=a.value}catch(l){return void e(l)}return a.done?void t(s):r["default"].resolve(s).then(function(t){n("next",t)},function(t){n("throw",t)})}("next")})})(),"news.zing.vn"!=window.location.hostname&&function(){try{if(window.self==window.top){var t=document.createElement("div")
if(t.id="app",t.className="zs",document.body.appendChild(t),/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent));else{var e=window.location.hostname
"news.zing.vn"!==e&&"mp3.zing.vn"!==e||setTimeout(function(){s["default"].loadFile("https://sp-zp.zdn.vn/chatbutton/main-1.2.2.js","js"),s["default"].loadFile("https://sp-zp.zdn.vn/chatbutton/main.142b31d74cee2e25afe3651f0591f9f4.css","css")},100)}}}catch(t){console.log("")}}()},function(t,e,n){t.exports={"default":n(50),__esModule:!0}},function(t,e,n){n(51),n(28),n(64),n(68),n(75),n(76),t.exports=n(2).Promise},function(t,e){},function(t,e,n){var i=n(17),r=n(18)
t.exports=function(t){return function(e,n){var o,a,s=r(e)+"",l=i(n),u=s.length
return 0>l||l>=u?t?"":void 0:(o=s.charCodeAt(l))<55296||o>56319||l+1===u||(a=s.charCodeAt(l+1))<56320||a>57343?t?s.charAt(l):o:t?s.slice(l,l+2):a-56320+(o-55296<<10)+65536}}},function(t,e,n){t.exports=!n(8)&&!n(19)(function(){return 7!=Object.defineProperty(n(20)("div"),"a",{get:function(){return 7}}).a})},function(t,e,n){var i=n(11)
t.exports=function(t,e){if(!i(t))return t
var n,r
if(e&&"function"==typeof(n=t.toString)&&!i(r=n.call(t)))return r
if("function"==typeof(n=t.valueOf)&&!i(r=n.call(t)))return r
if(!e&&"function"==typeof(n=t.toString)&&!i(r=n.call(t)))return r
throw TypeError("Can't convert object to primitive value")}},function(t,e,n){t.exports=n(6)},function(t,e,n){"use strict"
var i=n(57),r=n(21),o=n(25),a={}
n(6)(a,n(3)("iterator"),function(){return this}),t.exports=function(t,e,n){t.prototype=i(a,{next:r(1,n)}),o(t,e+" Iterator")}},function(t,e,n){var i=n(5),r=n(58),o=n(34),a=n(24)("IE_PROTO"),s=function(){},l="prototype",u=function(){var t,e=n(20)("iframe"),i=o.length
for(e.style.display="none",n(35).appendChild(e),e.src="javascript:",(t=e.contentWindow.document).open(),t.write("<script>document.F=Object</script>"),t.close(),u=t.F;i--;)delete u[l][o[i]]
return u()}
t.exports=Object.create||function(t,e){var n
return null!==t?(s[l]=i(t),n=new s,s[l]=null,n[a]=t):n=u(),void 0===e?n:r(n,e)}},function(t,e,n){var i=n(7),r=n(5),o=n(31)
t.exports=n(8)?Object.defineProperties:function(t,e){r(t)
for(var n,a=o(e),s=a.length,l=0;s>l;)i.f(t,n=a[l++],e[n])
return t}},function(t,e,n){var i=n(14),r=n(22),o=n(61)(!1),a=n(24)("IE_PROTO")
t.exports=function(t,e){var n,s=r(t),l=0,u=[]
for(n in s)n!=a&&i(s,n)&&u.push(n)
for(;e.length>l;)i(s,n=e[l++])&&(~o(u,n)||u.push(n))
return u}},function(t,e,n){var i=n(15)
t.exports=Object("z").propertyIsEnumerable(0)?Object:function(t){return"String"==i(t)?t.split(""):Object(t)}},function(t,e,n){var i=n(22),r=n(23),o=n(62)
t.exports=function(t){return function(e,n,a){var s,l=i(e),u=r(l.length),c=o(a,u)
if(t&&n!=n){for(;u>c;)if((s=l[c++])!=s)return!0}else for(;u>c;c++)if((t||c in l)&&l[c]===n)return t||c||0
return!t&&-1}}},function(t,e,n){var i=n(17),r=Math.max,o=Math.min
t.exports=function(t,e){return(t=i(t))<0?r(t+e,0):o(t,e)}},function(t,e,n){var i=n(14),r=n(26),o=n(24)("IE_PROTO"),a=Object.prototype
t.exports=Object.getPrototypeOf||function(t){return t=r(t),i(t,o)?t[o]:"function"==typeof t.constructor&&t instanceof t.constructor?t.constructor.prototype:t instanceof Object?a:null}},function(t,e,n){n(65)
for(var i=n(1),r=n(6),o=n(12),a=n(3)("toStringTag"),s="CSSRuleList,CSSStyleDeclaration,CSSValueList,ClientRectList,DOMRectList,DOMStringList,DOMTokenList,DataTransferItemList,FileList,HTMLAllCollection,HTMLCollection,HTMLFormElement,HTMLSelectElement,MediaList,MimeTypeArray,NamedNodeMap,NodeList,PaintRequestList,Plugin,PluginArray,SVGLengthList,SVGNumberList,SVGPathSegList,SVGPointList,SVGStringList,SVGTransformList,SourceBufferList,StyleSheetList,TextTrackCueList,TextTrackList,TouchList".split(","),l=0;l<s.length;l++){var u=s[l],c=i[u],h=c&&c.prototype
h&&!h[a]&&r(h,a,u),o[u]=o.Array}},function(t,e,n){"use strict"
var i=n(66),r=n(67),o=n(12),a=n(22)
t.exports=n(29)(Array,"Array",function(t,e){this._t=a(t),this._i=0,this._k=e},function(){var t=this._t,e=this._k,n=this._i++
return!t||n>=t.length?(this._t=void 0,r(1)):r(0,"keys"==e?n:"values"==e?t[n]:[n,t[n]])},"values"),o.Arguments=o.Array,i("keys"),i("values"),i("entries")},function(t,e){t.exports=function(){}},function(t,e){t.exports=function(t,e){return{value:e,done:!!t}}},function(t,e,n){"use strict"
var i,r,o,a,s=n(30),l=n(1),u=n(10),c=n(36),h=n(4),f=n(11),d=n(13),p=n(69),m=n(70),g=n(40),y=n(41).set,v=n(72)(),w=n(27),x=n(42),b=n(43),_="Promise",B=l.TypeError,k=l.process,E=l[_],T="process"==c(k),S=function(){},P=r=w.f,A=!!function(){try{var t=E.resolve(1),e=(t.constructor={})[n(3)("species")]=function(t){t(S,S)}
return(T||"function"==typeof PromiseRejectionEvent)&&t.then(S)instanceof e}catch(t){}}(),R=function(t){var e
return!(!f(t)||"function"!=typeof(e=t.then))&&e},z=function(t,e){if(!t._n){t._n=!0
var n=t._c
v(function(){for(var i=t._v,r=1==t._s,o=0,a=function(t){var e,n,o=r?t.ok:t.fail,a=t.resolve,s=t.reject,l=t.domain
try{o?(r||(2==u._h&&L(u),u._h=1),!0===o?e=i:(l&&l.enter(),e=o(i),l&&l.exit()),e===t.promise?s(B("Promise-chain cycle")):(n=R(e))?n.call(e,a,s):a(e)):s(i)}catch(u){s(u)}};n.length>o;)a(n[o++])
t._c=[],t._n=!1,e&&!t._h&&I(t)})}},I=function(t){y.call(l,function(){var e,n,i,r=t._v,o=C(t)
if(o&&(e=x(function(){T?k.emit("unhandledRejection",r,t):(n=l.onunhandledrejection)?n({promise:t,reason:r}):(i=l.console)&&i.error&&i.error("Unhandled promise rejection",r)}),t._h=T||C(t)?2:1),t._a=void 0,o&&e.e)throw e.v})},C=function(t){return 1!==t._h&&0===(t._a||t._c).length},L=function(t){y.call(l,function(){var e
T?k.emit("rejectionHandled",t):(e=l.onrejectionhandled)&&e({promise:t,reason:t._v})})},O=function(t){var e=this
e._d||(e._d=!0,(e=e._w||e)._v=t,e._s=2,e._a||(e._a=e._c.slice()),z(e,!0))},M=function(t){var e,n=this
if(!n._d){n._d=!0,n=n._w||n
try{if(n===t)throw B("Promise can't be resolved itself");(e=R(t))?v(function(){var t={_w:n,_d:!1}
try{e.call(i,u(M,t,1),u(O,t,1))}catch(i){O.call(t,i)}}):(n._v=t,n._s=1,z(n,!1))}catch(t){O.call({_w:n,_d:!1},t)}}}
A||(E=function(t){p(this,E,_,"_h"),d(t),i.call(this)
try{t(u(M,this,1),u(O,this,1))}catch(t){O.call(this,t)}},(i=function(t){this._c=[],this._a=void 0,this._s=0,this._d=!1,this._v=void 0,this._h=0,this._n=!1}).prototype=n(73)(E.prototype,{then:function(t,e){var n=P(g(this,E))
return n.ok="function"!=typeof t||t,n.fail="function"==typeof e&&e,n.domain=T?k.domain:void 0,this._c.push(n),this._a&&this._a.push(n),this._s&&z(this,!1),n.promise},"catch":function(t){return this.then(void 0,t)}}),o=function(){var t=new i
this.promise=t,this.resolve=u(M,t,1),this.reject=u(O,t,1)},w.f=P=function(t){return t===E||t===a?new o(t):r(t)}),h(h.G+h.W+h.F*!A,{Promise:E}),n(25)(E,_),n(74)(_),a=n(2)[_],h(h.S+h.F*!A,_,{reject:function(t){var e=P(this)
return(0,e.reject)(t),e.promise}}),h(h.S+h.F*(s||!A),_,{resolve:function(t){return b(s&&this===a?E:this,t)}}),h(h.S+h.F*!(A&&n(44)(function(t){E.all(t)["catch"](S)})),_,{all:function(t){var e=this,n=P(e),i=n.resolve,r=n.reject,o=x(function(){var n=[],o=0,a=1
m(t,!1,function(t){var s=o++,l=!1
n.push(void 0),a++,e.resolve(t).then(function(t){l||(l=!0,n[s]=t,--a||i(n))},r)}),--a||i(n)})
return o.e&&r(o.v),n.promise},race:function(t){var e=this,n=P(e),i=n.reject,r=x(function(){m(t,!1,function(t){e.resolve(t).then(n.resolve,i)})})
return r.e&&i(r.v),n.promise}})},function(t,e){t.exports=function(t,e,n,i){if(!(t instanceof e)||void 0!==i&&i in t)throw TypeError(n+": incorrect invocation!")
return t}},function(t,e,n){var i=n(10),r=n(37),o=n(38),a=n(5),s=n(23),l=n(39),u={},c={};(e=t.exports=function(t,e,n,h,f){var d,p,m,g,y=f?function(){return t}:l(t),v=i(n,h,e?2:1),w=0
if("function"!=typeof y)throw TypeError(t+" is not iterable!")
if(o(y)){for(d=s(t.length);d>w;w++)if((g=e?v(a(p=t[w])[0],p[1]):v(t[w]))===u||g===c)return g}else for(m=y.call(t);!(p=m.next()).done;)if((g=r(m,v,p.value,e))===u||g===c)return g}).BREAK=u,e.RETURN=c},function(t,e){t.exports=function(t,e,n){var i=void 0===n
switch(e.length){case 0:return i?t():t.call(n)
case 1:return i?t(e[0]):t.call(n,e[0])
case 2:return i?t(e[0],e[1]):t.call(n,e[0],e[1])
case 3:return i?t(e[0],e[1],e[2]):t.call(n,e[0],e[1],e[2])
case 4:return i?t(e[0],e[1],e[2],e[3]):t.call(n,e[0],e[1],e[2],e[3])}return t.apply(n,e)}},function(t,e,n){var i=n(1),r=n(41).set,o=i.MutationObserver||i.WebKitMutationObserver,a=i.process,s=i.Promise,l="process"==n(15)(a)
t.exports=function(){var t,e,n,u=function(){var i,r
for(l&&(i=a.domain)&&i.exit();t;){r=t.fn,t=t.next
try{r()}catch(i){throw t?n():e=void 0,i}}e=void 0,i&&i.enter()}
if(l)n=function(){a.nextTick(u)}
else if(!o||i.navigator&&i.navigator.standalone)if(s&&s.resolve){var c=s.resolve()
n=function(){c.then(u)}}else n=function(){r.call(i,u)}
else{var h=!0,f=document.createTextNode("")
new o(u).observe(f,{characterData:!0}),n=function(){f.data=h=!h}}return function(i){var r={fn:i,next:void 0}
e&&(e.next=r),t||(t=r,n()),e=r}}},function(t,e,n){var i=n(6)
t.exports=function(t,e,n){for(var r in e)n&&t[r]?t[r]=e[r]:i(t,r,e[r])
return t}},function(t,e,n){"use strict"
var i=n(1),r=n(2),o=n(7),a=n(8),s=n(3)("species")
t.exports=function(t){var e="function"==typeof r[t]?r[t]:i[t]
a&&e&&!e[s]&&o.f(e,s,{configurable:!0,get:function(){return this}})}},function(t,e,n){"use strict"
var i=n(4),r=n(2),o=n(1),a=n(40),s=n(43)
i(i.P+i.R,"Promise",{"finally":function(t){var e=a(this,r.Promise||o.Promise),n="function"==typeof t
return this.then(n?function(n){return s(e,t()).then(function(){return n})}:t,n?function(n){return s(e,t()).then(function(){throw n})}:t)}})},function(t,e,n){"use strict"
var i=n(4),r=n(27),o=n(42)
i(i.S,"Promise",{"try":function(t){var e=r.f(this),n=o(t)
return(n.e?e.reject:e.resolve)(n.v),e.promise}})},function(t,e,n){t.exports=n(78)},function(t,e,n){var i=function(){return this}()||Function("return this")(),r=i.regeneratorRuntime&&Object.getOwnPropertyNames(i).indexOf("regeneratorRuntime")>=0,o=r&&i.regeneratorRuntime
if(i.regeneratorRuntime=void 0,t.exports=n(79),r)i.regeneratorRuntime=o
else try{delete i.regeneratorRuntime}catch(t){i.regeneratorRuntime=void 0}},function(t,e){!function(e){"use strict"
function n(t,e,n,o){var a,s,l,c,h=e&&e.prototype instanceof r?e:r,d=Object.create(h.prototype),m=new f(o||[])
return d._invoke=(a=t,s=n,l=m,c=k,function(t,e){if(c===T)throw Error("Generator is already running")
if(c===S){if("throw"===t)throw e
return p()}for(l.method=t,l.arg=e;;){var n=l.delegate
if(n){var r=u(n,l)
if(r){if(r===P)continue
return r}}if("next"===l.method)l.sent=l._sent=l.arg
else if("throw"===l.method){if(c===k)throw c=S,l.arg
l.dispatchException(l.arg)}else"return"===l.method&&l.abrupt("return",l.arg)
c=T
var o=i(a,s,l)
if("normal"===o.type){if(c=l.done?S:E,o.arg===P)continue
return{value:o.arg,done:l.done}}"throw"===o.type&&(c=S,l.method="throw",l.arg=o.arg)}}),d}function i(t,e,n){try{return{type:"normal",arg:t.call(e,n)}}catch(t){return{type:"throw",arg:t}}}function r(){}function o(){}function a(){}function s(t){["next","throw","return"].forEach(function(e){t[e]=function(t){return this._invoke(e,t)}})}function l(t){var e
this._invoke=function(n,r){function o(){return new Promise(function(e,o){!function a(e,n,r,o){var s=i(t[e],t,n)
if("throw"!==s.type){var l=s.arg,u=l.value
return u&&"object"==typeof u&&y.call(u,"__await")?Promise.resolve(u.__await).then(function(t){a("next",t,r,o)},function(t){a("throw",t,r,o)}):Promise.resolve(u).then(function(t){l.value=t,r(l)},o)}o(s.arg)}(n,r,e,o)})}return e=e?e.then(o,o):o()}}function u(t,e){var n=t.iterator[e.method]
if(n===m){if(e.delegate=null,"throw"===e.method){if(t.iterator["return"]&&(e.method="return",e.arg=m,u(t,e),"throw"===e.method))return P
e.method="throw",e.arg=new TypeError("The iterator does not provide a 'throw' method")}return P}var r=i(n,t.iterator,e.arg)
if("throw"===r.type)return e.method="throw",e.arg=r.arg,e.delegate=null,P
var o=r.arg
return o?o.done?(e[t.resultName]=o.value,e.next=t.nextLoc,"return"!==e.method&&(e.method="next",e.arg=m),e.delegate=null,P):o:(e.method="throw",e.arg=new TypeError("iterator result is not an object"),e.delegate=null,P)}function c(t){var e={tryLoc:t[0]}
1 in t&&(e.catchLoc=t[1]),2 in t&&(e.finallyLoc=t[2],e.afterLoc=t[3]),this.tryEntries.push(e)}function h(t){var e=t.completion||{}
e.type="normal",delete e.arg,t.completion=e}function f(t){this.tryEntries=[{tryLoc:"root"}],t.forEach(c,this),this.reset(!0)}function d(t){if(t){var e=t[w]
if(e)return e.call(t)
if("function"==typeof t.next)return t
if(!isNaN(t.length)){var n=-1,i=function r(){for(;++n<t.length;)if(y.call(t,n))return r.value=t[n],r.done=!1,r
return r.value=m,r.done=!0,r}
return i.next=i}}return{next:p}}function p(){return{value:m,done:!0}}var m,g=Object.prototype,y=g.hasOwnProperty,v="function"==typeof Symbol?Symbol:{},w=v.iterator||"@@iterator",x=v.asyncIterator||"@@asyncIterator",b=v.toStringTag||"@@toStringTag",_="object"==typeof t,B=e.regeneratorRuntime
if(B)_&&(t.exports=B)
else{(B=e.regeneratorRuntime=_?t.exports:{}).wrap=n
var k="suspendedStart",E="suspendedYield",T="executing",S="completed",P={},A={}
A[w]=function(){return this}
var R=Object.getPrototypeOf,z=R&&R(R(d([])))
z&&z!==g&&y.call(z,w)&&(A=z)
var I=a.prototype=r.prototype=Object.create(A)
o.prototype=I.constructor=a,a.constructor=o,a[b]=o.displayName="GeneratorFunction",B.isGeneratorFunction=function(t){var e="function"==typeof t&&t.constructor
return!!e&&(e===o||"GeneratorFunction"===(e.displayName||e.name))},B.mark=function(t){return Object.setPrototypeOf?Object.setPrototypeOf(t,a):(t.__proto__=a,b in t||(t[b]="GeneratorFunction")),t.prototype=Object.create(I),t},B.awrap=function(t){return{__await:t}},s(l.prototype),l.prototype[x]=function(){return this},B.AsyncIterator=l,B.async=function(t,e,i,r){var o=new l(n(t,e,i,r))
return B.isGeneratorFunction(e)?o:o.next().then(function(t){return t.done?t.value:o.next()})},s(I),I[b]="Generator",I[w]=function(){return this},I.toString=function(){return"[object Generator]"},B.keys=function(t){var e=[]
for(var n in t)e.push(n)
return e.reverse(),function i(){for(;e.length;){var n=e.pop()
if(n in t)return i.value=n,i.done=!1,i}return i.done=!0,i}},B.values=d,f.prototype={constructor:f,reset:function(t){if(this.prev=0,this.next=0,this.sent=this._sent=m,this.done=!1,this.delegate=null,this.method="next",this.arg=m,this.tryEntries.forEach(h),!t)for(var e in this)"t"===e.charAt(0)&&y.call(this,e)&&!isNaN(+e.slice(1))&&(this[e]=m)},stop:function(){this.done=!0
var t=this.tryEntries[0].completion
if("throw"===t.type)throw t.arg
return this.rval},dispatchException:function(t){function e(e,i){return o.type="throw",o.arg=t,n.next=e,i&&(n.method="next",n.arg=m),!!i}if(this.done)throw t
for(var n=this,i=this.tryEntries.length-1;i>=0;--i){var r=this.tryEntries[i],o=r.completion
if("root"===r.tryLoc)return e("end")
if(r.tryLoc<=this.prev){var a=y.call(r,"catchLoc"),s=y.call(r,"finallyLoc")
if(a&&s){if(this.prev<r.catchLoc)return e(r.catchLoc,!0)
if(this.prev<r.finallyLoc)return e(r.finallyLoc)}else if(a){if(this.prev<r.catchLoc)return e(r.catchLoc,!0)}else{if(!s)throw Error("try statement without catch or finally")
if(this.prev<r.finallyLoc)return e(r.finallyLoc)}}}},abrupt:function(t,e){for(var n=this.tryEntries.length-1;n>=0;--n){var i=this.tryEntries[n]
if(i.tryLoc<=this.prev&&y.call(i,"finallyLoc")&&this.prev<i.finallyLoc){var r=i
break}}r&&("break"===t||"continue"===t)&&r.tryLoc<=e&&e<=r.finallyLoc&&(r=null)
var o=r?r.completion:{}
return o.type=t,o.arg=e,r?(this.method="next",this.next=r.finallyLoc,P):this.complete(o)},complete:function(t,e){if("throw"===t.type)throw t.arg
return"break"===t.type||"continue"===t.type?this.next=t.arg:"return"===t.type?(this.rval=this.arg=t.arg,this.method="return",this.next="end"):"normal"===t.type&&e&&(this.next=e),P},finish:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var n=this.tryEntries[e]
if(n.finallyLoc===t)return this.complete(n.completion,n.afterLoc),h(n),P}},"catch":function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var n=this.tryEntries[e]
if(n.tryLoc===t){var i=n.completion
if("throw"===i.type){var r=i.arg
h(n)}return r}}throw Error("illegal catch attempt")},delegateYield:function(t,e,n){return this.delegate={iterator:d(t),resultName:e,nextLoc:n},"next"===this.method&&(this.arg=m),P}}}}(function(){return this}()||Function("return this")())},function(t,e,n){"use strict"
function i(t){return t&&t.__esModule?t:{"default":t}}function r(t){if(Array.isArray(t)){for(var e=0,n=Array(t.length);e<t.length;e++)n[e]=t[e]
return n}return(0,o["default"])(t)}Object.defineProperty(e,"__esModule",{value:!0})
var o=i(n(81)),a=i(n(0)),s=i(n(45)),l=function(){function t(t,e){for(var n=0;n<e.length;n++){var i=e[n]
i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),(0,a["default"])(t,i.key,i)}}return function(e,n,i){return n&&t(e.prototype,n),i&&t(e,i),e}}(),u=i(n(88)),c=i(n(93)),h=i(n(101)),f=i(n(102)),d=i(n(103)),p=i(n(104)),m=i(n(105)),g=i(n(106)),y=function(){function t(){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t),this.shareButtons=[],this.followButton=[],this.followButtonOnly=[],this.chatwidget=null,this.callButton=null,this.mapShareButton={},this.zShareTimer=null,this.commentIFrame=null,this.socialPlugins={},this.receiveMessage=this.receiveMessage.bind(this),this.reloadSocial=this.reloadSocial.bind(this),window.addEventListener("message",this.receiveMessage,!0),window.addEventListener("focus",this.reloadSocial,!1),"remove"in Element.prototype||(Element.prototype.remove=function(){this.parentNode&&this.parentNode.removeChild(this)})}return l(t,[{key:"reloadSocial",value:function(){this.shareButtons.map(function(t){t.reload()})}},{key:"init",value:function(){var t=this
if(console.log("Zalo Social Plugin is loaded successfully"),this.socialPlugins=this.findAllSocialPluginDiv(),this.socialPlugins.share&&(console.log("socialPluginsShare: ",this.socialPlugins.share),this.socialPlugins.share.map(function(e){var n=m["default"].create(),i=new c["default"](e,n,t)
i.render(),t.mapShareButton[n]=i,t.shareButtons.push(i)})),this.socialPlugins.follow&&this.socialPlugins.follow.map(function(e){var n=m["default"].create(),i=new h["default"](e,n)
i.render(),t.followButton.push(i)}),this.socialPlugins.followonly&&this.socialPlugins.followonly.map(function(e){var n=m["default"].create(),i=new f["default"](e,n)
i.render(),t.followButtonOnly.push(i)}),this.socialPlugins.comment){var e=new d["default"](this.socialPlugins.comment)
e.render(),this.commentIFrame=e}if(this.socialPlugins.chatwidget){var n=m["default"].create(),i=new u["default"](this.socialPlugins.chatwidget,n)
i.render(),this.chatwidget=i}if(this.socialPlugins.call){var r=m["default"].create(),o=new p["default"](this.socialPlugins.call,r)
o.render(),this.callButton=o}}},{key:"receiveMessage",value:function(t){if(t.data){if(t.data.url&&g["default"].isMaliciousScheme(t.data.url))return
switch(t.data.cmd){case"zsdk_newtab":this.openInNewTab(t.data.url)
break
case"zsdk_popup":this.openInPopup(t.data.url,t.data.title,t.data.width,t.data.height)
break
case"zsdk_call_qr_widget":this.onOpenCallQrWidget(t.data.url,t.data.text)
break
case"zsdk_call_qr":this.onOpenCallQr(t.data.url,t.data.text)
break
case"zsdk_redirect":this.redirect(t.data.url)
break
case"zsdk_button_click":this.mapShareButton[t.data.id]&&this.mapShareButton[t.data.id].onButtonClick()
break
case"zsdk_update_share_data":this.mapShareButton[t.data.id]&&this.mapShareButton[t.data.id].setData(t.data.data)
break
case"zsdk_resize_parent":this.resizeParent(t.data.height)
break
case"zsdk_get_top_body_parent":this.getTopParentBody()
break
case"zsdk_excute_recaptcha":this.executeRecaptcha(t.data)}}}},{key:"reload",value:function(){this.shareButtons.map(function(t){t.destroy()}),this.shareButtons=[],this.followButton=[],this.followButtonOnly=[],null!=this.chatwidget&&this.chatwidget.destroy(),this.chatwidget=null,this.callButton=null,null!=this.commentIFrame&&this.commentIFrame.destroy(),this.commentIFrame=null,this.init()}},{key:"retry",value:function(){var t={share:[],follow:[],followonly:[]}
t.share=[].concat(r(document.getElementsByClassName("zalo-share-button"))),t.follow=[].concat(r(document.getElementsByClassName("zalo-follow-button"))),t.followonly=[].concat(r(document.getElementsByClassName("zalo-follow-only-button"))),t.comment=document.getElementsByClassName("zalo-comment-plugin")[0],t.chatwidget=document.getElementsByClassName("zalo-chat-widget")[0],t.call=document.getElementsByClassName("zalo-call-button")[0],(0,s["default"])(t)!=(0,s["default"])(this.socialPlugins)&&this.reload()}},{key:"findAllSocialPluginDiv",value:function(){var t={share:[],follow:[],followonly:[]}
return t.share=[].concat(r(document.getElementsByClassName("zalo-share-button"))),t.follow=[].concat(r(document.getElementsByClassName("zalo-follow-button"))),t.followonly=[].concat(r(document.getElementsByClassName("zalo-follow-only-button"))),t.comment=document.getElementsByClassName("zalo-comment-plugin")[0],t.chatwidget=document.getElementsByClassName("zalo-chat-widget")[0],t.call=document.getElementsByClassName("zalo-call-button")[0],t.share?t:void 0}},{key:"redirect",value:function(t){window.location.href=t}},{key:"openInNewTab",value:function(t){var e=this,n=window.open(t,"_blank")
n.focus(),null!=this.zShareTimer&&clearInterval(this.zShareTimer),this.zShareTimer=setInterval(function(){n.closed&&(clearInterval(e.zShareTimer),e.zShareTimer=null,e.shareButtons.map(function(t){t.reload()}))},1e3)}},{key:"openInPopup",value:function(t,e,n,i){var r=this,o=this.popupCenter(t,e,n,i)
null!=this.zShareTimer&&clearInterval(this.zShareTimer),this.zShareTimer=setInterval(function(){o&&o.closed&&(clearInterval(r.zShareTimer),r.zShareTimer=null,r.shareButtons.map(function(t){t.reload()}),r.followButton.map(function(t){t.reload()}),r.followButtonOnly.map(function(t){t.reload()}),r.commentIFrame&&r.commentIFrame.reload())},1e3)}},{key:"executeRecaptcha",value:function(t){switch(t.typeIframe){case"chat_oa_widget":break
case"comment_iframe":GLOBAL_IFRAME=this.commentIFrame.getIframe}grecaptcha.execute(GLOBAL_ID_RECAPTCHA)}},{key:"popupCenter",value:function(t,e,n,i){var r=null!=window.screenLeft?window.screenLeft:screen.left,o=null!=window.screenTop?window.screenTop:screen.top,a=(window.innerWidth?window.innerWidth:document.documentElement.clientWidth?document.documentElement.clientWidth:screen.width)/2-n/2+r,s=(window.innerHeight?window.innerHeight:document.documentElement.clientHeight?document.documentElement.clientHeight:screen.height)/2-i/2+o
return window.open(t,e,"directories=0,titlebar=0,toolbar=0,location=0,status=0,menubar=0,scrollbars=0,resizable=0,width="+n+", height="+i+", top="+s+", left="+a)}},{key:"resizeParent",value:function(t){this.commentIFrame.resizeParent(t)}},{key:"getTopParentBody",value:function(){this.commentIFrame.getTopParentBody()}},{key:"openChatWidget",value:function(){this.chatwidget.openChatWidget()}},{key:"closeChatWidget",value:function(){this.chatwidget.closeChatWidget()}},{key:"onOpenCallQrWidget",value:function(t,e){this.chatwidget.showQRModal(t,e)}},{key:"onOpenCallQr",value:function(t,e){this.callButton.showQRModal(t,e)}}]),t}()
e["default"]=y},function(t,e,n){t.exports={"default":n(82),__esModule:!0}},function(t,e,n){n(28),n(83),t.exports=n(2).Array.from},function(t,e,n){"use strict"
var i=n(10),r=n(4),o=n(26),a=n(37),s=n(38),l=n(23),u=n(84),c=n(39)
r(r.S+r.F*!n(44)(function(t){Array.from(t)}),"Array",{from:function(t){var e,n,r,h,f=o(t),d="function"==typeof this?this:Array,p=arguments.length,m=p>1?arguments[1]:void 0,g=void 0!==m,y=0,v=c(f)
if(g&&(m=i(m,p>2?arguments[2]:void 0,2)),null==v||d==Array&&s(v))for(n=new d(e=l(f.length));e>y;y++)u(n,y,g?m(f[y],y):f[y])
else for(h=v.call(f),n=new d;!(r=h.next()).done;y++)u(n,y,g?a(h,m,[r.value,y],!0):r.value)
return n.length=y,n}})},function(t,e,n){"use strict"
var i=n(7),r=n(21)
t.exports=function(t,e,n){e in t?i.f(t,e,r(0,n)):t[e]=n}},function(t,e,n){n(86)
var i=n(2).Object
t.exports=function(t,e,n){return i.defineProperty(t,e,n)}},function(t,e,n){var i=n(4)
i(i.S+i.F*!n(8),"Object",{defineProperty:n(7).f})},function(t,e,n){var i=n(2),r=i.JSON||(i.JSON={stringify:JSON.stringify})
t.exports=function(t){return r.stringify.apply(r,arguments)}},function(t,e,n){"use strict"
function i(t){return t&&t.__esModule?t:{"default":t}}Object.defineProperty(e,"__esModule",{value:!0})
var r=i(n(0)),o=function(){function t(t,e){for(var n=0;n<e.length;n++){var i=e[n]
i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),(0,r["default"])(t,i.key,i)}}return function(e,n,i){return n&&t(e.prototype,n),i&&t(e,i),e}}(),a=i(n(9)),s=i(n(16)),l=function(){function t(e,n){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t),u.call(this),this.id=n,this.data={},this.element=e,this.data=this.getDataFromElement(e),this.chatBoxLeft=null,this.chatBoxTop=null,this.chatBoxHeight=null,this.chatBoxWidth=null,this.selected=null,this.x_pos=0,this.y_pos=0,this.x_elem=0,this.y_elem=0,this.type=0,this.chatBoxHeightCurrent=0,this.chatBoxWidthCurrent=0,this.x_elem_relative=0,this.y_elem_relative=0,this.hitToTop=!1,this.hitToLeft=!1,this.hitToRight=!1,this.hitToBottom=!1,this.initWindowWidth=window.innerWidth,this.initWindowHeight=window.innerHeight,this.checkResizeWindow=!1,this.isChatBoxOpened=!1,this.dragHolderDragging=!1,this.isHandleClosedBoxChatToolTip=!1,this.closedBox_top=null,this.closedBox_bottom=null,this.closedBox_left=null,this.closedBox_right=null,this.initClosedBoxWidth=null,this.data.android=s["default"].isAndroid()&&s["default"].isMobile(),this.data.ios=s["default"].isIOS()&&s["default"].isMobile(),this.receiveMessage=this.receiveMessage.bind(this),window.addEventListener("message",this.receiveMessage),window.addEventListener("resize",this.handleResizeWindow,!0),document.onmousemove=this._move_chat_box,document.onmouseup=this._destroy}return o(t,[{key:"getDataFromElement",value:function(t){var e={}
e.position=t.getAttribute("data-position"),e.oaid=t.getAttribute("data-oaid"),e.welcomemessage=t.getAttribute("data-welcome-message"),e.autopopup=t.getAttribute("data-autopopup")
var n=document.getElementsByClassName("zalo-chat-widget")[0],i=window.getComputedStyle(n,null).getPropertyValue("left")
return e.leftside=t.getAttribute("data-left-side")||"auto"==i?"false":"true",e.width=t.getAttribute("data-width"),e.height=t.getAttribute("data-height"),e.style=t.getAttribute("data-style"),e.width&&"0"!==e.width||(e.width=440),e.height&&"0"!==e.height||(e.height=813),e.style?1!=e.style&&2!=e.style&&(e.style=2,console.warn("[ZaloSocialPlugin] [ChatWidgetPlugin] | Warning: Need to set 'data-style' attribute equals to 1 or 2"),console.warn("[ZaloSocialPlugin] [ChatWidgetPlugin] | Warning: 1 for RECTANGLE style - 2 for CIRCLE style")):e.style=2,e.id=this.id,e.domain=document.domain,e}},{key:"validate",value:function(){return!!this.data.oaid||(console.warn("[Zalo Social Plugin]","The chat widget button have no data-oaid attribute"),!1)}},{key:"updateDragHolderElementStyle",value:function(){if(this.isChatBoxOpened)this.dragHolder.style.left=0,this.dragHolder.style.right="",this.dragHolder.style.width="80%"
else{if(this.isRectangleVersion())return void(this.dragHolder.style.width="0px")
window.getComputedStyle(this.element,null).getPropertyValue("left").replace("px","")<10?(this.dragHolder.style.left=0,this.dragHolder.style.right=""):(this.dragHolder.style.left="",this.dragHolder.style.right=0),this.dragHolder.style.width=this.isHandleClosedBoxChatToolTip?this.initClosedBoxWidth+"px":"70px"}}},{key:"render",value:function(){this.validate()&&(this.iframe=document.createElement("iframe"),this.iframe.frameBorder=0,this.iframe.allowFullscreen="true",this.iframe.scrolling="no",this.iframe.width=260,this.iframe.height=46,this.iframe.style.maxHeight="90vh",this.iframe.style.position="absolute",this.iframe.style.bottom="0px","true"===this.data.leftside?this.iframe.style.left="0px":this.iframe.style.right="0px",this.element.style.zIndex="2147483644",this.element.style.border="none",this.element.style.visibility="visible",this.element.style.bottom="0px",this.element.style.left=this.element.style.left||"",this.element.style.right="0px",this.element.style.position="fixed",this.element.style.width="300px",this.iframe.src="https://page.widget.zalo.me/"+a["default"].jsonToQueryString(this.data),this.element.appendChild(this.iframe),this.dragHolder=document.createElement("div"))}},{key:"destroy",value:function(){this.iframe.remove(),this.dragHolder.remove(),this.element.removeEventListener("message",this.receiveMessage)}},{key:"reload",value:function(){this.iframe&&this.iframe.contentWindow&&this.iframe.contentWindow.postMessage("zshare_reload","https://sp.zalo.me")}},{key:"openChatWidget",value:function(){this.iframe&&this.iframe.contentWindow&&this.iframe.contentWindow.postMessage("open-chat-widget","*")}},{key:"closeChatWidget",value:function(){this.iframe&&this.iframe.contentWindow&&this.iframe.contentWindow.postMessage("close-chat-widget","*")}},{key:"getTheElementStyleLeftPosition",value:function(t){this.iframe&&this.iframe.contentWindow&&this.iframe.contentWindow.postMessage("the_element_style_left_"+t,"*")}},{key:"getWindowLocationHostName",value:function(t){this.iframe&&this.iframe.contentWindow&&this.iframe.contentWindow.postMessage("window_location_hostname_"+t,"*")}},{key:"showQRModal",value:function(t,e){this.overlayDiv=document.createElement("div"),this.overlayDiv.id="zl-modal",this.overlayDiv.style.cssText="position:fixed;width:100%;height:100vh;z-index:2147483645;background:rgba(0, 0, 0, 0.5);left:0;top:0;display:flex;justify-content:center",this.modalDiv=document.createElement("div"),this.modalDiv.id="zl-modal__container",this.modalDiv.style.cssText="position: fixed;z-index:2147483646;width: 400px;height: 434px;background:#FFFFFF;border-radius:8px;top:80px;display:flex;flex-direction:column;align-items:center;justify-content:center;",this.QRImg=document.createElement("img"),this.QRImg.id="zl-modal__container__qr",this.QRImg.src=t,this.QRImg.style.cssText="width:300.18px;height:300.18px;object-fit: contain;",this.textP=document.createElement("p")
var n=document.createTextNode(e)
this.textP.appendChild(n),this.textP.style.cssText="font-family:Roboto;font-style:normal;font-weight:normal;font-size: 14px;line-height:18px;color: #667685;margin-top:16px;",this.modalDiv.appendChild(this.QRImg),this.modalDiv.appendChild(this.textP),this.overlayDiv.appendChild(this.modalDiv),document.getElementsByTagName("body")[0].appendChild(this.overlayDiv),window.addEventListener("click",function(t){if(!document.getElementById("zl-modal__container")||!document.getElementById("zl-modal__container").contains(t.target)){var e=document.getElementById("zl-modal")
e&&e.remove()}})}},{key:"receiveMessage",value:function(t){if(t.data)switch(t.data.cmd){case"zchat_widget_close_chat_box":this.iframe&&(this.isRectangleVersion()||(this.initClosedBoxWidth||this.getWindowLocationHostName(window.location.hostname),this.isHandleClosedBoxChatToolTip||this.getTheElementStyleLeftPosition(window.getComputedStyle(this.element,null).getPropertyValue("left")),this.initClosedBoxWidth=t.data.width),this.isChatBoxOpened=!1,this.updateDragHolderElementStyle(),this.iframe.height=t.data.height,this.iframe.width=t.data.width,this.element.style.height=t.data.height+"px",this.element.style.width=t.data.width+"px",this.element.style.top=this.closedBox_top||"",this.element.style.bottom=this.closedBox_bottom||"0px",this.element.style.left=this.closedBox_left||"",this.element.style.right=this.closedBox_right||"0px",this.offResizeAndDrag())
break
case"zchat_widget_open_chat_box":this.iframe&&(this.isChatBoxOpened=!0,null==this.chatBoxHeight?(this.iframe.height=t.data.height,this.element.style.height=t.data.height+"px"):(this.iframe.height=this.chatBoxHeight,this.element.style.height=this.chatBoxHeight+"px"),null==this.chatBoxWidth?(this.iframe.width=t.data.width,this.element.style.width=t.data.width+"px"):(this.iframe.width=this.chatBoxWidth,this.element.style.width=this.chatBoxWidth+"px"),null==this.chatBoxLeft&&null==this.chatBoxTop?("true"===this.data.leftside?this.element.style.left="52px":this.element.style.right="52px",this.element.style.bottom="52px"):(this.element.style.left=this.chatBoxLeft+"px",this.element.style.top=this.chatBoxTop+"px"),this.handleResizeWindow())
break
case"zchat_widget_toggle_sticker":if(this.iframe){if(+this.iframe.height<+t.data.height){var e=this.element.getAttribute("style")+"z-index:2147483644!important"
this.element.setAttribute("style",e),this.iframe.style.minHeight="80vh",this.iframe.style.minWidth="400px"}else this.element.style.zIndex="2147483644",this.iframe.style.minHeight="",this.iframe.style.minWidth=""
null==this.chatBoxHeight?(this.iframe.height=t.data.height,this.element.style.height=t.data.height+"px"):(this.iframe.height=this.chatBoxHeight,this.element.style.height=this.chatBoxHeight+"px"),null==this.chatBoxWidth?(this.iframe.width=t.data.width,this.element.style.width=t.data.width+"px"):(this.iframe.width=this.chatBoxWidth,this.element.style.width=this.chatBoxWidth+"px")}break
case"zchat_widget_show_light_box":this.iframe&&(this.element.style.height="100%",this.element.style.width="100%",this.element.style.top="0px",this.element.style.left="0px",this.iframe.height="100%",this.iframe.width="100%",this.offResizeAndDrag())
break
case"zchat_widget_close_light_box":this.iframe&&(this.element.style.height=null==this.chatBoxHeight?"470px":this.chatBoxHeight+"px",this.element.style.width=null==this.chatBoxWidth?"350px":this.chatBoxWidth+"px",this.iframe.height=null==this.chatBoxHeight?470:this.chatBoxHeight,this.iframe.width=null==this.chatBoxWidth?350:this.chatBoxWidth,this.element.style.top=null==this.chatBoxTop?"":this.chatBoxTop+"px",this.element.style.left=null==this.chatBoxLeft?"":this.chatBoxLeft+"px",this.onResizeAndDrag())}}},{key:"handleHolderDragging",value:function(){if(this.dragHolderDragging){if(this.isChatBoxOpened)this.chatBoxLeft=this.element.offsetLeft,this.chatBoxTop=this.element.offsetTop,this.chatBoxWidth=this.element.offsetWidth,this.chatBoxHeight=this.element.offsetHeight
else{if(this.isRectangleVersion())return
this.saveClosedBoxPosition(),this.element.offsetLeft<=window.innerWidth/2?(this.closedBox_right="",this.closedBox_left="0px",this.chatBoxLeft=0,this.chatBoxTop=this.element.offsetTop):(this.closedBox_right="0px",this.closedBox_left="",this.chatBoxLeft="",this.chatBoxTop=this.element.offsetTop),this.element.style.left=this.closedBox_left||"",this.element.style.right=this.closedBox_right||""}this.dragHolderDragging=!1}}},{key:"saveClosedBoxPosition",value:function(){this.isRectangleVersion()||this.isChatBoxOpened||(this.closedBox_top=this.element.style.top,this.closedBox_bottom=this.element.style.bottom,this.closedBox_left=this.element.style.left,this.closedBox_right=this.element.style.right)}},{key:"closeChatBoxClosedToolTip",value:function(){this.isRectangleVersion()||this.iframe&&!this.isChatBoxOpened&&(this.isHandleClosedBoxChatToolTip=!0,this.iframe.width=70,this.element.style.width="70px",this.iframe.contentWindow.postMessage("close-chat-box-closed-tooltip","*"))}}]),t}(),u=function(){var t=this
this.isRectangleVersion=function(){return 1==t.data.style},this._drag_chat_box_init=function(e){t.type=e,t.selected=t.element,t.x_elem=t.x_pos-t.selected.offsetLeft,t.y_elem=t.y_pos-t.selected.offsetTop,t.chatBoxHeightCurrent=t.selected.offsetHeight,t.chatBoxWidthCurrent=t.selected.offsetWidth,t.x_elem_relative=t.x_pos,t.y_elem_relative=t.y_pos,t.checkResizeWindow=!1,document.getElementById("overlay").style.display="block"},this._move_chat_box=function(e){if(t.x_pos=document.all?window.event.clientX:e.pageX,t.y_pos=document.all?window.event.clientY:e.pageY,null!==t.selected)switch(t.type){case"move_chat_box":t.handleHitToTop(),t.handleHitToLeft(),t.handleHitToRight(),t.handleHitToBottom()
break
case"left-resize":t.handleLeftResize()
break
case"right-resize":t.handleRightResize()
break
case"top-resize":t.handleTopResize()
break
case"bottom-resize":t.handleBottomResize()
break
case"top-left-resize":t.handleTopResize(),t.handleLeftResize()
break
case"top-right-resize":t.handleTopResize(),t.handleRightResize()
break
case"bottom-left-resize":t.handleBottomResize(),t.handleLeftResize()
break
case"bottom-right-resize":t.handleBottomResize(),t.handleRightResize()}},this._destroy=function(){t.handleHolderDragging(),t.selected=null,t.type=0
var e=document.getElementById("overlay")
e&&(e.style.display="none")},this.handleResizeWindow=function(){var e=!1
if((t.initWindowHeight>window.innerHeight||t.element.offsetTop+t.element.offsetHeight>=window.innerHeight)&&(t.element.style.top="auto"),t.initWindowWidth>window.innerWidth){var n=t.initWindowWidth-window.innerWidth
e=t.element.style.left.replace("px","")-n<=0}return t.element.style.left?t.element.style.left.replace("px","")>=window.innerWidth?(t.initWindowWidth=window.innerWidth,t.element.style.left=""):e?(t.initWindowWidth=window.innerWidth,t.element.style.left="0px"):(window.innerWidth<=t.element.offsetWidth?(t.element.style.left="",t.checkResizeWindow=!0):t.checkResizeWindow?t.element.style.left="":t.element.style.left=t.element.offsetLeft<0?"0px":t.element.offsetLeft+window.innerWidth-t.initWindowWidth+"px",t.initWindowWidth=window.innerWidth,void(t.chatBoxLeft=t.element.offsetLeft)):(t.initWindowWidth=window.innerWidth,t.element.style.left="")},this.handleTopResize=function(){var e=t.selected.offsetTop+t.selected.offsetHeight,n=t.selected.offsetTop+t.selected.offsetHeight-(t.y_pos-t.y_elem)
t.y_pos-t.y_elem>0&&(t.selected.style.height=n>470?n+"px":"470px",t.iframe.height=n>470?n:470,t.selected.style.top=n>=470?t.y_pos-t.y_elem+"px":e-470+"px"),t.chatBoxHeight=t.iframe.height,t.chatBoxTop=t.selected.offsetTop},this.handleLeftResize=function(){var e=t.selected.offsetLeft+t.selected.offsetWidth,n=t.selected.offsetLeft+t.selected.offsetWidth-(t.x_pos-t.x_elem)
t.x_pos-t.x_elem>0&&(t.selected.style.width=n>350?n+"px":"350px",t.iframe.width=n>350?n:350,t.selected.style.left=n>=350?t.x_pos-t.x_elem+"px":e-350+"px"),t.chatBoxWidth=t.iframe.width,t.chatBoxLeft=t.selected.offsetLeft},this.handleRightResize=function(){var e=t.x_pos-t.x_elem_relative+t.chatBoxWidthCurrent
t.x_pos<window.innerWidth-14?(t.selected.style.width=e>350?e+"px":"350px",t.iframe.width=e>350?e:350):(t.selected.style.width=window.innerWidth-t.selected.offsetLeft-14+"px",t.iframe.width=window.innerWidth-t.selected.offsetLeft-14),t.chatBoxWidth=t.iframe.width},this.handleBottomResize=function(){var e=t.y_pos-t.y_elem_relative+t.chatBoxHeightCurrent
t.y_pos<window.innerHeight-1?(t.selected.style.height=e>470?e+"px":"470px",t.iframe.height=e>470?e:470):(t.selected.style.height=window.innerHeight-t.selected.offsetTop+"px",t.iframe.height=window.innerHeight-t.selected.offsetTop),t.chatBoxHeight=t.iframe.height},this.handleHitToTop=function(){0==t.selected.offsetTop&&1==t.hitToTop&&t.y_pos-t.y_elem>35&&(t.selected.style.top="35px",t.hitToTop=!1),t.selected.offsetTop<35?(t.hitToTop=!0,t.selected.style.top="0px",t.isRectangleVersion()&&(t.chatBoxTop=t.y_pos-t.y_elem,0==t.selected.offsetTop&&(t.chatBoxTop=0))):(t.selected.style.top=t.y_pos-t.y_elem+"px",t.isRectangleVersion()&&(t.chatBoxTop=t.selected.offsetTop))},this.handleHitToLeft=function(){0==t.selected.offsetLeft&&1==t.hitToLeft&&t.x_pos-t.x_elem>35&&(t.selected.style.left="35px",t.hitToLeft=!1),t.selected.offsetLeft<35?(t.hitToLeft=!0,t.selected.style.left="0px",t.isRectangleVersion()&&(t.chatBoxLeft=t.x_pos-t.x_elem,0==t.selected.offsetLeft&&(t.chatBoxLeft=0))):(t.selected.style.left=t.x_pos-t.x_elem+"px",t.isRectangleVersion()&&(t.chatBoxLeft=t.x_pos-t.x_elem))},this.handleHitToRight=function(){var e=window.innerWidth-t.selected.offsetLeft-t.selected.offsetWidth
0==e&&1==t.hitToRight&&t.x_elem-t.x_pos>35&&(t.selected.style.left=window.innerWidth-35+"px",t.hitToRight=!1),35>e?(t.hitToLeft=!0,t.selected.style.left=window.innerWidth-t.selected.offsetWidth-15+"px",t.isRectangleVersion()&&(t.chatBoxWidth=t.selected.offsetWidth)):t.isRectangleVersion()&&(t.chatBoxWidth=t.selected.offsetWidth),t.isRectangleVersion()&&(t.chatBoxLeft=t.selected.offsetLeft)},this.handleHitToBottom=function(){var e=window.innerHeight-t.selected.offsetTop-t.selected.offsetHeight
0==t.offsetBottom&&1==t.hitToBottom&&t.y_elem-t.y_pos>35&&(t.selected.style.top=window.innerHeight-35+"px",t.hitToBottom=!1),35>e?(t.hitToBottom=!0,t.selected.style.top=window.innerHeight-t.selected.offsetHeight+"px",t.isRectangleVersion()&&(t.chatBoxHeight=t.selected.offsetHeight)):t.isRectangleVersion()&&(t.chatBoxHeight=t.selected.offsetHeight),t.isRectangleVersion()&&(t.chatBoxTop=t.selected.offsetTop)},this.offResizeAndDrag=function(){document.getElementById("drag-holder").style.display="block",document.getElementById("drag-left").style.display="none",document.getElementById("drag-right").style.display="none",document.getElementById("drag-top").style.display="none",document.getElementById("drag-bottom").style.display="none",document.getElementById("drag-top-left").style.display="none",document.getElementById("drag-top-right").style.display="none",document.getElementById("drag-bottom-left").style.display="none",document.getElementById("drag-bottom-right").style.display="none"},this.onResizeAndDrag=function(){document.getElementById("drag-holder").style.display="block",document.getElementById("drag-left").style.display="block",document.getElementById("drag-right").style.display="block",document.getElementById("drag-top").style.display="block",document.getElementById("drag-bottom").style.display="block",document.getElementById("drag-top-left").style.display="block",document.getElementById("drag-top-right").style.display="block",document.getElementById("drag-bottom-left").style.display="block",document.getElementById("drag-bottom-right").style.display="block"}}
e["default"]=l},function(t,e,n){t.exports={"default":n(90),__esModule:!0}},function(t,e,n){n(91),t.exports=n(2).Object.keys},function(t,e,n){var i=n(26),r=n(31)
n(92)("keys",function(){return function(t){return r(i(t))}})},function(t,e,n){var i=n(4),r=n(2),o=n(19)
t.exports=function(t,e){var n=(r.Object||{})[t]||Object[t],a={}
a[t]=e(n),i(i.S+i.F*o(function(){n(1)}),"Object",a)}},function(t,e,n){"use strict"
function i(t){return t&&t.__esModule?t:{"default":t}}Object.defineProperty(e,"__esModule",{value:!0})
var r=i(n(0)),o=i(n(45)),a=function(){function t(t,e){for(var n=0;n<e.length;n++){var i=e[n]
i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),(0,r["default"])(t,i.key,i)}}return function(e,n,i){return n&&t(e.prototype,n),i&&t(e,i),e}}(),s=i(n(9)),l=i(n(16)),u=i(n(94)),c=n(96),h=function(){function t(e,n,i){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t),this.sdk=i,this.id=n,this.data={},this.element=e,this.data=this.getDataFromElement(e),this.data.android=l["default"].isAndroid()&&l["default"].isMobile(),this.data.ios=l["default"].isIOS()&&l["default"].isMobile(),this.data.baseUrl="https://sp.zalo.me",this.receiveMessage=this.receiveMessage.bind(this),this.shareOnMobile=this.shareOnMobile.bind(this),this.handleOpenShare=this.handleOpenShare.bind(this)}return a(t,[{key:"getDataFromElement",value:function(t){var e={}
return e.dev=t.getAttribute("data-dev"),e.color=t.getAttribute("data-color"),e.oaid=t.getAttribute("data-oaid"),e.href=t.getAttribute("data-href"),e.href||(e.href=window.location.href),e.layout=t.getAttribute("data-layout"),e.customize=t.getAttribute("data-customize"),e.callback=t.getAttribute("data-callback"),e.share=parseInt(t.getAttribute("data-share-type")),e.share||(e.share=0),e.layout||(e.layout="1"),e.customize?"false"===e.customize?e.customize=!1:e.customize=!0:e.customize=!1,e.id=this.id,e.domain=document.domain,e.width="0px",e.height="0px",e}},{key:"validate",value:function(){return this.data.oaid?!!this.data.href||(console.warn("[Zalo Social Plugin]","The share button have no data-href attribute"),!1):(console.warn("[Zalo Social Plugin]","The share button have no data-oaid attribute"),!1)}},{key:"render",value:function(){if(console.log("2.1.1"),this.validate()){if(this.iframe=document.createElement("iframe"),this.iframe.id=this.id,this.iframe.name=this.id,this.iframe.frameBorder=0,this.iframe.allowFullscreen="true",this.iframe.scrolling="no",this.iframe.style.position="relative",this.data.customize)this.iframe.style.zIndex=999999,this.iframe.width="0px",this.iframe.height="0px",this.iframe.style.position="absolute",this.iframe.style.top="0px",this.iframe.style.left="0px",this.listenEventClickButton()
else{switch(this.element.style.position="relative",this.iframe.style.zIndex=99,this.element.style.display="inline-block",this.iframe.style.position="absolute",this.iframe.style.top="0px",this.iframe.style.left="0px",this.data.layout){case"1":this.data.width="70",this.data.height="20"
break
case"2":this.data.width="20",this.data.height="20"
break
case"3":this.data.width="30",this.data.height="30"
break
case"4":this.data.width="40",this.data.height="40"
break
case"5":this.data.width="40",this.data.height="60"}this.iframe.width=this.data.width+"px",this.element.style.width=this.data.width+"px",this.iframe.height=this.data.height+"px",this.element.style.height=this.data.height+"px"}var t={url:this.data.href},e={id:this.id.hex,layout:this.data.layout,color:this.data.color,customize:this.data.customize,width:this.data.width,height:this.data.height,isDesktop:!this.data.android&&!this.data.ios||!1,url:this.data.href,d:encodeURIComponent(c.Base64.encode((0,o["default"])(t))),shareType:this.data.share}
this.data.hrefBtn="https://button-share.zalo.me/share_inline"+s["default"].jsonToQueryString(e),this.iframe.src=this.data.hrefBtn,this.data.customize?document.getElementsByTagName("body")[0].appendChild(this.iframe):this.element.appendChild(this.iframe),window.addEventListener("message",this.receiveMessage)}}},{key:"listenEventClickButton",value:function(){this.element.addEventListener("click",this.onButtonClick.bind(this),!1)}},{key:"onButtonClick",value:function(){this.iframe&&this.iframe.contentWindow&&this.iframe.contentWindow.postMessage({type:"clickOpenShare",id:this.id.hex},"*")}},{key:"destroy",value:function(){this.iframe.remove(),this.element.removeEventListener("click",this.onButtonClick),window.removeEventListener("message",this.receiveMessage)}},{key:"reload",value:function(){this.iframe&&this.iframe.contentWindow&&this.iframe.contentWindow.postMessage("zshare_reload","https://sp.zalo.me")}},{key:"setData",value:function(t){this.frameData=t}},{key:"shareOnMobile",value:function(){if(null!=this.data){var t=encodeURIComponent(this.data.href)
return this.data.android?(this.sdk.redirect("intent://zaloapp.com/#Intent;action=android.intent.action.SEND;type=text/plain;S.android.intent.extra.SUBJECT=;S.android.intent.extra.TEXT="+t+";B.hidePostFeed=false;B.backToSource=true;end"),!1):this.data.ios?(this.sdk.redirect("zaloshareext://shareext?url="+t+"&type=8&version=1"),!1):void 0}}},{key:"handleOpenShare",value:function(){u["default"].clickShareButton()
var t=(0,o["default"])({errorCode:0})
u["default"].trackStatClickShare("https://sp.zalo.me/l/stats","OAid="+(this.data.oaid?""+this.data.oaid:"0")+"&actionId=6&params="+t,function(){}),this.position=this.getPositionIframe(),this.data.customize?(this.iframe.style.top=this.position.top+"px",this.iframe.style.left=this.position.left+"px",this.iframe.style.width="433px",this.iframe.style.height="350px"):(this.iframe.style.zIndex=999999,"left"===this.position.horizontal?(this.iframe.style.right="0px",this.iframe.style.left="auto"):(this.iframe.style.left="0px",this.iframe.style.right="auto"),"top"===this.position.vertical?(this.iframe.style.bottom="0px",this.iframe.style.top="auto"):(this.iframe.style.top="0px",this.iframe.style.bottom="auto"),this.iframe.style.width="470px",this.iframe.style.height="450px"),this.iframe&&this.iframe.contentWindow&&this.iframe.contentWindow.postMessage({type:"changeAlignLayoutShare",align:this.position,id:this.id.hex},"*")}},{key:"getPositionIframe",value:function(){var t=Math.max(document.documentElement.clientHeight,window.innerHeight||0),e=Math.max(document.documentElement.clientWidth,window.innerWidth||0),n=this.element.getBoundingClientRect()
console.log("rect: ",n),console.log("h = ",t)
var i="bottom",r="right"
if(this.data.customize){var o=this.getCoords(this.element),a=o.top+this.element.offsetHeight+5,s=o.left+this.element.offsetWidth/2
return t-n.bottom<355&&(a=a-360-n.height,i="top"),e-n.right<477&&(s-=430,r="left"),{top:a,left:s,vertical:i,horizontal:r}}return t-n.bottom<355&&(i="top"),e-n.right<477&&(r="left"),{vertical:i,horizontal:r}}},{key:"getCoords",value:function(t){var e=t.getBoundingClientRect(),n=document.body,i=document.documentElement,r=window.pageYOffset||i.scrollTop||n.scrollTop,o=window.pageXOffset||i.scrollLeft||n.scrollLeft,a=i.clientTop||n.clientTop||0,s=i.clientLeft||n.clientLeft||0,l=e.top+r-a,u=e.left+o-s
return{top:Math.round(l),left:Math.round(u)}}},{key:"receiveMessage",value:function(t){if(t.data&&t.data.id===this.id.hex)switch(t.data.cmd){case"zsdk_share_resize":this.data.customize?(this.iframe.style.height=350+t.data.height+"px","top"===this.position.vertical&&(this.iframe.style.top=this.position.top-t.data.height+"px")):this.iframe.style.height=450+t.data.height+"px"
break
case"zsdk_open_share":this.handleOpenShare()
break
case"zsdk_share_on_mobile":this.shareOnMobile()
break
case"zsdk_close_share":this.data.customize?(this.iframe.style.width="0px",this.iframe.style.height="0px"):(this.iframe.style.zIndex=99,this.iframe.style.width=this.data.width+"px",this.iframe.style.height=this.data.height+"px"),window[this.data.callback]&&window[this.data.callback]({data:1})
break
case"zsdk_login_zalo":this.handleLoginZalo()}}}]),t}()
e["default"]=h},function(t,e,n){"use strict"
function i(t){return t&&t.__esModule?t:{"default":t}}Object.defineProperty(e,"__esModule",{value:!0})
var r=i(n(0)),o=function(){function t(t,e){for(var n=0;n<e.length;n++){var i=e[n]
i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),(0,r["default"])(t,i.key,i)}}return function(e,n,i){return n&&t(e.prototype,n),i&&t(e,i),e}}(),a=i(n(95)),s=2,l=function(){function t(){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t)}return o(t,null,[{key:"trackStatClickShare",value:function(t,e,n){a["default"].postJSOBWithCredentials(t,e,n)}},{key:"clickShareButton",value:function(){a["default"].getTextWithCredentials("https://sp.zalo.me/l/share?action="+s,function(){})}},{key:"trackingError",value:function(t,e){a["default"].getTextWithCredentials("https://sp.zalo.me/tracking/log?error="+encodeURIComponent(t)+"&data="+e,function(){})}}]),t}()
e["default"]=l},function(t,e,n){"use strict"
Object.defineProperty(e,"__esModule",{value:!0})
var i,r=n(0),o=(i=r)&&i.__esModule?i:{"default":i},a=function(){function t(t,e){for(var n=0;n<e.length;n++){var i=e[n]
i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),(0,o["default"])(t,i.key,i)}}return function(e,n,i){return n&&t(e.prototype,n),i&&t(e,i),e}}(),s=function(){function t(){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t)}return a(t,null,[{key:"getJSONWithCredentials",value:function(t,e){fetch(t,{credentials:"include",method:"get"}).then(function(t){return t.json()}).then(function(t){e(t)})}},{key:"getTextWithCredentials",value:function(t,e){fetch(t,{credentials:"include",method:"get"}).then(function(t){return t.text()}).then(function(t){e(t)})}},{key:"postJSOBWithCredentials",value:function(t,e,n){fetch(t,{method:"post",credentials:"include",headers:{"Content-Type":"application/x-www-form-urlencoded"},body:e}).then(function(t){return t.json()}).then(function(t){n(t)})}}]),t}()
e["default"]=s},function(t,e,n){(function(t){var i
!function(t){"use strict"
var r,o=t.Base64
if(a.exports)try{r=n(97).Buffer}catch(a){}var s="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",l=function(t){for(var e={},n=0,i=t.length;i>n;n++)e[t.charAt(n)]=n
return e}(s),u=String.fromCharCode,c=function(t){if(t.length<2)return(e=t.charCodeAt(0))<128?t:2048>e?u(192|e>>>6)+u(128|63&e):u(224|e>>>12&15)+u(128|e>>>6&63)+u(128|63&e)
var e=65536+1024*(t.charCodeAt(0)-55296)+(t.charCodeAt(1)-56320)
return u(240|e>>>18&7)+u(128|e>>>12&63)+u(128|e>>>6&63)+u(128|63&e)},h=/[\uD800-\uDBFF][\uDC00-\uDFFFF]|[^\x00-\x7F]/g,f=function(t){return t.replace(h,c)},d=function(t){var e=[0,2,1][t.length%3],n=t.charCodeAt(0)<<16|(t.length>1?t.charCodeAt(1):0)<<8|(t.length>2?t.charCodeAt(2):0)
return""+s.charAt(n>>>18)+s.charAt(n>>>12&63)+(e>=2?"=":s.charAt(n>>>6&63))+(e>=1?"=":s.charAt(63&n))},p=t.btoa?function(e){return t.btoa(e)}:function(t){return t.replace(/[\s\S]{1,3}/g,d)},m=r?r.from&&r.from!==Uint8Array.from?function(t){return(t.constructor===r.constructor?t:r.from(t)).toString("base64")}:function(t){return(t.constructor===r.constructor?t:new r(t)).toString("base64")}:function(t){return p(f(t))},g=function(t,e){return e?m(t+"").replace(/[+\/]/g,function(t){return"+"==t?"-":"_"}).replace(/=/g,""):m(t+"")},y=RegExp("[?-?][?-?]|[?-?][?-?]{2}|[?-?][?-?]{3}","g"),v=function(t){switch(t.length){case 4:var e=((7&t.charCodeAt(0))<<18|(63&t.charCodeAt(1))<<12|(63&t.charCodeAt(2))<<6|63&t.charCodeAt(3))-65536
return u(55296+(e>>>10))+u(56320+(1023&e))
case 3:return u((15&t.charCodeAt(0))<<12|(63&t.charCodeAt(1))<<6|63&t.charCodeAt(2))
default:return u((31&t.charCodeAt(0))<<6|63&t.charCodeAt(1))}},w=function(t){return t.replace(y,v)},x=function(t){var e=t.length,n=e%4,i=(e>0?l[t.charAt(0)]<<18:0)|(e>1?l[t.charAt(1)]<<12:0)|(e>2?l[t.charAt(2)]<<6:0)|(e>3?l[t.charAt(3)]:0),r=[u(i>>>16),u(i>>>8&255),u(255&i)]
return r.length-=[0,0,2,1][n],r.join("")},b=t.atob?function(e){return t.atob(e)}:function(t){return t.replace(/[\s\S]{1,4}/g,x)},_=r?r.from&&r.from!==Uint8Array.from?function(t){return""+(t.constructor===r.constructor?t:r.from(t,"base64"))}:function(t){return""+(t.constructor===r.constructor?t:new r(t,"base64"))}:function(t){return w(b(t))},B=function(t){return _((t+"").replace(/[-_]/g,function(t){return"-"==t?"+":"/"}).replace(/[^A-Za-z0-9\+\/]/g,""))}
if(t.Base64={VERSION:"2.3.2",atob:b,btoa:p,fromBase64:B,toBase64:g,utob:f,encode:g,encodeURI:function(t){return g(t,!0)},btou:w,decode:B,noConflict:function(){var e=t.Base64
return t.Base64=o,e}},"function"==typeof Object.defineProperty){var k=function(t){return{value:t,enumerable:!1,writable:!0,configurable:!0}}
t.Base64.extendString=function(){Object.defineProperty(String.prototype,"fromBase64",k(function(){return B(this)})),Object.defineProperty(String.prototype,"toBase64",k(function(t){return g(this,t)})),Object.defineProperty(String.prototype,"toBase64URI",k(function(){return g(this,!0)}))}}t.Meteor&&(Base64=t.Base64),a.exports?a.exports.Base64=t.Base64:void 0===(i=function(){return t.Base64}.apply(e,[]))||(a.exports=i)}("undefined"!=typeof self?self:"undefined"!=typeof window?window:void 0!==t?t:this)}).call(this,n(46))},function(t,e,n){"use strict";(function(t){function i(){return o.TYPED_ARRAY_SUPPORT?2147483647:1073741823}function r(t,e){if(i()<e)throw new RangeError("Invalid typed array length")
return o.TYPED_ARRAY_SUPPORT?(t=new Uint8Array(e)).__proto__=o.prototype:(null===t&&(t=new o(e)),t.length=e),t}function o(t,e,n){if(!(o.TYPED_ARRAY_SUPPORT||this instanceof o))return new o(t,e,n)
if("number"==typeof t){if("string"==typeof e)throw Error("If encoding is specified then the first argument must be a string")
return l(this,t)}return a(this,t,e,n)}function a(t,e,n,i){if("number"==typeof e)throw new TypeError('"value" argument must not be a number')
return"undefined"!=typeof ArrayBuffer&&e instanceof ArrayBuffer?function(t,e,n,i){if(e.byteLength,0>n||e.byteLength<n)throw new RangeError("'offset' is out of bounds")
if(e.byteLength<n+(i||0))throw new RangeError("'length' is out of bounds")
return e=void 0===n&&void 0===i?new Uint8Array(e):void 0===i?new Uint8Array(e,n):new Uint8Array(e,n,i),o.TYPED_ARRAY_SUPPORT?(t=e).__proto__=o.prototype:t=u(t,e),t}(t,e,n,i):"string"==typeof e?function(t,e,n){if("string"==typeof n&&""!==n||(n="utf8"),!o.isEncoding(n))throw new TypeError('"encoding" must be a valid string encoding')
var i=0|h(e,n),a=(t=r(t,i)).write(e,n)
return a!==i&&(t=t.slice(0,a)),t}(t,e,n):function(t,e){if(o.isBuffer(e)){var n=0|c(e.length)
return 0===(t=r(t,n)).length?t:(e.copy(t,0,0,n),t)}if(e){if("undefined"!=typeof ArrayBuffer&&e.buffer instanceof ArrayBuffer||"length"in e)return"number"!=typeof e.length||(i=e.length)!=i?r(t,0):u(t,e)
if("Buffer"===e.type&&I(e.data))return u(t,e.data)}var i
throw new TypeError("First argument must be a string, Buffer, ArrayBuffer, Array, or array-like object.")}(t,e)}function s(t){if("number"!=typeof t)throw new TypeError('"size" argument must be a number')
if(0>t)throw new RangeError('"size" argument must not be negative')}function l(t,e){if(s(e),t=r(t,0>e?0:0|c(e)),!o.TYPED_ARRAY_SUPPORT)for(var n=0;e>n;++n)t[n]=0
return t}function u(t,e){var n=e.length<0?0:0|c(e.length)
t=r(t,n)
for(var i=0;n>i;i+=1)t[i]=255&e[i]
return t}function c(t){if(t>=i())throw new RangeError("Attempt to allocate Buffer larger than maximum size: 0x"+i().toString(16)+" bytes")
return 0|t}function h(t,e){if(o.isBuffer(t))return t.length
if("undefined"!=typeof ArrayBuffer&&"function"==typeof ArrayBuffer.isView&&(ArrayBuffer.isView(t)||t instanceof ArrayBuffer))return t.byteLength
"string"!=typeof t&&(t=""+t)
var n=t.length
if(0===n)return 0
for(var i=!1;;)switch(e){case"ascii":case"latin1":case"binary":return n
case"utf8":case"utf-8":case void 0:return O(t).length
case"ucs2":case"ucs-2":case"utf16le":case"utf-16le":return 2*n
case"hex":return n>>>1
case"base64":return W(t).length
default:if(i)return O(t).length
e=(""+e).toLowerCase(),i=!0}}function f(t,e,n){var i=t[e]
t[e]=t[n],t[n]=i}function d(t,e,n,i,r){if(0===t.length)return-1
if("string"==typeof n?(i=n,n=0):n>2147483647?n=2147483647:-2147483648>n&&(n=-2147483648),n=+n,isNaN(n)&&(n=r?0:t.length-1),0>n&&(n=t.length+n),n>=t.length){if(r)return-1
n=t.length-1}else if(0>n){if(!r)return-1
n=0}if("string"==typeof e&&(e=o.from(e,i)),o.isBuffer(e))return 0===e.length?-1:p(t,e,n,i,r)
if("number"==typeof e)return e&=255,o.TYPED_ARRAY_SUPPORT&&"function"==typeof Uint8Array.prototype.indexOf?r?Uint8Array.prototype.indexOf.call(t,e,n):Uint8Array.prototype.lastIndexOf.call(t,e,n):p(t,[e],n,i,r)
throw new TypeError("val must be string, number or Buffer")}function p(t,e,n,i,r){function o(t,e){return 1===s?t[e]:t.readUInt16BE(e*s)}var a,s=1,l=t.length,u=e.length
if(void 0!==i&&("ucs2"===(i=(i+"").toLowerCase())||"ucs-2"===i||"utf16le"===i||"utf-16le"===i)){if(t.length<2||e.length<2)return-1
s=2,l/=2,u/=2,n/=2}if(r){var c=-1
for(a=n;l>a;a++)if(o(t,a)===o(e,-1===c?0:a-c)){if(-1===c&&(c=a),a-c+1===u)return c*s}else-1!==c&&(a-=a-c),c=-1}else for(n+u>l&&(n=l-u),a=n;a>=0;a--){for(var h=!0,f=0;u>f;f++)if(o(t,a+f)!==o(e,f)){h=!1
break}if(h)return a}return-1}function m(t,e,n,i){n=+n||0
var r=t.length-n
i?(i=+i)>r&&(i=r):i=r
var o=e.length
if(o%2!=0)throw new TypeError("Invalid hex string")
i>o/2&&(i=o/2)
for(var a=0;i>a;++a){var s=parseInt(e.substr(2*a,2),16)
if(isNaN(s))return a
t[n+a]=s}return a}function g(t,e,n,i){return U(function(t){for(var e=[],n=0;n<t.length;++n)e.push(255&t.charCodeAt(n))
return e}(e),t,n,i)}function y(t,e,n){return 0===e&&n===t.length?R.fromByteArray(t):R.fromByteArray(t.slice(e,n))}function v(t,e,n){n=Math.min(t.length,n)
for(var i=[],r=e;n>r;){var o,a,s,l,u=t[r],c=null,h=u>239?4:u>223?3:u>191?2:1
if(n>=r+h)switch(h){case 1:128>u&&(c=u)
break
case 2:128==(192&(o=t[r+1]))&&(l=(31&u)<<6|63&o)>127&&(c=l)
break
case 3:o=t[r+1],a=t[r+2],128==(192&o)&&128==(192&a)&&(l=(15&u)<<12|(63&o)<<6|63&a)>2047&&(55296>l||l>57343)&&(c=l)
break
case 4:o=t[r+1],a=t[r+2],s=t[r+3],128==(192&o)&&128==(192&a)&&128==(192&s)&&(l=(15&u)<<18|(63&o)<<12|(63&a)<<6|63&s)>65535&&1114112>l&&(c=l)}null===c?(c=65533,h=1):c>65535&&(c-=65536,i.push(c>>>10&1023|55296),c=56320|1023&c),i.push(c),r+=h}return function(t){var e=t.length
if(C>=e)return String.fromCharCode.apply(String,t)
for(var n="",i=0;e>i;)n+=String.fromCharCode.apply(String,t.slice(i,i+=C))
return n}(i)}function w(t,e,n){var i=""
n=Math.min(t.length,n)
for(var r=e;n>r;++r)i+=String.fromCharCode(127&t[r])
return i}function x(t,e,n){var i=""
n=Math.min(t.length,n)
for(var r=e;n>r;++r)i+=String.fromCharCode(t[r])
return i}function b(t,e,n){var i=t.length;(!e||0>e)&&(e=0),(!n||0>n||n>i)&&(n=i)
for(var r="",o=e;n>o;++o)r+=L(t[o])
return r}function _(t,e,n){for(var i=t.slice(e,n),r="",o=0;o<i.length;o+=2)r+=String.fromCharCode(i[o]+256*i[o+1])
return r}function B(t,e,n){if(t%1!=0||0>t)throw new RangeError("offset is not uint")
if(t+e>n)throw new RangeError("Trying to access beyond buffer length")}function k(t,e,n,i,r,a){if(!o.isBuffer(t))throw new TypeError('"buffer" argument must be a Buffer instance')
if(e>r||a>e)throw new RangeError('"value" argument is out of bounds')
if(n+i>t.length)throw new RangeError("Index out of range")}function E(t,e,n,i){0>e&&(e=65535+e+1)
for(var r=0,o=Math.min(t.length-n,2);o>r;++r)t[n+r]=(e&255<<8*(i?r:1-r))>>>8*(i?r:1-r)}function T(t,e,n,i){0>e&&(e=4294967295+e+1)
for(var r=0,o=Math.min(t.length-n,4);o>r;++r)t[n+r]=e>>>8*(i?r:3-r)&255}function S(t,e,n,i,r,o){if(n+i>t.length)throw new RangeError("Index out of range")
if(0>n)throw new RangeError("Index out of range")}function P(t,e,n,i,r){return r||S(t,0,n,4),z.write(t,e,n,i,23,4),n+4}function A(t,e,n,i,r){return r||S(t,0,n,8),z.write(t,e,n,i,52,8),n+8}var R=n(98),z=n(99),I=n(100)
e.Buffer=o,e.SlowBuffer=function(t){return+t!=t&&(t=0),o.alloc(+t)},e.INSPECT_MAX_BYTES=50,o.TYPED_ARRAY_SUPPORT=void 0!==t.TYPED_ARRAY_SUPPORT?t.TYPED_ARRAY_SUPPORT:function(){try{var t=new Uint8Array(1)
return t.__proto__={__proto__:Uint8Array.prototype,foo:function(){return 42}},42===t.foo()&&"function"==typeof t.subarray&&0===t.subarray(1,1).byteLength}catch(t){return!1}}(),e.kMaxLength=i(),o.poolSize=8192,o._augment=function(t){return t.__proto__=o.prototype,t},o.from=function(t,e,n){return a(null,t,e,n)},o.TYPED_ARRAY_SUPPORT&&(o.prototype.__proto__=Uint8Array.prototype,o.__proto__=Uint8Array,"undefined"!=typeof Symbol&&Symbol.species&&o[Symbol.species]===o&&Object.defineProperty(o,Symbol.species,{value:null,configurable:!0})),o.alloc=function(t,e,n){return i=null,a=e,l=n,s(o=t),0>=o?r(i,o):void 0!==a?"string"==typeof l?r(i,o).fill(a,l):r(i,o).fill(a):r(i,o)
var i,o,a,l},o.allocUnsafe=function(t){return l(null,t)},o.allocUnsafeSlow=function(t){return l(null,t)},o.isBuffer=function(t){return!(null==t||!t._isBuffer)},o.compare=function(t,e){if(!o.isBuffer(t)||!o.isBuffer(e))throw new TypeError("Arguments must be Buffers")
if(t===e)return 0
for(var n=t.length,i=e.length,r=0,a=Math.min(n,i);a>r;++r)if(t[r]!==e[r]){n=t[r],i=e[r]
break}return i>n?-1:n>i?1:0},o.isEncoding=function(t){switch((t+"").toLowerCase()){case"hex":case"utf8":case"utf-8":case"ascii":case"latin1":case"binary":case"base64":case"ucs2":case"ucs-2":case"utf16le":case"utf-16le":return!0
default:return!1}},o.concat=function(t,e){if(!I(t))throw new TypeError('"list" argument must be an Array of Buffers')
if(0===t.length)return o.alloc(0)
var n
if(void 0===e)for(e=0,n=0;n<t.length;++n)e+=t[n].length
var i=o.allocUnsafe(e),r=0
for(n=0;n<t.length;++n){var a=t[n]
if(!o.isBuffer(a))throw new TypeError('"list" argument must be an Array of Buffers')
a.copy(i,r),r+=a.length}return i},o.byteLength=h,o.prototype._isBuffer=!0,o.prototype.swap16=function(){var t=this.length
if(t%2!=0)throw new RangeError("Buffer size must be a multiple of 16-bits")
for(var e=0;t>e;e+=2)f(this,e,e+1)
return this},o.prototype.swap32=function(){var t=this.length
if(t%4!=0)throw new RangeError("Buffer size must be a multiple of 32-bits")
for(var e=0;t>e;e+=4)f(this,e,e+3),f(this,e+1,e+2)
return this},o.prototype.swap64=function(){var t=this.length
if(t%8!=0)throw new RangeError("Buffer size must be a multiple of 64-bits")
for(var e=0;t>e;e+=8)f(this,e,e+7),f(this,e+1,e+6),f(this,e+2,e+5),f(this,e+3,e+4)
return this},o.prototype.toString=function(){var t=0|this.length
return 0===t?"":0===arguments.length?v(this,0,t):function(t,e,n){var i=!1
if((void 0===e||0>e)&&(e=0),e>this.length)return""
if((void 0===n||n>this.length)&&(n=this.length),0>=n)return""
if((n>>>=0)<=(e>>>=0))return""
for(t||(t="utf8");;)switch(t){case"hex":return b(this,e,n)
case"utf8":case"utf-8":return v(this,e,n)
case"ascii":return w(this,e,n)
case"latin1":case"binary":return x(this,e,n)
case"base64":return y(this,e,n)
case"ucs2":case"ucs-2":case"utf16le":case"utf-16le":return _(this,e,n)
default:if(i)throw new TypeError("Unknown encoding: "+t)
t=(t+"").toLowerCase(),i=!0}}.apply(this,arguments)},o.prototype.equals=function(t){if(!o.isBuffer(t))throw new TypeError("Argument must be a Buffer")
return this===t||0===o.compare(this,t)},o.prototype.inspect=function(){var t="",n=e.INSPECT_MAX_BYTES
return this.length>0&&(t=this.toString("hex",0,n).match(/.{2}/g).join(" "),this.length>n&&(t+=" ... ")),"<Buffer "+t+">"},o.prototype.compare=function(t,e,n,i,r){if(!o.isBuffer(t))throw new TypeError("Argument must be a Buffer")
if(void 0===e&&(e=0),void 0===n&&(n=t?t.length:0),void 0===i&&(i=0),void 0===r&&(r=this.length),0>e||n>t.length||0>i||r>this.length)throw new RangeError("out of range index")
if(i>=r&&e>=n)return 0
if(i>=r)return-1
if(e>=n)return 1
if(this===t)return 0
for(var a=(r>>>=0)-(i>>>=0),s=(n>>>=0)-(e>>>=0),l=Math.min(a,s),u=this.slice(i,r),c=t.slice(e,n),h=0;l>h;++h)if(u[h]!==c[h]){a=u[h],s=c[h]
break}return s>a?-1:a>s?1:0},o.prototype.includes=function(t,e,n){return-1!==this.indexOf(t,e,n)},o.prototype.indexOf=function(t,e,n){return d(this,t,e,n,!0)},o.prototype.lastIndexOf=function(t,e,n){return d(this,t,e,n,!1)},o.prototype.write=function(t,e,n,i){if(void 0===e)i="utf8",n=this.length,e=0
else if(void 0===n&&"string"==typeof e)i=e,n=this.length,e=0
else{if(!isFinite(e))throw Error("Buffer.write(string, encoding, offset[, length]) is no longer supported")
e|=0,isFinite(n)?(n|=0,void 0===i&&(i="utf8")):(i=n,n=void 0)}var r=this.length-e
if((void 0===n||n>r)&&(n=r),t.length>0&&(0>n||0>e)||e>this.length)throw new RangeError("Attempt to write outside buffer bounds")
i||(i="utf8")
for(var o,a,s,l,u,c,h,f,d,p=!1;;)switch(i){case"hex":return m(this,t,e,n)
case"utf8":case"utf-8":return f=e,d=n,U(O(t,(h=this).length-f),h,f,d)
case"ascii":return g(this,t,e,n)
case"latin1":case"binary":return g(this,t,e,n)
case"base64":return l=this,u=e,c=n,U(W(t),l,u,c)
case"ucs2":case"ucs-2":case"utf16le":case"utf-16le":return a=e,s=n,U(function(t,e){for(var n,i,r,o=[],a=0;a<t.length&&!((e-=2)<0);++a)n=t.charCodeAt(a),i=n>>8,r=n%256,o.push(r),o.push(i)
return o}(t,(o=this).length-a),o,a,s)
default:if(p)throw new TypeError("Unknown encoding: "+i)
i=(""+i).toLowerCase(),p=!0}},o.prototype.toJSON=function(){return{type:"Buffer",data:Array.prototype.slice.call(this._arr||this,0)}}
var C=4096
o.prototype.slice=function(t,e){var n,i=this.length
if((t=~~t)<0?(t+=i)<0&&(t=0):t>i&&(t=i),(e=void 0===e?i:~~e)<0?(e+=i)<0&&(e=0):e>i&&(e=i),t>e&&(e=t),o.TYPED_ARRAY_SUPPORT)(n=this.subarray(t,e)).__proto__=o.prototype
else{var r=e-t
n=new o(r,void 0)
for(var a=0;r>a;++a)n[a]=this[a+t]}return n},o.prototype.readUIntLE=function(t,e,n){t|=0,e|=0,n||B(t,e,this.length)
for(var i=this[t],r=1,o=0;++o<e&&(r*=256);)i+=this[t+o]*r
return i},o.prototype.readUIntBE=function(t,e,n){t|=0,e|=0,n||B(t,e,this.length)
for(var i=this[t+--e],r=1;e>0&&(r*=256);)i+=this[t+--e]*r
return i},o.prototype.readUInt8=function(t,e){return e||B(t,1,this.length),this[t]},o.prototype.readUInt16LE=function(t,e){return e||B(t,2,this.length),this[t]|this[t+1]<<8},o.prototype.readUInt16BE=function(t,e){return e||B(t,2,this.length),this[t]<<8|this[t+1]},o.prototype.readUInt32LE=function(t,e){return e||B(t,4,this.length),(this[t]|this[t+1]<<8|this[t+2]<<16)+16777216*this[t+3]},o.prototype.readUInt32BE=function(t,e){return e||B(t,4,this.length),16777216*this[t]+(this[t+1]<<16|this[t+2]<<8|this[t+3])},o.prototype.readIntLE=function(t,e,n){t|=0,e|=0,n||B(t,e,this.length)
for(var i=this[t],r=1,o=0;++o<e&&(r*=256);)i+=this[t+o]*r
return i>=(r*=128)&&(i-=Math.pow(2,8*e)),i},o.prototype.readIntBE=function(t,e,n){t|=0,e|=0,n||B(t,e,this.length)
for(var i=e,r=1,o=this[t+--i];i>0&&(r*=256);)o+=this[t+--i]*r
return o>=(r*=128)&&(o-=Math.pow(2,8*e)),o},o.prototype.readInt8=function(t,e){return e||B(t,1,this.length),128&this[t]?-1*(255-this[t]+1):this[t]},o.prototype.readInt16LE=function(t,e){e||B(t,2,this.length)
var n=this[t]|this[t+1]<<8
return 32768&n?4294901760|n:n},o.prototype.readInt16BE=function(t,e){e||B(t,2,this.length)
var n=this[t+1]|this[t]<<8
return 32768&n?4294901760|n:n},o.prototype.readInt32LE=function(t,e){return e||B(t,4,this.length),this[t]|this[t+1]<<8|this[t+2]<<16|this[t+3]<<24},o.prototype.readInt32BE=function(t,e){return e||B(t,4,this.length),this[t]<<24|this[t+1]<<16|this[t+2]<<8|this[t+3]},o.prototype.readFloatLE=function(t,e){return e||B(t,4,this.length),z.read(this,t,!0,23,4)},o.prototype.readFloatBE=function(t,e){return e||B(t,4,this.length),z.read(this,t,!1,23,4)},o.prototype.readDoubleLE=function(t,e){return e||B(t,8,this.length),z.read(this,t,!0,52,8)},o.prototype.readDoubleBE=function(t,e){return e||B(t,8,this.length),z.read(this,t,!1,52,8)},o.prototype.writeUIntLE=function(t,e,n,i){t=+t,e|=0,n|=0,i||k(this,t,e,n,Math.pow(2,8*n)-1,0)
var r=1,o=0
for(this[e]=255&t;++o<n&&(r*=256);)this[e+o]=t/r&255
return e+n},o.prototype.writeUIntBE=function(t,e,n,i){t=+t,e|=0,n|=0,i||k(this,t,e,n,Math.pow(2,8*n)-1,0)
var r=n-1,o=1
for(this[e+r]=255&t;--r>=0&&(o*=256);)this[e+r]=t/o&255
return e+n},o.prototype.writeUInt8=function(t,e,n){return t=+t,e|=0,n||k(this,t,e,1,255,0),o.TYPED_ARRAY_SUPPORT||(t=Math.floor(t)),this[e]=255&t,e+1},o.prototype.writeUInt16LE=function(t,e,n){return t=+t,e|=0,n||k(this,t,e,2,65535,0),o.TYPED_ARRAY_SUPPORT?(this[e]=255&t,this[e+1]=t>>>8):E(this,t,e,!0),e+2},o.prototype.writeUInt16BE=function(t,e,n){return t=+t,e|=0,n||k(this,t,e,2,65535,0),o.TYPED_ARRAY_SUPPORT?(this[e]=t>>>8,this[e+1]=255&t):E(this,t,e,!1),e+2},o.prototype.writeUInt32LE=function(t,e,n){return t=+t,e|=0,n||k(this,t,e,4,4294967295,0),o.TYPED_ARRAY_SUPPORT?(this[e+3]=t>>>24,this[e+2]=t>>>16,this[e+1]=t>>>8,this[e]=255&t):T(this,t,e,!0),e+4},o.prototype.writeUInt32BE=function(t,e,n){return t=+t,e|=0,n||k(this,t,e,4,4294967295,0),o.TYPED_ARRAY_SUPPORT?(this[e]=t>>>24,this[e+1]=t>>>16,this[e+2]=t>>>8,this[e+3]=255&t):T(this,t,e,!1),e+4},o.prototype.writeIntLE=function(t,e,n,i){if(t=+t,e|=0,!i){var r=Math.pow(2,8*n-1)
k(this,t,e,n,r-1,-r)}var o=0,a=1,s=0
for(this[e]=255&t;++o<n&&(a*=256);)0>t&&0===s&&0!==this[e+o-1]&&(s=1),this[e+o]=(t/a>>0)-s&255
return e+n},o.prototype.writeIntBE=function(t,e,n,i){if(t=+t,e|=0,!i){var r=Math.pow(2,8*n-1)
k(this,t,e,n,r-1,-r)}var o=n-1,a=1,s=0
for(this[e+o]=255&t;--o>=0&&(a*=256);)0>t&&0===s&&0!==this[e+o+1]&&(s=1),this[e+o]=(t/a>>0)-s&255
return e+n},o.prototype.writeInt8=function(t,e,n){return t=+t,e|=0,n||k(this,t,e,1,127,-128),o.TYPED_ARRAY_SUPPORT||(t=Math.floor(t)),0>t&&(t=255+t+1),this[e]=255&t,e+1},o.prototype.writeInt16LE=function(t,e,n){return t=+t,e|=0,n||k(this,t,e,2,32767,-32768),o.TYPED_ARRAY_SUPPORT?(this[e]=255&t,this[e+1]=t>>>8):E(this,t,e,!0),e+2},o.prototype.writeInt16BE=function(t,e,n){return t=+t,e|=0,n||k(this,t,e,2,32767,-32768),o.TYPED_ARRAY_SUPPORT?(this[e]=t>>>8,this[e+1]=255&t):E(this,t,e,!1),e+2},o.prototype.writeInt32LE=function(t,e,n){return t=+t,e|=0,n||k(this,t,e,4,2147483647,-2147483648),o.TYPED_ARRAY_SUPPORT?(this[e]=255&t,this[e+1]=t>>>8,this[e+2]=t>>>16,this[e+3]=t>>>24):T(this,t,e,!0),e+4},o.prototype.writeInt32BE=function(t,e,n){return t=+t,e|=0,n||k(this,t,e,4,2147483647,-2147483648),0>t&&(t=4294967295+t+1),o.TYPED_ARRAY_SUPPORT?(this[e]=t>>>24,this[e+1]=t>>>16,this[e+2]=t>>>8,this[e+3]=255&t):T(this,t,e,!1),e+4},o.prototype.writeFloatLE=function(t,e,n){return P(this,t,e,!0,n)},o.prototype.writeFloatBE=function(t,e,n){return P(this,t,e,!1,n)},o.prototype.writeDoubleLE=function(t,e,n){return A(this,t,e,!0,n)},o.prototype.writeDoubleBE=function(t,e,n){return A(this,t,e,!1,n)},o.prototype.copy=function(t,e,n,i){if(n||(n=0),i||0===i||(i=this.length),e>=t.length&&(e=t.length),e||(e=0),i>0&&n>i&&(i=n),i===n)return 0
if(0===t.length||0===this.length)return 0
if(0>e)throw new RangeError("targetStart out of bounds")
if(0>n||n>=this.length)throw new RangeError("sourceStart out of bounds")
if(0>i)throw new RangeError("sourceEnd out of bounds")
i>this.length&&(i=this.length),t.length-e<i-n&&(i=t.length-e+n)
var r,a=i-n
if(this===t&&e>n&&i>e)for(r=a-1;r>=0;--r)t[r+e]=this[r+n]
else if(1e3>a||!o.TYPED_ARRAY_SUPPORT)for(r=0;a>r;++r)t[r+e]=this[r+n]
else Uint8Array.prototype.set.call(t,this.subarray(n,n+a),e)
return a},o.prototype.fill=function(t,e,n,i){}}).call(this,n(46))},function(t,e,n){"use strict"
e.byteLength=function(t){return 3*t.length/4-u(t)},e.toByteArray=function(t){},e.fromByteArray=function(t){}
for(var i=[],r=[],o=("undefined"!=typeof Uint8Array?Uint8Array:Array,"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"),a=0,s=o.length;s>a;++a)i[a]=o[a],r[o.charCodeAt(a)]=a
r["-".charCodeAt(0)]=62,r["_".charCodeAt(0)]=63},function(t,e){e.read=function(t,e,n,i,r){},e.write=function(t,e,n,i,r,o){}},function(t,e){({}).toString,t.exports=Array.isArray||function(t){}},function(t,e,n){"use strict"
function i(t){return t&&t.__esModule?t:{"default":t}}Object.defineProperty(e,"__esModule",{value:!0})
var r=i(n(0)),o=function(){function t(t,e){for(var n=0;n<e.length;n++){var i=e[n]
i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),(0,r["default"])(t,i.key,i)}}return function(e,n,i){return n&&t(e.prototype,n),i&&t(e,i),e}}(),a=(i(n(9)),i(n(16))),s=function(){function t(e){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t),this.element=e,this.data=this.getDataFromElement(e),this.data.android=a["default"].isAndroid()&&a["default"].isMobile(),this.data.ios=a["default"].isIOS()&&a["default"].isMobile()}return o(t,[{key:"getDataFromElement",value:function(t){}},{key:"validate",value:function(){}},{key:"render",value:function(){}},{key:"reload",value:function(){}}]),t}()
e["default"]=s},function(t,e,n){"use strict"
function i(t){return t&&t.__esModule?t:{"default":t}}Object.defineProperty(e,"__esModule",{value:!0})
var r=i(n(0)),o=function(){function t(t,e){for(var n=0;n<e.length;n++){var i=e[n]
i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),(0,r["default"])(t,i.key,i)}}return function(e,n,i){return n&&t(e.prototype,n),i&&t(e,i),e}}(),a=(i(n(9)),function(){return o(t,[{key:"checkInAppZalo",value:function(){}},{key:"getDataFromElement",value:function(t){}},{key:"validate",value:function(){}},{key:"render",value:function(){}},{key:"reload",value:function(){this.iframe.contentWindow.postMessage("close_zlogin_popup","https://button-follow.zalo.me")}},{key:"receiveMessage",value:function(t){}}]),t}())
e["default"]=a},function(t,e,n){"use strict"
function i(t){return t&&t.__esModule?t:{"default":t}}Object.defineProperty(e,"__esModule",{value:!0})
var r=i(n(0)),o=function(){function t(t,e){for(var n=0;n<e.length;n++){var i=e[n]
i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),(0,r["default"])(t,i.key,i)}}return function(e,n,i){return n&&t(e.prototype,n),i&&t(e,i),e}}(),a=(i(n(16)),i(n(9)),function(){return o(t,[{key:"getDataFromElement",value:function(t){}},{key:"validate",value:function(t){}},{key:"reload",value:function(){}},{key:"resizeParent",value:function(t){document.getElementsByClassName("zalo-comment-plugin")[0].style.height=t+"px"}},{key:"getTopParentBody",value:function(){}},{key:"render",value:function(){}},{key:"destroy",value:function(){}},{key:"getIframe",get:function(){}}]),t}())
e["default"]=a},function(t,e,n){"use strict"
function i(t){return t&&t.__esModule?t:{"default":t}}Object.defineProperty(e,"__esModule",{value:!0})
var r=i(n(0)),o=function(){function t(t,e){for(var n=0;n<e.length;n++){var i=e[n]
i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),(0,r["default"])(t,i.key,i)}}return function(e,n,i){return n&&t(e.prototype,n),i&&t(e,i),e}}(),a=(i(n(9)),function(){return o(t,[{key:"getDataFromElement",value:function(t){}},{key:"validate",value:function(){}},{key:"render",value:function(){}},{key:"showQRModal",value:function(t,e){}},{key:"reload",value:function(){this.iframe.contentWindow.postMessage("close_zlogin_popup","https://button-call.zalo.me")}}]),t}())
e["default"]=a},function(t,e){function n(){}function i(t,e){return Math.floor(Math.random()*(e-t+1))+t}n.maxFromBits=function(t){return Math.pow(2,t)},n.limitUI04=n.maxFromBits(4),n.limitUI06=n.maxFromBits(6),n.limitUI08=n.maxFromBits(8),n.limitUI12=n.maxFromBits(12),n.limitUI14=n.maxFromBits(14),n.limitUI16=n.maxFromBits(16),n.limitUI32=n.maxFromBits(32),n.limitUI40=n.maxFromBits(40),n.limitUI48=n.maxFromBits(48),n.randomUI04=function(){},n.randomUI06=function(){return i(0,n.limitUI06-1)},n.randomUI08=function(){return i(0,n.limitUI08-1)},n.randomUI12=function(){return i(0,n.limitUI12-1)},n.randomUI14=function(){},n.randomUI16=function(){return i(0,n.limitUI16-1)},n.randomUI32=function(){return i(0,n.limitUI32-1)},n.randomUI40=function(){},n.randomUI48=function(){return(0|Math.random()*(1<<30))+(0|Math.random()*(1<<18))*(1<<30)},n.paddedString=function(t,e,n){n=n||"0"
for(var i=e-(t+="").length;i>0;i>>>=1,n+=n)1&i&&(t=n+t)
return t},n.prototype.fromParts=function(t,e,i,r,o,a){return this.version=i>>12&15,this.hex=n.paddedString(t.toString(16),8)+"-"+n.paddedString(e.toString(16),4)+"-"+n.paddedString(i.toString(16),4)+"-"+n.paddedString(r.toString(16),2)+n.paddedString(o.toString(16),2)+"-"+n.paddedString(a.toString(16),12),this},n.prototype.toString=function(){return this.hex},n.prototype.toURN=function(){},n.prototype.toBytes=function(){},n.prototype.equals=function(t){},n.getTimeFieldValues=function(t){},n._create4=function(){return(new n).fromParts(n.randomUI32(),n.randomUI16(),16384|n.randomUI12(),128|n.randomUI06(),n.randomUI08(),n.randomUI48())},n._create1=function(){},n.create=function(t){return this["_create"+(t=t||4)]()},n.fromTime=function(t,e){},n.firstFromTime=function(t){},n.lastFromTime=function(t){},n.fromURN=function(t){var e
return(e=/^(?:urn:uuid:|\{)?([0-9a-f]{8})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{2})([0-9a-f]{2})-([0-9a-f]{12})(?:\})?$/i.exec(t))?(new n).fromParts(parseInt(e[1],16),parseInt(e[2],16),parseInt(e[3],16),parseInt(e[4],16),parseInt(e[5],16),parseInt(e[6],16)):null},n.fromBytes=function(t){},n.fromBinary=function(t){},n["new"]=function(){},n.newTS=function(){},t.exports=n},function(t,e,n){"use strict"
Object.defineProperty(e,"__esModule",{value:!0})
var i,r=n(0),o=(i=r)&&i.__esModule?i:{"default":i},a=function(){function t(t,e){for(var n=0;n<e.length;n++){var i=e[n]
i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),(0,o["default"])(t,i.key,i)}}return function(e,n,i){return n&&t(e.prototype,n),i&&t(e,i),e}}(),s=function(){return a(t,null,[{key:"isMaliciousScheme",value:function(t){}}]),t}()
e["default"]=s},function(t,e,n){"use strict"
Object.defineProperty(e,"__esModule",{value:!0})
var i,r=n(0),o=(i=r)&&i.__esModule?i:{"default":i},a=function(){function t(t,e){for(var n=0;n<e.length;n++){var i=e[n]
i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),(0,o["default"])(t,i.key,i)}}return function(e,n,i){return n&&t(e.prototype,n),i&&t(e,i),e}}(),s=function(){return a(t,null,[{key:"loadFile",value:function(t,e){}}]),t}()
e["default"]=s}])})}catch(e){throw get("https://sp.zalo.me/tracking/log?error="+encodeURIComponent(e)+"&data=InitSDK"),Error(e)}"undefined"==typeof ZA&&(window._zap=window._zap||[],window._zap.push(["_setAccount","ZA-43317204427353"]),function(t,e,n,i,r,o,a){o=e.createElement(n),a=e.getElementsByTagName(n)[0],o.async=1,o.src=i+"?"+Math.floor((new Date).getTime()/864e5),a.parentNode.insertBefore(o,a)}(window,document,"script","//za.zdn.vn/v3/za.js","ZA"))
