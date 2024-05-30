import React from 'react'
import PropTypes from 'prop-types'

import Template from 'rdmo/core/assets/js/components/Template'

const Buttons = ({ next, prev, help, fetchPage }) => {
  return (
    <>
      <Template template={help} />

      <div className="interview-buttons">
        <div className="pull-right">
          <button type="button" onClick={() => fetchPage(next)} disabled={!next}
                  className="btn btn-default btn-xs">
            {gettext('Proceed')}
          </button>
        </div>

        <div>
          <button type="button" onClick={() => fetchPage(prev, true)} disabled={!prev}
                  className="btn btn-default btn-xs">
            {gettext('Back')}
          </button>
        </div>
      </div>
    </>
  )
}

Buttons.propTypes = {
  next: PropTypes.number,
  prev: PropTypes.number,
  help: PropTypes.string.isRequired,
  fetchPage: PropTypes.func.isRequired
}

export default Buttons
