import isNil from 'lodash/isNil'

import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

import { elementTypes } from '../constants/elements'

const parseLocation = () => {
  const pathname = window.location.pathname

  const regex = /\/management\/(?<elementType>[a-z]+)[/]*((?<elementId>\d+)[/]*)?((?<elementAction>[a-z]+)[/]*)?$/
  const match = pathname.match(regex)

  if (match && Object.values(elementTypes).includes(match.groups.elementType)) {
    return match.groups
  } else {
    // if the regex did not match, load the catalogs
    return { elementType: 'catalogs' }
  }
}

const updateLocation = (elementType, elementId, elementAction) => {
  const pathname = buildPath(elementType, elementId, elementAction)
  if (pathname != window.location.pathname) {
    history.pushState(null, null, pathname)
  }
}

const buildPath = (...args) => {
  return generatePath(`${baseUrl}/management/`, ...args)
}

const buildApiPath = (...args) => {
  return generatePath(`${baseUrl}/api/v1/`, ...args)
}

const generatePath = (basePath, ...args) => {
  let path = basePath

  args.forEach(arg => {
    if (!isNil(arg)) {
      path += arg + '/'
    }
  })

  return path
}

export { parseLocation, updateLocation, buildPath, buildApiPath }
