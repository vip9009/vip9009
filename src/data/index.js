import general from './site/general.json'
import categories from './site/categories.json'
import footer from './site/footer.json'
import contacts from './site/contacts.json'
import infoPages from './site/info-pages.json'

// Every JSON file in ./sections is picked up automatically, so the local
// admin tool can add new categories/sections without editing code.
const sectionModules = import.meta.glob('./sections/*.json', { eager: true })

function normalizeModule(mod) {
  return mod?.default ?? mod
}

export const sections = Object.values(sectionModules)
  .map(normalizeModule)
  .filter(Boolean)
  .sort((a, b) => (a.sort ?? 999) - (b.sort ?? 999))

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
