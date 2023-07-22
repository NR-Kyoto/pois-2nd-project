import path from "path";
import {defineConfig} from "vite";
import {createVuePlugin} from "vite-plugin-vue2";
import Components from 'unplugin-vue-components/vite'
import {VuetifyResolver} from "unplugin-vue-components/resolvers";

const HOST = "0.0.0.0"
const REPLACEMENT = `${path.resolve(__dirname, './src')}/`


export default () => {
    return defineConfig({
        base: "./",
        server: {
            host: HOST,
        },
        logLevel: "info",
        optimizeDeps: {
            //检测需要预构建的依赖项
            entries: [],
            //默认情况下，不在 node_modules 中的，链接的包不会预构建
            include: ['axios'],
            exclude:['your-package-name'] //排除在优化之外
        },
        resolve: {
            extensions: ['.vue', '.mjs', '.js', '.ts', '.jsx', '.tsx', '.json'],
            alias: [
                {
                    find: '@/',
                    replacement: REPLACEMENT,
                },
                {
                    find: 'src/',
                    replacement: REPLACEMENT,
                },
            ],
        },
        plugins: [
            createVuePlugin(),
            Components({
                resolvers: [
                    VuetifyResolver(),
                ],
            })
        ],
        css: {
            preprocessorOptions: {
                sass: {
                    additionalData: "\n@import '@/scss/variables.scss'\n",
                },
            },
        },
    })
}
