import { filterUriPrefix, filterSearch} from './filter'

function filterElementsByChanged(elements, selectFilterChanged) {
  if (!selectFilterChanged) return elements
  return elements.filter((element) => (element.changed || element.created))
}

function filterElementsByUri(elements, searchString) {
  if (!searchString) return elements
  return elements.filter((element) => filterSearch(searchString, element))
}

function filterElementsByUriPrefix(elements, searchUriPrefix) {
  if (!searchUriPrefix) return elements
  return elements.filter((element) => filterUriPrefix(searchUriPrefix, element))
}

function filterImportElements(elements, selectFilterChanged, selectedUriPrefix, searchString) {
  let filteredElements = elements
  filteredElements = filterElementsByChanged(filteredElements, selectFilterChanged)
  filteredElements = filterElementsByUriPrefix(filteredElements, selectedUriPrefix)
  filteredElements = filterElementsByUri(filteredElements, searchString)
  return filteredElements
}

export default filterImportElements
