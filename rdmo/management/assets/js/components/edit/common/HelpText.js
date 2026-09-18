import React from 'react'
import PropTypes from 'prop-types'
import { isEmpty } from 'lodash'

const HelpText = ({ help }) => (
  !isEmpty(help) && (
    <div className="form-text">
      {help}
    </div>
  )
)

HelpText.propTypes = {
  help: PropTypes.string
}

export default HelpText
