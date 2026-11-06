import { useDispatch, useSelector } from 'react-redux'
import { get } from 'lodash'

import { deleteConfig, updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { isTruthy } from 'rdmo/core/assets/js/utils/config'

export const useQuestionHelp = (question) => {
  const dispatch = useDispatch()

  const configPath = `display.help.question.${question.id}`

  const showHelp = useSelector((state) => isTruthy(get(state.config, configPath)))
  const toggleHelp = () => dispatch(showHelp ? deleteConfig(configPath) : updateConfig(configPath, true))

  return [showHelp, toggleHelp]
}
