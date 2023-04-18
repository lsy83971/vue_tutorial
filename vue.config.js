const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
    transpileDependencies: true,
    devServer:{
	port: 8081,   // 端口号
	host:"0.0.0.0",
	proxy: {
	    '^/flask': {
		target: 'http://127.0.0.1:5005',
		secure:false,
		changeOrigin: true,
	    },
	    '^/model': {
		target: 'http://127.0.0.1:5006',
		secure:false,
		changeOrigin: true,
	    }
	}
    }
})


