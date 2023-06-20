import trim from 'lodash/trim'
import isUndefined from 'lodash/isUndefined'
import isNil from 'lodash/isNil'

import { elementTypes } from '../constants/elements'

const parseLocation = (basePath, pathname) => {
  const path = pathname.replace(basePath, '')
  const tokens = trim(path, '/').split('/')

  let elementType = null,
      elementId = null,
      elementAction = null

  if (!isUndefined(tokens[0]) && Object.values(elementTypes).includes(tokens[0])) {
    elementType = tokens[0]

    if (!isUndefined(tokens[1])) {
      if (/^\d+$/.test(tokens[1])) {
        elementId = tokens[1]

        if (!isUndefined(tokens[2]) && /^[a-z]+$/.test(tokens[2])) {
          elementAction = tokens[2]
        }

      } else if (/^[a-z]+$/.test(tokens[1])) {
        elementAction = tokens[1]
      }
    }
  }

  return { elementType , elementId, elementAction }
}

const updateLocation = (basePath, elementType, elementId, elementAction) => {
  const pathname = buildPath(basePath, elementType, elementId, elementAction)
  if (pathname != window.location.pathname) {
    history.pushState(null, null, pathname)
  }
}

const buildPath = (basePath, ...args) => {
  let path = basePath

  args.forEach(arg => {
    if (!isNil(arg)) {
      path += arg + '/'
    }
  })

  return path
}

export { parseLocation, updateLocation, buildPath }
