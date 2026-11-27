import { computed, reactive, watch } from 'vue'

const STORAGE_KEY = 'paopao-cart-v1'

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

const state = reactive({
  items: load(),
})

watch(
  () => state.items,
  (items) => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(items))
    } catch {
      /* ignore quota errors */
    }
  },
  { deep: true },
)

function keyOf(sectionId, index, option) {
  return `${sectionId}:${index}:${option || ''}`
}

export function useCart() {
  const count = computed(() => state.items.reduce((sum, item) => sum + item.qty, 0))
  const subtotal = computed(() =>
    state.items.reduce((sum, item) => sum + Number(item.price) * item.qty, 0),
  )

  function add({ sectionId, index, title, price, image, option = '', qty = 1 }) {
    const key = keyOf(sectionId, index, option)
    const existing = state.items.find((item) => item.key === key)
    if (existing) {
      existing.qty += qty
      return
    }
    state.items.push({
      key,
      sectionId,
      index,
      title,
      price: Number(price),
      image,
      option,
      qty,
    })
  }

  function updateQty(key, qty) {
    const item = state.items.find((entry) => entry.key === key)
    if (!item) return
    item.qty = Math.max(1, Math.min(99, Number(qty) || 1))
  }

  function remove(key) {
    const idx = state.items.findIndex((item) => item.key === key)
    if (idx > -1) state.items.splice(idx, 1)
  }

  function clear() {
    state.items.splice(0, state.items.length)
  }

  return {
    get items() {
      return state.items
    },
    count,
    subtotal,
    add,
    updateQty,
    remove,
    clear,
  }
}
