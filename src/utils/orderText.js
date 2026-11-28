import { formatPrice } from '@/utils'

export function buildOrderText({ items, subtotal, shippingFee, total, address = '' }) {
  const lines = []
  lines.push('【商品订单信息】')
  lines.push('')
  if (address.trim()) {
    lines.push('收货信息：')
    lines.push(address.trim())
    lines.push('')
  }
  lines.push('商品清单：')
  items.forEach((item, index) => {
    lines.push(`${index + 1}. ${item.title}`)
    if (item.option) lines.push(`   口味/规格：${item.option}`)
    lines.push(`   单价：${formatPrice(item.price)} × ${item.qty}`)
    lines.push(`   小计：${formatPrice(Number(item.price) * item.qty)}`)
  })
  lines.push('')
  lines.push(`商品小计：${formatPrice(subtotal)}`)
  lines.push(`运费：${shippingFee ? formatPrice(shippingFee) : '免运费'}`)
  lines.push(`合计：${formatPrice(total)}`)
  lines.push('')
  lines.push('付款方式：联系客服确认（微信 / QQ）')
  lines.push('客服 QQ：1220820788')
  lines.push('请把这段订单信息发给客服，确认商品、运费和付款方式。')
  return lines.join('\n')
}

export async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch {
    /* fall back below */
  }
  try {
    const area = document.createElement('textarea')
    area.value = text
    area.setAttribute('readonly', '')
    area.style.position = 'fixed'
    area.style.top = '-9999px'
    area.style.opacity = '0'
    document.body.appendChild(area)
    area.select()
    area.setSelectionRange(0, area.value.length)
    const ok = document.execCommand('copy')
    area.remove()
    return ok
  } catch {
    return false
  }
}
