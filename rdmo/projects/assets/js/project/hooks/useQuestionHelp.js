import { useDispatch, useSelector } from 'react-redux'
import { get } from 'lodash'

import { updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'

export const useQuestionHelp = (question) => {
  const dispatch = useDispatch()

  const config = useSelector((state) => state.config)
  const configPath = `display.help.question.${question.id}`

  const showHelp = isTruthy(get(config, configPath, ''))
  const toggleHelp = () => dispatch(updateConfig(configPath, !showHelp))

  return [showHelp, toggleHelp]
}
