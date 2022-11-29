import trim from 'lodash/trim';
import isUndefined from 'lodash/isUndefined';

const parseLocation = (basePath, pathname) => {
  const path = pathname.replace(basePath, '')
  const tokens = trim(path, '/').split('/')

  const elementType = tokens.length >= 1 ? tokens[0] : null
  const elementId = tokens.length >= 2 ? tokens[1] : null

  return { elementType , elementId }
}

const updateLocation = (basePath, elementType, elementId) => {
  let pathname = basePath
  if (!isUndefined(elementType)) {
    pathname += elementType + '/'
  }
  if (!isUndefined(elementId)) {
    pathname += elementId + '/'
  }

  if (pathname != window.location.pathname) {
    history.pushState(null, null, pathname);
  }
}

export { parseLocation, updateLocation }
