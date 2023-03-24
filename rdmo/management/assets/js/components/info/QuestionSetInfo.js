import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { ExtendLink } from '../common/Links'

import useBool from '../../hooks/useBool'

const QuestionSetInfo = ({ questionset, elements }) => {

  const [extendPages, togglePages] = useBool(false)
  const [extendQuestionSet, toggleQuestionSets] = useBool(false)

  const pages = elements.pages.filter(e => questionset.pages.includes(e.id))
  const questionsets = elements.questionsets.filter(e => questionset.parents.includes(e.id))

  return (
    <div className="element-info">
      {
        pages.length > 0 && <>
          <p>
            <span dangerouslySetInnerHTML={{
              __html: interpolate(ngettext(
                'This question set is used in <b>one page</b>.',
                'This question set is used in <b>%s pages</b>.',
                pages.length), [pages.length])}} />
            <ExtendLink extend={extendPages} onClick={togglePages} />
          </p>
          {
            extendPages && pages.map((page, index) => (
              <p key={index}>
                <code className="code-questions">{page.uri}</code>
              </p>
            ))
          }
        </>
      }
      {
        questionsets.length > 0 && <>
          <p>
            <span dangerouslySetInnerHTML={{
              __html: interpolate(ngettext(
                'This question set is used in <b>one question set</b>.',
                'This question set is used in <b>%s question sets</b>.',
                questionsets.length), [questionsets.length])}} />
            <ExtendLink extend={extendQuestionSet} onClick={toggleQuestionSets} />
          </p>
          {
            extendQuestionSet && questionsets.map((questionset, index) => (
              <p key={index}>
                <code className="code-questions">{questionset.uri}</code>
              </p>
            ))
          }
        </>
      }
    </div>
  )
}

QuestionSetInfo.propTypes = {
  questionset: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired
}

export default QuestionSetInfo
