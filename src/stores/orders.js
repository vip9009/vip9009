const STORAGE_KEY = 'paopao-orders-v1'

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

function save(orders) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(orders))
  } catch {
    /* ignore quota errors */
  }
}

export function createOrder(order) {
  const orders = load()
  const now = new Date()
  const stamp = [
    now.getFullYear(),
    String(now.getMonth() + 1).padStart(2, '0'),
    String(now.getDate()).padStart(2, '0')
  ].join('')
  const random = String(Math.floor(Math.random() * 9000) + 1000)
  const id = `PP${stamp}${random}`
  const record = {
    id,
    status: '待付款',
    createdAt: now.toISOString(),
    ...order
  }
  orders.unshift(record)
  save(orders.slice(0, 50))
  return record
}

export function findOrder(id) {
  const value = String(id || '').trim().toUpperCase()
  if (!value) return null
  return load().find((order) => order.id.toUpperCase() === value) || null
}

export function listOrders() {
  return load()
}
