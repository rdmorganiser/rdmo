import React from 'react'
import PropTypes from 'prop-types'
import { isUndefined } from 'lodash'

const ImportInfo = ({ elementsLength, updatedLength, createdLength, changedLength, warningsLength, errorsLength }) => {
  return ( !isUndefined(elementsLength) && elementsLength > 0 &&
    <div className="pull-right">
      {
        elementsLength > 0 && <span>{gettext('Total')}: {elementsLength} </span>
      }
      {
        updatedLength > 0 && <span>{gettext('Updated')}: {updatedLength} </span>
      }
      { updatedLength > 0 &&
        <span>{' ('}{gettext('Changed')}: {changedLength}{') '}</span>
      }
      {
        createdLength > 0 && <span>{gettext('Created')}: {createdLength} </span>
      }
       {
        warningsLength > 0 && <span>{gettext('Warnings')}: {warningsLength} </span>
      }
      {
        errorsLength > 0 && <span>{gettext('Errors')}: {errorsLength} </span>
      }
    </div>
  )
}

ImportInfo.propTypes = {
  elementsLength: PropTypes.number,
  updatedLength: PropTypes.number,
  createdLength: PropTypes.number,
  changedLength: PropTypes.number,
  warningsLength: PropTypes.number,
  errorsLength: PropTypes.number,
}

export default ImportInfo
