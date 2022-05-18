const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({

    transpileDependencies: true,
    devServer:{
	proxy: {
	    '^/flask': {
		target: 'http://localhost:5005',
		secure:false,
		changeOrigin: true,
	    },
	    '^/model': {
		target: 'http://localhost:5006',
		secure:false,
		changeOrigin: true,
	    }
	}
    }
})

