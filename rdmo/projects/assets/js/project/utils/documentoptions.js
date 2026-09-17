import { get } from 'lodash'

import { isTruthy } from 'rdmo/core/assets/js/utils/config'

export const paramsFromConfig = (config) => {
  const include_help = isTruthy(get(config, 'document.includeHelp')) ? 'true' : 'false'
  const hide_answers = isTruthy(get(config, 'document.hideAnswers')) ? 'true' : 'false'
  return {'include_help': include_help, 'hide_answers': hide_answers}
}
