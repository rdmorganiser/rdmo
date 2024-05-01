import { isNil } from 'lodash'

const initQuestionSet = (questionset) => {
  questionset.elements.forEach((element) => {
    if (element.model == 'questions.questionset') {
      initQuestionSet(element)
    } else {
      initQuestion(element)
    }
  })

  // aggregate optionsets from decendants
  questionset.optionsets = questionset.elements.reduce((optionsets, element) => {
    if (element.model == 'questions.questionset') {
        return optionsets.concat(element.optionsets)
      } else {
        return [...optionsets, ...element.optionsets]
      }
  }, [])

  // aggregate attributes from decendants
  questionset.attributes = questionset.elements.reduce((attributes, element) => {
    if (element.model == 'questions.questionset') {
        return attributes.concat(element.attributes)
      } else {
        return [...attributes, element.attribute]
      }
  }, [questionset.attribute]).filter((a) => !isNil(a))
}


// eslint-disable-next-line no-unused-vars
const initQuestion = (question) => {
  // kept for potential future use ...
}

const initPage = (page) => initQuestionSet(page)

export { initPage }
