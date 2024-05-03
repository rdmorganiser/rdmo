import { isNil } from 'lodash'

const initQuestionSet = (questionset) => {
  questionset.elements.forEach((element) => {
    if (element.model == 'questions.questionset') {
      initQuestionSet(element)
    } else {
      initQuestion(element, questionset)
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

const initQuestion = (question, questionset) => {
  // store if this question is part of a set collection
  // to store value.set_collection later
  question.set_collection = questionset.is_collection
}

const initPage = (page) => initQuestionSet(page)

export { initPage }
