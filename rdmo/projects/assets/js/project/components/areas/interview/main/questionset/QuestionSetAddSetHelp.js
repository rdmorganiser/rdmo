import React from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'

import Template from 'rdmo/core/assets/js/components/Template'

import { isReadOnly } from '../../../../../../common/utils/permissions'

const QuestionSetAddSetHelp = ({ questionset }) => {
  const readOnly = useSelector((state) => isReadOnly(state.combinedPermissions))

  return !readOnly && questionset.is_collection && (
    <Template template="project_interview_add_set_help" />
  )
}

QuestionSetAddSetHelp.propTypes = {
  questionset: PropTypes.object.isRequired,
}

export default QuestionSetAddSetHelp
