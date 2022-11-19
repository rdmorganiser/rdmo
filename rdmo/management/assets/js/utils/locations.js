import _ from 'lodash'

const parseLocation = (basePath, pathname) => {
  const path = pathname.replace(basePath, '')
  const tokens = _.trim(path, '/').split('/')

  const config = {}
  if (tokens.length >= 1) {
    config.resource = tokens[0]
  }
  if (tokens.length >= 2) {
    config.id = tokens[1]
  }

  return config
}

const updateLocation = (basePath, { resource, id }) => {
  let pathname = basePath
  if (!_.isUndefined(resource)) {
    pathname += resource + '/'
  }
  if (!_.isUndefined(id)) {
    pathname += id + '/'
  }
  history.pushState(null, null, pathname);
}

export { parseLocation, updateLocation }
