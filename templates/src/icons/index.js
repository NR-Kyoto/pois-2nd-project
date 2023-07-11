/*
 * @Author: dnimo kuochingcha@gmail.com
 * @Date: 2023-06-27 16:49:15
 * @LastEditors: dnimo kuochingcha@gmail.com
 * @LastEditTime: 2023-06-27 16:49:25
 * @FilePath: /giraffe/src/scss/icons/index.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
const req = require.context('./svg', false, /\.svg$/)

const requireAll = requireContext => requireContext.keys().map(requireContext)
requireAll(req)