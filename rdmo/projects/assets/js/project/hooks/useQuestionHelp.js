import { useDispatch } from 'react-redux'

import { deleteConfig, updateConfig } from 'rdmo/core/assets/js/actions/configActions'
import { useConfig } from 'rdmo/core/assets/js/hooks'

export const useQuestionHelp = (question) => {
  const dispatch = useDispatch()

  const configPath = `display.help.question.${question.id}`

  const [showHelp] = useConfig(configPath, false)
  const toggleHelp = () => dispatch(showHelp ? deleteConfig(configPath) : updateConfig(configPath, true))

  return [showHelp, toggleHelp]
}
