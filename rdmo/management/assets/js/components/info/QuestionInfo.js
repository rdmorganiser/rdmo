import React from 'react'
import PropTypes from 'prop-types'

import { ExtendLink, CodeLink } from '../common/Links'

import useBool from '../../hooks/useBool'

const QuestionInfo = ({ question, elements, elementActions }) => {

  const [extendPages, togglePages] = useBool(false)
  const [extendQuestionSet, toggleQuestionSets] = useBool(false)

  const pages = elements.pages.filter(e => question.pages.includes(e.id))
  const questionsets = elements.questionsets.filter(e => question.questionsets.includes(e.id))

  const fetchPage = (page) => elementActions.fetchElement('pages', page.id)
  const fetchQuestionSet = (questionset) => elementActions.fetchElement('questionsets', questionset.id)

  return (
    <div className="element-info">
      <p>
        <span dangerouslySetInnerHTML={{
          __html: interpolate(ngettext(
            'This question is used in <b>one page</b>.',
            'This question is used in <b>%s pages</b>.',
            pages.length), [pages.length])}} />
        {pages.length > 0 && <ExtendLink extend={extendPages} onClick={togglePages} />}
      </p>
      {
        extendPages && pages.map((page, index) => (
          <p key={index}>
            <CodeLink className="code-questions" uri={page.uri} onClick={() => fetchPage(page)} />
          </p>
        ))
      }
      <p>
        <span dangerouslySetInnerHTML={{
          __html: interpolate(ngettext(
            'This question set is used in <b>one question set</b>.',
            'This question set is used in <b>%s question sets</b>.',
            questionsets.length), [questionsets.length])}} />
        {questionsets.length > 0 && <ExtendLink extend={extendQuestionSet} onClick={toggleQuestionSets} />}
      </p>
      {
        extendQuestionSet && questionsets.map((questionset, index) => (
          <p key={index}>
            <CodeLink className="code-questions" uri={questionset.uri} onClick={() => fetchQuestionSet(questionset)} />
          </p>
        ))
      }
    </div>
  )
}

QuestionInfo.propTypes = {
  question: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default QuestionInfo
