import uniq from 'lodash/uniq'
import isNil from 'lodash/isNil'

const getAttributes = (page) => {
  if (isNil(page)) {
    return []
  } else {
    // return a unique list of the page's attribute and the page's elements attributes
    return uniq(
      (isNil(page._attribute) ? [] : [page._attribute.id]).concat(
        page.elements.filter(element => !isNil(element._attribute)).map(element => element._attribute.id)
      )
    )
  }
}

const initPage = (page) => {
  page.elements = page.elements.map((element) => {
    if (element.model == 'questions.questionset') {
      return initQuestionSet(element)
    } else {
      return initQuestion(element)
    }
  })

  return page
}

const initQuestionSet = (questionset) => initPage(questionset)

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

export { getAttributes, initPage }
