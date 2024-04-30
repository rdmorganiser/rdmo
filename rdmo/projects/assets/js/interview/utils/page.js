import { isNil } from 'lodash'

const initQuestionSet = (questionset) => {
  questionset.elements.forEach((element) => {
    if (element.model == 'questions.questionset') {
      initQuestionSet(element)
    } else {
      initQuestion(element)
    }
  })

  // aggregate attributes from decendant questionsets and questions
  questionset.attributes = questionset.elements.reduce((attributes, element) => {
    if (element.model == 'questions.questionset') {
        return attributes.concat(element.attributes)
      } else {
        return [...attributes, element.attribute]
      }
  }, [questionset.attribute]).filter((a) => !isNil(a))
}

const initQuestion = (question) => {
  // aggregate options from optionsets
  question.options = question.optionsets.reduce((acc, cur) => {
    acc = acc.concat(cur.options.map((option) => {
      option.optionset = cur.id
      return option
    }))

    return acc
  }, [])
}

const initPage = (page) => initQuestionSet(page)

export { initPage }
