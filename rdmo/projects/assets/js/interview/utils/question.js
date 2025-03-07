export const getQuestionTextId = (question) => question.text && `question-text-${question.id}`

export const getQuestionHelpId = (question) => question.help && `question-help-${question.id}`
