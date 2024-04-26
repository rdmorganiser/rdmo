import isEmpty from 'lodash/isEmpty'
import isUndefined from 'lodash/isUndefined'
import get from 'lodash/get'
import toNumber from 'lodash/toNumber'

const filterElement = (config, filter, filterSites, filterEditors, element) => {
  const strings = get(config, `filter.${filter}.search`, '').trim().split(' '),
        uriPrefix = get(config, `filter.${filter}.uri_prefix`, ''),
        site = get(config, 'filter.sites', ''),
        editor = get(config, 'filter.editors', '')
  return (
    strings.some(search => filterSearch(search, element)) &&
    filterUriPrefix(uriPrefix, element) &&
    (!filterSites || filterSite(site, element)) &&
    (!filterEditors || filterEditor(editor, element))
  )
}

const filterSearch = (search, element) => {
  return (
    isEmpty(search) ||
    element.uri.includes(search) ||
    (!isUndefined(element.title) && element.title.toLowerCase().includes(search.toLowerCase())) ||
    (!isUndefined(element.text) &&  element.text.toLowerCase().includes(search.toLowerCase()))
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

export { filterElement, getUriPrefixes, getExportParams, filterUriPrefix, filterSearch }
