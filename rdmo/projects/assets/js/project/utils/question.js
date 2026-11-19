import { isEmpty } from 'lodash'

import { getSetId } from './set'

export const getQuestionTextId = (question, set) => (
  question.text && `question-text-${getSetId(set)}-${question.id}`
)

export const getQuestionHelpId = (question, set) => (
  `question-help-${getSetId(set)}-${question.id}`
)

export const getQuestionCheckboxId = (question, set, option) => (
  `checkbox-${getSetId(set)}-${question.id}-${option.id}`
)

export const hasAddValueHelp = (question, templates, readOnly) => (
  !readOnly &&
  !isEmpty(templates.project_interview_add_value_help) &&
  question.is_collection &&
  question.widget_type != 'checkbox'
)
