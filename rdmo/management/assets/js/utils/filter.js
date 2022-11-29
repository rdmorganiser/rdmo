import isEmpty from 'lodash/isEmpty';

const filterUri = (filterUri, element) => {
  if (isEmpty(filterUri) || element.uri.includes(filterUri)) {
    return true
  } else {
    return false
  }
}

const filterUriPrefix = (filterUriPrefix, element) => {
  if (isEmpty(filterUriPrefix) || element.uri.startsWith(filterUriPrefix)) {
    return true
  } else {
    return false
  }
}

const filterElements = (config, elements) => {
  return elements.reduce((filteredElements, element) => {
    if (config.filterUri.trim().split(' ').some(
      uri => filterUri(uri, element)
    ) && filterUriPrefix(config.filterUriPrefix, element)) {
      filteredElements.push(element)
    }

    return filteredElements
  }, [])
}

export { filterElements }
