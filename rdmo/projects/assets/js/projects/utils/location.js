import { isNil } from 'lodash'

import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

export const parseLocation = () => {
  const match = window.location.pathname.match(/\/projects\/import\/(?<importKey>[\w-]+)[/]*$/)
  return { importKey: match ? match.groups.importKey : null }
}

export const buildPath = ({ importKey }) => {
  return isNil(importKey) ? `${baseUrl}/projects/` : `${baseUrl}/projects/import/${importKey}/`
}

export const updateLocation = (location) => {
  const pathname = buildPath(location)
  if (pathname != window.location.pathname) {
    history.pushState(null, null, pathname)
  }
}
