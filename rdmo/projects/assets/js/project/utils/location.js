import { baseUrl } from 'rdmo/core/assets/js/utils/meta'
import { projectId } from '../utils/meta'
import { isEmpty } from 'lodash'

export const parseLocation = () => {
  const pathname = window.location.pathname

  const m1 = pathname.match(/\/projects\/\d+\/(?<page>[a-z-]+)\/(?<itemId>\d+)\/(?<itemAction>[a-z-]+)[/]*$/)
  if (m1) {
    return m1.groups
  }

  const m2 = pathname.match(/\/projects\/\d+\/(?<page>[a-z-]+)\/(?<itemId>\d+)[/]*$/)
  if (m2) {
    return m2.groups
  }

  const m3 = pathname.match(/\/projects\/\d+\/(?<page>[a-z-]+)[/]*$/)
  if (m3) {
    return m3.groups
  }

  return {
    page: ''
  }
}

export const updateLocation = (page, itemId, itemAction) => {
  const pathname = buildPath(page, itemId, itemAction)
  if (pathname != window.location.pathname) {
    history.pushState(null, null, pathname)
  }
}

export const buildPath = (page, itemId, itemAction) => {
  let path = `${baseUrl}/projects/${projectId}/`

  if (!isEmpty(page)) {
    path += page + '/'

    if (!isEmpty(itemId)) {
      path += itemId + '/'

      if (!isEmpty(itemAction)) {
        path += itemAction + '/'
      }
    }
  }

  return path
}
