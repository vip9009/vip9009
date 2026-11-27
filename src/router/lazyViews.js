const lazyViews = {
  category: () => import('@/views/CategoryView.vue'),
  product: () => import('@/views/ProductView.vue'),
  search: () => import('@/views/SearchView.vue'),
  contact: () => import('@/views/ContactView.vue'),
  info: () => import('@/views/InfoView.vue'),
  sitemap: () => import('@/views/SitemapView.vue'),
  cart: () => import('@/views/CartView.vue'),
  checkout: () => import('@/views/CheckoutView.vue'),
  activity: () => import('@/views/ActivityView.vue'),
  notFound: () => import('@/views/NotFoundView.vue')
}

const preloaded = new Set()

export function preloadView(name) {
  const loader = lazyViews[name]
  if (!loader || preloaded.has(name)) return
  preloaded.add(name)
  loader().catch(() => {
    // A failed prefetch is harmless: the router will load it again on navigation.
    preloaded.delete(name)
  })
}

/**
 * After the homepage is interactive, quietly warm up the route chunks.
 * Chunks are a few KB each, so this removes the blank delay on first navigation.
 */
export function preloadPrimaryViews() {
  ;['category', 'product', 'contact', 'search', 'info', 'cart', 'checkout', 'activity'].forEach(preloadView)
}

export default lazyViews
