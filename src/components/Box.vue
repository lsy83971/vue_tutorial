<template>
<textarea v-model='node.s.v' v-for='(idx, node) in info' @key='idx' />
</template>

<script>
var opts={
    box:{
	hspace:30,
	vspace:20,
	hmargin:50,
	vmargin:50,	
    },
    s:{
	v:'as $f\n:sb',
	chd:[],
	sur:null,
	visable:1,
    }
}
  
export default {
    data(){
	return {
	    info:{
		root:{
		    s:structuredClone(opts.s)
		}
	    }
	}
    },

    methods:{
	
    }
    
}

</script>
