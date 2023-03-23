import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { ExtendLink } from '../common/ElementLinks'

import useBool from '../../hooks/useBool'

const OptionSetInfo = ({ optionset, elements }) => {

  const [extendQuestions, toggleQuestions] = useBool(false)

  const questions = elements.questions.filter(e => optionset.questions.includes(e.id))

  return (
    <div className="element-info">
      {
        questions.length > 0 && <>
          <p>
            <span dangerouslySetInnerHTML={{
              __html: interpolate(ngettext(
                'This option set is used in <b>one question</b>.',
                'This option set is used in <b>%s questions</b>.',
                questions.length), [questions.length])}} />
            <ExtendLink extend={extendQuestions} onClick={toggleQuestions} />
          </p>
          {
            extendQuestions && questions.map((question, index) => (
              <p key={index}>
                <code className="code-questions">{question.uri}</code>
              </p>
            ))
          }
        </>
      }
    </div>
  )
}

OptionSetInfo.propTypes = {
  optionset: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired
}

export default OptionSetInfo
