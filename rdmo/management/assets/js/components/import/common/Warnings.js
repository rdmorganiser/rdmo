import React from 'react'
import PropTypes from 'prop-types'
import WarningsListGroup from './WarningsListGroup'
import isUndefined from 'lodash/isUndefined'

const Warnings = ({elementWarnings, elementModel, shouldShowURI = true}) => {
  const show = !isUndefined(elementWarnings) && Object.keys(elementWarnings).length > 0
  const warningsHeadingText = <strong>{gettext('Warnings')}</strong>

  return show && (
    <div className="panel panel-warning">
      <div className="panel-heading">{warningsHeadingText}</div>
      <WarningsListGroup
        elementWarnings={elementWarnings}
        elementModel={elementModel}
        shouldShowURI={shouldShowURI}
      />
    </div>
  )
}

Warnings.propTypes = {
  elementWarnings: PropTypes.object.isRequired,
  elementModel: PropTypes.string.isRequired,
  shouldShowURI: PropTypes.bool
}

export default Warnings
