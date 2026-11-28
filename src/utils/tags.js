const LEFT_TAG_COLORS = [
  { background: '#111111', color: '#ffffff' },
  { background: '#ff0077', color: '#ffffff' },
  { background: '#16c8d6', color: '#ffffff' },
  { background: '#14c98e', color: '#063b2a' },
  { background: '#7500c0', color: '#ffffff' },
  { background: '#3a37ff', color: '#ffffff' },
  { background: '#ff5a5a', color: '#ffffff' },
  { background: '#a8f000', color: '#1a2b00' },
  { background: '#9a9a9a', color: '#ffffff' },
  { background: '#ff7c7c', color: '#ffffff' },
  { background: '#00a3ff', color: '#ffffff' },
  { background: '#ff8a00', color: '#1f1200' },
]

function hashLabel(value) {
  let hash = 0
  for (let index = 0; index < value.length; index += 1) {
    hash = (hash * 31 + value.charCodeAt(index)) | 0
  }
  return Math.abs(hash)
}

// 左侧标签没有固定色板，按标签名生成稳定的随机颜色
export function leftTagStyle(label) {
  return LEFT_TAG_COLORS[hashLabel(String(label || '')) % LEFT_TAG_COLORS.length]
}
