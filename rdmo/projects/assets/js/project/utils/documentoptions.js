import { get } from 'lodash'

import { isTruthy } from 'rdmo/core/assets/js/utils/config'

export const getDocumentParameters = (config) => {
  const include_help = isTruthy(get(config, 'document.includeHelp')) ? 'true' : 'false'
  return {'include_help': include_help}
}
