import { baseUrl } from 'rdmo/core/assets/js/utils/meta'
import { projectId } from '../utils/meta'
import { isEmpty } from 'lodash'

export const parseLocation = () => {
  const pathname = window.location.pathname

  const patterns = [
    /\/projects\/\d+\/(?<page>[a-z-]+)\/(?<pageId>\d+)\/(?<action>[a-z-]+)\/(?<actionId>\d+)[/]*$/,
    /\/projects\/\d+\/(?<page>[a-z-]+)\/(?<pageId>\d+)\/(?<action>[a-z-]+)[/]*$/,
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

  if (!isEmpty(page)) {
    segments.push(page)

    if (!isEmpty(pageId)) segments.push(pageId)
    if (!isEmpty(action)) segments.push(action)
    if (!isEmpty(actionId)) segments.push(actionId)
  }

  return segments.join('/') + '/'
}
