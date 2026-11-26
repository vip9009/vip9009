import { reactive, watch } from 'vue'

const STORAGE_KEY = 'paopao-wishlist-v1'

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

const state = reactive({ items: load() })

watch(
  () => state.items,
  (items) => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(items))
    } catch {
      /* ignore */
    }
  },
  { deep: true }
)

function keyOf(sectionId, index) {
  return `${sectionId}:${index}`
}

export function useWishlist() {
  function has(sectionId, index) {
    return state.items.some((item) => item.key === keyOf(sectionId, index))
  }

  function toggle(item) {
    const key = keyOf(item.sectionId, item.index)
    if (state.items.some((entry) => entry.key === key)) {
      state.items = state.items.filter((entry) => entry.key !== key)
    } else {
      state.items.push({ key, ...item })
    }
  }

  return { items: state.items, has, toggle }
}
