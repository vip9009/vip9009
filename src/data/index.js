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

function bySort(a, b) {
  return (a[1].sort ?? 999) - (b[1].sort ?? 999)
}

function buildNav() {
  return Object.entries(categories)
    .filter(([, category]) => !category.parent && category.nav !== false)
    .sort(bySort)
    .map(([id, category]) => {
      const children = (category.children || [])
        .map((childId) => [childId, categories[childId]])
        .filter(([, child]) => Boolean(child))
        .sort(bySort)
        .map(([childId, child]) => ({
          label: child.title,
          to: child.to || `/category/${id}?sub=${childId}`
        }))

      return {
        label: category.title,
        to: category.to || `/category/${id}`,
        ...(children.length ? { children } : {})
      }
    })
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
  nav: buildNav(),
  footerWidgets: footer.widgets,
  contacts,
  infoPages
}
