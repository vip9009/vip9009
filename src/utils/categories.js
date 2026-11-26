export const brandAliases = {
  悦刻: ['悦刻', 'relx'],
  雪加: ['雪加', 'snowplus'],
  冰熊: ['冰熊', 'zgar'],
  柚子: ['柚子', 'yooz']
}

export function filterByBrand(products, brand) {
  const value = String(brand || '').trim()
  if (!value) return products
  const words = (brandAliases[value] || [value]).map((word) => word.toLowerCase())
  return products.filter((product) => {
    const title = product.title.toLowerCase()
    return words.some((word) => title.includes(word))
  })
}
