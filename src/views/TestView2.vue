<template>
<section>
  <div id="PopoverContent" class="d-none">
    <div class="input-group">
      <input type="text"
	     class="form-control"
	     placeholder="Recipient's username"
	     id='popoverinput'
	     >
    </div>
  </div>
</section>
<div style='overflow:auto;margin-left:5px'>  
  <div style='float:left'>
    <p style='margin-bottom:3px'>
      <button class="btn btn-primary" type="button" data-bs-toggle="offcanvas"
	      id='sidebar_open'
	      data-bs-target="#offcanvasScrolling1">Save load</button>
      <button class="btn btn-primary" type="button" data-bs-toggle="offcanvas"
	      id='sidebar_open'
	      data-bs-target="#offcanvasScrolling">layer</button>
      <button class="btn btn-primary" type="button" data-bs-toggle="offcanvas"
	      id='sidebar_open'
	      data-bs-target="#offcanvasScrolling2">Color</button>
      <button class="btn btn-primary" type="button" 
	      @click='showcode()'>code</button>
    </p>
  </div>
</div>      


<div class="offcanvas offcanvas-end"
     data-bs-scroll="true"
     data-bs-backdrop="false"
     tabindex="-1"
     id="offcanvasScrolling1" >
  <div class="offcanvas-header">
    <h5 class="offcanvas-title" id="offcanvasScrollingLabel1">Save load</h5>
    <button id='sidebar_close'
	    type="button"
	    class="btn-close text-reset"
	    data-bs-dismiss="offcanvas"
	    aria-label="Close"></button>
  </div>
  <div style='margin:5px;padding:5px'>
    <div class="input-group mb-2">
      <input id='saver_filename'
	     type="text" class="form-control"
	     placeholder="Recipient's username"
	     />
      <button @click='IOSave()'>save</button>
    </div>
    
    <div class="input-group mb-2">
      <input class='form-control'
      	     id='loader_filename' type="file"
	     />
      <button @click='IOLoad()'>load</button>    
    </div>
  </div>
</div>

<div class="offcanvas offcanvas-end"
     data-bs-scroll="true"
     data-bs-backdrop="false"
     tabindex="-1"
     id="offcanvasScrolling2" >
  <div class="offcanvas-header">
    <h5 class="offcanvas-title" id="offcanvasScrollingLabel2">Color</h5>
    <button id='sidebar_close'
	    type="button"
	    class="btn-close text-reset"
	    data-bs-dismiss="offcanvas"
	    aria-label="Close"></button>
  </div>

  
  <div style='margin:5px;padding:5px'>
    <div style='float:left;font-size: small;'>add color</div>        
    <div class="input-group">
      <select
	style='height:28px;margin:1px;padding:1px'
	class="form-select form-select-sm"
	v-model='input.layer_color_add'
	>
	<template v-for='(op, idx) in opts.input_layers'
		  :key='idx'>
		  <option :value="op"
			  v-if="op!='topic'">{{op}}</option>
	</template>
      </select>
    </div>
    <div class='input-group'>
      <input class='form-control'
	     v-model='input.layer_color_add_json'
	     />
      <button @click='LayerColorAdd()'>Add Color</button>    
    </div>

    <div style='float:left;font-size: small;'>delete color</div>    
    <div class='input-group'>

      <select
	style='height:28px;margin:1px;padding:1px'
	class="form-select form-select-sm"
	v-model='input.layer_color_delete'
	>
	<template v-for='(op, idx) in opts.input_layers'
		  :key='idx'>
		  <option :value="op"
			  v-if="op!='topic'">{{op}}</option>
	</template>
      </select>
      <button @click='LayerColorDelete()'>Delete Color</button>    
    </div>

    <div style='float:left;font-size: small;'>change color</div>    
    <div class='input-group'>

      <select
	style='height:28px;margin:1px;padding:1px'
	class="form-select form-select-sm"
	v-model='input.layer_color_change'
	>
	<template v-for='(op, idx) in opts.cmap'
		  :key='idx'>
		  <option :value="idx"
			  v-if="op!='topic'">{{idx}}</option>
	</template>
      </select>
      <button @click='LayerColorChange()'>Change Color</button>    
    </div>
    <div style='float:left;font-size: small;'>current color</div>
    <div style='float:left;font-size: small;'>{{colormode}}:{{opts.cmap[colormode]}}</div>        

    
  </div>
</div>


<div class="offcanvas offcanvas-end"
     data-bs-scroll="true"
     data-bs-backdrop="false"
     tabindex="-1"
     id="offcanvasScrolling" >
  <div class="offcanvas-header">
    <h5 class="offcanvas-title" id="offcanvasScrollingLabel">Layer Function</h5>
    <button id='sidebar_close'
	    type="button"
	    class="btn-close text-reset"
	    data-bs-dismiss="offcanvas"
	    aria-label="Close"></button>
  </div>
  <div style='margin:5px;padding:5px'>
    <div style='float:left;font-size: small;'>add layer</div>                      
    <div style='margin:1px;padding:1px'
	 class="input-group">
      <input id='layer_add'
	     style='height:28px;margin:1px;padding:1px'
	     v-model='input.layer_add'
	     type="text" class="form-control"
	     placeholder="LayerName"
	     />
      <button
	style='height:28px;margin:1px;padding:1px'		    	
	@click='LayerInputAdd(input.layer_add)'>ADD</button>
    </div>
    <div style='float:left;font-size: small;'>delete layer</div>                
    <div style='margin:1px;padding:1px'
	   class="input-group">
      <select
	style='height:28px;margin:1px;padding:1px'
	class="form-select form-select-sm"
	v-model='input.layer_delete'
	>
	<option v-for='(op, idx) in opts.input_layers' :key='idx' :value="op">{{op}}</option>
      </select>
      <button
	style='height:28px;margin:1px;padding:1px'		    
	@click='LayerInputDelete(input.layer_delete)'>DELETE</button>
    </div>
    <div style='float:left;font-size: small;'>select layer</div>            
    <div style='margin:1px;padding:1px'
	 class="input-group">
      <select
	style='height:28px;margin:1px;padding:1px'		    
	@change='LayerInputChangeG()'
	class="form-select form-select-sm"
	v-model='onshowglobal'
	>
	<option v-for='(op, idx) in opts.input_layers' :key='idx' :value="op">{{op}}</option>
      </select>
    </div>
  </div>
</div>


<nav aria-label="breadcrumb"
     style='padding:5px;padding-left:10px;height:auto;overflow:auto'>
  <ol class="breadcrumb" style='margin-bottom:0px'> 
    <li class="breadcrumb-item">Layer:</li>
    <li class="breadcrumb-item"
	v-for='(op, idx) in opts.input_layers'
	:key='idx'><a @click="LayerInputChangeC(op)">{{op}}</a></li>
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
      	@focus='ActFocus($event)'
      	@blur='ActBlur($event)'
      	@keydown='KeyRaw($event)'
      	v-model='node.layer[node.onshow].input'
      	:id='idx'
      	:class="ClsBox(idx)">
	
      </textarea>
      
      <span class='dot'
	    @click='OnClickExpander($event)'        
	    :id="'e_'+idx"></span>
    </template>
  </div>
</div>

<div style='margin:5px'>
  <div v-if='opts.show_code'>
    <h3 style='text-align:left'>code table:</h3>
    <div id='tree_result' style='margin:3px;'>      
      <table class="table table-striped">  
	<thead>
	  <tr>
            <th style='width:10%;text-align:left'>id</th>
            <th style='width:10%;text-align:left'>name</th>
            <th style='width:80%;text-align:left'>code</th>		  
	  </tr>
	</thead>
	<tbody>
	  <template v-for='(node, idx) in info' :key="idx">
	    <!-- tr :class="nra_cls(node)" -->
	    <tr>
	      <td style='text-align:left'
		  @click='ActIn(node.id,true)'
		  >{{node.id}}</td>
	      <td style='text-align:left'>{{node.name}}</td>	  
	      <td style='text-align:left'>{{node.v}}</td>
	    </tr>
	  </template>
	</tbody>
      </table>
    </div>
  </div>
</div>
</template>  
<script>


// TODO: https://v5.bootcss.com/docs/content/tables/
// TODO: fold result
// TODO: Save Load cureent status
// TODO: Show Total Result

// Done: Show Total code
// Done: focus This fold suffix bug
// Done: Paste maintains width and height
// Done: lastnode can click on  
// Done: todo only surfix

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
	layer:{
	    topic:{
		input:"topic"
	    }
	},
	onshow:'topic',
	oncolor:'normal',	
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
	    },
	    struct: {
	    },
	    opts:{ // search
		cNO: 1,
		offset_x:200,
		offset_y:200,
		width:opts.width,
		height:opts.height,
		input_layers:["topic"],
		cmap:{
		    normal:{
			default:"black",
			active:"green",
			activefunc:"orange",			
		    }
		}
	    },
	    isalive:1,
	    onshowglobal:"topic",
	    colormode:"normal",
	    show_code:0,
	    active_node:0,
	    keymode:"input",
	    isshow:{},
	    cpnode:"None",
	    input:{
		layer_add:"",
	    }
	}
    },
    computed: {
    },
    watch: {
    },
    mounted() {
	pxy = this;	
	this.info={
		root:this.NodeNew('root'),
		c_0:this.NodeNew('c_0'),
	}
	this.struct={
		root: ['c_0'],
		c_0: [],
	}
	this.WatchThis();
	this.SetThis();
	
	$g('jsm_canvas').style.left='0px'
	$g('jsm_canvas').style.right='0px'

    },
    updated() {
	
	if (this.opts.isalive == 1){
  	    this.WatchThis();
  	    //this.SetThis();	    
	}
    },
    methods: {
	//1 get
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
	    }
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
		$c(info[j]);
		if (info[j]["sur"] != 0){
		    info[j]["sur"]=namemap[info[j]["sur"]]
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
	GetLayer(i){
	    var n=this.Get(i);
	    var add_info=n.layer[n.onshow]
	    
	    return n.layer[n.onshow]
	},

	// 2.watch
	WatchThis(){
	    this.WatchParent();
	    //this.WatchActive();	    
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
	//WatchActive(){
	//    var anode=this.anode()
	//    if (anode!=0){
	//	this.opts.last_active_node=anode
	//    }
	//},
	WatchShowAdd(i){
	    pxy=this;
	    $c(i)
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
	

	// 3.set
	
	SetSize(i){
	    var n=this.GetLayer(i);
	    n.w1=$g(i).offsetWidth;
	    n.h1=$g(i).offsetHeight;
	},
	
	SetCoordinate(){
	    var r=this.GetLayer('root');
	    this.opts.offset_x=r.x0-r.x6+opts.hmargin;
	    this.opts.offset_y=r.y0-r.y5+opts.vmargin;
	    
	    for (let i in this.info){
		// 计算box位置
		var st=$g(i).style
		if (this.isshow[i]==0){
		    st.position = 'absolute'		    
		    st.visibility = 'hidden';
		    st.left = '10px'
		    st.top = '10px'
		}else{
		    var n=this.GetLayer(i);
		    st.position = 'absolute'
		    st.visibility = 'visible';
		    st.left = (n.x1+this.opts.offset_x)+"px"
		    st.top = (n.y1+this.opts.offset_y)+"px"
		    
		}

		// 计算expander标记位置
		var st1=$ge(i).style		
		if (this.isexpander[i]==0){
		    st1.position = 'absolute'
		    st1.visibility = 'hidden';
		    st1.left = '10px'
		    st1.top = '10px'
		}else{
		    var n=this.GetLayer(i);
		    st1.position = 'absolute'
		    st1.visibility = 'visible';
		    st1.left = (n.x2+this.opts.offset_x)+"px"
		    st1.top = (n.y0-opts.expandsize/2+this.opts.offset_y)+"px"
		    st1.height = opts.expandsize+"px"
		    st1.width = opts.expandsize+"px"
		    
		}
	    }
	    
	},
	
	
	SetLineEnd(x1,y1,x2,y2,dash=false){
	    var ctx=$g('jsm_canvas').getContext('2d');
	    //ctx.globalAlpha = 1;
	    //ctx.globalCompositeOperation="hue"
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
	    ctx.strokeStyle = '#000000';
	    ctx.lineCap = 'butt';
	    // ctx.moveTo(x1,y1)
	    // ctx.lineTo((x1+x2)/2,y1)
	    // ctx.lineTo((x1+x2)/2,y2)
	    // ctx.lineTo(x2,y2)
	    
	    ctx.moveTo((x1+x2)/2,y2)	    
	    ctx.lineTo(x2,y2)
	    ctx.stroke();
	    
	},

	SetLine(x1,y1,x2,y2,dash=false){
	    var ctx=$g('jsm_canvas').getContext('2d');
	    //ctx.globalAlpha = 1;
	    //ctx.globalCompositeOperation="hue"
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
	    ctx.strokeStyle = '#000000';
	    ctx.lineCap = 'square';
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
	    var w=this.GetLayer('root').w3+2*opts.hmargin;
	    var h=this.GetLayer('root').h3+2*opts.vmargin;
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
		    var c=this.struct[i]
		    var c0=this.GetLayer(i)  
		    if (c.length>0){
			var ctx=$g('jsm_canvas').getContext('2d');			    
			ctx.beginPath();
			ctx.setLineDash([]);
			ctx.strokeStyle = '#000000';

			var c1=this.GetLayer(c[0])
			var c2=this.GetLayer(c[c.length-1])

			var y0=c0.y0
			var y1=c1.y0
			var y2=c2.y0
			var x1=c0.x2+opts.expandsize
			var x2=c1.x6

			x1=x1+this.opts.offset_x
			x2=x2+this.opts.offset_x

			y0=y0+this.opts.offset_y
			y1=y1+this.opts.offset_y
			y2=y2+this.opts.offset_y
			ctx.lineCap = 'square';
			ctx.moveTo((x1+x2)/2,y1)
			ctx.lineTo((x1+x2)/2,y2)
			ctx.stroke();
			ctx.lineCap = 'butt';
			ctx.moveTo(x1,y0)
			ctx.lineTo((x1+x2)/2,y0)
			ctx.stroke();			
			
			for (let j in this.struct[i]){
			    var o1=c0
			    var o2=this.GetLayer(this.struct[i][j]);
			    var x1=o1.x2+opts.expandsize
			    var y1=o1.y0
			    var x2=o2.x6
			    var y2=o2.y0
			    this.SetLineEnd(x1,y1,x2,y2,false);
			}
			
		    }
		    
		}
		
		if ((i in this.front) && (this.isshow[i]==1)){
		    var p=this.GetLayer(this.front[i])
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
	    var n=this.GetLayer(i)
	    var n1=this.Get(i)
	    var c=this.GetChildren(i);
	    if ((c.length==0) || (n1.show==0)){
		n.w2=0;
		n.h2=0;
		n.w2_add=0
	    }else{
		var w2=0;
		var h2=0;
		for (let j in c){
		    this.SetLayout(c[j]);
		    this.GetLayer(c[j]).h4=h2;
		    w2=Math.max(w2,this.GetLayer(c[j]).w3);
		    h2=h2+this.GetLayer(c[j]).h3+opts.vspace;
		}
		h2=h2-opts.vspace;
		n.w2=w2
		n.h2=h2
		n.w2_add=w2+opts.hspace
	    }
	    
	    if ((n1.sur==0) || (n1.show==0)){
		n.h4=0;
		n.w4=0;
		n.w4_add=0;
	    }else{
		this.SetLayout(n1.sur);
		var sur=this.GetLayer(n1.sur)
		n.w4=sur.w3;
		n.h4=sur.h3;
		n.w4_add=n.w4+opts.hspace
	    }
	    n.w3=n.w1+n.w2_add+n.w4_add
	    n.h3=Math.max(n.h1,n.h2,n.h4)		
	},
	
	SetLayoutBack(i){
	    this.SetSize(i);
	    var n=this.GetLayer(i)
	    var n1=this.Get(i)	    
	    var c=this.GetChildren(i);
	    if ((c.length==0) || (n1.show==0)){
		n.w2=0;
		n.h2=0;
		n.w2_add=0
	    }else{
		var w2=0;
		var h2=0;
		for (let j in c){
		    this.GetLayer(c[j]).h4=h2;		    
		    w2=Math.max(w2,this.GetLayer(c[j]).w3);
		    h2=h2+this.GetLayer(c[j]).h3+opts.vspace;
		}
		h2=h2-opts.vspace;
		n.w2=w2
		n.h2=h2
		n.w2_add=w2+opts.hspace
	    }
	    
	    
	    if ((n1.sur==0) || (n1.show==0)){
		n.h4=0;
		n.w4=0;
		n.w4_add=0;
	    }else{
		var sur=this.GetLayer(n1.sur)
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
	    var n=this.GetLayer(i);
	    var n1=this.Get(i);	    
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
	    
	    
	    if (n1.sur!=0){
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
	    var n=this.GetLayer(i);	      
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
	    var n=this.GetLayer(i);
	    var n1=this.Get(i);	    
	    if (i=='root'){
		this.SetPositionX(i,0)
		this.SetPositionY(i,0)		  
	    }else if(i in this.front){
		var p=this.GetLayer(this.front[i]);
		var x=p.x9+n.w1/2
		var y=p.y0
		this.SetPositionX(i,x)
		this.SetPositionY(i,y)
	    }else{
		var p=this.GetLayer(this.parent[i]);
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
		if (n1.sur!=0){
		    this.SetPosition(n1.sur)
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


	// 3.layer
	LayerInputAdd(i){
	    let index=this.opts.input_layers.indexOf(i)
	    if (index>=0){
		return
	    }

	    this.opts.input_layers=this.opts.input_layers.concat([i])
	    let nl=new Object();
	    nl["input"]=i
	    for (let j in this.info){
		this.info[j].layer[i]=structuredClone(nl);
				this.info[j].layer[i]=structuredClone(nl);
	    }
	},
	LayerInputDelete(i){
	    if (i=="topic"){
		alert("Cannot delete topic layer")
		return
	    }
	    let index=this.opts.input_layers.indexOf(i)
	    if (index<0){
		alert("Cannot find layer");
		return
	    }
	    this.opts.input_layers.splice(index, 1);
	    for (let j in this.info){
		delete(this.info[j].layer[i])
		if (this.info[j].onshow==i){
		    this.info[j].onshow="topic"
		}
	    }
	    if (this.onshowglobal==i){
		this.onshowglobal="topic"
	    }
	},
	LayerInputChangeG(i){
	    if (!i){
		i=this.onshowglobal;
	    }
	    this.onshowglobal=i
	    for (let j in pxy.info){
		this.info[j].onshow=i
	    }
	    this.WatchThis();	    
	    this.SetThis();
	},
	LayerInputChangeC(op,i){
	    if (!i){
		i=this.active_node
	    }
	    this.info[i].onshow=op
	    this.WatchThis();
	    this.SetThis();
	},
	LayerColorAdd(){
	    var n=this.input.layer_color_add
	    var j=JSON.parse(this.input.layer_color_add_json)
	    this.opts.cmap[n]=j
	    alert("Add Color success");
	},
	LayerColorDelete(){
	    var n=this.input.layer_color_delete
	    delete(this.opts.cmap[n])
	    alert("Delete Color success");
	    if (this.colormode==n){
		this.colormode="normal"
	    }
	},
	LayerColorChange(){
	    this.colormode=this.input.layer_color_change;
	},
	
	// Node
	NodeNew(i){
	    var n=structuredClone(opts.node)
	    var l=this.opts.input_layers
	    for (let i in l){
		n.layer[l[i]]=new Object();
		n.layer[l[i]].input=l[i]
	    }
	    n.onshow=this.onshowglobal;
	    return n
	},
	NodeAdd(i,name=null){
	    if (!name){
		name=this.GetNewnodeName();
	    }
	    this.struct[i].push(name);
	    this.struct[name]=[];
	    this.info[name]=this.NodeNew(i)
	    this.WatchThis();
	    this.$nextTick(() => {
		pxy.SetThisBack(name);
		pxy.NodeShow(i)
	    })
	    return name
	},
	NodeAddSur(i){
	    var name=this.GetNewnodeName();
	    var n=this.Get(i);
	    if (n.sur!=0){
		throw new Error(`node already have sur`);
	    }
	    n.sur=name
	    this.struct[name]=[];
	    this.info[name]=this.NodeNew(i)
	    this.WatchThis();
	    this.$nextTick(() => {
		this.SetThisBack(name);
		pxy.NodeShow(i)		
	    })
	},
	NodeDrop(i){
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
	NodeHide(i){
	    this.Get(i).show=0;
	    this.WatchThis();
	    this.SetThis();
	},
	NodeShow(i){
	    this.Get(i).show=1;
	    this.WatchThis();
	    this.SetThis();
	},
	NodeShowRecur(i){
	    //this.Get(i).show=1;
	    var p=this.GetParentOrFront(i);
	    if (p!=0){
		this.Get(p).show=1;
		this.NodeShowRecur(p)
	    }
	},
	NodeToggle(i){
	    this.Get(i).show=1-this.Get(i).show
	    this.WatchThis();
	    //this.SetThisBack(i);
	    this.SetThis();
	},
	NodeCopy(f){
	    this.cpnode=f
	},
	NodeUp(f){
	    var p=this.parent[f]
	    var pl=this.struct[p]
	    var index=pl.indexOf(f)
	    zIndexUp(pl,index)
	    this.WatchThis();
	    this.SetThisBack(p);
	    
	},
	NodeDown(f){
	    var p=this.parent[f]
	    var pl=this.struct[p]
	    var index=pl.indexOf(f)
	    zIndexDown(pl,index);
	    this.WatchThis();
	    this.SetThisBack(p);
	},
	NodePaste(t){
	    this.NodeCopyPaste(this.cpnode,t)
	},
	NodeCopyPaste(f,t){
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
	NodeFoldFor(n){
	    var c=this.GetDescendantSur(n)
	    c=c.concat([n])
	    for (let i in this.info){
		if ($.inArray(i,c) == -1){
		    this.info[i].show=0		    
		}
	    }
	    this.NodeShowRecur(n)
	    this.WatchThis()
	    this.SetThis()	
	},
	// Act
	
	ActFocus(event){
	    var target=event.target;
	    var id=target.id
	    $ah(target);
	    this.active_node=id;
	    this.SetThisBack(id);
	},
	ActBlur(event){
	    this.keymode="input";
	},
	ActIn(i,shownode){
	    if (i==0){
		return
	    }
	    if (!$g(i)){
		return
	    }
	    if (shownode){
		this.ShowNodeRecur(i);
		this.WatchThis();
		this.SetThis();		
	    }
	    $g(i).focus()
	    this.keymode="function"
	},
	// move
	MoveLeft(f){
	    if (f!="root"){
		var p=this.parent[f]
		if (!!p){
		    this.ActIn(p)		    
		}
	    }
	},
	MoveRight(f){
	    var n=this.struct[f][0]
	    if (!!n){
		this.ActIn(n)
	    }
	},
	MoveSur(f){
	    var n=this.info[f].sur
	    if (n){
		this.ActIn(n)
	    }
	},
	MoveFront(f){
	    var n=this.front[f]
	    if (!!n){
		this.ActIn(n)
	    }
	},
	MoveUp(f){
	    if (f!="root"){
		var p=this.parent[f]
		if (!p){
		    return
		}
		var pl=this.struct[p]
		var index=pl.indexOf(f)
		if (index!=0){
		    this.ActIn(pl[index-1])
		}
	    }
	},
	MoveDown(f){
	    if (f!="root"){
		var p=this.parent[f];
		if (!p){
		    return
		}
		var pl=this.struct[p]
		var length = pl.length
		var index=pl.indexOf(f)
		if((index+1) != length){
		    this.ActIn(pl[index+1])		    
		}
	    }
	},
	//
	KeyRaw(event){
	    var target=event.target;
	    var id=target.id
	    var k=event.keyCode
	    if (k == 27){
		$("S1");
		event.preventDefault();
		this.keymode="function";
	    }else if (this.keymode=="function"){
		$("S2");		
		this.KeyFunction(event)
	    }else{
		$("S3");
		this.KeyNormal(event);
	    }
	},
	KeyFunction(event){
	    var target=event.target;
	    var id=target.id
	    var k=event.keyCode
	    event.preventDefault();	    
	    switch(k){
	    case 32: // SPACE
		this.keymode="input";
		break;
	    case 65: // A
		var nodeid=this.NodeAdd(id);
		this.$nextTick(() => {this.ActIn(nodeid);})
		break;
		
	    case 9: // tab
		var nodeid=this.NodeToggle(id);
		break;
	    case 70: // f
		this.NodeFoldFor(id);
		break;
		
	    case 46: // DELETE
		if (id!='root'){
		    var p=this.GetParentOrFront(id);
		    this.NodeDrop(id);
		    this.$nextTick(() => {this.ActIn(p);})		    
		}else{
		    throw new Error("you mustn't drop root node");
		}
		break;
	    case 68: // D
		if (id!='root'){
		    this.NodeDrop(id)
		}else{
		    throw new Error("you mustn't drop root node");
		}
		break;
	    case 67: // C copy
		this.NodeCopy(id)
		break;
	    case 80: // P paste
		this.NodePaste(id)
		break;
	    case 83: //S
		var nodeid=this.NodeAddSur(id);
		break;
	    case 38: //c-up
		if (event.ctrlKey){
		    this.NodeUp(id);		      
		}else{
		    this.MoveUp(id);
		}
		break;
		
	    case 37: //left
		if (event.shiftKey){
		    this.MoveFront(id)
		}else{
		    this.MoveLeft(id);
		}
		break;
		
	    case 39: //right
		if (event.shiftKey){
		    this.MoveSur(id);		    
		}else{
		    this.MoveRight(id);
		}
		break;
		
	    case 40: //c-down
		if (event.ctrlKey){
		    this.NodeDown(id);		      
		}else{
		    this.MoveDown(id);
		}
		break;
//	    case 71: //G
//		//this.resOn(id);
//		if (event.shiftKey){
//		    this.$nextTick(() => {
//			this.resOn(id)
//			var target=$gc("res_"+id)[0]
//			if (target){
//			    goto(target);			    
//			}
//		    })
//		}else{
//		    this.$nextTick(() => {
//			this.resOn(id)
//			var target=$gc("res_node_"+id)[0]
//			if (target){
//			    goto(target);			    
//			}
//		    })
//		}
//		break;
	    }
	},
	KeyNormal(event){
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
	// 格式
	// 显示内容表格

	// table
	TblShowCode(){
	    this.opts.show_code=1-this.opts.show_code
	},

	// class
	ClsBox(idx){
	    $c("ClsBox");
	    var style=new Object()
	    style['inputBox']=true
	    if (this.colormode=="normal"){
		var color=this.opts.cmap[this.colormode]
		if (idx==this.active_node){
		    if (this.keymode=="function"){
			style["inputBox"+color["activefunc"]]=true
		    }else{
			style["inputBox"+color["active"]]=true
		    }
		}else{
		    style["inputBox"+color["default"]]=true
		}
	    }else{
		var color=this.opts.cmap[this.colormode]
		var n=this.info[idx].layer[this.colormode].input
		$c(color)
		$c(n)				
		if ("default" in color){
		    var dc=color["default"]
		}else{
		    var dc="black"
		}
		for (let i in color){
		    if (n==i){
			dc=color[i]
		    }
		}
		style["inputBox"+dc]=true
	    }
	    return style
	},

	// 改变color
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
	//

	
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
	
//	nra_cls(node){
//	    var d=new Object()
//	    //d["active_res"]=(node.id==this.opts.active_result_node)
//	    d["table-danger"]=(node.id==this.opts.active_result_node)
//	    
//	    d["res_node_"+node.id]=true
//	    return d
//	},
//	ra_cls(node){
//	    var d=new Object()
//	    //d["active_res"]=(node.id==this.opts.active_result_node)
//	    d["table-danger"]=(node.id==this.opts.active_result_node)	    
//	    d["res_"+node.id]=true
//	    return d
//	},

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

	// IO ******************************************************
	IOTreeInfo(){
	    return {'info':this.info,
		    'struct':this.struct,
		    'opts':this.opts}
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
		pxy.$nextTick(() => {
		    for (let i in pxy.info){
			var n=d1.info[i]
			$g(i).style.width=n.layer[n.onshow].w1+"px"
			$g(i).style.height=n.layer[n.onshow].h1+"px"
		    }
		    pxy.WatchThis()
		    pxy.SetThis()			  
		}
			     )
	    }
	    var text=utils.read(file_data,f)
	},
	// 1.get
	
	
	
	
	// 5.on
	OnClickExpander(event){
	    var target=event.target;
	    var eid=target.id
	    var id=eid.substring(2)
	    this.NodeToggle(id)
	    
	},
	timer(){
	    var myDate = new Date();
	    $c(myDate.getSeconds())
	    $c(myDate.getMilliseconds())	    
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
  .inputBoxorange {
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


.inputBox{
    font-family: "Courier New", Courier, monospace;
    font-size: small;
}

#code_editor{
    /* margin: 4px; */
    /* float:left; */
    text-align:left;
    width:500px;
    height:450px;
    border-style:solid;
    height:300px;
    margin-left:5px;
}

#code_result{
    /* margin: 4px; */
    /* float:left; */
    text-align:left;
    width:500px;
    height:432px;
    border-style:solid;        
    margin-top:0px;
    font-family: "Courier New", Courier, monospace;
    font-size: small;
    height:300px;
    resize:none;
    margin-left:5px;
}


</style>
