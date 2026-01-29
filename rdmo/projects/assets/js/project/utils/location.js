import { baseUrl } from 'rdmo/core/assets/js/utils/meta'
import { projectId } from '../utils/meta'
import { isNil } from 'lodash'

export const locationKeys = ['area', 'snapshotId', 'viewId', 'detail']

export const parseLocation = () => {
  let pathname = window.location.pathname
  let location = {
    'area': 'dashboard'
  }

  if (pathname.length > 1) {
    pathname = pathname.replace(/\/+$/, '')
  }

  const patterns = [
    /\/projects\/\d+\/(?<area>(snapshots))\/(?<snapshotId>\d+)\/views\/(?<viewId>\d+)[/]*$/,
    /\/projects\/\d+\/(?<area>(snapshots))\/(?<snapshotId>\d+)\/(?<detail>[a-z-]+)[/]*$/,
    /\/projects\/\d+\/(?<area>(snapshots))\/(?<snapshotId>\d+)[/]*$/,
    /\/projects\/\d+\/(?<area>[a-z-]+)\/views\/(?<viewId>\d+)[/]*$/,
    /\/projects\/\d+\/(?<area>[a-z-]+)\/(?<detail>[a-z-]+)[/]*$/,
    /\/projects\/\d+\/(?<area>[a-z-]+)[/]*$/
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

export const buildPath = ({ area, snapshotId, viewId, detail }) => {
  const segments = [baseUrl, 'projects', projectId]

  if (!isNil(area) && area != 'dashboard') {
    segments.push(area)
  }
  if (!isNil(snapshotId)) segments.push(snapshotId)
  if (!isNil(viewId)) segments.push('views', viewId)
  if (!isNil(detail)) segments.push(detail)

  return segments.join('/') + '/'
}
