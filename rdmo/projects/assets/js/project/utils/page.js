import { get, isNil } from 'lodash'

const checkElement = (element, set) => {
  if (element.model == 'questions.questionset') {
    return checkQuestionSet(element, set)
  } else {
    return checkQuestion(element, set)
  }
}

const checkQuestionSet = (questionset, set) => {
  return !questionset.has_conditions || get(set, `questionsets.${questionset.id}`)
}

const checkQuestion = (question, set) => {
  return !question.has_conditions || get(set, `questions.${question.id}`)
}

const groupElements = (elements, set) => {
  return elements.filter((element) => checkElement(element, set)).reduce((cards, element, index, elements) => {
    // start a new card for the first element, for elements without a width,
    // and for elements following an element without a width
    if (index == 0 || !element.width || !elements[index - 1].width) {
      cards.push([element])
    } else {
      cards[cards.length - 1].push(element)
    }
    return cards
  }, [])
}

const initQuestionSet = (questionset, level = 0) => {
  questionset.level = level

  questionset.elements.forEach((element) => {
    element.parent = questionset

    if (element.model == 'questions.questionset') {
      initQuestionSet(element, level + 1)
    } else {
      initQuestion(element, questionset)
    }
  })

  // aggregate questionsets from descendants
  questionset.questionsets = questionset.elements.reduce((questionsets, element) => {
    if (element.model == 'questions.questionset') {
      return [...questionsets, element, ...element.questionsets] // add this questionset and all it's questionsets
    } else {
      return questionsets  // do nothing
    }
  }, [])

  // aggregate questions from descendants
  questionset.questions = questionset.elements.reduce((questions, element) => {
    if (element.model == 'questions.questionset') {
      return questions.concat(element.questions)  // add the questions of this questionset
    } else {
      return [...questions, element]  // add this question
    }
  }, [])

  // aggregate optionsets from descendants
  questionset.optionsets = questionset.elements.reduce((optionsets, element) => {
    if (element.model == 'questions.questionset') {
      return optionsets.concat(element.optionsets)  // add all optionsets of the questions of this questionset
    } else {
      return [...optionsets, ...element.optionsets]  // add all optionsets of this question
    }
  }, [])

  // aggregate attributes from descendants
  questionset.attributes = questionset.elements.reduce((attributes, element) => {
    if (element.model == 'questions.questionset') {
      return attributes.concat(element.attributes)  // add all attributes of this questionset and its questions
    } else {
      return [...attributes, element.attribute]  // add the attribute of this question
    }
  }, [questionset.attribute]).filter((a) => !isNil(a))
}

const initQuestion = (question, questionset) => {
  // store if this question is part of a set collection
  // to store value.set_collection later
  question.set_collection = questionset.is_collection
}

const initPage = (page) => initQuestionSet(page)

export { checkElement, checkQuestion, checkQuestionSet, groupElements, initPage }
