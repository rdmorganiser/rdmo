import isEmpty from 'lodash/isEmpty'
import isUndefined from 'lodash/isUndefined'
import get from 'lodash/get'
import isNil from 'lodash/isNil'
import toNumber from 'lodash/toNumber'

const filterString = (string, element) => {
  return (
    isEmpty(string) ||
    element.uri.includes(string) ||
    (!isUndefined(element.title) && element.title.includes(string)) ||
    (!isUndefined(element.text) && element.text.includes(string))
  )
}

const filterUriPrefix = (uriPrefix, element) => {
  return isEmpty(uriPrefix) || element.uri.startsWith(uriPrefix)
}

const filterSite = (site, element) => {
  return isEmpty(site) || element.sites.includes(toNumber(site))
}

const filterElement = (filter, element) => {
  if (isNil(filter)) {
    return true
  } else {
    const strings = get(filter, 'string', '').trim().split(' '),
          uriPrefix = get(filter, 'uriPrefix', ''),
          site = get(filter, 'site', '')
    return (
      strings.some(string => filterString(string, element)) &&
      filterUriPrefix(uriPrefix, element) &&
      filterSite(site, element)
    )
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

export { filterElement, getUriPrefixes }
