import React from 'react'
import PropTypes from 'prop-types'

const Buttons = ({ currentPage, onPrev, onNext }) => {
  return (
    <>
      <div className="interview-buttons">
        <div className="pull-right">
          <button type="button" onClick={onNext} disabled={!currentPage.next_page}
                  className="btn btn-default btn-xs">
            {gettext('Proceed')}
            {/* TODO: handle */}
            {/*{gettext('Skip')}*/}
          </button>
        </div>

        <div>
          <button type="button" onClick={onPrev} disabled={!currentPage.prev_page}
                  className="btn btn-default btn-xs">
            {gettext('Skip')}
          </button>
        </div>
      </div>
    </>
  )
}

Buttons.propTypes = {
  currentPage: PropTypes.object.isRequired,
  onPrev: PropTypes.func.isRequired,
  onNext: PropTypes.func.isRequired
}

export default Buttons
