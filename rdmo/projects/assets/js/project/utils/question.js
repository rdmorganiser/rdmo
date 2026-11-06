import { isEmpty } from 'lodash'

export const getQuestionTextId = (question) => question.text && `question-text-${question.id}`

export const getQuestionHelpId = (question) => `question-help-${question.id}`

export const hasAddValueHelp = (question, templates, readOnly) => (
  !readOnly &&
  !isEmpty(templates.project_interview_add_value_help) &&
  question.is_collection &&
  question.widget_type != 'checkbox'
)
