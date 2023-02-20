import trim from 'lodash/trim'
import isUndefined from 'lodash/isUndefined'
import isNil from 'lodash/isNil'

import { elementTypes } from '../constants/elements'

const parseLocation = (basePath, pathname) => {
  const path = pathname.replace(basePath, '')
  const tokens = trim(path, '/').split('/')

  let elementType = null, elementId = null
  if (!isUndefined(tokens[0]) && elementTypes.includes(tokens[0])) {
    elementType = tokens[0]
  }
  if (!isUndefined(tokens[1]) && /^\d+$/.test(tokens[1])) {
    elementId = tokens[1]
  }

  return { elementType , elementId }
}

const updateLocation = (basePath, elementType, elementId) => {
  let pathname = basePath + elementType + '/'

  if (!isNil(elementId)) {
    pathname += elementId + '/'
  }

  if (pathname != window.location.pathname) {
    history.pushState(null, null, pathname);
  }
}

export { parseLocation, updateLocation }
