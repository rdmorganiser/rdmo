import _ from 'lodash'

const parseLocation = (basePath, pathname) => {
  const path = pathname.replace(basePath, '')
  const tokens = _.trim(path, '/').split('/')

  const config = {
    basePath: basePath
  }
  if (tokens.length >= 1) {
    config.resourceType = tokens[0]
  }
  if (tokens.length >= 2) {
    config.resourceId = tokens[1]
  }

  return config
}

const updateLocation = ({ basePath, resourceType, resourceId }) => {
  let pathname = basePath
  if (!_.isUndefined(resourceType)) {
    pathname += resourceType + '/'
  }
  if (!_.isUndefined(resourceId)) {
    pathname += resourceId + '/'
  }
  history.pushState(null, null, pathname);
}

export { parseLocation, updateLocation }
