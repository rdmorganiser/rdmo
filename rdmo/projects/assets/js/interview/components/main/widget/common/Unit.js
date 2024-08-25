import React from 'react'
import PropTypes from 'prop-types'
import { isEmpty, isUndefined } from 'lodash'

const Unit = ({ unit, inputValue }) => {
  return (!isEmpty(unit) || !isUndefined(inputValue)) && (
    <div className="unit">
      {
        !isUndefined(inputValue) && (
          <>
            <span>{inputValue}</span>
            {' '}
          </>
        )
      }
      {
        !isEmpty(unit) && !isUndefined(inputValue) && (' ')
      }
      {
        !isEmpty(unit) && (
          <span title={gettext('The unit for this answer.')}>{unit}</span>
        )
      }
    </div>
  )
}

Unit.propTypes = {
  unit: PropTypes.string,
  inputValue: PropTypes.string,
}

export default Unit
