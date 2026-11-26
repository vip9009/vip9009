import { productsData, site } from '@/data'
import { asset } from './index'
import { filterByBrand } from './categories'

const prefetched = new Set()

function canPrefetchImages() {
  if (typeof window === 'undefined') return false
  const connection = navigator.connection
  if (connection?.saveData) return false
  return !/^(slow-2g|2g)$/.test(connection?.effectiveType || '')
}

function prefetchImage(path) {
  if (!path || prefetched.has(path)) return
  prefetched.add(path)
  const img = new Image()
  img.decoding = 'async'
  img.src = asset(path)
}

export function prefetchCategoryImages(categoryId, brand = '', sub = '') {
  if (!canPrefetchImages()) return
  const category = site.categories[categoryId]
  const owner = category?.parent ? site.categories[category.parent] : category
  if (!owner?.section) return
  const section = productsData.sections.find((item) => item.id === owner.section)
  if (!section) return

  let products = section.products
  if (sub) {
    products = products.filter((product) => product.subcategory === sub)
  } else if (category?.parent) {
    products = products.filter((product) => product.subcategory === categoryId)
  } else if (brand) {
    products = filterByBrand(products, brand)
  }

  products.slice(0, 4).forEach((product) => prefetchImage(product.localImage))
}

export function prefetchProductImage(sectionId, index) {
  if (!canPrefetchImages()) return
  const section = productsData.sections.find((item) => item.id === sectionId)
  const product = section?.products[Number(index)]
  if (product) prefetchImage(product.localImage)
}

export function prefetchPathImages(path) {
  const [pathname, query = ''] = String(path).split('?')
  const params = new URLSearchParams(query)

  if (pathname.startsWith('/category/')) {
    prefetchCategoryImages(
      pathname.split('/')[2],
      params.get('brand') || '',
      params.get('sub') || ''
    )
  } else if (pathname.startsWith('/product/')) {
    const parts = pathname.split('/')
    prefetchProductImage(parts[2], parts[3])
  }
}
