import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'

import { fetchElement } from '../../actions/elementActions'

import { ExtendLink, CodeLink } from '../common/Links'

import useBool from '../../hooks/useBool'

const OptionSetInfo = ({ optionset }) => {
  const dispatch = useDispatch()

  const elements = useSelector((state) => state.elements)

  const [extendQuestions, toggleQuestions] = useBool(false)

  const questions = elements.questions.filter(e => optionset.questions.includes(e.id))

  const fetchQuestion = (question) => dispatch(fetchElement('questions', question.id))

  return (
    <div className="element-info">
      <p>
        <span dangerouslySetInnerHTML={{
          __html: interpolate(ngettext(
            'This option set is used in <b>one question</b>.',
            'This option set is used in <b>%s questions</b>.',
            questions.length), [questions.length])}} />
        {questions.length > 0 && <ExtendLink extend={extendQuestions} onClick={toggleQuestions} />}
      </p>
      {
        extendQuestions && questions.map((question, index) => (
          <p key={index}>
            <CodeLink className="code-questions" uri={question.uri} onClick={() => fetchQuestion(question)} />
          </p>
        ))
      }
    </div>
  )
}

OptionSetInfo.propTypes = {
  optionset: PropTypes.object.isRequired
}

export default OptionSetInfo
