import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'

import Html from 'rdmo/core/assets/js/components/Html'

import { fetchElement } from '../../actions/elementActions'

import { ExtendLink, CodeLink } from '../common/Links'

import useBool from '../../hooks/useBool'

const QuestionInfo = ({ question }) => {
  const dispatch = useDispatch()

  const elements = useSelector((state) => state.elements)

  const [extendPages, togglePages] = useBool(false)
  const [extendQuestionSet, toggleQuestionSets] = useBool(false)

  const pages = elements.pages.filter(e => question.pages.includes(e.id))
  const questionsets = elements.questionsets.filter(e => question.questionsets.includes(e.id))

  const fetchPage = (page) => dispatch(fetchElement('pages', page.id))
  const fetchQuestionSet = (questionset) => dispatch(fetchElement('questionsets', questionset.id))

  return (
    <div className="mb-2">
      <p className="mb-1">
        <Html html={interpolate(ngettext(
          'This question is used in <b>one page</b>.',
          'This question is used in <b>%s pages</b>.',
          pages.length), [pages.length])} />
        {pages.length > 0 && <ExtendLink extend={extendPages} onClick={togglePages} />}
      </p>
      {
        extendPages && pages.map((page, index) => (
          <p className="mb-1" key={index}>
            <CodeLink type="questions" uri={page.uri} onClick={() => fetchPage(page)} />
          </p>
        ))
      }
      <p className="mb-1">
        <Html html={interpolate(ngettext(
            'This question set is used in <b>one question set</b>.',
            'This question set is used in <b>%s question sets</b>.',
            questionsets.length), [questionsets.length])} />
        {questionsets.length > 0 && <ExtendLink extend={extendQuestionSet} onClick={toggleQuestionSets} />}
      </p>
      {
        extendQuestionSet && questionsets.map((questionset, index) => (
          <p className="mb-1" key={index}>
            <CodeLink type="questions" uri={questionset.uri} onClick={() => fetchQuestionSet(questionset)} />
          </p>
        ))
      }
    </div>
  )
}

QuestionInfo.propTypes = {
  question: PropTypes.object.isRequired
}

export default QuestionInfo
