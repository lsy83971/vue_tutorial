const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
    transpileDependencies: true,
    devServer:{
	proxy: {
	    '^/flask': {
		target: 'http://localhost:5005',  //要解决跨域的接口的域名
		secure:false,           //如果是https接口，需要配置这个参数
		changeOrigin: true,  // 如果接口跨域，需要进行这个参数配置
	    }
	}
    }
})

