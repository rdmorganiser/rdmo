import { baseUrl } from 'rdmo/core/assets/js/utils/meta'
import { projectId } from '../utils/meta'
import { isUndefined } from 'lodash'

export const parseLocation = () => {
  let pathname = window.location.pathname

  if (pathname.length > 1) {
    pathname = pathname.replace(/\/+$/, '')
  }

  const patterns = [
    /\/projects\/\d+\/(?<page>[a-z-]+)\/(?<pageId>\d+)\/(?<action>[a-z-]+)\/(?<actionId>\d+)[/]*$/,
    /\/projects\/\d+\/(?<page>[a-z-]+)\/(?<pageId>\d+)\/(?<action>[a-z-]+)[/]*$/,
    /\/projects\/\d+\/(?<page>[a-z-]+)\/(?<pageId>\d+)[/]*$/,
    /\/projects\/\d+\/(?<page>[a-z-]+)\/(?<action>[a-z-]+)\/(?<actionId>\d+)[/]*$/,
    /\/projects\/\d+\/(?<page>[a-z-]+)\/(?<action>[a-z-]+)[/]*$/,
    /\/projects\/\d+\/(?<page>[a-z-]+)[/]*$/
  ]

  for (const pattern of patterns) {
    const match = pathname.match(pattern)
    if (match) return match.groups
  }

  return {
    page: ''
  }
}

export const updateLocation = ({ page, pageId, action, actionId }) => {
  const pathname = buildPath({ page, pageId, action, actionId })
  if (pathname != window.location.pathname) {
    history.pushState(null, null, pathname)
  }
}

export const buildPath = ({ page, pageId, action, actionId }) => {
  const segments = [baseUrl, 'projects', projectId]

  if (!isUndefined(page)) {
    segments.push(page)

    if (!isUndefined(pageId)) segments.push(pageId)
    if (!isUndefined(action)) segments.push(action)
    if (!isUndefined(actionId)) segments.push(actionId)
  }

  return segments.join('/') + '/'
}
