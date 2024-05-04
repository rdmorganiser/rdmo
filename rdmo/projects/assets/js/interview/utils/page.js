import { get, isNil } from 'lodash'

const checkQuestionSet = (questionset, set) => {
  return !questionset.has_conditions || get(set, `questionsets.${questionset.id}`)
}

const checkQuestion = (question, set) => {
  return !question.has_conditions || get(set, `questions.${question.id}`)
}

const initQuestionSet = (questionset) => {
  questionset.elements.forEach((element) => {
    if (element.model == 'questions.questionset') {
      initQuestionSet(element)
    } else {
      initQuestion(element, questionset)
    }
  })

  // aggregate questionsets from decendants
  questionset.questionsets = questionset.elements.reduce((questionsets, element) => {
    return (element.model == 'questions.questionset') ? [...questionsets, element] : questionsets
  }, [])

  // aggregate optionsets from decendants
  questionset.questions = questionset.elements.reduce((questions, element) => {
    return (element.model == 'questions.question') ? [...questions, element] : questions
  }, [])

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

export { checkQuestionSet, checkQuestion, initPage }
