const TONES = {
  cyan: { background: '#16c8d6', color: '#ffffff' },
  lime: { background: '#a8f000', color: '#1a2b00' },
  green: { background: '#14c98e', color: '#063b2a' },
  purple: { background: '#7500c0', color: '#ffffff' },
  blue: { background: '#3a37ff', color: '#ffffff' },
  coral: { background: '#ff5a5a', color: '#ffffff' },
  black: { background: '#111111', color: '#ffffff' },
  gray: { background: '#9a9a9a', color: '#ffffff' },
  pink: { background: '#e6007e', color: '#ffffff' }
}

// 活动角标：右上角粉色标签。其余商品标签统一放到图片左下角。
const PROMO_PATTERN = /上新|盒|赠|增|买|活动|折扣|推荐/

const FEATURE_TONES = {
  '自定义': 'cyan',
  '自定义口感': 'cyan',
  '模式切换': 'cyan',
  '凉度调节': 'cyan',
  '呼吸灯': 'lime',
  'nic1-2%': 'lime',
  '免充电': 'green',
  '油芯分离': 'green',
  '强击喉': 'black',
  '极致顺滑': 'black',
  '烟杆': 'gray',
  '适配悦刻弹': 'gray',
  '棉芯': 'gray',
  'korea': 'purple',
  'mini game': 'blue',
  'smart vape': 'purple',
  '口味切换': 'coral'
}

function normalize(value) {
  return String(value || '').trim().toLowerCase()
}

export function isPromoTag(label) {
  const value = String(label || '').trim()
  if (!value) return false
  return value.toUpperCase() === 'HOT' || PROMO_PATTERN.test(value)
}

export function isFeatureTag(label) {
  const value = String(label || '').trim()
  return Boolean(value) && !isPromoTag(value)
}

export function featureTagStyle(label) {
  const tone = FEATURE_TONES[normalize(label)] || 'gray'
  return TONES[tone] || TONES.gray
}
