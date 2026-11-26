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
