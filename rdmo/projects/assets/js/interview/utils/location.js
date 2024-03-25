import baseUrl from 'rdmo/core/assets/js/utils/baseUrl'
import projectId from '../utils/projectId'

const parseLocation = () => {
  const pathname = window.location.pathname

  const m1 = pathname.match(/\/interview\/(?<pageId>\d+)[/]*$/)
  if (m1) {
    return m1.groups
  }

  return {}
}

const updateLocation = (pageId) => {
  const pathname = buildPath(pageId)
  if (pathname != window.location.pathname) {
    history.pushState(null, null, pathname)
  }
}

const buildPath = (pageId) => {
  return `${baseUrl}/projects/${projectId}/interview/${pageId}/`
}

export { parseLocation, updateLocation, buildPath }
