import React from 'react'
import PropTypes from 'prop-types'

const Buttons = ({ page, onClick }) => {
  return (
    <>
      <div className="interview-buttons">
        <div className="pull-right">
          <button type="button" onClick={() => onClick(page.next_page)} disabled={!page.next_page}
                  className="btn btn-default btn-xs">
            {gettext('Proceed')}
            {/* TODO: handle */}
            {/*{gettext('Skip')}*/}
          </button>
        </div>

        <div>
          <button type="button" onClick={() => onClick(page.prev_page)} disabled={!page.prev_page}
                  className="btn btn-default btn-xs">
            {gettext('Skip')}
          </button>
        </div>
      </div>
    </>
  )
}

Buttons.propTypes = {
  page: PropTypes.object.isRequired,
  onClick: PropTypes.func.isRequired
}

export default Buttons
