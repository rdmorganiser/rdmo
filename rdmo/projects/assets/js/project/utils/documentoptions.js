import { get } from 'lodash'

import { isTruthy } from 'rdmo/core/assets/js/utils/config'

export const getQuestionsParameters = (config) => {
  const include_help = isTruthy(get(config, 'document.questions.includeHelp')) ? 'true' : 'false'
  const include_answers = isTruthy(get(config, 'document.questions.includeAnswers')) ? 'true' : 'false'

  return {'include_help': include_help, 'include_answers': include_answers}
}

export const getAnswersParameters = (config) => {
  const include_help = isTruthy(get(config, 'document.answers.includeHelp')) ? 'true' : 'false'

  return {'include_help': include_help}
}
