import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'

import { fetchElement } from '../../actions/elementActions'
import useBool from '../../hooks/useBool'

import { CodeLink, ExtendLink } from '../common/Links'

const OptionSetInfo = ({ optionset }) => {
  const dispatch = useDispatch()

  const elements = useSelector((state) => state.elements)

  const [extendQuestions, toggleQuestions] = useBool(false)

  const questions = elements.questions.filter(e => optionset.questions.includes(e.id))

  const fetchQuestion = (question) => dispatch(fetchElement('questions', question.id))

  return (
    <div className="mb-2">
      <p className="mb-1">
        <Html html={
          interpolate(ngettext(
            'This option set is used in <b>one question</b>.',
            'This option set is used in <b>%s questions</b>.',
            questions.length), [questions.length])
        } />
        {questions.length > 0 && <ExtendLink extend={extendQuestions} onClick={toggleQuestions} />}
      </p>
      {
        extendQuestions && questions.map((question, index) => (
          <p className="mb-1" key={index}>
            <CodeLink type="questions" uri={question.uri} onClick={() => fetchQuestion(question)} />
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
