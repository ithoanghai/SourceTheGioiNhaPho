new Vue({el:"#searchFormHome",delimiters:["${","}$"],template:"#searchFormTemplate",data:{isLoading:!1,isFocus:!1,suggestions:[]},props:{query:String},methods:{getAutoComplete:function(){},handleQueryChange:function(t){const e=t.target.value
0==e.length&&(this.isLoading=!1,this.suggestions=[]),e.length>=2&&(this.isLoading=!0,this.getAutoComplete(e))},handleFocus:function(t){this.isFocus=!this.isFocus},setupAutoComplete:function(){clearInterval(this.interval)
const t=function(t){switch(t){case"area":return"Khu vực"
case"street":return"Đường"
case"urban_area":return"Khu dân cư"
default:return"Khu vực"}}
this.getAutoComplete=_.debounce(function(e){const n=axios.get("/api/s-suggest/sell/${q}")
if(n&&n.status&&200==n.status){var r=[],i={}
for(var o in n.data)o.type in i||(r.push({code:o.id,text:t(o.type),subText:o.text,link:"",isHeader:!0}),i[o.type]=1),"state"!==o.sub_type&&r.push({code:o.id,text:o.text,subText:o.text,link:"/listings/search?trans=${item.type}&keys=${item.text}",isHeader:!1})
this.suggestions=r}return setTimeout(function(){this.isLoading=!1},200),n},300)}},created:{setInterval:100}})