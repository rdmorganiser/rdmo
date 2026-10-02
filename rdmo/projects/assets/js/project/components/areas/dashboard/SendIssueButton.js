import React from 'react'
import PropTypes from 'prop-types'

import { LinkButton } from 'rdmo/core/assets/js/components'

const SendIssueButton = ({ onClick }) => (
  <LinkButton
    onClick={
      (event) => {
        event.stopPropagation()
        onClick()
      }
    }
    aria-label={gettext('Send task')}
    title={gettext('Send task')}
  >
    <i className="bi bi-send" aria-hidden="true" />
  </LinkButton>
)

SendIssueButton.propTypes = {
  onClick: PropTypes.func.isRequired,
}

export default SendIssueButton
