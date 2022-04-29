<template>
  
<span class="dot"></span>

<div id='jsm_outer' style='height:800px;width:1000px;border-style:solid'>
  <div id='jsm_inner' style="overflow: auto;position: relative;width: 100%;height: 100%;">
    <canvas id='jsm_canvas' style='position:absolute' z-index='1' />    
<template  v-for='(node, idx) in info' :key="idx">
  <textarea
    style='z-index:auto;text-overflow:ellipsis;outline:none'
    @focus='OnFocus($event)'
    @blur='OnBlur($event)'
    @keydown='OnKeydown($event)'
    v-model='node.v'
    :id='idx'
    :class="{'readonly': ActiveNodeIs(idx),
	     'onalive': ActiveNodeIs(idx),
	    }">
  </textarea>
  <span class='dot'
	@click='OnClickExpander($event)'        
	:id="'e_'+idx"></span>
</template>
  </div>
</div>
<div>
  <div id='data_selector' style='margin:3px;'>
    <div>
      <input id='saver_filename' />
      <button @click='IOSave()'>saveJSM</button>
    </div>
    <div>    
      <input class='input_file' id='loader_filename' type="file"  />
      <button @click='IOLoad()'>loadJSM</button>
    </div>
    <div>      
      <input class='input_file' id='json_loader_filename' type="file"  />
      <button @click='FlaskLoadjson()'>loadJson</button>
    </div>      
  </div>
</div>

</template>

<script>
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
//      |             -------          	|  
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

import axios from 'axios';

var $d = document;  
var $g = function (id) { return $d.getElementById(id); };
var $ge = function (id) { return $d.getElementById('e_'+id); };
var $c = console.log;
var $cr = function (tag) { return $d.createElement(tag); };
var $w = global

var opts={
    height:800,
    width:1000,
    hmargin:100,
    vmargin:50,
    hspace:30,
    vspace:20,
    expandsize:14,
    node:{
	v:'as $f\n:root',
	show:1,
	sur:0
    }
};
var result
var utils= {
    read: function (file_data,f) {
        var reader = new FileReader();
	reader.onload = function() {
	    f(this.result,file_data.name)
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
		$(error)
	    })
    }
}

export default {
    data () {
	return {
	    info:{
		'root':structuredClone(opts.node),
		'c_0':structuredClone(opts.node)
	    },
	    struct: {
		'root': ['c_0'],
		'c_0': [],	
	    },
	    opts:{
		"cNO": 1,
		"offset_x":200,
		"offset_y":200,
		"width":opts.width,
		"height":opts.height,
		"isalive":1,
		"active_node":0,
		
	    }
	}
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
	
	pxy=this;
	utils.post('flask/run',{'a':1},(response => ($c(response.data))))
	
	
    },
    updated() {
	if (this.opts.isalive==1){
  	    this.WatchThis();	    	    
  	    this.SetThis();	    
	}
    },
    methods: {
	FlaskSendTree(){
	    var s=this.IOTreeInfo();
	    utils.post('flask/tree',s,(response => ($c(response.data))))
	},
	FlaskLoadjson(){
            var file_input = document.getElementById('json_loader_filename');
            var files = file_input.files;
	    $c(file_input)
	    $c(files)	    
	    if(files.length == 0){
		return 0
	    }else{
		var file_data = files[0];
		$c(file_data)	    		
	    }
	    var f=function(result,name) {
		var d = JSON.parse(result);
		utils.post("flask/loaddata",d,
			   (response => ($c(response.data)))
			  )
		pxy.info=d['info']
		pxy.struct=d['struct']
		pxy.opts=d['opts']
		//pxy.WatchThis()
	    }
	    var text=utils.read(file_data,f)
	    $c(text)
	    $c('GG')	    
	},
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
	    $c(file_input)
	    $c(files)	    
	    if(files.length == 0){
		return 0
	    }else{
		var file_data = files[0];
		$c(file_data)	    		
	    }
	    var f=function(result,name) {
		var d = JSON.parse(result);
		pxy.info=d['info']
		pxy.struct=d['struct']
		pxy.opts=d['opts']
		//pxy.WatchThis()
	    }
	    var text=utils.read(file_data,f)
	    $c(text)
	    $c('GG')	    
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
	ActiveOn(i){
	    $c("activeOn:")
	    $c(i);
	    $g(i).focus()
	    this.opts.active_node=i
	},
	ActiveOff(){
	    this.opts.active_node=0
	},
	// 1.get
	GetChildren(i){
	    if (i in this.struct){
		return this.struct[i]
	    }else{
		return []
	    }
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
	    }
	    return des	    
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
	
	AddNode(i){
	    var name=this.GetNewnodeName();
	    this.ShowNode(i)
	    this.struct[i].push(name);
	    this.struct[name]=[];
	    this.info[name]=structuredClone(opts.node)
	    this.WatchThis();
	    return name
	    //this.SetThis();
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
	    //this.SetThis();
	},
	
	DropNode(i){
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
		$c(n)
		$c(p)		
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
	    this.SetThis();
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
	ToggleNode(i){
	    this.Get(i).show=1-this.Get(i).show
	    this.WatchThis();
	    this.SetThis();
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
	    this.Get('root').h3
	    var w=this.Get('root').w3+2*opts.hmargin;
	    var h=this.Get('root').h3+2*opts.vmargin;
	    w=Math.max(this.opts.width,w);
	    h=Math.max(this.opts.height,h);
	    this.opts.width=w;
	    this.opts.height=h;
	    $g('jsm_canvas').height=h
	    $g('jsm_canvas').width=w
	    this.SetCanvasClear();
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
			$c("GG")
			$c(i)
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
		    
		    $c("HH")
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
		$c(i)
		var p=this.Get(this.front[i]);
		var x=p.x9+n.w1/2
		var y=p.y0
		this.SetPositionX(i,x)
		this.SetPositionY(i,y)
	    }else{
		var p=this.Get(this.parent[i]);
		$c('set position:')
		$c(i)				
		$c(this.parent[i])
		$c(p)
		$c(n)		
		var x=p.x4+n.w1/2
		var y=p.y3+n.h4+n.h3/2
		this.SetPositionX(i,x)
		this.SetPositionY(i,y)
	    }
	    
	    var c=this.GetChildren(i);
	    for (let j in c){
		this.SetPosition(c[j])
	    }
	    if (n.sur!=0){
		this.SetPosition(n.sur)
	    }
            //node_element.style.left = (_offset.x + p.x) + 'px';
            //node_element.style.top = (_offset.y + p.y) + 'px';
	    
	},
	SetThis(){
	    this.SetLayout('root');
	    this.SetPosition('root');	
	    this.SetCoordinate();
	    this.SetCanvas();	      
	    $c(this.info);  
	},
	
	
	// 5.on
	OnFocus(event){
	    var target=event.target;
	    var id=target.id
	    $c(id)	    
	    target.style.height = "auto";
	    target.style.height = (target.scrollHeight) + "px";
	    
	    //this.info[target.id].height=target.offsetHeight;
	    //this.info[target.id].width=target.offsetWidth;	
	    //$c(this.info);
	    //$c(typeof(this.info));
	    this.SetThis();
	    pxy.opts.active_node=id;	    
	},
	OnBlur(event){
	    var target=event.target;
	    var id=target.id
	    target.style.height = "auto";
	    target.style.height = (target.scrollHeight) + "px";
	    //this.info[target.id].height=target.offsetHeight;
	    //this.info[target.id].width=target.offsetWidth;	
	    //$c(this.info);
	    //$c(typeof(this.info));
	    this.SetThis();
	    pxy.opts.active_node=0;	    
	},
	OnClickExpander(event){
	    var target=event.target;
	    var eid=target.id
	    $c('gg');
	    $c(eid);
	    var id=eid.substring(2)
	    this.ToggleNode(id)
	    
	},
	OnKeydown(event){
	    var target=event.target;
	    var id=target.id
	    var k=event.keyCode
	    $c('catch id:');	    
	    $c(id);
	    $c('catch key:');	    
	    $c(k);
	    
	    if (k == 27){
		$c('goto activate:');	    
		event.preventDefault();
		this.ActiveOn(id)
	    }else if (this.opts.active_node==id){
		$c('goto activate mode:');	    
		this.OnKeydownActiveMode(event)
		
	    }else{
		$c('goto default mode:');	    		
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
		this.ActiveOff()
		break;
	    case 65:
		var nodeid=this.AddNode(id);
		//this.$nextTick(() => {this.ActiveOn(nodeid);})
		break;
		
	    case 9:
		var nodeid=this.ToggleNode(id);
		break;
	    case 46:
		if (id!='root'){
		    this.DropNode(id)
		}else{
		    throw new Error("you mustn't drop root node");
		}
		break;
	    case 83:
		var nodeid=this.AddSurNode(id);
		break;
	    }

	},
	OnKeydownFixSize(event){
	    var target=event.target;
	    var id=target.id
	    $c(id);
	    target.style.height = "auto";
	    target.style.height = (target.scrollHeight) + "px";
	    this.SetThis()
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
.onalive {
    border-color: red;
    border-width: 3px;    
}
#data_selector{
    margin: 5px;
    width: 40%;
}
#data_selector div{
    margin: 5px;
    width: 40%;
}

#data_selector button{
    margin-top: 1px;
    margin-bottom: 1px;    
    width:30%;
}
#data_selector input{
    margin-top: 1px;
    margin-bottom: 1px;    
    width:60%;
    float:left; 
}
.input_file{
    margin: 4px;
    width:60%;
    float:left    
}


</style>
