import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import lazyViews from './lazyViews'

const router = createRouter({
  // Hash history is the safest choice for GitHub Pages:
  // no 404.html or server rewrites are needed.
  history: createWebHashHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeView, meta: { title: '泡泡哥雾化 – 专业电子烟分类目录，正品可验证' } },
    { path: '/category/:id', name: 'category', component: lazyViews.category },
    { path: '/product/:section/:index', name: 'product', component: lazyViews.product },
    { path: '/search', name: 'search', component: lazyViews.search, meta: { title: '搜索 - 泡泡哥雾化' } },
    { path: '/contact', name: 'contact', component: lazyViews.contact, meta: { title: '联系我们 - 泡泡哥雾化' } },
    { path: '/cart', name: 'cart', component: lazyViews.cart, meta: { title: '购物车 - 泡泡哥雾化' } },
    { path: '/checkout', name: 'checkout', component: lazyViews.checkout, meta: { title: '填写收货信息 - 泡泡哥雾化' } },
    { path: '/info/:slug', name: 'info', component: lazyViews.info },
    { path: '/sitemap', name: 'sitemap', component: lazyViews.sitemap, meta: { title: '网站地图 - 泡泡哥雾化' } },
    { path: '/:pathMatch(.*)*', name: 'not-found', component: lazyViews.notFound, meta: { title: '页面不存在 - 泡泡哥雾化' } }
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0 }
  }
})

router.afterEach((to) => {
  if (to.meta.title) document.title = to.meta.title
})

export default router
