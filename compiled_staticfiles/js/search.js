// Ion.RangeSlider
// version 2.2.0 Build: 380
// © Denis Ineshin, 2017
// https://github.com/IonDen
//
// Project page:    http://ionden.com/a/plugins/ion.rangeSlider/en.html
// GitHub page:     https://github.com/IonDen/ion.rangeSlider
//
// Released under MIT licence:
// http://ionden.com/a/plugins/licence-en.html
// =====================================================================================================================
(function(o){"function"==typeof define&&define.amd?define(["jquery"],function(e){return o(e,document,window,navigator)}):"object"==typeof exports?o(require("jquery"),document,window,navigator):o(jQuery,document,window,navigator)})(function(o,e,t,i){"use strict";var s=0,a=function(){var e,t=i.userAgent,s=/msie\s\d+/i;return!!(0<t.search(s)&&(e=s.exec(t).toString(),e=e.split(" ")[1],9>e))&&(o("html").addClass("lt-ie9"),!0)}();Function.prototype.bind||(Function.prototype.bind=function(o){var e=this,t=[].slice;if("function"!=typeof e)throw new TypeError;var r=t.call(arguments,1),i=function(){if(this instanceof i){var s=function(){};s.prototype=e.prototype;var a=new s,n=e.apply(a,r.concat(t.call(arguments)));return Object(n)===n?n:a}return e.apply(o,r.concat(t.call(arguments)))};return i}),Array.prototype.indexOf||(Array.prototype.indexOf=function(o,e){var t;if(null==this)throw new TypeError("\"this\" is null or not defined");var r=Object(this),i=r.length>>>0;if(0===i)return-1;var s=+e||0;if(Math.abs(s)===1/0&&(s=0),s>=i)return-1;for(t=Math.max(0<=s?s:i-Math.abs(s),0);t<i;){if(t in r&&r[t]===o)return t;t++}return-1});var n=function(r,i,s){this.VERSION="2.2.0",this.input=r,this.plugin_count=s,this.current_plugin=0,this.calc_count=0,this.update_tm=0,this.old_from=0,this.old_to=0,this.old_min_interval=null,this.raf_id=null,this.dragging=!1,this.force_redraw=!1,this.no_diapason=!1,this.has_tab_index=!0,this.is_key=!1,this.is_update=!1,this.is_start=!0,this.is_finish=!1,this.is_active=!1,this.is_resize=!1,this.is_click=!1,i=i||{},this.$cache={win:o(t),body:o(e.body),input:o(r),cont:null,rs:null,min:null,max:null,from:null,to:null,single:null,bar:null,line:null,s_single:null,s_from:null,s_to:null,shad_single:null,shad_from:null,shad_to:null,edge:null,grid:null,grid_labels:[]},this.coords={x_gap:0,x_pointer:0,w_rs:0,w_rs_old:0,w_handle:0,p_gap:0,p_gap_left:0,p_gap_right:0,p_step:0,p_pointer:0,p_handle:0,p_single_fake:0,p_single_real:0,p_from_fake:0,p_from_real:0,p_to_fake:0,p_to_real:0,p_bar_x:0,p_bar_w:0,grid_gap:0,big_num:0,big:[],big_w:[],big_p:[],big_x:[]},this.labels={w_min:0,w_max:0,w_from:0,w_to:0,w_single:0,p_min:0,p_max:0,p_from_fake:0,p_from_left:0,p_to_fake:0,p_to_left:0,p_single_fake:0,p_single_left:0};var a,n,c,l=this.$cache.input,_=l.prop("value");for(c in a={type:"single",min:10,max:100,from:null,to:null,step:1,min_interval:0,max_interval:0,drag_interval:!1,values:[],p_values:[],from_fixed:!1,from_min:null,from_max:null,from_shadow:!1,to_fixed:!1,to_min:null,to_max:null,to_shadow:!1,prettify_enabled:!0,prettify_separator:" ",prettify:null,force_edges:!1,keyboard:!0,grid:!1,grid_margin:!0,grid_num:4,grid_snap:!1,hide_min_max:!1,hide_from_to:!1,prefix:"",postfix:"",max_postfix:"",decorate_both:!0,values_separator:" \u2014 ",input_values_separator:";",disable:!1,block:!1,extra_classes:"",scope:null,onStart:null,onChange:null,onFinish:null,onUpdate:null},"INPUT"!==l[0].nodeName&&console&&console.warn&&console.warn("Base element should be <input>!",l[0]),n={type:l.data("type"),min:l.data("min"),max:l.data("max"),from:l.data("from"),to:l.data("to"),step:l.data("step"),min_interval:l.data("minInterval"),max_interval:l.data("maxInterval"),drag_interval:l.data("dragInterval"),values:l.data("values"),from_fixed:l.data("fromFixed"),from_min:l.data("fromMin"),from_max:l.data("fromMax"),from_shadow:l.data("fromShadow"),to_fixed:l.data("toFixed"),to_min:l.data("toMin"),to_max:l.data("toMax"),to_shadow:l.data("toShadow"),prettify_enabled:l.data("prettifyEnabled"),prettify_separator:l.data("prettifySeparator"),force_edges:l.data("forceEdges"),keyboard:l.data("keyboard"),grid:l.data("grid"),grid_margin:l.data("gridMargin"),grid_num:l.data("gridNum"),grid_snap:l.data("gridSnap"),hide_min_max:l.data("hideMinMax"),hide_from_to:l.data("hideFromTo"),prefix:l.data("prefix"),postfix:l.data("postfix"),max_postfix:l.data("maxPostfix"),decorate_both:l.data("decorateBoth"),values_separator:l.data("valuesSeparator"),input_values_separator:l.data("inputValuesSeparator"),disable:l.data("disable"),block:l.data("block"),extra_classes:l.data("extraClasses")},n.values=n.values&&n.values.split(","),n)n.hasOwnProperty(c)&&(void 0===n[c]||""===n[c])&&delete n[c];void 0!==_&&""!==_&&(_=_.split(n.input_values_separator||i.input_values_separator||";"),_[0]&&_[0]==+_[0]&&(_[0]=+_[0]),_[1]&&_[1]==+_[1]&&(_[1]=+_[1]),i&&i.values&&i.values.length?(a.from=_[0]&&i.values.indexOf(_[0]),a.to=_[1]&&i.values.indexOf(_[1])):(a.from=_[0]&&+_[0],a.to=_[1]&&+_[1])),o.extend(a,i),o.extend(a,n),this.options=a,this.update_check={},this.validate(),this.result={input:this.$cache.input,slider:null,min:this.options.min,max:this.options.max,from:this.options.from,from_percent:0,from_value:null,to:this.options.to,to_percent:0,to_value:null},this.init()};n.prototype={init:function(o){this.no_diapason=!1,this.coords.p_step=this.convertToPercent(this.options.step,!0),this.target="base",this.toggleInput(),this.append(),this.setMinMax(),o?(this.force_redraw=!0,this.calc(!0),this.callOnUpdate()):(this.force_redraw=!0,this.calc(!0),this.callOnStart()),this.updateScene()},append:function(){var o="<span class=\"irs js-irs-"+this.plugin_count+" "+this.options.extra_classes+"\"></span>";this.$cache.input.before(o),this.$cache.input.prop("readonly",!0),this.$cache.cont=this.$cache.input.prev(),this.result.slider=this.$cache.cont,this.$cache.cont.html("<span class=\"irs\"><span class=\"irs-line\" tabindex=\"0\"><span class=\"irs-line-left\"></span><span class=\"irs-line-mid\"></span><span class=\"irs-line-right\"></span></span><span class=\"irs-min\">0</span><span class=\"irs-max\">1</span><span class=\"irs-from\">0</span><span class=\"irs-to\">0</span><span class=\"irs-single\">0</span></span><span class=\"irs-grid\"></span><span class=\"irs-bar\"></span>"),this.$cache.rs=this.$cache.cont.find(".irs"),this.$cache.min=this.$cache.cont.find(".irs-min"),this.$cache.max=this.$cache.cont.find(".irs-max"),this.$cache.from=this.$cache.cont.find(".irs-from"),this.$cache.to=this.$cache.cont.find(".irs-to"),this.$cache.single=this.$cache.cont.find(".irs-single"),this.$cache.bar=this.$cache.cont.find(".irs-bar"),this.$cache.line=this.$cache.cont.find(".irs-line"),this.$cache.grid=this.$cache.cont.find(".irs-grid"),"single"===this.options.type?(this.$cache.cont.append("<span class=\"irs-bar-edge\"></span><span class=\"irs-shadow shadow-single\"></span><span class=\"irs-slider single\"></span>"),this.$cache.edge=this.$cache.cont.find(".irs-bar-edge"),this.$cache.s_single=this.$cache.cont.find(".single"),this.$cache.from[0].style.visibility="hidden",this.$cache.to[0].style.visibility="hidden",this.$cache.shad_single=this.$cache.cont.find(".shadow-single")):(this.$cache.cont.append("<span class=\"irs-shadow shadow-from\"></span><span class=\"irs-shadow shadow-to\"></span><span class=\"irs-slider from\"></span><span class=\"irs-slider to\"></span>"),this.$cache.s_from=this.$cache.cont.find(".from"),this.$cache.s_to=this.$cache.cont.find(".to"),this.$cache.shad_from=this.$cache.cont.find(".shadow-from"),this.$cache.shad_to=this.$cache.cont.find(".shadow-to"),this.setTopHandler()),this.options.hide_from_to&&(this.$cache.from[0].style.display="none",this.$cache.to[0].style.display="none",this.$cache.single[0].style.display="none"),this.appendGrid(),this.options.disable?(this.appendDisableMask(),this.$cache.input[0].disabled=!0):(this.$cache.input[0].disabled=!1,this.removeDisableMask(),this.bindEvents()),this.options.disable||(this.options.block?this.appendDisableMask():this.removeDisableMask()),this.options.drag_interval&&(this.$cache.bar[0].style.cursor="ew-resize")},setTopHandler:function(){var o=this.options.min,e=this.options.max,t=this.options.from,r=this.options.to;t>o&&r===e?this.$cache.s_from.addClass("type_last"):r<e&&this.$cache.s_to.addClass("type_last")},changeLevel:function(o){"single"===o?(this.coords.p_gap=this.toFixed(this.coords.p_pointer-this.coords.p_single_fake),this.$cache.s_single.addClass("state_hover")):"from"===o?(this.coords.p_gap=this.toFixed(this.coords.p_pointer-this.coords.p_from_fake),this.$cache.s_from.addClass("state_hover"),this.$cache.s_from.addClass("type_last"),this.$cache.s_to.removeClass("type_last")):"to"===o?(this.coords.p_gap=this.toFixed(this.coords.p_pointer-this.coords.p_to_fake),this.$cache.s_to.addClass("state_hover"),this.$cache.s_to.addClass("type_last"),this.$cache.s_from.removeClass("type_last")):"both"===o?(this.coords.p_gap_left=this.toFixed(this.coords.p_pointer-this.coords.p_from_fake),this.coords.p_gap_right=this.toFixed(this.coords.p_to_fake-this.coords.p_pointer),this.$cache.s_to.removeClass("type_last"),this.$cache.s_from.removeClass("type_last")):void 0},appendDisableMask:function(){this.$cache.cont.append("<span class=\"irs-disable-mask\"></span>"),this.$cache.cont.addClass("irs-disabled")},removeDisableMask:function(){this.$cache.cont.remove(".irs-disable-mask"),this.$cache.cont.removeClass("irs-disabled")},remove:function(){this.$cache.cont.remove(),this.$cache.cont=null,this.$cache.line.off("keydown.irs_"+this.plugin_count),this.$cache.body.off("touchmove.irs_"+this.plugin_count),this.$cache.body.off("mousemove.irs_"+this.plugin_count),this.$cache.win.off("touchend.irs_"+this.plugin_count),this.$cache.win.off("mouseup.irs_"+this.plugin_count),a&&(this.$cache.body.off("mouseup.irs_"+this.plugin_count),this.$cache.body.off("mouseleave.irs_"+this.plugin_count)),this.$cache.grid_labels=[],this.coords.big=[],this.coords.big_w=[],this.coords.big_p=[],this.coords.big_x=[],cancelAnimationFrame(this.raf_id)},bindEvents:function(){this.no_diapason||(this.$cache.body.on("touchmove.irs_"+this.plugin_count,this.pointerMove.bind(this)),this.$cache.body.on("mousemove.irs_"+this.plugin_count,this.pointerMove.bind(this)),this.$cache.win.on("touchend.irs_"+this.plugin_count,this.pointerUp.bind(this)),this.$cache.win.on("mouseup.irs_"+this.plugin_count,this.pointerUp.bind(this)),this.$cache.line.on("touchstart.irs_"+this.plugin_count,this.pointerClick.bind(this,"click")),this.$cache.line.on("mousedown.irs_"+this.plugin_count,this.pointerClick.bind(this,"click")),this.$cache.line.on("focus.irs_"+this.plugin_count,this.pointerFocus.bind(this)),this.options.drag_interval&&"double"===this.options.type?(this.$cache.bar.on("touchstart.irs_"+this.plugin_count,this.pointerDown.bind(this,"both")),this.$cache.bar.on("mousedown.irs_"+this.plugin_count,this.pointerDown.bind(this,"both"))):(this.$cache.bar.on("touchstart.irs_"+this.plugin_count,this.pointerClick.bind(this,"click")),this.$cache.bar.on("mousedown.irs_"+this.plugin_count,this.pointerClick.bind(this,"click"))),"single"===this.options.type?(this.$cache.single.on("touchstart.irs_"+this.plugin_count,this.pointerDown.bind(this,"single")),this.$cache.s_single.on("touchstart.irs_"+this.plugin_count,this.pointerDown.bind(this,"single")),this.$cache.shad_single.on("touchstart.irs_"+this.plugin_count,this.pointerClick.bind(this,"click")),this.$cache.single.on("mousedown.irs_"+this.plugin_count,this.pointerDown.bind(this,"single")),this.$cache.s_single.on("mousedown.irs_"+this.plugin_count,this.pointerDown.bind(this,"single")),this.$cache.edge.on("mousedown.irs_"+this.plugin_count,this.pointerClick.bind(this,"click")),this.$cache.shad_single.on("mousedown.irs_"+this.plugin_count,this.pointerClick.bind(this,"click"))):(this.$cache.single.on("touchstart.irs_"+this.plugin_count,this.pointerDown.bind(this,null)),this.$cache.single.on("mousedown.irs_"+this.plugin_count,this.pointerDown.bind(this,null)),this.$cache.from.on("touchstart.irs_"+this.plugin_count,this.pointerDown.bind(this,"from")),this.$cache.s_from.on("touchstart.irs_"+this.plugin_count,this.pointerDown.bind(this,"from")),this.$cache.to.on("touchstart.irs_"+this.plugin_count,this.pointerDown.bind(this,"to")),this.$cache.s_to.on("touchstart.irs_"+this.plugin_count,this.pointerDown.bind(this,"to")),this.$cache.shad_from.on("touchstart.irs_"+this.plugin_count,this.pointerClick.bind(this,"click")),this.$cache.shad_to.on("touchstart.irs_"+this.plugin_count,this.pointerClick.bind(this,"click")),this.$cache.from.on("mousedown.irs_"+this.plugin_count,this.pointerDown.bind(this,"from")),this.$cache.s_from.on("mousedown.irs_"+this.plugin_count,this.pointerDown.bind(this,"from")),this.$cache.to.on("mousedown.irs_"+this.plugin_count,this.pointerDown.bind(this,"to")),this.$cache.s_to.on("mousedown.irs_"+this.plugin_count,this.pointerDown.bind(this,"to")),this.$cache.shad_from.on("mousedown.irs_"+this.plugin_count,this.pointerClick.bind(this,"click")),this.$cache.shad_to.on("mousedown.irs_"+this.plugin_count,this.pointerClick.bind(this,"click"))),this.options.keyboard&&this.$cache.line.on("keydown.irs_"+this.plugin_count,this.key.bind(this,"keyboard")),a&&(this.$cache.body.on("mouseup.irs_"+this.plugin_count,this.pointerUp.bind(this)),this.$cache.body.on("mouseleave.irs_"+this.plugin_count,this.pointerUp.bind(this))))},pointerFocus:function(){if(!this.target){var o,e;e="single"===this.options.type?this.$cache.single:this.$cache.from,o=e.offset().left,o+=e.width()/2-1,this.pointerClick("single",{preventDefault:function(){},pageX:o})}},pointerMove:function(o){if(this.dragging){var e=o.pageX||o.originalEvent.touches&&o.originalEvent.touches[0].pageX;this.coords.x_pointer=e-this.coords.x_gap,this.calc()}},pointerUp:function(t){if(this.current_plugin===this.plugin_count){if(this.is_active)this.is_active=!1;else return;this.$cache.cont.find(".state_hover").removeClass("state_hover"),this.force_redraw=!0,a&&o("*").prop("unselectable",!1),this.updateScene(),this.restoreOriginalMinInterval(),(o.contains(this.$cache.cont[0],t.target)||this.dragging)&&this.callOnFinish(),this.dragging=!1}},pointerDown:function(t,r){r.preventDefault();var e=r.pageX||r.originalEvent.touches&&r.originalEvent.touches[0].pageX;2===r.button||("both"===t&&this.setTempMinInterval(),!t&&(t=this.target||"from"),this.current_plugin=this.plugin_count,this.target=t,this.is_active=!0,this.dragging=!0,this.coords.x_gap=this.$cache.rs.offset().left,this.coords.x_pointer=e-this.coords.x_gap,this.calcPointerPercent(),this.changeLevel(t),a&&o("*").prop("unselectable",!0),this.$cache.line.trigger("focus"),this.updateScene())},pointerClick:function(o,t){t.preventDefault();var e=t.pageX||t.originalEvent.touches&&t.originalEvent.touches[0].pageX;2===t.button||(this.current_plugin=this.plugin_count,this.target=o,this.is_click=!0,this.coords.x_gap=this.$cache.rs.offset().left,this.coords.x_pointer=+(e-this.coords.x_gap).toFixed(),this.force_redraw=!0,this.calc(),this.$cache.line.trigger("focus"))},key:function(o,t){if(!(this.current_plugin!==this.plugin_count||t.altKey||t.ctrlKey||t.shiftKey||t.metaKey)){switch(t.which){case 83:case 65:case 40:case 37:t.preventDefault(),this.moveByKey(!1);break;case 87:case 68:case 38:case 39:t.preventDefault(),this.moveByKey(!0);}return!0}},moveByKey:function(o){var e=this.coords.p_pointer,t=(this.options.max-this.options.min)/100;t=this.options.step/t,o?e+=t:e-=t,this.coords.x_pointer=this.toFixed(this.coords.w_rs/100*e),this.is_key=!0,this.calc()},setMinMax:function(){if(this.options){if(this.options.hide_min_max)return this.$cache.min[0].style.display="none",void(this.$cache.max[0].style.display="none");if(this.options.values.length)this.$cache.min.html(this.decorate(this.options.p_values[this.options.min])),this.$cache.max.html(this.decorate(this.options.p_values[this.options.max]));else{var o=this._prettify(this.options.min),e=this._prettify(this.options.max);this.result.min_pretty=o,this.result.max_pretty=e,this.$cache.min.html(this.decorate(o,this.options.min)),this.$cache.max.html(this.decorate(e,this.options.max))}this.labels.w_min=this.$cache.min.outerWidth(!1),this.labels.w_max=this.$cache.max.outerWidth(!1)}},setTempMinInterval:function(){var o=this.result.to-this.result.from;null===this.old_min_interval&&(this.old_min_interval=this.options.min_interval),this.options.min_interval=o},restoreOriginalMinInterval:function(){null!==this.old_min_interval&&(this.options.min_interval=this.old_min_interval,this.old_min_interval=null)},calc:function(o){if(this.options&&(this.calc_count++,(10===this.calc_count||o)&&(this.calc_count=0,this.coords.w_rs=this.$cache.rs.outerWidth(!1),this.calcHandlePercent()),!!this.coords.w_rs)){this.calcPointerPercent();var e=this.getHandleX();switch("both"===this.target&&(this.coords.p_gap=0,e=this.getHandleX()),"click"===this.target&&(this.coords.p_gap=this.coords.p_handle/2,e=this.getHandleX(),this.target=this.options.drag_interval?"both_one":this.chooseHandle(e)),this.target){case"base":var r=(this.options.max-this.options.min)/100,i=(this.result.from-this.options.min)/r,s=(this.result.to-this.options.min)/r;this.coords.p_single_real=this.toFixed(i),this.coords.p_from_real=this.toFixed(i),this.coords.p_to_real=this.toFixed(s),this.coords.p_single_real=this.checkDiapason(this.coords.p_single_real,this.options.from_min,this.options.from_max),this.coords.p_from_real=this.checkDiapason(this.coords.p_from_real,this.options.from_min,this.options.from_max),this.coords.p_to_real=this.checkDiapason(this.coords.p_to_real,this.options.to_min,this.options.to_max),this.coords.p_single_fake=this.convertToFakePercent(this.coords.p_single_real),this.coords.p_from_fake=this.convertToFakePercent(this.coords.p_from_real),this.coords.p_to_fake=this.convertToFakePercent(this.coords.p_to_real),this.target=null;break;case"single":if(this.options.from_fixed)break;this.coords.p_single_real=this.convertToRealPercent(e),this.coords.p_single_real=this.calcWithStep(this.coords.p_single_real),this.coords.p_single_real=this.checkDiapason(this.coords.p_single_real,this.options.from_min,this.options.from_max),this.coords.p_single_fake=this.convertToFakePercent(this.coords.p_single_real);break;case"from":if(this.options.from_fixed)break;this.coords.p_from_real=this.convertToRealPercent(e),this.coords.p_from_real=this.calcWithStep(this.coords.p_from_real),this.coords.p_from_real>this.coords.p_to_real&&(this.coords.p_from_real=this.coords.p_to_real),this.coords.p_from_real=this.checkDiapason(this.coords.p_from_real,this.options.from_min,this.options.from_max),this.coords.p_from_real=this.checkMinInterval(this.coords.p_from_real,this.coords.p_to_real,"from"),this.coords.p_from_real=this.checkMaxInterval(this.coords.p_from_real,this.coords.p_to_real,"from"),this.coords.p_from_fake=this.convertToFakePercent(this.coords.p_from_real);break;case"to":if(this.options.to_fixed)break;this.coords.p_to_real=this.convertToRealPercent(e),this.coords.p_to_real=this.calcWithStep(this.coords.p_to_real),this.coords.p_to_real<this.coords.p_from_real&&(this.coords.p_to_real=this.coords.p_from_real),this.coords.p_to_real=this.checkDiapason(this.coords.p_to_real,this.options.to_min,this.options.to_max),this.coords.p_to_real=this.checkMinInterval(this.coords.p_to_real,this.coords.p_from_real,"to"),this.coords.p_to_real=this.checkMaxInterval(this.coords.p_to_real,this.coords.p_from_real,"to"),this.coords.p_to_fake=this.convertToFakePercent(this.coords.p_to_real);break;case"both":if(this.options.from_fixed||this.options.to_fixed)break;e=this.toFixed(e+.001*this.coords.p_handle),this.coords.p_from_real=this.convertToRealPercent(e)-this.coords.p_gap_left,this.coords.p_from_real=this.calcWithStep(this.coords.p_from_real),this.coords.p_from_real=this.checkDiapason(this.coords.p_from_real,this.options.from_min,this.options.from_max),this.coords.p_from_real=this.checkMinInterval(this.coords.p_from_real,this.coords.p_to_real,"from"),this.coords.p_from_fake=this.convertToFakePercent(this.coords.p_from_real),this.coords.p_to_real=this.convertToRealPercent(e)+this.coords.p_gap_right,this.coords.p_to_real=this.calcWithStep(this.coords.p_to_real),this.coords.p_to_real=this.checkDiapason(this.coords.p_to_real,this.options.to_min,this.options.to_max),this.coords.p_to_real=this.checkMinInterval(this.coords.p_to_real,this.coords.p_from_real,"to"),this.coords.p_to_fake=this.convertToFakePercent(this.coords.p_to_real);break;case"both_one":if(this.options.from_fixed||this.options.to_fixed)break;var t=this.convertToRealPercent(e),a=this.result.from_percent,n=this.result.to_percent,c=n-a,l=c/2,_=t-l,d=t+l;0>_&&(_=0,d=_+c),100<d&&(d=100,_=d-c),this.coords.p_from_real=this.calcWithStep(_),this.coords.p_from_real=this.checkDiapason(this.coords.p_from_real,this.options.from_min,this.options.from_max),this.coords.p_from_fake=this.convertToFakePercent(this.coords.p_from_real),this.coords.p_to_real=this.calcWithStep(d),this.coords.p_to_real=this.checkDiapason(this.coords.p_to_real,this.options.to_min,this.options.to_max),this.coords.p_to_fake=this.convertToFakePercent(this.coords.p_to_real);}"single"===this.options.type?(this.coords.p_bar_x=this.coords.p_handle/2,this.coords.p_bar_w=this.coords.p_single_fake,this.result.from_percent=this.coords.p_single_real,this.result.from=this.convertToValue(this.coords.p_single_real),this.result.from_pretty=this._prettify(this.result.from),this.options.values.length&&(this.result.from_value=this.options.values[this.result.from])):(this.coords.p_bar_x=this.toFixed(this.coords.p_from_fake+this.coords.p_handle/2),this.coords.p_bar_w=this.toFixed(this.coords.p_to_fake-this.coords.p_from_fake),this.result.from_percent=this.coords.p_from_real,this.result.from=this.convertToValue(this.coords.p_from_real),this.result.from_pretty=this._prettify(this.result.from),this.result.to_percent=this.coords.p_to_real,this.result.to=this.convertToValue(this.coords.p_to_real),this.result.to_pretty=this._prettify(this.result.to),this.options.values.length&&(this.result.from_value=this.options.values[this.result.from],this.result.to_value=this.options.values[this.result.to])),this.calcMinMax(),this.calcLabels()}},calcPointerPercent:function(){return this.coords.w_rs?void(0>this.coords.x_pointer||isNaN(this.coords.x_pointer)?this.coords.x_pointer=0:this.coords.x_pointer>this.coords.w_rs&&(this.coords.x_pointer=this.coords.w_rs),this.coords.p_pointer=this.toFixed(100*(this.coords.x_pointer/this.coords.w_rs))):void(this.coords.p_pointer=0)},convertToRealPercent:function(o){var e=100-this.coords.p_handle;return 100*(o/e)},convertToFakePercent:function(o){var e=100-this.coords.p_handle;return o/100*e},getHandleX:function(){var o=100-this.coords.p_handle,e=this.toFixed(this.coords.p_pointer-this.coords.p_gap);return 0>e?e=0:e>o&&(e=o),e},calcHandlePercent:function(){this.coords.w_handle="single"===this.options.type?this.$cache.s_single.outerWidth(!1):this.$cache.s_from.outerWidth(!1),this.coords.p_handle=this.toFixed(100*(this.coords.w_handle/this.coords.w_rs))},chooseHandle:function(o){if("single"===this.options.type)return"single";var e=this.coords.p_from_real+(this.coords.p_to_real-this.coords.p_from_real)/2;return o>=e?this.options.to_fixed?"from":"to":this.options.from_fixed?"to":"from"},calcMinMax:function(){this.coords.w_rs&&(this.labels.p_min=100*(this.labels.w_min/this.coords.w_rs),this.labels.p_max=100*(this.labels.w_max/this.coords.w_rs))},calcLabels:function(){!this.coords.w_rs||this.options.hide_from_to||("single"===this.options.type?(this.labels.w_single=this.$cache.single.outerWidth(!1),this.labels.p_single_fake=100*(this.labels.w_single/this.coords.w_rs),this.labels.p_single_left=this.coords.p_single_fake+this.coords.p_handle/2-this.labels.p_single_fake/2,this.labels.p_single_left=this.checkEdges(this.labels.p_single_left,this.labels.p_single_fake)):(this.labels.w_from=this.$cache.from.outerWidth(!1),this.labels.p_from_fake=100*(this.labels.w_from/this.coords.w_rs),this.labels.p_from_left=this.coords.p_from_fake+this.coords.p_handle/2-this.labels.p_from_fake/2,this.labels.p_from_left=this.toFixed(this.labels.p_from_left),this.labels.p_from_left=this.checkEdges(this.labels.p_from_left,this.labels.p_from_fake),this.labels.w_to=this.$cache.to.outerWidth(!1),this.labels.p_to_fake=100*(this.labels.w_to/this.coords.w_rs),this.labels.p_to_left=this.coords.p_to_fake+this.coords.p_handle/2-this.labels.p_to_fake/2,this.labels.p_to_left=this.toFixed(this.labels.p_to_left),this.labels.p_to_left=this.checkEdges(this.labels.p_to_left,this.labels.p_to_fake),this.labels.w_single=this.$cache.single.outerWidth(!1),this.labels.p_single_fake=100*(this.labels.w_single/this.coords.w_rs),this.labels.p_single_left=(this.labels.p_from_left+this.labels.p_to_left+this.labels.p_to_fake)/2-this.labels.p_single_fake/2,this.labels.p_single_left=this.toFixed(this.labels.p_single_left),this.labels.p_single_left=this.checkEdges(this.labels.p_single_left,this.labels.p_single_fake)))},updateScene:function(){this.raf_id&&(cancelAnimationFrame(this.raf_id),this.raf_id=null),clearTimeout(this.update_tm),this.update_tm=null;this.options&&(this.drawHandles(),this.is_active?this.raf_id=requestAnimationFrame(this.updateScene.bind(this)):this.update_tm=setTimeout(this.updateScene.bind(this),300))},drawHandles:function(){(this.coords.w_rs=this.$cache.rs.outerWidth(!1),!!this.coords.w_rs)&&(this.coords.w_rs!==this.coords.w_rs_old&&(this.target="base",this.is_resize=!0),(this.coords.w_rs!==this.coords.w_rs_old||this.force_redraw)&&(this.setMinMax(),this.calc(!0),this.drawLabels(),this.options.grid&&(this.calcGridMargin(),this.calcGridLabels()),this.force_redraw=!0,this.coords.w_rs_old=this.coords.w_rs,this.drawShadow()),this.coords.w_rs&&(this.dragging||this.force_redraw||this.is_key)&&((this.old_from!==this.result.from||this.old_to!==this.result.to||this.force_redraw||this.is_key)&&(this.drawLabels(),this.$cache.bar[0].style.left=this.coords.p_bar_x+"%",this.$cache.bar[0].style.width=this.coords.p_bar_w+"%","single"===this.options.type?(this.$cache.s_single[0].style.left=this.coords.p_single_fake+"%",this.$cache.single[0].style.left=this.labels.p_single_left+"%"):(this.$cache.s_from[0].style.left=this.coords.p_from_fake+"%",this.$cache.s_to[0].style.left=this.coords.p_to_fake+"%",(this.old_from!==this.result.from||this.force_redraw)&&(this.$cache.from[0].style.left=this.labels.p_from_left+"%"),(this.old_to!==this.result.to||this.force_redraw)&&(this.$cache.to[0].style.left=this.labels.p_to_left+"%"),this.$cache.single[0].style.left=this.labels.p_single_left+"%"),this.writeToInput(),(this.old_from!==this.result.from||this.old_to!==this.result.to)&&!this.is_start&&(this.$cache.input.trigger("change"),this.$cache.input.trigger("input")),this.old_from=this.result.from,this.old_to=this.result.to,!this.is_resize&&!this.is_update&&!this.is_start&&!this.is_finish&&this.callOnChange(),(this.is_key||this.is_click)&&(this.is_key=!1,this.is_click=!1,this.callOnFinish()),this.is_update=!1,this.is_resize=!1,this.is_finish=!1),this.is_start=!1,this.is_key=!1,this.is_click=!1,this.force_redraw=!1))},drawLabels:function(){if(this.options){var o,e,t,r,i,s=this.options.values.length,a=this.options.p_values;if(!this.options.hide_from_to)if("single"===this.options.type)s?(o=this.decorate(a[this.result.from]),this.$cache.single.html(o)):(r=this._prettify(this.result.from),o=this.decorate(r,this.result.from),this.$cache.single.html(o)),this.calcLabels(),this.$cache.min[0].style.visibility=this.labels.p_single_left<this.labels.p_min+1?"hidden":"visible",this.$cache.max[0].style.visibility=this.labels.p_single_left+this.labels.p_single_fake>100-this.labels.p_max-1?"hidden":"visible";else{s?(this.options.decorate_both?(o=this.decorate(a[this.result.from]),o+=this.options.values_separator,o+=this.decorate(a[this.result.to])):o=this.decorate(a[this.result.from]+this.options.values_separator+a[this.result.to]),e=this.decorate(a[this.result.from]),t=this.decorate(a[this.result.to]),this.$cache.single.html(o),this.$cache.from.html(e),this.$cache.to.html(t)):(r=this._prettify(this.result.from),i=this._prettify(this.result.to),this.options.decorate_both?(o=this.decorate(r,this.result.from),o+=this.options.values_separator,o+=this.decorate(i,this.result.to)):o=this.decorate(r+this.options.values_separator+i,this.result.to),e=this.decorate(r,this.result.from),t=this.decorate(i,this.result.to),this.$cache.single.html(o),this.$cache.from.html(e),this.$cache.to.html(t)),this.calcLabels();var n=Math.min(this.labels.p_single_left,this.labels.p_from_left),c=this.labels.p_single_left+this.labels.p_single_fake,l=this.labels.p_to_left+this.labels.p_to_fake,_=Math.max(c,l);this.labels.p_from_left+this.labels.p_from_fake>=this.labels.p_to_left?(this.$cache.from[0].style.visibility="hidden",this.$cache.to[0].style.visibility="hidden",this.$cache.single[0].style.visibility="visible",this.result.from===this.result.to?("from"===this.target?this.$cache.from[0].style.visibility="visible":"to"===this.target?this.$cache.to[0].style.visibility="visible":!this.target&&(this.$cache.from[0].style.visibility="visible"),this.$cache.single[0].style.visibility="hidden",_=l):(this.$cache.from[0].style.visibility="hidden",this.$cache.to[0].style.visibility="hidden",this.$cache.single[0].style.visibility="visible",_=Math.max(c,l))):(this.$cache.from[0].style.visibility="visible",this.$cache.to[0].style.visibility="visible",this.$cache.single[0].style.visibility="hidden"),this.$cache.min[0].style.visibility=n<this.labels.p_min+1?"hidden":"visible",this.$cache.max[0].style.visibility=_>100-this.labels.p_max-1?"hidden":"visible"}}},drawShadow:function(){var e,t,r,i,s=this.options,o=this.$cache,a="number"==typeof s.from_min&&!isNaN(s.from_min),n="number"==typeof s.from_max&&!isNaN(s.from_max),c="number"==typeof s.to_min&&!isNaN(s.to_min),l="number"==typeof s.to_max&&!isNaN(s.to_max);"single"===s.type?s.from_shadow&&(a||n)?(e=this.convertToPercent(a?s.from_min:s.min),t=this.convertToPercent(n?s.from_max:s.max)-e,e=this.toFixed(e-this.coords.p_handle/100*e),t=this.toFixed(t-this.coords.p_handle/100*t),e+=this.coords.p_handle/2,o.shad_single[0].style.display="block",o.shad_single[0].style.left=e+"%",o.shad_single[0].style.width=t+"%"):o.shad_single[0].style.display="none":(s.from_shadow&&(a||n)?(e=this.convertToPercent(a?s.from_min:s.min),t=this.convertToPercent(n?s.from_max:s.max)-e,e=this.toFixed(e-this.coords.p_handle/100*e),t=this.toFixed(t-this.coords.p_handle/100*t),e+=this.coords.p_handle/2,o.shad_from[0].style.display="block",o.shad_from[0].style.left=e+"%",o.shad_from[0].style.width=t+"%"):o.shad_from[0].style.display="none",s.to_shadow&&(c||l)?(r=this.convertToPercent(c?s.to_min:s.min),i=this.convertToPercent(l?s.to_max:s.max)-r,r=this.toFixed(r-this.coords.p_handle/100*r),i=this.toFixed(i-this.coords.p_handle/100*i),r+=this.coords.p_handle/2,o.shad_to[0].style.display="block",o.shad_to[0].style.left=r+"%",o.shad_to[0].style.width=i+"%"):o.shad_to[0].style.display="none")},writeToInput:function(){"single"===this.options.type?(this.options.values.length?this.$cache.input.prop("value",this.result.from_value):this.$cache.input.prop("value",this.result.from),this.$cache.input.data("from",this.result.from)):(this.options.values.length?this.$cache.input.prop("value",this.result.from_value+this.options.input_values_separator+this.result.to_value):this.$cache.input.prop("value",this.result.from+this.options.input_values_separator+this.result.to),this.$cache.input.data("from",this.result.from),this.$cache.input.data("to",this.result.to))},callOnStart:function(){this.writeToInput(),this.options.onStart&&"function"==typeof this.options.onStart&&(this.options.scope?this.options.onStart.call(this.options.scope,this.result):this.options.onStart(this.result))},callOnChange:function(){this.writeToInput(),this.options.onChange&&"function"==typeof this.options.onChange&&(this.options.scope?this.options.onChange.call(this.options.scope,this.result):this.options.onChange(this.result))},callOnFinish:function(){this.writeToInput(),this.options.onFinish&&"function"==typeof this.options.onFinish&&(this.options.scope?this.options.onFinish.call(this.options.scope,this.result):this.options.onFinish(this.result))},callOnUpdate:function(){this.writeToInput(),this.options.onUpdate&&"function"==typeof this.options.onUpdate&&(this.options.scope?this.options.onUpdate.call(this.options.scope,this.result):this.options.onUpdate(this.result))},toggleInput:function(){this.$cache.input.toggleClass("irs-hidden-input"),this.has_tab_index?this.$cache.input.prop("tabindex",-1):this.$cache.input.removeProp("tabindex"),this.has_tab_index=!this.has_tab_index},convertToPercent:function(o,e){var t,r,i=this.options.max-this.options.min;return i?(t=e?o:o-this.options.min,r=t/(i/100),this.toFixed(r)):(this.no_diapason=!0,0)},convertToValue:function(o){var e,t,r=this.options.min,i=this.options.max,s=r.toString().split(".")[1],a=i.toString().split(".")[1],n=0,c=0;if(0===o)return this.options.min;if(100===o)return this.options.max;s&&(e=s.length,n=e),a&&(t=a.length,n=t),e&&t&&(n=e>=t?e:t),0>r&&(c=Math.abs(r),r=+(r+c).toFixed(n),i=+(i+c).toFixed(n));var l,_=(i-r)/100*o+r,d=this.options.step.toString().split(".")[1];return d?_=+_.toFixed(d.length):(_/=this.options.step,_*=this.options.step,_=+_.toFixed(0)),c&&(_-=c),l=d?+_.toFixed(d.length):this.toFixed(_),l<this.options.min?l=this.options.min:l>this.options.max&&(l=this.options.max),l},calcWithStep:function(o){var e=Math.round(o/this.coords.p_step)*this.coords.p_step;return 100<e&&(e=100),100===o&&(e=100),this.toFixed(e)},checkMinInterval:function(e,t,r){var i,s,a=this.options;return a.min_interval?(i=this.convertToValue(e),s=this.convertToValue(t),"from"===r?s-i<a.min_interval&&(i=s-a.min_interval):i-s<a.min_interval&&(i=s+a.min_interval),this.convertToPercent(i)):e},checkMaxInterval:function(e,t,r){var i,s,a=this.options;return a.max_interval?(i=this.convertToValue(e),s=this.convertToValue(t),"from"===r?s-i>a.max_interval&&(i=s-a.max_interval):i-s>a.max_interval&&(i=s+a.max_interval),this.convertToPercent(i)):e},checkDiapason:function(e,t,r){var i=this.convertToValue(e),s=this.options;return"number"!=typeof t&&(t=s.min),"number"!=typeof r&&(r=s.max),i<t&&(i=t),i>r&&(i=r),this.convertToPercent(i)},toFixed:function(o){return o=o.toFixed(20),+o},_prettify:function(o){return this.options.prettify_enabled?this.options.prettify&&"function"==typeof this.options.prettify?this.options.prettify(o):this.prettify(o):o},prettify:function(o){var e=o.toString();return e.replace(/(\d{1,3}(?=(?:\d\d\d)+(?!\d)))/g,"$1"+this.options.prettify_separator)},checkEdges:function(o,e){return this.options.force_edges?(0>o?o=0:o>100-e&&(o=100-e),this.toFixed(o)):this.toFixed(o)},validate:function(){var e,t,s=this.options,o=this.result,r=s.values,a=r.length;if("string"==typeof s.min&&(s.min=+s.min),"string"==typeof s.max&&(s.max=+s.max),"string"==typeof s.from&&(s.from=+s.from),"string"==typeof s.to&&(s.to=+s.to),"string"==typeof s.step&&(s.step=+s.step),"string"==typeof s.from_min&&(s.from_min=+s.from_min),"string"==typeof s.from_max&&(s.from_max=+s.from_max),"string"==typeof s.to_min&&(s.to_min=+s.to_min),"string"==typeof s.to_max&&(s.to_max=+s.to_max),"string"==typeof s.grid_num&&(s.grid_num=+s.grid_num),s.max<s.min&&(s.max=s.min),a)for(s.p_values=[],s.min=0,s.max=a-1,s.step=1,s.grid_num=s.max,s.grid_snap=!0,t=0;t<a;t++)e=+r[t],isNaN(e)?e=r[t]:(r[t]=e,e=this._prettify(e)),s.p_values.push(e);("number"!=typeof s.from||isNaN(s.from))&&(s.from=s.min),("number"!=typeof s.to||isNaN(s.to))&&(s.to=s.max),"single"===s.type?(s.from<s.min&&(s.from=s.min),s.from>s.max&&(s.from=s.max)):(s.from<s.min&&(s.from=s.min),s.from>s.max&&(s.from=s.max),s.to<s.min&&(s.to=s.min),s.to>s.max&&(s.to=s.max),this.update_check.from&&(this.update_check.from!==s.from&&s.from>s.to&&(s.from=s.to),this.update_check.to!==s.to&&s.to<s.from&&(s.to=s.from)),s.from>s.to&&(s.from=s.to),s.to<s.from&&(s.to=s.from)),("number"!=typeof s.step||isNaN(s.step)||!s.step||0>s.step)&&(s.step=1),"number"==typeof s.from_min&&s.from<s.from_min&&(s.from=s.from_min),"number"==typeof s.from_max&&s.from>s.from_max&&(s.from=s.from_max),"number"==typeof s.to_min&&s.to<s.to_min&&(s.to=s.to_min),"number"==typeof s.to_max&&s.from>s.to_max&&(s.to=s.to_max),o&&(o.min!==s.min&&(o.min=s.min),o.max!==s.max&&(o.max=s.max),(o.from<o.min||o.from>o.max)&&(o.from=s.from),(o.to<o.min||o.to>o.max)&&(o.to=s.to)),("number"!=typeof s.min_interval||isNaN(s.min_interval)||!s.min_interval||0>s.min_interval)&&(s.min_interval=0),("number"!=typeof s.max_interval||isNaN(s.max_interval)||!s.max_interval||0>s.max_interval)&&(s.max_interval=0),s.min_interval&&s.min_interval>s.max-s.min&&(s.min_interval=s.max-s.min),s.max_interval&&s.max_interval>s.max-s.min&&(s.max_interval=s.max-s.min)},decorate:function(e,t){var r="",i=this.options;return i.prefix&&(r+=i.prefix),r+=e,i.max_postfix&&(i.values.length&&e===i.p_values[i.max]?(r+=i.max_postfix,i.postfix&&(r+=" ")):t===i.max&&(r+=i.max_postfix,i.postfix&&(r+=" "))),i.postfix&&(r+=i.postfix),r},updateFrom:function(){this.result.from=this.options.from,this.result.from_percent=this.convertToPercent(this.result.from),this.result.from_pretty=this._prettify(this.result.from),this.options.values&&(this.result.from_value=this.options.values[this.result.from])},updateTo:function(){this.result.to=this.options.to,this.result.to_percent=this.convertToPercent(this.result.to),this.result.to_pretty=this._prettify(this.result.to),this.options.values&&(this.result.to_value=this.options.values[this.result.to])},updateResult:function(){this.result.min=this.options.min,this.result.max=this.options.max,this.updateFrom(),this.updateTo()},appendGrid:function(){if(this.options.grid){var e,t,r,s,a,n=this.options,o=n.max-n.min,c=n.grid_num,l=0,_=0,d=4,p=0,m="";for(this.calcGridMargin(),n.grid_snap?50<o?(c=50/n.step,l=this.toFixed(n.step/.5)):(c=o/n.step,l=this.toFixed(n.step/(o/100))):l=this.toFixed(100/c),4<c&&(d=3),7<c&&(d=2),14<c&&(d=1),28<c&&(d=0),e=0;e<c+1;e++){for(r=d,_=this.toFixed(l*e),100<_&&(_=100),this.coords.big[e]=_,s=(_-l*(e-1))/(r+1),t=1;t<=r&&0!==_;t++)p=this.toFixed(_-s*t),m+="<span class=\"irs-grid-pol small\" style=\"left: "+p+"%\"></span>";m+="<span class=\"irs-grid-pol\" style=\"left: "+_+"%\"></span>",a=this.convertToValue(_),a=n.values.length?n.p_values[a]:this._prettify(a),m+="<span class=\"irs-grid-text js-grid-text-"+e+"\" style=\"left: "+_+"%\">"+a+"</span>"}this.coords.big_num=Math.ceil(c+1),this.$cache.cont.addClass("irs-with-grid"),this.$cache.grid.html(m),this.cacheGridLabels()}},cacheGridLabels:function(){var o,e,t=this.coords.big_num;for(e=0;e<t;e++)o=this.$cache.grid.find(".js-grid-text-"+e),this.$cache.grid_labels.push(o);this.calcGridLabels()},calcGridLabels:function(){var o,e,t=[],r=[],s=this.coords.big_num;for(o=0;o<s;o++)this.coords.big_w[o]=this.$cache.grid_labels[o].outerWidth(!1),this.coords.big_p[o]=this.toFixed(100*(this.coords.big_w[o]/this.coords.w_rs)),this.coords.big_x[o]=this.toFixed(this.coords.big_p[o]/2),t[o]=this.toFixed(this.coords.big[o]-this.coords.big_x[o]),r[o]=this.toFixed(t[o]+this.coords.big_p[o]);for(this.options.force_edges&&(t[0]<-this.coords.grid_gap&&(t[0]=-this.coords.grid_gap,r[0]=this.toFixed(t[0]+this.coords.big_p[0]),this.coords.big_x[0]=this.coords.grid_gap),r[s-1]>100+this.coords.grid_gap&&(r[s-1]=100+this.coords.grid_gap,t[s-1]=this.toFixed(r[s-1]-this.coords.big_p[s-1]),this.coords.big_x[s-1]=this.toFixed(this.coords.big_p[s-1]-this.coords.grid_gap))),this.calcGridCollision(2,t,r),this.calcGridCollision(4,t,r),o=0;o<s;o++)e=this.$cache.grid_labels[o][0],this.coords.big_x[o]!==Number.POSITIVE_INFINITY&&(e.style.marginLeft=-this.coords.big_x[o]+"%")},calcGridCollision:function(o,e,t){var r,s,a,n=this.coords.big_num;for(r=0;r<n&&(s=r+o/2,!(s>=n));r+=o)a=this.$cache.grid_labels[s][0],a.style.visibility=t[r]<=e[s]?"visible":"hidden"},calcGridMargin:function(){this.options.grid_margin&&(this.coords.w_rs=this.$cache.rs.outerWidth(!1),this.coords.w_rs&&(this.coords.w_handle="single"===this.options.type?this.$cache.s_single.outerWidth(!1):this.$cache.s_from.outerWidth(!1),this.coords.p_handle=this.toFixed(100*(this.coords.w_handle/this.coords.w_rs)),this.coords.grid_gap=this.toFixed(this.coords.p_handle/2-.1),this.$cache.grid[0].style.width=this.toFixed(100-this.coords.p_handle)+"%",this.$cache.grid[0].style.left=this.coords.grid_gap+"%"))},update:function(e){this.input&&(this.is_update=!0,this.options.from=this.result.from,this.options.to=this.result.to,this.update_check.from=this.result.from,this.update_check.to=this.result.to,this.options=o.extend(this.options,e),this.validate(),this.updateResult(e),this.toggleInput(),this.remove(),this.init(!0))},reset:function(){this.input&&(this.updateResult(),this.update())},destroy:function(){this.input&&(this.toggleInput(),this.$cache.input.prop("readonly",!1),o.data(this.input,"ionRangeSlider",null),this.remove(),this.input=null,this.options=null)}},o.fn.ionRangeSlider=function(e){return this.each(function(){o.data(this,"ionRangeSlider")||o.data(this,"ionRangeSlider",new n(this,e,s++))})},function(){for(var o=0,e=["ms","moz","webkit","o"],r=0;r<e.length&&!t.requestAnimationFrame;++r)t.requestAnimationFrame=t[e[r]+"RequestAnimationFrame"],t.cancelAnimationFrame=t[e[r]+"CancelAnimationFrame"]||t[e[r]+"CancelRequestAnimationFrame"];t.requestAnimationFrame||(t.requestAnimationFrame=function(e){var r=new Date().getTime(),i=Math.max(0,16-(r-o)),s=t.setTimeout(function(){e(r+i)},i);return o=r+i,s}),t.cancelAnimationFrame||(t.cancelAnimationFrame=function(o){clearTimeout(o)})}()});

var map,markerData=[],markers=[],districts=[];function initialize(){window.initMap?window.initMap():setTimeout(initialize,200)}function callbackInitMap(){initialize()}districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""}),districts.push({code:"",text:""})
var log = console.log;
new Vue({
    el: '#topSearchForm',
    // delimiters: ["[[", "]]"],
    delimiters: ['${', '}$'],
    template: '#topSearchTemplate',
    data() {
        return {
            isLoading: false,
            isFocus: false,
            suggestions: [],
        }
    },
    props: {
        query: String
    },
    methods: {
        getAutoComplete: () => {
        },
        handleQueryChange: function (e) {
            const q = e.target.value;
            if (q.length == 0) {
                this.isLoading = false;
                this.suggestions = [];
            }
            if (q.length >= 2) {
                this.isLoading = true;
                this.getAutoComplete(q);
            }
        },
        handleFocus: function (e) {
            this.isFocus = !this.isFocus;
        },
        setupAutoComplete: function () {
            clearInterval(this.interval);
            const getHeaderText = (itemType) => {
                switch (itemType) {
                    case 'area':
                        return 'Khu vực';
                    case 'street':
                        return 'Đường';
                    case 'urban_area':
                        return 'Khu dân cư'
                    default:
                        return 'Khu vực'
                }
            }

            this.getAutoComplete = _.debounce(async (q) => {
                const resp = await axios.get(`/api/s-suggest/sell/${q}`)
                if (resp && resp.status && resp.status == 200) {
                    let suggestions = [];
                    let headers = {};
                    for (const item of resp.data) {
                        //hide smaller div
                        //console.log("bigger");
                        if (!(item.type in headers)) {
                            suggestions.push({
                                code: "",
                                text: getHeaderText(item.type),
                                subText: "",
                                link: "",
                                isHeader: true,
                            })
                            headers[item.type] = 1
                        }
                        if (item.sub_type !== 'state') {
                            suggestions.push({
                                code: item.id,
                                text: item.text,
                                subText: item.sub_text,
                                link: "/listings/search?trans=${item.type}&keys=${item.text}",
                                isHeader: false,
                            })
                        }

                    }
                    this.suggestions = suggestions;
                }
                setTimeout(() => {
                    this.isLoading = false;
                }, 200);
                return resp;
            }, 300);
        },
    },
    created() {
       this.interval = setInterval(() => {
           if (window._ && axios) {
               this.setupAutoComplete();
           }
       }, 100)
    }
})

const InfoWindowComponent = Vue.extend({
    template: '#infoWindowTemplate',
    delimiters: ["[[", "]]"],
    props: {
        listing: Object
    },
    methods: {
        getListingDetailURL: function (id) {
            return `/listings/${id}`
        },
    },
});

// new ContactPopUpComponent().$mount('#contactPopUp');
const defaultSliderPriceOptions = {
    type: "double",
    min: 0,
    max: 20,
    from: 0,
    to: 1000,
    step: 0.5,
    grid: true,
    values_separator: "-",
    postfix: "",
    max_postfix: "+",
}
const defaultAreaSliderOptions = {
    type: "double",
    min: 0,
    max: 500,
    from: 0,
    to: 10000,
    step: 0.5,
    grid: true,
    values_separator: "-",
    postfix: "",
    max_postfix: "+",
}

let counter = 0;
const PropertyListComponent = Vue.extend({
    template: '#propertyListTemplate',
    delimiters: ["[[", "]]"],
    props: {
        listings: Array,
        pagination: Object,
        isViewGrid: Boolean,
        Simple: Boolean,
        isLoading: Boolean,
        goTo: Function,
        showContactProject: Function,
    },
    methods: {
        getListingDetailURL: function (id) {
            return `/listings/${id}`
        },
        getDistrict: function (district_code) {
            try {infoWindowTemplate
                return districts.find(item => item.code == district_code).text;
            } catch (e) {
                return '';
            }
        }
    },
})

Vue.component('property-list', PropertyListComponent)

new Vue({
    el: "#search-content",
    delimiters: ['[[', ']]'],
    data() {
        return {
            showFilterType: '',
            showMobileFilter: false,
            houseTypes: houseTypes,
            houseTypeFilter: {},
            minPrice: 0,
            maxPrice: 20,
            minArea: 0,
            maxArea: 500,
            bedroomFilter: [],
            bathroomFilter: '',
            viewtypeFilter: '',
            directionFilters: [],
            isVerifiedFilter: undefined,
            isExclusiveFilter: undefined,
            statusFilters: [],
            isViewGrid: true,
            isFirstLoad: true,
            isLoading: false,
            sortOption: 'priority',
            showSortOptions: false,
            queryParams: new URLSearchParams(window.location.search),
            listings: [],
            pagination: {},
            scriptsReady: false,
            checkingInterval: null,
            showContactPopup: false,
        }
    },
    computed: {
        displayListingNumText: function () {
            return `${this.listings.length} trong số ${this.pagination.total} sản phẩm`;
        },
        filterPriceText: function () {
            if (this.minPrice === 0 && this.maxPrice === 20) {
                return "Khoảng giá";
            } else if (this.minPrice >= 20) {
                return "Trên 20 tỷ";
            } else {
                return `${this.minPrice} - ${this.maxPrice} tỷ`;
            }
        },
        filterAreaText: function () {
            if (this.minArea === 0 && this.maxArea === 500) {
                return "Diện tích";
            } else if (this.minArea >= 500) {
                return "Trên 500 m²";
            } else {
                return `${this.minArea}m² - ${this.maxArea}m²`;
            }
        },
        sortString: function () {
            switch (this.sortOption) {
                case 'price_descend':
                    return 'Giá giảm dần';
                case 'price_ascend':
                    return 'Giá tăng dần';
                case 'created':
                    return 'Mới nhất';
                default:
                    return 'Ưu tiên'
            }
        },
        houseTypeFilterMark: function () {
            return Object.values(this.houseTypeFilter).filter(item => item !== '').length;
        },
        otherFilterMark: function () {
            return this.countOtherFilter();
        },
        mobileFilterMark: function () {
            let curLength = 0;
            if (this.minPrice !== 0 || this.maxPrice !== 20)
                curLength += 1;

            if (this.minArea !== 0 || this.maxArea !== 500)
                curLength += 1;

            if (this.houseTypeFilterMark > 0)
                curLength += this.houseTypeFilterMark;

            if (this.bedroomFilter.length > 0)
                curLength += this.bedroomFilter.length;

            curLength += this.countOtherFilter();

            return curLength
        },
        viewResultsMark: function () {
            let curLength = 0;
            if (this.viewtypeFilter === 'grid' || this.viewtypeFilter === 'list')
                curLength += 1;
            return curLength;
        },
    },
    methods: {
        closeFilterPopup: function (e) {
            const target$ = $(e.target);
            if (!target$.closest(`#${e.data.type}`).length) {
                this.showFilterType = '';
            }
        },
        toggleFilterType: function (type) {
            $(document).off('click.searchFilter');

            if (this.showFilterType !== type) {
                this.showFilterType = type;
            } else {
                this.showFilterType = '';
            }

        },
        toggleMobileFilter: function () {
            if (this.showMobileFilter) {
                $('.main-header').css('z-index', '')
            } else {
                $('.main-header').css('z-index', 0)
            }
            this.showMobileFilter = !this.showMobileFilter;
        },
        resetMobileFilter: function () {

        },
        applyMobileFilter: async function () {
            const priceFrom = this.$mobilePriceSlider.result.from;
            const priceTo = this.$mobilePriceSlider.result.to;
            this.setPrices(priceFrom, priceTo);

            const {from, to} = this.$mobileAreaSlider.result;
            this.setArea(from, to);

            let houseTypeFilter = this.houseTypeFilter;
            $('#mobileFilter [name="houseTypeFilter"]:checked').map((index, item) => {
                if (item.value) {
                    houseTypeFilter[item.value] = (item.value);
                }
            });
            this.setHouseFilter(houseTypeFilter);

            this.setOtherFilters($('#mobileFilter'))

            await this.getListings();
            this.setMarkers();
            this.toggleMobileFilter();

        },
        resetHouseFilter: function () {
            let htFilter = {};
            this.houseTypes.map(ht => {
                htFilter[ht.type] = '';
            })
            this.houseTypeFilter = htFilter;
            $('#leads .check').prop('checked', false);
        },
        cancelHouseFilter: function () {
            this.toggleFilterType('houseFilter');
            $('#leads .check').prop('checked', false);
            Object.values(this.houseTypeFilter).map(item => {
                if (item)
                    $(`#leads .check[value=${item}]`).prop('checked', true);
            })
        },
        setHouseFilter: function (houseTypeFilter) {
            if (JSON.stringify(this.houseTypeFilter) === JSON.stringify(houseTypeFilter)) return;
            this.houseTypeFilter = houseTypeFilter;
            const houseFilterItems = Object.values(houseTypeFilter).filter(item => item !== '');
            if (houseFilterItems.length > 0) {
                const houseParam = houseFilterItems.join(',');
                this.updateQueryParams({'hoty': houseParam})
            } else {
                this.removeQueryParams('hoty')
            }
        },
        applyHouseFilter: async function () {
            let houseTypeFilter = this.houseTypeFilter;
            $('#houseFilter input[name="houseTypeFilter"]').map((index, item) => {
                if (item.checked) {
                    houseTypeFilter[item.value] = item.value;
                } else {
                    houseTypeFilter[item.value] = '';
                }
            });
            this.setHouseFilter(houseTypeFilter);
            this.toggleFilterType('houseFilter');
            await this.getListings();
            this.setMarkers();
        },
        toggleShowSortOptions: function () {
            this.showSortOptions = !this.showSortOptions;
        },
        setPrices: function (from, to) {
            if (from === undefined || to === undefined) return;
            if (this.minPrice === from && this.maxPrice === to) return;

            let newTo = to;
            let newFrom = from;

            if (newTo >= 20) newTo = 1000;

            if (newFrom >= 20) {
                newFrom = 20;
                newTo = 1000;
            }

            this.minPrice = from;
            this.maxPrice = to;
            this.$priceSlider.update({
                from : from,
                to: to,
            });
            this.$mobilePriceSlider.update({
                from : from,
                to: to,
            })
            this.updateQueryParams({minPrice: newFrom, maxPrice: newTo})
        },
        quickSetPrice: async function (from, to) {
            this.setPrices(from, to);
            this.toggleFilterType('priceFilter');
            await this.getListings();
            this.setMarkers();
        },
        resetPriceSlider: function () {
            this.$priceSlider.update(defaultSliderPriceOptions);
            this.$mobilePriceSlider.update(defaultSliderPriceOptions);
        },
        applySliderPrice: async function () {
            const {from, to} = this.$priceSlider.result;
            this.setPrices(from, to);
            this.toggleFilterType('priceFilter');
            await this.getListings();
            this.setMarkers();
        },
        setArea: function (from, to) {
            if (from === undefined || to === undefined) return;
            if (this.minArea === from && this.maxArea === to) return;
            let newTo = to;
            let newFrom = from;

            if (newTo >= 500) newTo = 20000;

            if (newFrom >= 500) {
                newTo = 20000;
            }

            this.minArea = from;
            this.maxArea = to;
            this.$areaSlider.update({
                from : from,
                to: to,
            });
            this.$mobileAreaSlider.update({
                from : from,
                to: to,
            })
            this.updateQueryParams({minArea: newFrom, maxArea: newTo})
        },
        quickSetArea: async function (from, to) {
            this.setArea(from, to);
            this.toggleFilterType('acreFilter');
            await this.getListings();
            this.setMarkers();
        },
        resetAreaSlider: function () {
            this.$areaSlider.update(defaultAreaSliderOptions);
            this.$mobileAreaSlider.update(defaultAreaSliderOptions);
        },
        applySliderArea: async function () {
            const {from, to} = this.$areaSlider.result;
            this.setArea(from, to);
            this.toggleFilterType('acreFilter');
            await this.getListings();
            this.setMarkers();
        },
        setOtherFilters: function (parentSelector) {
            let bedFilter = [];
            parentSelector.find('input[name="bedrooms"]:checked').map((index, item) => {
                bedFilter.push(item.value)
            });
            this.setBedroomFilter(bedFilter);

            const bathrooms = parentSelector.find('input[name="bathrooms"]:checked').first().val()
            this.setBathroomFilter(bathrooms);

            let directions = [];
            parentSelector.find('input[name="direction"]:checked').map((index, item) => {
                directions.push(item.value)
            });
            this.setDirectionFilter(directions);

            const isVerified = parentSelector.find('input[name="is_verified"]').first().prop('checked')
            this.setIsVerifiedFilter(isVerified);

            const isExclusive = parentSelector.find('input[name="is_exclusive"]').first().prop('checked');
            this.setIsExclusiveFilter(isExclusive)

            let statuses = []
            parentSelector.find('input[name="status"]:checked').map((index, item) => {
                statuses.push(item.value);
            });
            this.setStatusFilter(statuses);
        },
        applyOthersFilter: async function () {
            this.setOtherFilters($('#otherFilters'));
            this.toggleFilterType('otherFilters');
            await this.getListings();
            this.setMarkers();
        },
        setViewResultsFilters: function (parentSelector) {
            const asview = parentSelector.find('input[name="asView"]:checked').first().val()
            if (!asview) return;
            if (this.viewtypeFilter === asview) return;
            this.viewtypeFilter = asview;
            if (asview !== 'grid'){
                this.updateQueryParams({'asview': asview});
                this.viewAsList()
            }
            else{
                this.removeQueryParams('asview');
                this.viewAsGrid()}
        },
        applyViewResultsFilter: async function () {
            this.setViewResultsFilters($('#viewResults'));
            this.toggleFilterType('viewResults');
            /*await this.getListings();*/
        },
        setBedroomFilter: function (filters) {
            if (!filters) return;
            if (JSON.stringify(this.bedroomFilter) === JSON.stringify(filters)) return;
            this.bedroomFilter = filters;
            this.updateQueryParams({'bed': filters})
        },
        setBathroomFilter: function (filter) {
            if (!filter) return;
            if (this.bathroomFilter === filter) return;
            this.bathroomFilter = filter;
            if (filter !== 'all')
                this.updateQueryParams({'bath': filter})
            else
                this.removeQueryParams('bath')
        },
        setDirectionFilter: function (filters) {
            if (!filters) return;
            if (JSON.stringify(this.directionFilters) === JSON.stringify(filters)) return;

            this.directionFilters = filters;
            this.updateQueryParams({'directions': filters})
        },
        setIsVerifiedFilter: function (value) {
            if (this.isVerifiedFilter === value) return;
            this.isVerifiedFilter = value;
            if (value === true) {
                this.updateQueryParams({'veri': value});
            } else {
                this.removeQueryParams('veri')
            }
        },
        setIsExclusiveFilter: function (value) {
            if (this.isExclusiveFilter === value) return;
            this.isExclusiveFilter = value;
            if (value === true) {
                this.updateQueryParams({'ecl': value});

            } else {
                this.removeQueryParams('ecl')
            }
        },
        setStatusFilter: function (filters) {
            if (!filters) return;
            if (JSON.stringify(this.statusFilters) === JSON.stringify(filters)) return;
            this.statusFilters = filters;
            this.updateQueryParams({'status': filters})
        },
        sortBy: async function (sortOption) {
            if (this.sortOption == sortOption) return;
            this.sortOption = sortOption;
            this.showSortOptions = false;
            this.updateQueryParams({sort: sortOption});
            await this.getListings();

            const sort_price_ascend = (a, b) => a.price - b.price;
            const sort_price_descend = (a, b) => b.price - a.price;
            const sort_priority = (a, b) => a.priority - b.priority;
            const sort_created = (a, b) => a.list_date - b.list_date;

            switch (sortOption) {
                case 'price_ascend':
                    this.listings.sort(sort_price_ascend)
                    break;
                case 'price_descend':
                    this.listings.sort(sort_price_descend)
                    break;
                case 'created':
                    this.listings.sort(sort_created)
                    break;
                default:
                    this.listings.sort(sort_priority)
                    break;
            }

            this.setMarkers();
        },
        countOtherFilter: function () {
            let curLength = 0;
            if (this.bathroomFilter && this.bathroomFilter !== 'all')
                curLength += 1;

            if (this.bedroomFilter.length > 0)
                curLength += this.bedroomFilter.length;

            if (this.directionFilters.length > 0)
                curLength += this.directionFilters.length;

            if (this.isVerifiedFilter === true)
                curLength += 1;

            if (this.isExclusiveFilter === true)
                curLength += 1;

            if (this.statusFilters.length > 0)
                curLength += this.statusFilters.length;

            return curLength;
        },
        viewAsGrid: async function () {
            this.isViewGrid = true;
        },
        viewAsList: async function () {
            this.isViewGrid = false;
        },
        viewAsSimple: async function () {
            this.isViewGrid = false;
        },
        getQueryParams: function () {
            return this.queryParams;
        },
        updateQueryParams: function (params) {
            const urlParams = this.getQueryParams();
            Object.keys(params).map((key) => {
                if (urlParams.has(key)) {
                    urlParams.set(key, params[key])
                } else {
                    urlParams.append(key, params[key])
                }
            })
            this.queryParams = urlParams;
        },
        removeQueryParams: function (key) {
            if (this.queryParams.has(key))
                this.queryParams.delete(key)
        },
        getListings: async function () {
            this.isLoading = true;
            const urlParams = this.getQueryParams();
            try {
                const resp = await axios.get(`/api/search?${urlParams.toString()}`)
                if (resp && resp.status === 200) {
                    const {listings, pagination, sortOption} = resp.data;
                    this.listings = listings;
                    this.pagination = pagination;
                    this.sortOption = sortOption;
                }
            } catch (e) {
                this.listings = [];
                this.pagination = {};
            }

            this.isLoading = false;
        },
        goTo: async function (page) {
            this.updateQueryParams({page})
            await this.getListings();
            this.setMarkers();
        },
        applySearchParams: async function () {

        },
        showContactProject: function () {
            this.showContactPopup = true;
        },
        closeContactProject: function () {
            this.showContactPopup = false;
        },
        setMarkers: function () {
            if (!map) return;
            this.listings.map((item, index) => {
                const marker = new google.maps.Marker({
                    position: new google.maps.LatLng(item.lat, item.long),
                    title: item.title,
                    map: map,
                    icon: normalIcon(),
                })
                google.maps.event.addListener(marker, 'click', (e) => this.openInfoWindow(index))
                markers.push(marker);
            })
        },
        openInfoWindow: function (index) {
            if (!index || !this.listings.length || this.listings.length < index) return;
            const listing = this.listings[index];
            const instance = new InfoWindowComponent({
                propsData: {
                    listing
                }
            })
            instance.$mount();
            const infoWindow = new google.maps.InfoWindow({
                content: instance.$el
            })
            infoWindow.open(map, markers[index])

            setTimeout(() => {
                instance.$destroy();
            }, 500)
        },
        initMap: function () {
            if (!google) return;
            const mapOptions = {
                zoom: 12,
                center: new google.maps.LatLng(21.0334474, 105.8401439),  // Hanoi
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            map = new google.maps.Map(document.getElementById('search-map'), mapOptions);
        },
        clearMarkers: function () {
            for (let i = 0; i < markers.length; i++) {
                markers[i].setMap(null)
            }
            markers = [];
        },
        checkIntervalCallback: function () {
            if (axios) {
                this.scriptsReady = true;
            }
            counter++;
            if (counter >= 20) {
                clearInterval(this.checkingInterval);
            } else {
                clearInterval(this.checkingInterval);
                const timeout = 200 + counter * 40;
                this.checkingInterval = setInterval(this.checkIntervalCallback, timeout);
            }
        }
    },
    created() {
        this.checkingInterval = setInterval(this.checkIntervalCallback, 200);
        window.initMap = this.initMap;

        let htFilter = {};
        this.houseTypes.map(ht => {
            htFilter[ht.type] = '';
        })
        this.houseTypeFilter = htFilter;
    },
    mounted() {
        setTimeout(() => {
            $(this.$refs.priceInput).ionRangeSlider(defaultSliderPriceOptions);
            $(this.$refs.mobilePriceInput).ionRangeSlider(defaultSliderPriceOptions);
            this.$priceSlider = $(this.$refs.priceInput).data('ionRangeSlider');
            this.$mobilePriceSlider = $(this.$refs.mobilePriceInput).data('ionRangeSlider');

            $(this.$refs.areaInput).ionRangeSlider(defaultAreaSliderOptions);
            $(this.$refs.mobileAreaInput).ionRangeSlider(defaultAreaSliderOptions);
            this.$areaSlider = $(this.$refs.areaInput).data('ionRangeSlider');
            this.$mobileAreaSlider = $(this.$refs.mobileAreaInput).data('ionRangeSlider');
        }, 100);
    },
    watch: {
        scriptsReady: async function () {
            clearInterval(this.checkingInterval);
            await this.getListings();
            this.setMarkers();
        },
        showFilterType: async function () {
            if (this.showFilterType) {
                $(document).on('click.searchFilter', {type: this.showFilterType}, this.closeFilterPopup)
            }
        }
    },
    destroyed: function () {
        this.$priceSlider.destroy()
    }
})
