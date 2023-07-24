import isEmpty from 'lodash/isEmpty'
import isUndefined from 'lodash/isUndefined'
import get from 'lodash/get'
import isNil from 'lodash/isNil'
import toNumber from 'lodash/toNumber'

const filterSearch = (search, element) => {
  return (
    isEmpty(search) ||
    element.uri.includes(search) ||
    (!isUndefined(element.title) && element.title.includes(search)) ||
    (!isUndefined(element.text) && element.text.includes(search))
  )
}

const filterUriPrefix = (uriPrefix, element) => {
  return isEmpty(uriPrefix) || element.uri.startsWith(uriPrefix)
}

const filterSite = (site, element) => {
  return isEmpty(site) || element.sites.includes(toNumber(site))
}

const filterEditor = (editor, element) => {
  return isEmpty(editor) || element.editors.includes(toNumber(editor))
}

const filterElement = (filter, element) => {
  if (isNil(filter)) {
    return true
  } else {
    const strings = get(filter, 'search', '').trim().split(' '),
          uriPrefix = get(filter, 'uri_prefix', ''),
          site = get(filter, 'sites', ''),
          editor = get(filter, 'editors', '')
    return (
      strings.some(search => filterSearch(search, element)) &&
      filterUriPrefix(uriPrefix, element) &&
      filterSite(site, element) &&
      filterEditor(editor, element)
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

const getExportParams = (filter) => {
  const exportParams = new URLSearchParams()

  if (!isUndefined(filter)) {
    for (const key in filter) {
      const value = filter[key]
      if (!isEmpty(value)) {
        exportParams.append(key, value)
      }
    }
  }

  return exportParams.toString()
}

export { filterElement, getUriPrefixes, getExportParams }
