import { isNil } from 'lodash'

const initQuestionSet = (questionset) => {
  questionset.elements = questionset.elements.map((element) => {
    if (element.model == 'questions.questionset') {
      return initQuestionSet(element)
    } else {
      return initQuestion(element)
    }
  })

  questionset.attributes = questionset.elements.reduce((agg, cur) => {
    if (cur.model == 'questions.questionset') {
        return agg.concat(cur.attributes)
      } else {
        return [...agg, cur.attribute]
      }
  }, [questionset.attribute]).filter((a) => !isNil(a))

  return questionset
}

const initQuestion = (question) => {
  question.options = question.optionsets.reduce((acc, cur) => {
    acc = acc.concat(cur.options.map((option) => {
      option.optionset = cur.id
      return option
    }))

    return acc
  }, [])

  return question
}

const initPage = (page) => initQuestionSet(page)

export { initPage }
