import { useMemo } from 'react'
import { filterUriPrefix, filterSearch} from './filter'

const filterChanged = (selectFilterChanged, element) => {
  return element.changed || element.created
}

function filterElementsByChanged(elements, selectFilterChanged) {
  if (!selectFilterChanged) return elements
  return elements.filter((element) => filterChanged(selectFilterChanged, element))
}

function filterElementsByUri(elements, searchString) {
  if (!searchString) return elements
  return elements.filter((element) => filterSearch(searchString, element))
}

function filterElementsByUriPrefix(elements, searchUriPrefix) {
  if (!searchUriPrefix) return elements
  return elements.filter((element) => filterUriPrefix(searchUriPrefix, element))
}

const useFilteredElements = (elements, selectFilterChanged, selectedUriPrefix, searchString) => {
  return useMemo(() => {
    let filteredElements = filterElementsByChanged(elements, selectFilterChanged)
    filteredElements = filterElementsByUriPrefix(filteredElements, selectedUriPrefix)
    filteredElements = filterElementsByUri(filteredElements, searchString)
    return filteredElements
  }, [elements, selectFilterChanged, selectedUriPrefix, searchString])
}

export default useFilteredElements
