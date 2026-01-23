import { baseUrl } from 'rdmo/core/assets/js/utils/meta'
import { projectId } from '../utils/meta'
import { isNil } from 'lodash'

export const parseLocation = () => {
  let pathname = window.location.pathname
  let location = {
    'panel': 'dashboard'
  }

  if (pathname.length > 1) {
    pathname = pathname.replace(/\/+$/, '')
  }

  const patterns = [
    /\/projects\/\d+\/(?<panel>(snapshots))\/(?<snapshotId>\d+)\/views\/(?<viewId>\d+)[/]*$/,
    /\/projects\/\d+\/(?<panel>(snapshots))\/(?<snapshotId>\d+)\/(?<detail>[a-z-]+)[/]*$/,
    /\/projects\/\d+\/(?<panel>[a-z-]+)\/views\/(?<viewId>\d+)[/]*$/,
    /\/projects\/\d+\/(?<panel>[a-z-]+)\/(?<detail>[a-z-]+)[/]*$/,
    /\/projects\/\d+\/(?<panel>[a-z-]+)[/]*$/
  ]

  for (const pattern of patterns) {
    const match = pathname.match(pattern)
    if (match) {
      location = match.groups
      break
    }
  }

  return location
}

export const updateLocation = (location) => {
  const pathname = buildPath(location)
  if (pathname != window.location.pathname) {
    history.pushState(null, null, pathname)
  }
}

export const buildPath = ({ panel, snapshotId, viewId, detail }) => {
  const segments = [baseUrl, 'projects', projectId]

  if (!isNil(panel) && panel != 'dashboard') {
    segments.push(panel)
  }
  if (!isNil(snapshotId)) segments.push(snapshotId)
  if (!isNil(viewId)) segments.push('views', viewId)
  if (!isNil(detail)) segments.push(detail)

  return segments.join('/') + '/'
}
