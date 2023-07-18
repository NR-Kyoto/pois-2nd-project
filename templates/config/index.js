export default {
  EVENT_OPEN: 'botui-open',
  EVENT_CLOSE: 'botui-close',
  EVENT_TOGGLE: 'botui-toggle',
  proxyTable: {
    // 设置代理请求
    '/api': {
     target: 'http://127.0.0.1:5000/api/', // 接口地址
     changeOrigin: true, //是否跨域
     pathRewrite: {
       '^/api': '/', //本身的接口地址没有"/api"这种通用前缀,所以要rewrite,如果本身有则去掉.
     },
   },
   },
}