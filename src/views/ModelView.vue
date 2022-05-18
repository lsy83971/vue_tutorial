<template>
<div>
  <template v-for='(node, idx) in info' :key='idx'>
    <select
      @change='Onselect($event)'
      :id='node.name' class="form-select form-select-sm"
      :disabled = '!node.active'
      v-model='node.select'
      >
      <option v-for='(op, idx1) in node.ops' :key='idx1' :value="op">{{op}}</option>
    </select>
  </template>
</div>

<div>

  <table
    v-if="!!new_render.data"
    class="table table-striped">  
	<thead>
	  <tr>
	    <th
	      v-for='(c,idx) in new_render.cols'
	      :key='idx'
	      style='width:10%;text-align:left'>{{c}}</th>
	  </tr>
	</thead>
	<tbody>
	  <template v-for='(nodes, idx) in new_render.itm' :key="idx">
	    <tr>
	      <td v-for='(node, idx) in nodes' :key='idx'
		>{{node}}</td>
	    </tr>
	  </template>
	</tbody>
      </table>

  
</div>
</template>


<script>
  // TODO:table index
  // TODO:table odhis label
  // TODO:table score
  
  
import axios from 'axios';

var $d = document;  
var $g = function (id) { return $d.getElementById(id); };
var $ge = function (id) { return $d.getElementById('e_'+id)};
var $gc = function (id) { return $d.getElementsByClassName(id); };
var $ah = function (target) {
    var lines=target.value.split("\n");
    if (lines.length<=1){
	//target.style.height = 30+'px'
	target.style.height = 26+'px'
    }else{
	target.style.height = "auto";
	target.style.height = (target.scrollHeight+7) + "px";
    }
}
var $c = console.log;
var $cr = function (tag) { return $d.createElement(tag); };
var $w = global

  
var utils= {
    read: function (file_data,f) {
        var reader = new FileReader();
	var fd=function(res,name){
	    try{return f(res,name)}
	    catch(err){
		alert("READERR:"+err.message)
	    }
	}
	reader.onload = function() {
	    fd(this.result,file_data.name)
	};
        reader.readAsText(file_data);	
    },
    save: function (file_data, type, name) {
        var blob;
        if (typeof $w.Blob === 'function') {
            blob = new Blob([file_data], { type: type });
        } else {
            var BlobBuilder = $w.BlobBuilder || $w.MozBlobBuilder || $w.WebKitBlobBuilder || $w.MSBlobBuilder;
            var bb = new BlobBuilder();
            bb.append(file_data);
            blob = bb.getBlob(type);
        }
        if (navigator.msSaveBlob) {
            navigator.msSaveBlob(blob, name);
        } else {
            var URL = $w.URL || $w.webkitURL;
            var bloburl = URL.createObjectURL(blob);
            var anchor = $cr('a');
            if ('download' in anchor) {
                anchor.style.visibility = 'hidden';
                anchor.href = bloburl;
                anchor.download = name;
                $d.body.appendChild(anchor);
                var evt = $d.createEvent('MouseEvents');
                evt.initEvent('click', true, true);
                anchor.dispatchEvent(evt);
                $d.body.removeChild(anchor);
            } else {
                location.href = bloburl;
            }
        }
    },
    post: function(url,data,f){
	// f: .then(response => (show.info = response.data))
	// data: object
	axios
	    .post(url,data)
	    .then(f)
	    .catch(function (error){
		alert("AXIOSERR:"+error.message)
	    })
    }
}

  
export default {
    data () {
	return {
	    new_render:{
		data:null,
	    },
	    info:[
		{
		    name:"MODEL",
		    active:true,
		    ops:['None',"a"],
		    select:"None",
		},
		{
		    name:"TYPE1",
		    active:false,
		    ops:['None'],
		    select:"None",
		},
		{
		    name:"TYPE2",
		    active:false,
		    ops:['None'],
		    select:"None",
		},
		{
		    name:"CHANNEL",
		    active:false,
		    ops:['None'],
		    select:"None",
		},
		{
		    name:"IDX",
		    active:false,
		    ops:['None'],
		    select:"None",
		}
	    ]
	}
    },

    mounted() {
	mdl=this;
	this.ModelSelect("RAW");
    },
    
    methods:{
	ParseNewRender(){
	    var d=this.new_render.data
	    var its=Object.keys(d)
	    var h1=d[its[0]]
	    var h1c=Object.keys(h1)
	    var cols=["index"]
	    var itm=[]
	    cols=cols.concat(h1c)

	    for (let i in its){
		var s1=[i]
		s1=s1.concat(Object.values(d[i]))
		itm.push(s1)
	    }
	    this.new_render.cols=cols
	    this.new_render.itm=itm
	},
	Onselect(evt){
	    var target=evt.target;
	    var id=target.id
	    var index=["RAW","MODEL","TYPE1","TYPE2"].indexOf(id)
	    if (index>=0){
		this.ModelSelect(id)		
	    }
	},
	ModelSelect(p){
	    try{
		var s=new Object()
		s["o"]=this.info
		s["p"]=p;
		utils.post('model/select',s,(response => {
		    $c(response.data);
		    this.info=response.data
		}))
	    }catch(err){
		alert("sendTreeErr:"+err.message)
	    }
	},
	ModelRender(){
	    try{
		var s=new Object()
		s["o"]=this.info
		utils.post('model/render',s,(response => {
		    $c(response.data);
		    this.new_render.data=response.data
		    this.ParseNewRender()
		}))
	    }catch(err){

		alert("sendTreeErr:"+err.message)
	    }
	}
    }
}    
  
</script>

<style>
</style>
