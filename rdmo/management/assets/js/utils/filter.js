import isEmpty from 'lodash/isEmpty';
import isUndefined from 'lodash/isUndefined';
import get from 'lodash/get';
import isNil from 'lodash/isNil';

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

const filterElements = (filterConfig, elements) => {
  if (isUndefined(elements)) {
    return []
  } else {
    return elements.reduce((filteredElements, element) => {
      if (get(filterConfig, 'uri', '').trim().split(' ').some(
        uri => filterUri(uri, element)
      ) && filterUriPrefix(get(filterConfig, 'uriPrefix', ''), element)) {
        filteredElements.push(element)
      }

      return filteredElements
    }, [])
  }
}

const filterElement = (filter, element) => {
  if (isNil(filter)) {
    return true
  } else {
    return (get(filter, 'uri', '').trim().split(' ').some(
      uri => filterUri(uri, element)
    ) && filterUriPrefix(get(filter, 'uriPrefix', ''), element))
  }
}

const getUriPrefixes = (elements) => {
  return elements.reduce((acc, cur) => {
    if (!acc.includes(cur.uri_prefix)) {
      acc.push(cur.uri_prefix)
    }
    return acc
  }, [])
}

export { filterElements, filterElement, getUriPrefixes }
