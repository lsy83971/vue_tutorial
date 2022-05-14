<template>
  <section>
    <div id="PopoverContent" class="d-none">
      <div class="input-group">
        <input type="text"
	       class="form-control"
	       placeholder="Recipient's username"
	       id='popoverinput'
	       oninput='pxy.popovertoname(this.value)'
	       >
      </div>
    </div>
  </section>
  <div style='overflow:auto'>  
    <div style='float:left'>
      <p style='margin-bottom:3px'>
	<button class="btn btn-primary"
		data-bs-toggle="collapse"
		href="#multiCollapseExample1"
		role="button"	    
		>Save Load</button>
	<button class="btn btn-primary" type="button"	      
		@click='FlaskSendTree()'>Run</button>
	<button class="btn btn-primary" type="button"	      
		@click='FlaskClearTree()'>clear</button>
	<button class="btn btn-primary" type="button" 
		@click='RevertTree()'>revert</button>
	<button class="btn btn-primary" type="button" 
		@click='FlaskSendCode()'>sendcode</button>
	<button class="btn btn-primary"
		data-bs-toggle="collapse"
		href="#multiCollapseExample2"
		role="button"	    
		>Editor</button>
      </p>
    </div>
  </div>      
  <div class="row">
    <div class="collapse multi-collapse" id="multiCollapseExample1"
	 style='height:fit-content;padding:5px;width:90%'
	 tabindex="-1"
	 aria-labelledby="offcanvasScrollingLabel">
      
      <div class="input-group mb-2">
	<input id='saver_filename'
	       type="text" class="form-control"
	       placeholder="Recipient's username"
	       aria-label="Recipient's username"
	       aria-describedby="button-addon2"	   
	       />
	<button @click='IOSave()'>saveJSM</button>
      </div>
      
      <div class="input-group mb-2">
	<input class='form-control'
      	       id='loader_filename' type="file"
	       />
	<button @click='IOLoad()'>loadJSM</button>    
      </div>
      
      <div class="input-group mb-3">
	<input class='form-control'
      	       id='json_loader_filename' type="file"
	       />
	<button @click='FlaskLoadjson()'>loadJson</button>
	
      </div>
    </div>
    <div class="collapse multi-collapse" id="multiCollapseExample2">
      <div style='overflow:auto;float:left'>
	<div id="code_editor" class="input"
	     style='height:300px'
	     >
	</div>
      </div>
      
      <div style='height:306px;float:left;margin-left:5px'>	
	<textarea id="code_result"
		  v-model='code_res'
		  style='height:300px;resize:none'
		  >
	</textarea>
      </div>
    </div>
  </div>
  
  <nav aria-label="breadcrumb"
       style='padding:5px;padding-left:10px;height:30px'>
    <ol class="breadcrumb"> 
      <li class="breadcrumb-item">GLOBAL:</li>      
      <li class="breadcrumb-item"><a @click="changeonshow('v')">code</a></li>
      <li class="breadcrumb-item"><a @click="changeonshow('id')">ID</a></li>
      <li class="breadcrumb-item"><a @click="changeonshow('rawname')">name</a></li>
      <li class="breadcrumb-item">NODE:</li>            
      <li class="breadcrumb-item"><a @click="changeNodeonshow('v')">code</a></li>
      <li class="breadcrumb-item"><a @click="changeNodeonshow('id')">ID</a></li>
      <li class="breadcrumb-item"><a @click="changeNodeonshow('rawname')">name</a></li>
      
      <li class="breadcrumb-item">context: {{context.node}}</li>
      <li class="breadcrumb-item"><a @click="ActiveOn(opts.last_active_node)">focusNode: {{anodeInfo()}}</a></li>
      <li class="breadcrumb-item">Err: {{nodeiserr()}}</li>
      <li class="breadcrumb-item">ErrChd: {{chderr()}}</li>      
      <li class="breadcrumb-item">Errs: {{totalerr()}}</li>
      <li class="breadcrumb-item">Stacks: {{StaTotal()}}</li>
      <li class="breadcrumb-item">Leaves: {{LeafTotal()}}</li>
      <li class="breadcrumb-item">Nodes: {{NodeTotal()}}</li>
      <li class="breadcrumb-item"><a @click="changecolor()">Color</a></li>
    </ol>
  </nav>
  
  <div id='jsm_outer'
       style="width:99%;height:calc(95vh - 160px);
      	      border-style:solid;
      	      margin:5px
      	      ">
    <div id='jsm_inner' style="overflow: auto;position: relative;width: 100%;height: 100%;">
      <canvas id='jsm_canvas' style='position:absolute' z-index='1' />    	
      <template  v-for='(node, idx) in info' :key="idx">
	<textarea
      	  style="height:30px;width:180px;z-index:auto;resize:both"
      	  @focus='OnFocus($event)'
      	  @blur='OnBlur($event)'
      	  @keydown='OnKeydown($event)'
      	  v-model='node[node.onshow]'
      	  :id='idx'
      	  :class="boxClass(idx)">

	</textarea>
	
	<span class='dot'
	      @click='OnClickExpander($event)'        
	      :id="'e_'+idx"></span>
      </template>
    </div>
  </div>
  <div id='tree_result' style='margin:3px;'>
    <!-- table class="table">  
      <colgroup>
	<col width="30px" />
	<col width="30px" />
	<col width="60px" />
	<col width="140px" />	
      </colgroup>    
      <thead>
	<tr>
          <th>id</th>
          <th>name</th>
          <th>route</th>
          <th>result</th>		  
	</tr>
      </thead>
      <tbody>
	<template v-for='(nodes, idx) in node_res' :key="idx">
	  <template
	    style="text-align:left"
	    class="node_res"
	    v-for='(node, idx) in nodes'
	    :key="idx" :node_res_id="node.id"
	    >
	    <tr :class="nra_cls(node)">
	      <td style='text-align:left'
		  @click='ActiveOn(node.id,true)'
		  >{{node.id}}</td>
	      <td style='text-align:left'>{{node.name_abbr}}</td>	  
	      <td style='text-align:left'>{{node.route}}</td>
	      <td style='text-align:left'>{{node.data.b_data}}</td>	    	      
	    </tr>
	  </template>
	</template>
      </tbody>
    </table -->

    <table class="table">  
      <colgroup>
	<col width="30px" />
	<col width="30px" />
	<col width="60px" />
	<col width="140px" />	
      </colgroup>    
      <thead>
	<tr>
          <th>id</th>
          <th>name</th>
          <th>route</th>
          <th>result</th>		  
	</tr>
      </thead>
      <tbody>
	<template v-for='(nodes, idx) in noderesult' :key="idx">
	  <template
	    style="text-align:left"
	    class="node_res"
	    v-for='(node, idx) in nodes'
	    :key="idx" :node_res_id="node.id"
	    >
	    <tr :class="nra_cls(node)">
	      <td style='text-align:left'
		  @click='ActiveOn(node.id,true)'
		  >{{node.id}}</td>
	      <td style='text-align:left'>{{node.name_abbr}}</td>	  
	      <td style='text-align:left'>{{node.route}}</td>
	      <td style='text-align:left'>{{node.data.b_data}}</td>	    	      
	    </tr>
	  </template>
	</template>
      </tbody>
    </table>

	    
    <table class="table">
      <colgroup>
	<col width="30px" />
	<col width="30px" />
	<col width="60px" />
	<col width="140px" />	
      </colgroup>    
      <thead>
	<tr>
          <th>id</th>
          <th>name</th>
          <th>route</th>
          <th>result</th>		  
	</tr>
      </thead>
      <tbody>
	<template v-for='(node, idx) in res' :key="idx">
	  <tr :class="ra_cls(node)">	  
	    <td style='text-align:left'
		@click='ActiveOn(node.id,true)'		
		>{{node.id}}</td>
	    <td style='text-align:left'>{{node.name_abbr}}</td>	  
	    <td style='text-align:left'>{{node.route}}</td>
	    <td style='text-align:left'>{{node.data.b_data}}</td>	    
	  </tr>
	</template>
      </tbody>
    </table>
  </div>
</template>  

<script>

// TODO: focus This fold suffix bug
// TODO: Paste maintains width and height
// TODO: lastnode can click on  
// todo only surfix
// node_element.clientHeight;

//      ³¤¿í:
//      w[n] ±íÊ¾ÐÎ×´nµÄ¿í
//      h[n] ±íÊ¾ÐÎ×´nµÄ³¤
//      ÌØÊâ: h4 ±íÊ¾ÔÚÐÖµÜÐÎ×´ÖÐµÄÏà¶Ô¸ß¶È
//
//      ---------------------------------
//      |3            -------           | 
//      | ---------   |2    |           | 
//      | |1      |   |     | --------- | 
//      | |       |   |     | |4      | | 	  	  
//      | |       |   |     | |       | | 
//      | |       |   |     | |       | | 
//      | |       |   |     | |       | | 
//      | |       |   |     | |       | | 	  	  
//      | |       |   |     | --------- | 	  	  
//      | ---------   |     |           | 	  	  
//      |             -------           |  
//      ---------------------------------
//      
//      Î»ÖÃ:
//      (xy)[(nx)_(ny)] ±íÊ¾Ïà¶ÔÎ»ÖÃ
//    X:6*1***0***2 * 4**3**5**9***1***1*7
//                                 0   1
//  Y 
//  5   ----------------------------------
//  3   |             -------            |  
//  1   | ---------   |*****|            |  
//  7   | |*******|   |*****|  --------- |
//      | |*******|   |*****|  |*******| |     
//      | |*******|   |*****|  |*******| |        
//  0   | |*******|   |*****|  |*******| |        
//      | |*******|   |*****|  |*******| |        
//      | |*******|   |*****|  |*******| |      	  	
//  8   | |*******|   |*****|  --------- |      	  	
//  2   | ---------   |*****|            |	  	  
//  4   |             -------            |	  
//  6   ----------------------------------

// TODO:contenteditable='true'

import axios from 'axios';

var $d = document;  
var $g = function (id) { return $d.getElementById(id); };
var $ge = function (id) { return $d.getElementById('e_'+id)};
var $gc = function (id) { return $d.getElementsByClassName(id); };
var $ah = function (target) {
    var lines=target.value.split("\n");
    if (lines.length<=1){
	target.style.height = 30+'px'
    }else{
	target.style.height = "auto";
	target.style.height = (target.scrollHeight+6) + "px";
    }
}
var $c = console.log;
var $cr = function (tag) { return $d.createElement(tag); };
var $w = global



function goto(tag){
    let bridge = tag;
    let body = $d.body
    let height = 0;
    do {
	height += bridge.offsetTop;
	bridge = bridge.offsetParent;
    } while(bridge !== body)
    
    window.scrollTo({
	top: height,
	behavior: 'smooth'
    })
}

function heightoftag(tag){
    let bridge = tag;
    let body = $d.body
    let height = 0;
    do {
	height += bridge.offsetTop;
	bridge = bridge.offsetParent;
    } while(bridge !== body)
    return height+'px'
}


var opts={
    height:800,
    width:1000,
    hmargin:100,
    vmargin:50,
    hspace:20,
    vspace:15,
    expandsize:14,
    node:{
	v:'as $f',
	rawname:'',
	onshow:'v',
	show:1,
	sur:0,
    }
};
var result
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


function swapArray(arr, index1, index2) {
    var a1=structuredClone(arr[index1])
    var a2=structuredClone(arr[index2])      
    arr[index2]=a1
    arr[index1]=a2
    return arr;
}
function zIndexUp(arr,index){
    if(index!= 0){
	swapArray(arr, index, index-1);
    }
}
function zIndexDown(arr,index){
    var length = arr.length
    if((index+1) != length){
	swapArray(arr, index, index+1);
    }
}
export default {
    data () {
	return {
	    info:{
		'root':structuredClone(opts.node),
		'c_0':structuredClone(opts.node),
	    },
	    struct: {
		'root': ['c_0'],
		'c_0': [],
	    },
	    opts:{

		"ggg":'a',
		"cNO": 1,
		"offset_x":200,
		"offset_y":200,
		"width":opts.width,
		"height":opts.height,
		"isalive":1,
		"color_mode":'code',
		"active_node":0,
		"active_input_node":0,
		"last_active_node":0,
		"active_popover_node":0,
		"active_result_node":0,
		"popover":0,
	    },
	    isshow:{},
	    //err_chd_cnt:null,
	    //err_cnt:null,
	    node_res:{},
	    res:{},
	    code_res:"",
	    cpnode:"None",
	    context:{"node":"None"},
	}
    },
    computed: {
	noderesult(){
	    var nodeid=this.opts.last_active_node
	    if (!(nodeid==0)){
		return {nodeid:this.node_res[nodeid]}
	    }else{
		return {}
	    }
	},
	noderawname:{
	    get () {
		var nodeid=this.opts.last_active_node
		if (nodeid==0) {
		    return ""
		} else {
		    return this.info[nodeid].rawname
		}
	    },
	    set (val) {
		var nodeid=this.opts.last_active_node
		if (nodeid==0) {
		    return ""
		} else {
		    this.info[nodeid].rawname=val
		}
	    }
	},
    },
    watch: {
	// struct(){
	//     this.GetParent()
	// },
	// deep:true
    },
    mounted() {
	this.WatchThis();
	this.SetThis();
	$g('jsm_canvas').style.left='0px'
	$g('jsm_canvas').style.right='0px'
	pxy = this;

	//editor = ace.edit("code_editor");
	//editor.session.setMode("ace/mode/python");
    },
    updated() {
	if (this.opts.isalive == 1){
	    //$c("UPDATE")
  	    this.WatchThis();
  	    //this.SetThis();	    
	}
    },
    methods: {
	boxClass(idx){
	    var o=new Object()
	    o['readonly']=this.ActiveNodeIs(idx)
	    o['onalive']=this.ActiveNodeIs(idx)
	    o['inputBox'+this.info[idx].color]=true
	    return o
	   // return {
	//	'readonly': ActiveNodeIs(idx),
      	//	'onalive': ActiveNodeIs(idx),
	//	('inputBox'+this.info[idx].color): true,
  	    //}
	},

	CountErr(){
	    pxy.err_cnt=new Object()
	    for (let i in pxy.info){
		var targets=this.node_res[i]
		if (!targets){
		    pxy.err_cnt[i]=0
		}else{
		    var c=0;
		    targets.forEach((x) => {
			if (x["err"] != ""){
			    c=c+1;
			}
		    })
		    pxy.err_cnt[i]=c
		}
	    }
	},
	CountChdErr(nodeid){
	    if (!nodeid){
		this.CountErr()		
		var nodeid='root';
		pxy.err_chd_cnt=new Object();
	    }
	    var c=pxy.err_cnt[nodeid];
	    var chd=this.GetChildrenSur(nodeid);
	    for (let i in chd){
		c=c+this.CountChdErr(chd[i])
	    }
	    pxy.err_chd_cnt[nodeid]=c
	    return c
	},
	changecolor(mode){
	    if (!mode){
		var old=this.opts.color_mode;
		if (old=="code"){
		    mode='err'
		}else{
		    mode='code'		    
		}
	    }
	    this.opts.color_mode=mode;
	    this.WatchThis();
	    this.SetThis();	    
	},
	changeNodeonshow(i){
	    var nodeid=this.opts.last_active_node
	    if (nodeid!=0){
		this.info[nodeid].onshow=i
	    }
	    this.SetThis();
	    //this.SetThisBack(i);
	},
	nodefoldfor(n){
	    var c=this.GetDescendantSur(n)
	    c=c.concat([n])
	    for (let i in this.info){
		if ($.inArray(i,c) == -1){
		    this.info[i].show=0		    
		}
	    }
	    this.ShowNodeRecur(n)
	    this.WatchThis()
	    this.SetThis()	
	},
	
	changeonshow(i){
	    for (let j in pxy.info){
		pxy.info[j].onshow=i
	    }
	    this.SetThis();
	},
	currentrawname(){
	    var nodeid=pxy.opts.active_popover_node;
	    return pxy.info[nodeid].rawname
	},
	popovertoname(v){
	    var nodeid=pxy.opts.active_popover_node;
	    pxy.info[nodeid].rawname=v
	},
	NodePopoverHideOther(){
	    var oldid=this.opts.active_popover_node;
	    $('#'+oldid).popover('hide');
	},
	NodePopoverShow(id){
	    if (id!=this.opts.active_popover_node){
		this.NodePopoverHideOther();
	    }
	    this.opts.active_popover_node=id
	    $('#'+id).popover('show')
	},
	NodePopoverHide(id){
	    if (id!=this.opts.active_popover_node){
		this.NodePopoverHideOther();		
	    }
	    this.opts.active_popover_node=id
	    $('#'+id).popover('hide')
	},
	anode(){
	    if (this.opts.active_node==0){
		return this.opts.active_input_node
	    }else{
		return this.opts.active_node
	    }
	},
	anodeObj(){
	    var nodeid=this.anode();
	    if (nodeid==0){
		return {}
	    }else{
		return this.info[nodeid]
	    }
	},
	anodeInfo(){
	    var nodeid=this.opts.last_active_node
	    if (nodeid in this.info){
		var name=this.info[nodeid].name
		if (nodeid==name){
		    return nodeid
		}else{
		    return nodeid+' | '+name
		}
	    }else{
		return '0'
	    }
	},
	nodeisnotcode(n){
	    return (this.info[n].onshow != 'v')
	},
	nodeiserr(n){
	    if (!n){
		var n=this.opts.last_active_node		
	    }
	    if (n==0){
		return 0
	    }
	    if (!this.err_cnt){
		return 0
	    }
	    if (!this.err_cnt[n]){
		return 0
	    }
	    return this.err_cnt[n]
	},
	StaTotal(){
	    var s=0
	    for (let i in this.node_res){
		s=s+this.node_res[i].length
	    }
	    return s
	},
	LeafTotal(){
	    return Object.keys(this.res).length
	},
	NodeTotal(){
	    return Object.keys(this.info).length
	},
	totalerr(){
	    if (!this.err_chd_cnt){
		return 0
	    }
	    return this.err_chd_cnt['root']
	},
	chderr(n){
	    if (!n){
		var n=this.opts.last_active_node		
	    }
	    if (!this.err_chd_cnt){
		return 0
	    }
	    if (!this.err_chd_cnt[n]){
		return 0
	    }
	    return this.err_chd_cnt[n]
	},
	
	nra_cls(node){
	    var d=new Object()
	    d["active_res"]=(node.id==pxy.opts.active_result_node)
	    d["res_node_"+node.id]=true
	    return d
	},
	ra_cls(node){
	    var d=new Object()
	    d["active_res"]=(node.id==pxy.opts.active_result_node)
	    d["res_"+node.id]=true
	    return d
	},
	
	resOn(id){
	    this.opts.active_result_node=id	    	    
	},
	//	  resOff(id){
	//	      this.opts.active_result_node=0
	//	  },
	//	  resToggle(id){
	//	      if (this.opts.active_result_node==id){
	//		  this.resOff(id)
	//	      }else{
	//		  this.resOn(id)		
	//	      }
	//	  },
	FlaskSendTree(){
	    try{
		var s=this.IOTreeInfo();
		this.opts.active_result_node=0;
		utils.post('flask/tree',s,(response => {
		    pxy.node_res=response.data['node_res'];
		    pxy.res=response.data['res'];
		    pxy.CountErr();
		    pxy.CountChdErr();
		    alert("load tree success")
		}))
	    }catch(err){
		alert("sendTreeErr:"+err.message)
	    }
	    
	},
	FlaskSendCode(){
	    var s={'code':editor.getSession().getValue(),
		   'context':this.context,
		  }
	    pxy.code_res="waiting!"
	    utils.post('flask/code',s,(response => {
		pxy.code_res=response.data['output'];		
	    }))
	    
	},
	FlaskClearTree(){
	    var s={}
	    utils.post('flask/clear',s,(response => {
		alert("clear!")
	    }))
	},
	
	FlaskLoadjson(){
	    try{
		var file_input = document.getElementById('json_loader_filename');
		var files = file_input.files;
		if(files.length == 0){
		    return 0
		}else{
		    var file_data = files[0];
		}
		var f=function(result,name) {
		    var d = JSON.parse(result);
		    utils.post("flask/loaddata",d,
			       (response => {
				   alert(response.data);
			       }))
		    //pxy.WatchThis()
		}
		var text=utils.read(file_data,f)
	    }catch(err){
		alert("FLASKLOADJSONERR:"+err.message)
	    }
	},
	
	IOTreeInfo(){
	    return {'info':this.info,
		    'struct':this.struct,
		    'opts':this.opts}
	},
	RevertTree(){
	    utils.post("flask/revert",{},
		       (response => {
			   var d=response.data;
			   this.info=d.info;
			   this.struct=d.struct;
			   this.opts=d.opts;
			   this.WatchThis();
			   this.SetThis();
		       }))
	    //pxy.WatchThis()
	},
	IOToJson(){
	    return JSON.stringify(
		{'info':this.info,
		 'struct':this.struct,
		 'opts':this.opts})
	},
	IOSave(){
	    var filename=$g('saver_filename').value;
	    var filetext=this.IOToJson()
	    utils.save(filetext,'text/jsm',filename)
	},
	IOLoad(){
            var file_input = document.getElementById('loader_filename');
            var files = file_input.files;
	    if(files.length == 0){
		return 0
	    }else{
		var file_data = files[0];
	    }
	    var f=function(result,name) {
		var d = JSON.parse(result);
		var d1 = structuredClone(d);
		pxy.info=d['info']
		pxy.struct=d['struct']
		pxy.opts=d['opts']
		if (!pxy.opts.color_mode){
		    pxy.opts.color_mode='code'
		}
		pxy.$nextTick(
		    () => {
			for (let i in pxy.info){
			    $g(i).style.width=d1.info[i].w1+"px"
			    $g(i).style.height=d1.info[i].h1+"px"
			}
			pxy.WatchThis()
			pxy.SetThis()			  
		    }
		)
	    }
	    var text=utils.read(file_data,f)
	},
	ActiveNodeIs(i){
	    if (i==this.opts.active_node){
		return true
	    }else{
		return false
	    }
	},
	ActiveIs(i){
	    if (this.opts.active_node!=0){
		return true
	    }else{
		return false
	    }
	},
	ActiveOn(i,shownode){
	    if (i==0){
		return
	    }
	    if (shownode){
		this.ShowNodeRecur(i);
		this.WatchThis();
		this.SetThis();		
	    }
	    $g(i).focus()
	    this.opts.active_node=i
	    this.opts.active_input_node=0


	    
	},
	ActiveOff(i){
	    this.opts.active_node=0
	    this.opts.active_input_node=i
	},
	// 1.get
	GetParentOrFront(i){
	    if (!!this.parent[i]){
		return this.parent[i]
	    }
	    if (!!this.front[i]){
		return this.front[i]
	    }
	    return 0
	},
	GetChildren(i){
	    if (i in this.struct){
		return this.struct[i]
	    }else{
		return []
	    }
	},
	GetChildrenSur(i){
	    if (i in this.struct){
		var des= this.struct[i]
	    }else{
		var des=[]
	    };
	    var n=this.Get(i);	    
	    if (n.sur !=0){
		des=des.concat([n.sur])		  
	    }
	    return des
	},
	
	GetDescendant(i){
	    var des=this.struct[i];
	    for (let i in des){
		des=des.concat(this.GetDescendant(des[i]))
	    }
	    return des	    
	},
	GetDescendantSur(i){
	    var des=this.struct[i];
	    var n=this.Get(i);
	    for (let i in des){
		des=des.concat(this.GetDescendantSur(des[i]))
	    }
	    if (n.sur !=0){
		des=des.concat([n.sur])		  
		des=des.concat(this.GetDescendantSur(n.sur))
	    }
	    return des	    
	},
	
	GetDescendantSurTree(i){
	    var ns=this.GetDescendantSur(i)
	    ns=[i].concat(ns)
	    var info=new Object();
	    var struct=new Object();
	    var namemap=new Object();
	    for (let j in ns){
		namemap[ns[j]]=this.GetNewnodeName();
		var tmp_info=structuredClone(this.info[ns[j]])
		var tmp_struct=structuredClone(this.struct[ns[j]])
		info[namemap[ns[j]]]=tmp_info
		struct[namemap[ns[j]]]=tmp_struct
	    }
	    for (let j in info){
		if (info[j]["sur"] != 0){
		    info[j]["sur"]=namemap[info[i]["sur"]]
		}
		var tmp_struct=struct[j].map(function(x){return namemap[x]})
		struct[j]=tmp_struct
	    }
	    return {"info":info,"struct":struct,"namemap":namemap,"root":i}
	},
	
	Get(i){
	    return this.info[i]
	},
	GetNewnodeName(){
	    var name='c_'+this.opts.cNO;
	    this.opts.cNO++;
	    return name
	},
	
	
	// 2.watch
	WatchThis(){
	    this.WatchParent();
	    this.WatchActive();	    
	    this.WatchName();
	    //this.WatchStruct();
	    this.WatchShow();
	    this.WatchExpander();
	},
	WatchParent(){
	    var d=new Object();
	    for (let i in this.struct){
		for (let j in this.struct[i]){
		    d[this.struct[i][j]]=i
		}
	    }
	    this.parent=d;
	    
	    var d1=new Object();
	    for (let i in this.info){
		var n=this.info[i]
		if (n.sur != 0){
		    d1[n.sur]=i
		}
	    }
	    this.front=d1;
	},
	WatchActive(){
	    var anode=this.anode()
	    if (anode!=0){
		this.opts.last_active_node=anode
	    }
	},
	WatchName(){
	    var cm=this.opts.color_mode;
	    for (let i in this.info){
		if (!this.info[i].rawname){
		    this.info[i].rawname=""
		}
		if (this.info[i].rawname==""){
		    this.info[i].name=i
		    this.info[i].rawname=i
		}else{
		    this.info[i].name=this.info[i].rawname;
		}
		//this.info[i].onshow=this.info[i][this.opts.onshow];
		this.info[i].id=i;
		if (!this.info[i].onshow){
		    this.info[i].onshow='v'
		}

		if (cm=="code"){
		    if (this.nodeisnotcode(i)){
			this.info[i].color="blue"
		    }else{
			this.info[i].color="black"
		    }
		}
		if (cm=="err"){
		    if (this.nodeiserr(i)){
			this.info[i].color="red"
			
		    }else{
			if (this.chderr(i)){
			    this.info[i].color="black"
			}else{
			    this.info[i].color="green"									    
			}
			
		    }

		}
		
		
	    };
	},
	WatchShowAdd(i){
	    this.isshow[i]=1;
	    if (this.Get(i).show==1){
		for (let j in this.struct[i]){
		    this.WatchShowAdd(this.struct[i][j]);
		}
		var sur=this.Get(i).sur
		if (sur != 0){
		    this.WatchShowAdd(sur);
		}
	    }
	},
	WatchShow(){
	    var s=new Object();
	    for (let i in this.info){
		s[i]=0
	    }
	    this.isshow=s;
	    this.WatchShowAdd('root');
	},
	WatchExpander(){
	    var s=new Object();
	    var s1=new Object();	    
	    for (let i in this.info){
		s[i]=0
		s1[i]=0				
		if ((this.isshow[i]==1) &&
		    ((this.struct[i].length>0) ||
		     (this.Get(i).sur!=0))
		   ){
		    s1[i]=1
		    if (this.Get(i).show==1){
			s[i]=1
		    }		
		}
	    }
	    this.isexpander=s1;
	    this.isshowchildren=s;	    
	},
	
	AddNode(i,name=null){
	    if (!name){
		name=this.GetNewnodeName();
	    }
	    this.ShowNode(i)
	    this.struct[i].push(name);
	    this.struct[name]=[];
	    this.info[name]=structuredClone(opts.node)
	    this.WatchThis();
	    this.$nextTick(() => {this.SetThisBack(name);})
	    return name

	},
	
	AddSurNode(i){
	    var name=this.GetNewnodeName();
	    var n=this.Get(i);
	    if (n.sur!=0){
		throw new Error(`node already have sur`);
	    }
	    n.sur=name
	    this.struct[name]=[];
	    this.info[name]=structuredClone(opts.node)
	    this.WatchThis();
	    this.$nextTick(() => {this.SetThisBack(name);})
	},
	
	DropNode(i){
	    var parent=this.parent[i]
	    var front=this.front[i]
	    
	    $d.activeElement.blur();	    
	    this.opts.isalive=0
	    var desc=this.GetDescendantSur(i);
	    desc=desc.concat([i])	    
	    
	    for (let j in desc){
		delete(this.info[desc[j]])
		delete(this.struct[desc[j]])
	    }
	    for (let j in desc){
		var n=desc[j];
		var p=this.parent[n]
		if (p in this.struct){
		    var l=this.struct[p];
		    var filtered=l.filter((value, index, arr) => {
			return value != n
		    });
		    this.struct[p]=filtered
		}
	    }

	    
	    if (i in this.front){
		p=this.front[i]
		this.Get(p).sur=0;
	    }
	    this.opts.isalive=1;
	    this.WatchThis();
	    this.$nextTick(
		() => {
		    if (!!front){
			this.SetThisBack(front)
			return
		    }
		    if (parent){
			this.SetThisBack(parent)
			return
		    }
		    
		}
	    )

	},
	HideNode(i){
	    this.Get(i).show=0;
	    this.WatchThis();
	    this.SetThis();
	},
	ShowNode(i){
	    this.Get(i).show=1;
	    this.WatchThis();
	    this.SetThis();
	},
	ShowNodeRecur(i){
	    //this.Get(i).show=1;
	    var p=this.GetParentOrFront(i);
	    if (p!=0){
		this.Get(p).show=1;
		this.ShowNodeRecur(p)
	    }
	},
	ToggleNode(i){
	    this.Get(i).show=1-this.Get(i).show
	    this.WatchThis();
	    //this.SetThisBack(i);
	    this.SetThis();
	},
	copyNode(f){
	    this.cpnode=f
	},
	upNode(f){
	    var p=this.parent[f]
	    var pl=this.struct[p]
	    var index=pl.indexOf(f)
	    zIndexUp(pl,index)
	    this.WatchThis();
	    this.SetThisBack(p);
	    
	},

	leftFocus(f){
	    if (f!="root"){
		var p=this.parent[f]
		if (!!p){
		    this.ActiveOn(p)		    
		}

	    }
	},
	rightFocus(f){
	    var n=this.struct[f][0]
	    if (!!n){
		this.ActiveOn(n)
	    }
	},
	surFocus(f){
	    var n=this.info[f].sur
	    if (n){
		this.ActiveOn(n)
	    }
	},
	frontFocus(f){
	    var n=this.front[f]
	    if (!!n){
		this.ActiveOn(n)
	    }
	},
	
	upFocus(f){
	    if (f!="root"){
		var p=this.parent[f]
		if (!p){
		    return
		}
		var pl=this.struct[p]
		var index=pl.indexOf(f)
		if (index!=0){
		    this.ActiveOn(pl[index-1])
		}
	    }
	},
	downFocus(f){
	    if (f!="root"){
		var p=this.parent[f]
		if (!p){
		    return
		}
		var pl=this.struct[p]
		var length = pl.length
		var index=pl.indexOf(f)
		if((index+1) != length){
		    this.ActiveOn(pl[index+1])		    
		}
	    }
	},
	
	downNode(f){
	    var p=this.parent[f]
	    var pl=this.struct[p]
	    var index=pl.indexOf(f)
	    zIndexDown(pl,index);
	    this.WatchThis();
	    this.SetThisBack(p);
	},
	pasteNode(t){
	    this.copyPasteNode(this.cpnode,t)
	},
	copyPasteNode(f,t){
	    var cpinfo=this.GetDescendantSurTree(f)
	    Object.assign(this.struct,cpinfo["struct"])
	    Object.assign(this.info,cpinfo["info"])
	    this.struct[t].push(cpinfo["namemap"][f]);
	    var old_info=structuredClone(cpinfo["info"])
	    this.WatchThis();
	    this.$nextTick(() => {
		this.SetThis();
		for (let k in old_info){
		    $g(k).style.width=old_info[k].w1+"px"
		    $g(k).style.height=old_info[k].h1+"px"
		}
	    })
	},
	contextNode(n){
	    this.context={"node":n}
	},
	
	// 4.set
	SetCoordinate(){
	    var r=this.Get('root');
	    this.opts.offset_x=r.x0-r.x6+opts.hmargin;
	    this.opts.offset_y=r.y0-r.y5+opts.vmargin;
	    
	    for (let i in this.info){
		if (this.isshow[i]==0){
		    $g(i).style.position = 'absolute'		    
		    $g(i).style.visibility = 'hidden';
		    $g(i).style.left = '10px'
		    $g(i).style.top = '10px'
		}else{
		    var n=this.Get(i);
		    $g(i).style.position = 'absolute'
		    $g(i).style.visibility = 'visible';
		    $g(i).style.left = (n.x1+this.opts.offset_x)+"px"
		    $g(i).style.top = (n.y1+this.opts.offset_y)+"px"
		    
		}
		
		if (this.isexpander[i]==0){
		    $ge(i).style.position = 'absolute'
		    $ge(i).style.visibility = 'hidden';
		    $ge(i).style.left = '10px'
		    $ge(i).style.top = '10px'
		}else{
		    var n=this.Get(i);		    
		    $ge(i).style.position = 'absolute'
		    $ge(i).style.visibility = 'visible';
		    $ge(i).style.left = (n.x2+this.opts.offset_x)+"px"
		    $ge(i).style.top = (n.y0-opts.expandsize/2+this.opts.offset_y)+"px"
		    $ge(i).style.height = opts.expandsize+"px"
		    $ge(i).style.width = opts.expandsize+"px"
		    
		}
	    }
	    
	},
	
	SetSize(i){
	    $ah($g(i));
	    this.info[i].w1=$g(i).offsetWidth;
	    this.info[i].h1=$g(i).offsetHeight;
	},
	
	SetLine(x1,y1,x2,y2,dash=false){
	    var ctx=$g('jsm_canvas').getContext('2d');		    
	    ctx.beginPath();
	    x1=x1+this.opts.offset_x
	    x2=x2+this.opts.offset_x	    
	    y1=y1+this.opts.offset_y
	    y2=y2+this.opts.offset_y
	    
	    if (dash==true){
		ctx.setLineDash([0.5,1]);
	    }else{
		ctx.setLineDash([]);		
	    }
	    ctx.moveTo(x1,y1)
	    ctx.lineTo((x1+x2)/2,y1)
	    ctx.lineTo((x1+x2)/2,y2)
	    ctx.lineTo(x2,y2)	    	    
	    ctx.stroke();
	    
	},
	
	SetCanvasClear(){
	    var ctx=$g('jsm_canvas').getContext('2d');
	    ctx.clearRect(0,0,this.opts.width,this.opts.height)
	},
	SetCanvas(){
	    var w=this.Get('root').w3+2*opts.hmargin;
	    var h=this.Get('root').h3+2*opts.vmargin;
	    //w=Math.max(this.opts.width,w);
	    //h=Math.max(this.opts.height,h);
	    this.opts.width=w;
	    this.opts.height=h;
	    $g('jsm_canvas').height=h
	    $g('jsm_canvas').width=w
	    this.SetCanvasClear();
	    //$c("CANVAS CLEAR");
	    for (let i in this.info){
		if (this.isshowchildren[i]){
		    for (let j in this.struct[i]){
			var o1=this.Get(i);
			var o2=this.Get(this.struct[i][j]);
			var x1=o1.x2+opts.expandsize
			var y1=o1.y0
			var x2=o2.x6
			var y2=o2.y0
			this.SetLine(x1,y1,x2,y2,false);
		    }
		    
		}
		
		if ((i in this.front) && (this.isshow[i]==1)){
		    var p=this.Get(this.front[i])
		    var x1=p.x5+10
		    var y1=p.y3
		    var x2=p.x9
		    var y2=p.y0
		    this.SetLine(x1,y1,x2,y2,true)
		    
		    var x1=p.x5+10
		    var y1=p.y4
		    var x2=p.x9
		    var y2=p.y0
		    this.SetLine(x1,y1,x2,y2,true)
		}
		
	    }
	    
	    
	    //$g('jsm_canvas').style.z-index=1
	    //$g('jsm_inner').scrollHeight=h+'px'
	    //$g('jsm_inner').scrollWidth=w+'px'	    
	    
	    
	    //todo
	},
	
	SetLayout(i){
	    this.SetSize(i);
	    var n=this.Get(i)	    
	    var c=this.GetChildren(i);
	    if ((c.length==0) || (n.show==0)){
		n.w2=0;
		n.h2=0;
		n.w2_add=0
	    }else{
		var w2=0;
		var h2=0;
		for (let j in c){
		    this.SetLayout(c[j]);
		    this.Get(c[j]).h4=h2;
		    w2=Math.max(w2,this.Get(c[j]).w3);
		    h2=h2+this.Get(c[j]).h3+opts.vspace;
		}
		h2=h2-opts.vspace;
		n.w2=w2
		n.h2=h2
		n.w2_add=w2+opts.hspace
	    }
	    
	    if ((n.sur==0) || (n.show==0)){
		n.h4=0;
		n.w4=0;
		n.w4_add=0;
	    }else{
		this.SetLayout(n.sur);
		var sur=this.Get(n.sur)
		n.w4=sur.w3;
		n.h4=sur.h3;
		n.w4_add=n.w4+opts.hspace
	    }
	    n.w3=n.w1+n.w2_add+n.w4_add
	    n.h3=Math.max(n.h1,n.h2,n.h4)		
	},

	SetLayoutBack(i){
	    this.SetSize(i);
	    var n=this.Get(i)
	    var c=this.GetChildren(i);
	    if ((c.length==0) || (n.show==0)){
		n.w2=0;
		n.h2=0;
		n.w2_add=0
	    }else{
		var w2=0;
		var h2=0;
		for (let j in c){
		    this.Get(c[j]).h4=h2;		    
		    w2=Math.max(w2,this.Get(c[j]).w3);
		    h2=h2+this.Get(c[j]).h3+opts.vspace;
		}
		h2=h2-opts.vspace;
		n.w2=w2
		n.h2=h2
		n.w2_add=w2+opts.hspace
	    }


	    if ((n.sur==0) || (n.show==0)){
		n.h4=0;
		n.w4=0;
		n.w4_add=0;
	    }else{
		var sur=this.Get(n.sur)
		n.w4=sur.w3;
		n.h4=sur.h3;
		n.w4_add=n.w4+opts.hspace
	    }
	    
	    n.w3=n.w1+n.w2_add+n.w4_add
	    n.h3=Math.max(n.h1,n.h2,n.h4)

	    
	    if (!!this.front[i]){
		this.SetLayoutBack(this.front[i])
		return
	    }
	    if (!!this.parent[i]){
		this.SetLayoutBack(this.parent[i])
		return
	    }
	},	
	
	SetPositionX(i,x){
	    var n=this.Get(i);
	    n.x0=x;
	    n.x1=n.x0-n.w1/2
	    n.x2=n.x0+n.w1/2
	    
	    
	    if (this.struct[i].length>0){
		n.x4=n.x2+opts.hspace
		n.x3=n.x4+n.w2/2
		n.x5=n.x4+n.w2
	    }else{
		n.x4=n.x2
		n.x3=n.x2
		n.x5=n.x2
	    }
	    
	    
	    if (n.sur!=0){
		n.x9=n.x5+opts.hspace
		n.x11=n.x9+n.w4		
		n.x10=n.x9+n.w4/2
		n.x6=n.x1		
		n.x7=n.x11
	    }else{
		n.x6=n.x1
		n.x7=n.x5
	    }
	    
	},
	SetPositionY(i,y){
	    var n=this.Get(i);	      
	    n.y0=y;
	    n.y1=n.y0-n.h1/2
	    n.y2=n.y0+n.h1/2
	    n.y3=n.y0-n.h2/2
	    n.y4=n.y0+n.h2/2
	    n.y5=n.y0-n.h3/2
	    n.y6=n.y0+n.h3/2
	    n.y7=n.y0-n.h4/2
	    n.y8=n.y0+n.h4/2
	},
	SetPosition(i){
	    var n=this.Get(i);
	    
	    if (i=='root'){
		this.SetPositionX(i,0)
		this.SetPositionY(i,0)		  
	    }else if(i in this.front){
		var p=this.Get(this.front[i]);
		var x=p.x9+n.w1/2
		var y=p.y0
		this.SetPositionX(i,x)
		this.SetPositionY(i,y)
	    }else{
		var p=this.Get(this.parent[i]);
		var x=p.x4+n.w1/2
		var y=p.y3+n.h4+n.h3/2
		this.SetPositionX(i,x)
		this.SetPositionY(i,y)
	    }

	    if (this.isshow[i]==1){
		var c=this.GetChildren(i);
		for (let j in c){
		    this.SetPosition(c[j])
		}
		if (n.sur!=0){
		    this.SetPosition(n.sur)
		}
	    }
	    // TODO HARD MODE : SOFT MODE
	    
//	    var c=this.GetChildren(i);
//	    for (let j in c){
//		this.SetPosition(c[j])
//	    }
//	    if (n.sur!=0){
//		this.SetPosition(n.sur)
//	    }
            //node_element.style.left = (_offset.x + p.x) + 'px';
            //node_element.style.top = (_offset.y + p.y) + 'px';
	},
	
	SetThis(){
	    //await this.$nextTick();	    
	    this.$nextTick(
		() => {
		    this.SetLayout('root');
		    this.SetPosition('root');	
		    this.SetCoordinate();
		    this.SetCanvas();	      
		}
	    )
	},


	SetThisBack(i){
	    //await this.$nextTick();
	    this.$nextTick(
		() => {
		    this.SetLayoutBack(i);
		    this.SetPosition('root');	
		    this.SetCoordinate();
		    this.SetCanvas();
		}
	    )
	},
	
	
	// 5.on
	OnFocus(event){
	    var target=event.target;
	    var id=target.id
	    //target.style.height = "auto";
	    //target.style.height = ((target.scrollHeight)+4) + "px";
	    $ah(target);

//	    this.NodePopoverHideOther();
//	    this.opts.active_popover_node=id;
//	    delete(this.opts.popover);
//	    const popover = new bootstrap.Popover(document.querySelector('#'+id), {
//		container: 'body',
//		title: 'Search',
//		html: true,
//		placement: 'bottom',
//		trigger:'manual',
//		sanitize: false,
//		content() {
//		    return document.querySelector('#PopoverContent').innerHTML;
//		}
//	    })
//	    this.opts.popover=popover
	    //this.info[target.id].height=target.offsetHeight;
	    //this.info[target.id].width=target.offsetWidth;	
	    //$c(this.info);
	    //$c(typeof(this.info));
	    pxy.opts.active_input_node=id;
	    this.WatchActive();
	    this.SetThisBack(id);

	    //pxy.opts.active_node=id;	    
	},
	OnBlur(event){

	    var target=event.target;
	    var id=target.id
	    //$c("blur")
	    $ah(target);	      
	    //target.style.height = "auto";
	    //target.style.height = ((target.scrollHeight)+4) + "px";
	    //this.info[target.id].height=target.offsetHeight;
	    //this.info[target.id].width=target.offsetWidth;	
	    //$c(this.info);
	    //$c(typeof(this.info));

	    this.SetThisBack(id);
	    pxy.opts.active_node=0;
	    pxy.opts.active_input_node=0;
	},
	OnClickExpander(event){
	    var target=event.target;
	    var eid=target.id
	    var id=eid.substring(2)
	    this.ToggleNode(id)
	    
	},
	timer(){
	    var myDate = new Date();
	    $c(myDate.getSeconds())
	    $c(myDate.getMilliseconds())	    
	},
	OnKeydown(event){
	    var target=event.target;
	    var id=target.id
	    var k=event.keyCode
	    // $c('catch id:');	    
	    // $c(id);
	    // $c('catch key:');	    
	    // $c(k);
	    
	    if (k == 27){
		//$c('goto activate:');	    
		event.preventDefault();
		this.ActiveOn(id)
	    }else if (this.opts.active_node==id){
		//$c('goto activate mode:');	    
		this.OnKeydownActiveMode(event)
	    }else{
		//$c('goto default mode:');	    		
		this.OnKeydownFixSize(event);
	    }

	},
	OnKeydownActiveMode(event){
	    var target=event.target;
	    var id=target.id
	    var k=event.keyCode
	    event.preventDefault();	    
	    switch(k){
	    case 32:
		this.ActiveOff(id)
		break;
	    case 65: // A
		var nodeid=this.AddNode(id);
		//this.$nextTick(() => {this.ActiveOn(nodeid);})
		break;
		
	    case 9: // tab
		var nodeid=this.ToggleNode(id);
		break;
	    case 70: // f
		this.nodefoldfor(id);
		break;
		
	    case 46: // DELETE
		if (id!='root'){
		    this.DropNode(id)
		}else{
		    throw new Error("you mustn't drop root node");
		}
		break;
	    case 68: // D
		if (id!='root'){
		    this.DropNode(id)
		}else{
		    throw new Error("you mustn't drop root node");
		}
		break;
	    case 67: // C copy
		this.copyNode(id)
		break;
	    case 80: // P paste
		this.pasteNode(id)
		break;
	    case 83: //S
		var nodeid=this.AddSurNode(id);
		break;
	    case 84: //T
		this.contextNode(id);
		break;
		
	    case 38: //c-up
		if (event.ctrlKey){
		    this.upNode(id);		      
		}else{
		    this.upFocus(id);
		}
		break;

	    case 37: //left
		if (event.shiftKey){
		    this.frontFocus(id)
		}else{
		    this.leftFocus(id);
		}
		break;

	    case 39: //right
		if (event.shiftKey){
		    this.surFocus(id);		    
		}else{
		    this.rightFocus(id);
		}
		break;
		
	    case 40: //c-down
		if (event.ctrlKey){
		    this.downNode(id);		      
		}else{
		    this.downFocus(id);
		}
		break;
	    case 82: //r
		this.NodePopoverShow(id)		    
		break;
		
	    case 89: //r
		this.NodePopoverHide(id);
		break;

		

	    case 71: //G
		//this.resOn(id);
		this.$nextTick(() => {
		      this.resOn(id)
		      var target=$gc("res_node_"+id)[0]
		      goto(target);
		  })
		  break;
	      }

	  },
	  OnKeydownFixSize(event){
	      var target=event.target;
	      var id=target.id
	      var h_old=target.style.height;
	      var w_old=target.style.width;
	      $ah(target);
	      var h_new=target.style.height;
	      var w_new=target.style.width;
	      
	      if (h_old != h_new){
		  this.SetThisBack(id)
		  return
	      }
	      if (w_old != w_new){
		  this.SetThisBack(id)
		  return
	      }
	  },
      }
  }
</script>

<style>
  .dot {
      background-color: #bbb;
      border-radius: 50%;
      display: inline-block;
  }
  .inputBoxgreen{
      border-color: green;
      outline-color:green;
      /* padding:0px;      */
      padding-left:0px;
      padding-right:0px;
      padding-top:0px;
      padding-bottom:0px;      
      border-width: 3px;
  }
  .inputBoxblue{
      border-color: blue;
      outline-color:blue;
      /* padding:0px;      */
      padding-left:0px;
      padding-right:0px;
      padding-top:0px;
      padding-bottom:0px;      
      border-width: 3px;
      
  }
  .inputBoxred{
      border-color: red;
      outline-color:red;
      /* padding:0px;      */
      padding-left:0px;
      padding-right:0px;
      padding-top:0px;
      padding-bottom:0px;      
      border-width: 3px;
      
  }
  .inputBoxblack{
      border-color: black;
      outline-color:black;
      /* padding:0px;      */
      padding-left:0px;
      padding-right:0px;
      padding-top:0px;
      padding-bottom:0px;      
      border-width: 3px;
      
  }
  
  
  .inputBox{
      padding-left:0px;
      padding-right:0px;
      padding-top:0px;
      padding-bottom:0px;      
      border-width: 3px;
  }
  .onalive {
      border-color: orange;
      outline-color:orange;
      /* padding:0px;      */
      padding-left:0px;
      padding-right:0px;
      padding-top:0px;
      padding-bottom:0px;      
      
      border-width: 3px;
      
  }
  #data_selector{
      float: left;
      margin: 5px;
      width: 60%;
  }
  
  #data_selector div{
      margin: 5px;
      width: 300px;
  }

  #data_selector button{
      /* margin-top: 1px;
    margin-bottom: 1px;    */
      width:30%;
  }
  #data_selector input{
      /* margin-top: 1px;
    margin-bottom: 1px;    */
      width:60%;
      float:left; 
  }

  #data_engine_info{
      margin:3px;
      overflow:auto;
  }
  
  #data_engine_info div{
      margin:3px;
      text-align:left;
      float:right;
      width:200px;
  }

  
  .input_file{
      /* margin: 4px; */
      width:60%;
      float:left    
  }
  #left_panel{
      /* margin: 4px; */
    width:1050px;
    /*height:1000px;*/
      overflow:auto;
      float:left;
  }


.active_res{
    border-style:solid;
    border-width: medium;    
    padding:0px;
    border-color: red;    
}

html {
    overflow-y: auto;
}
body{
    width: 99vw;
    overflow:hidden;
    padding-right: calc(100vw - 100%);
}
</style>
