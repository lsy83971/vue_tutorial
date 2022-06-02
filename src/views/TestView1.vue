<template>
  <button class="btn btn-primary" type="button" data-bs-toggle="offcanvas"
	  id='sidebar_open'
	  data-bs-target="#offcanvasScrolling"
	  >Select A Model Report!</button>
  <div class="offcanvas offcanvas-end"
       data-bs-scroll="true"
       data-bs-backdrop="false"
       tabindex="-1"
       id="offcanvasScrolling" >
    <div class="offcanvas-header">
      <h5 class="offcanvas-title" id="offcanvasScrollingLabel">Selector</h5>
      <button id='sidebar_close'
	      type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div style='margin:5px;padding:5px'>
      <template v-for='(node, idx) in info' :key='idx'>
	<div style='margin:2px;padding:2px'>
	  <div style='float:left;font-size: small;'>{{node.name}}:</div>
	  <select
	    @change='Onselect($event)'
	    :id='node.name' class="form-select form-select-sm"
	    :disabled = '!node.active'
	    v-model='node.select'
	    >
	    <option v-for='(op, idx1) in node.ops' :key='idx1' :value="op">{{op}}</option>
	  </select>
	</div>	
      </template>
      <div style='margin:2px;padding:2px'>
	<div>
	  <button class="btn btn-primary"
		  @click='ModelRender()'
		  style='margin-top:15px;padding:0px;width:100%;height:45px;font-size:large'
		  >render</button>
	</div>
      </div>
    </div>    
  </div>
<div style='padding:10px'
     id='tblResult'
     class='isshow'
     >
  <template v-for='(tbl, idx) in stacks' :key="idx">
    <div>
      <nav aria-label="breadcrumb"
	   style='padding:5px;padding-left:10px;height:auto;overflow:auto'>
	<ol class="breadcrumb" style='margin-bottom:0px'> 
	  <li v-for='(sl, idx1) in tbl.info' class="breadcrumb-item" :key='idx1'>{{sl.select}}</li>
	  <li class="breadcrumb-item"><a :pid='idx' @click='OnLoad($event)'>load</a></li>	  
	  <!-- li class="breadcrumb-item"><a :pid='idx' @click='OnReset($event)'>reset</a></li -->
	  <li class="breadcrumb-item"><a :pid='idx' @click='OnDelete($event)'>delete</a></li>
	</ol>
      </nav>
      <div style='overflow:auto;
		  margin:5px;
		  padding:10px;
		  border: solid;
		  border-width: 1px;
		  border-top-left-radius: .25rem;
		  border-top-right-radius: .25rem;'>
	<!-- table
	     class="table table-striped" :id='idx' -->

	<table
	  class="display nowrap" :id='idx'>
	
	  <thead>
	    <tr>
	      <th
		style="text-align:center;font-size: small;"
		v-for='(c,idx) in tbl.col'
		:key='idx'
		>{{c}}</th>
	    </tr>
	  </thead>
	</table>
      </div>
    </div>    
  </template>
</div>
</template>


<script>
  // TODO:table index
  // TODO:table odhis label
// TODO:table score


  // TODO:DELETE REVISE after crum
// TODO: input left  
  
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
	    stacks:{},
	    new_render:{
		data:null,
	    },
	    opts:{
		cNO:1
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
	$g('sidebar_close').addEventListener('click',function(){mdl.changeSideHidden()});
	$g('sidebar_open').addEventListener('click',function(){mdl.changeSideHidden()});
    },
    computed:{
	tblClass(){
	    $c("class:")
	    var res=new Object()
	    var sidebar= $g('offcanvasScrolling')
	    if (!sidebar){
		$c("no sidebar")
		res['isHidden']=false
	    }else{
		$c("have sidebar")		
		var isHidden=($g('offcanvasScrolling').style.visibility=='hidden')
		res['isHidden']=isHidden
	    }
	    $c(res);
	    return res
	},

    },
    methods:{
	changeSideHidden(){
		    var sidebar= $g('offcanvasScrolling')
		    if (!!sidebar){
			var isHidden=(!$('#offcanvasScrolling').hasClass('show'))
			$c(isHidden)
			if (isHidden){
			    $("#tblResult").removeClass("isHidden");
			    $("#tblResult").addClass("isshow");
			}else{
			    $("#tblResult").addClass("isHidden");
			    $("#tblResult").removeClass("isshow");
			}
		    }
	},
	NewNodeName(){
	    var name='c_'+this.opts.cNO;
	    this.opts.cNO++;
	    return name
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
	ModelRender(nodeid){
	    this.tmp_render_node=nodeid
	    try{
		var s=new Object()
		var info=structuredClone(this.info)
		s["o"]=info
		utils.post('model/render',s,(response => {
		    $c(response.data);
		    this.new_render.test=response.data
		    this.new_render.data=JSON.parse(response.data.data);
		    this.new_render.col=response.data.col
		    this.new_render.info=info
		    this.new_render.type=response.data.type

		    var data=this.new_render.data;
		    var nodeid=this.tmp_render_node
		    var type=this.new_render.type
		    $c("types:")
		    $c(type)
		    var col=this.new_render.col
		    var columns=[]
		    for (let j in col){
			var i=col[j]
			var tmpd={"data":i}
			let tmp_type=type[i]
			$c("tmp_types:")
			$c(i);
			$c(tmp_type)
			if (tmp_type["type"]=="process"){
			    if (!!tmp_type["process_color"]){
				tmp_type.color=tmp_type["process_color"]
			    }else{
				tmp_type.color="blue"
			    }
			    tmpd['render']=function(data, type){
				if (type==="display"){
				    return '<progress class="'+ tmp_type["color"] +'" value="' + data + '" max="'+tmp_type['process_max']+'"></progress> '+data
				}else{
				    return data
				}
			    }
			}
			columns.push(tmpd)
		    }
		    $c(columns)
		    if (!nodeid){
			$c("new id:")
			var nodeid=this.NewNodeName()
		    }
		    this.stacks[nodeid]=structuredClone(this.new_render);
		    $("GGGG1");
		    this.$nextTick(
			() => {
			    $("#"+nodeid).DataTable({
				stripeClasses:[],
				createdRow: function( row, data, dataIndex ) {
				    if ( data["color"] == "black" ) {
					$(row).addClass('box_bgcolor_black');
				    }
				},
				data:data,
				columns:columns,
			    })
			}
		    );
		}))
	    }catch(err){

		alert("sendTreeErr:"+err.message)
	    }
	},
	OnDelete(evt){
	    var target=evt.target;
	    this.test1=target
	    var id=target.getAttribute('pid')
	    $c("id:")
	    $c(id)
	    delete this.stacks[id]
	},
	OnLoad(evt){
	    var target=evt.target;
	    var id=target.getAttribute('pid')
	    this.info=this.stacks[id].info;
	},
	OnReset(evt){
	    var target=evt.target;
	    var id=target.getAttribute('pid')
	    $c("reset:");
	    $c(id);
	    this.ModelRender(id);
	}
    }
}    
  
</script>

<style>
  th{
  text-align:center;
  font-size: small;
  /*
  width:10%;
  text-align:left; */
  }
  td{
  text-align:center;
  font-size: small;
  }
  table{
      float:left;
  }
  .isshow{
      margin:10px;
      /* height:calc(97vw - 400px); */
  }
  
  .isHidden{
      margin-top:10px;
      margin-left:10px;
      margin-bottom:10px;            
      margin-right:400px;
      /* height:calc(97vw - 400px); */
  }


  progress[class='red'] {
      -webkit-appearance: none;
      appearance: none;      
      height: 0.5em;
      /* vertical-align: -0.2em; */
      width: 10em;      
  }



  progress[class='red']::-webkit-progress-bar {
      background-color: #eee;
      border-radius: 0.25em;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1) inset;
  }

  progress[class='red']::-webkit-progress-value {
         /* background-image:
	 /* -webkit-linear-gradient(-45deg, 
	                          transparent 33%, rgba(0, 0, 0, .1) 33%, 
	                          rgba(0,0, 0, .1) 66%, transparent 66%),
	  -webkit-linear-gradient(top, 
	                          rgba(255, 255, 255, .25), 
	                          rgba(0, 0, 0, .25)),
	  -webkit-linear-gradient(left, #09c, #f44); */
      

	  /* background-size: 35px 20px, 90% 90%, 90% 90%; */
	  border-radius: 0.25em; 
	  background:red;
  }


  progress[class='green'] {
      -webkit-appearance: none;
      appearance: none;      
      height: 0.5em;
      /* vertical-align: -0.2em; */
      width: 10em;      
  }



  progress[class='green']::-webkit-progress-bar {
      background-color: #eee;
      border-radius: 0.25em;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1) inset;
  }

  progress[class='green']::-webkit-progress-value {
         /* background-image:
	 /* -webkit-linear-gradient(-45deg, 
	                          transparent 33%, rgba(0, 0, 0, .1) 33%, 
	                          rgba(0,0, 0, .1) 66%, transparent 66%),
	  -webkit-linear-gradient(top, 
	                          rgba(255, 255, 255, .25), 
	                          rgba(0, 0, 0, .25)),
	  -webkit-linear-gradient(left, #09c, #f44); */
      

	  /* background-size: 35px 20px, 90% 90%, 90% 90%; */
	  border-radius: 0.25em; 
	  background:green;
  }

  .box_bgcolor_black{
      box-shadow: inset 0 0 0 9999px rgba(0,0,0,0.05);
  }

  
</style>
