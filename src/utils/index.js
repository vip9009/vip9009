const BASE = import.meta.env.BASE_URL || './'

export function asset(path) {
  if (!path) return ''
  if (/^(https?:)?\/\//.test(path) || path.startsWith('data:')) return path
  return BASE.replace(/\/$/, '') + '/' + path.replace(/^\//, '')
}

export function decodeEntities(value = '') {
  return String(value)
    .replace(/&#(\d+);/g, (_, code) => String.fromCharCode(Number(code)))
    .replace(/&#x([0-9a-f]+);/gi, (_, code) => String.fromCharCode(parseInt(code, 16)))
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&hellip;/g, '…')
    .replace(/&nbsp;/g, ' ')
}

export function productRoute(sectionId, index) {
  return `/product/${sectionId}/${index}`
}

export function formatPrice(value) {
  const number = Number(value)
  if (!Number.isFinite(number)) return `¥${value ?? ''}`
  return `¥${number % 1 === 0 ? number.toFixed(0) : number.toFixed(2)}`
}

export function detectBrand(product) {
  if (product?.brand) return product.brand
  const text = String(product?.title || '').toLowerCase()
  const brands = [
    ['RELX', ['悦刻', 'relx']],
    ['SnowPlus', ['雪加', 'snowplus']],
    ['ZGAR', ['冰熊', 'zgar']],
    ['YOOZ', ['柚子', 'yooz']],
    ['ELFBAR', ['elfbar', '爱奇迹']],
    ['LAMI', ['徕米', 'lami']],
    ['BUBBLEMON', ['bubblemon']],
    ['SONG', ['song', '崧']],
    ['MOTI', ['moti']],
    ['VOZOL', ['vozol']],
    ['BEKE', ['beke', '贝壳']],
    ['DRAGON BAR', ['dragon bar', '阿童木']]
  ]
  const hit = brands.find(([, keys]) => keys.some((key) => text.includes(key)))
  return hit ? hit[0] : ''
}

export function allProducts(sections) {
  return sections.flatMap((section) =>
    section.products.map((product, index) => ({
      ...product,
      sectionId: section.id,
      sectionTitle: section.title,
      index
    }))
  )
}
