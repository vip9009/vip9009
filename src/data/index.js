import hot from './sections/hot.json'
import disposables from './sections/disposables.json'
import jimu from './sections/jimu.json'
import pods from './sections/pods.json'
import general from './site/general.json'
import categories from './site/categories.json'
import footer from './site/footer.json'
import contacts from './site/contacts.json'
import infoPages from './site/info-pages.json'

/**
 * 数据按“商品分区 / 站点配置”拆分，方便单独维护。
 * 仍然是构建期静态数据，不会额外产生网络请求。
 */
export const sections = [hot, disposables, jimu, pods]

export const productsData = {
  sections
}

export const site = {
  ...general,
  categories,
  footerWidgets: footer.widgets,
  contacts,
  infoPages
}
