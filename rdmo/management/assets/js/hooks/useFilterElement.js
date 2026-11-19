import { useConfig } from 'rdmo/core/assets/js/hooks'

import { filterElement } from '../utils/filter'

const useFilterElement = (filter, filterSites, filterEditors, element) => {
  const [search] = useConfig(`filter.${filter}.search`, '')
  const [uriPrefix] = useConfig(`filter.${filter}.uri_prefix`, '')
  const [site] = useConfig('filter.sites', '')
  const [editor] = useConfig('filter.editors', '')

  return filterElement({ search, uriPrefix, site, editor }, filterSites, filterEditors, element)
}

export default useFilterElement
