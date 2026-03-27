import React from 'react'
import PropTypes from 'prop-types'
import isUndefined from 'lodash/isUndefined'

import WarningsListGroup from './WarningsListGroup'

const Warnings = ({ elementWarnings, elementModel, elementURI, shouldShowURI = true }) => {
  const show = !isUndefined(elementWarnings) && Object.keys(elementWarnings).length > 0
  const warningsHeadingText = <strong>{gettext('Warnings')}</strong>

  return show && (
    <div className="card text-bg-warning my-2">
      <div className="card-header">{warningsHeadingText}</div>
      <WarningsListGroup
        elementWarnings={elementWarnings}
        elementModel={elementModel}
        elementURI={elementURI}
        shouldShowURI={shouldShowURI}
      />
    </div>
  )
}

Warnings.propTypes = {
  elementWarnings: PropTypes.object.isRequired,
  elementModel: PropTypes.string.isRequired,
  elementURI: PropTypes.string.isRequired,
  shouldShowURI: PropTypes.bool
}

export default Warnings
