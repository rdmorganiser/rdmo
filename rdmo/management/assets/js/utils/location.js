import trim from 'lodash/trim'
import isUndefined from 'lodash/isUndefined'
import isNil from 'lodash/isNil'

import { elementTypes } from '../constants/elements'

const parseLocation = (basePath, pathname) => {
  const path = pathname.replace(basePath, '')
  const tokens = trim(path, '/').split('/')

  let elementType = null
  if (!isUndefined(tokens[0]) && elementTypes.includes(tokens[0])) {
    elementType = tokens[0]
  }

  let elementId = null
  if (!isUndefined(tokens[1]) && /^\d+$/.test(tokens[1])) {
    elementId = tokens[1]
  }

  let elementAction = null
  if (!isUndefined(tokens[2]) && /^[a-z]+$/.test(tokens[2])) {
    elementAction = tokens[2]
  }

  return { elementType , elementId, elementAction }
}

const updateLocation = (basePath, elementType, elementId, elementAction) => {
  let pathname = basePath + elementType + '/'

  if (!isNil(elementId)) {
    pathname += elementId + '/'
  }

  if (!isNil(elementAction)) {
    pathname += elementAction + '/'
  }

  if (pathname != window.location.pathname) {
    history.pushState(null, null, pathname);
  }
}

export { parseLocation, updateLocation }
