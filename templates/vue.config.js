/*
 * @Author: dnimo kuochingcha@gmail.com
 * @Date: 2022-02-11 19:34:46
 * @LastEditors: dnimo kuochingcha@gmail.com
 * @LastEditTime: 2023-06-27 17:38:23
 * @FilePath: /pois-2nd-project/giraffe/vue.config.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
module.exports = {
  "transpileDependencies": [
    "vuetify"
  ]
}
config.module
  .rule('svg')
  .exclude.add(resolve('./src/icons'))
  .end()
config.module
  .rule('icons')
  .test(/\.svg$/)
  .include.add(resolve('./src/icons'))
  .end()
  .use('svg-sprite-loader')
  .loader('svg-sprite-loader')
  .options({
  symbolId: 'icon-[name]'
  })
  .end()