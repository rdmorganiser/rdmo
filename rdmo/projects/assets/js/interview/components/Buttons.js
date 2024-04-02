import React from 'react'
import PropTypes from 'prop-types'

const Buttons = ({ page, help, onClick }) => {
  return (
    <>
      <div className="interview-navigation-help" dangerouslySetInnerHTML={{
        '__html': help
      }}></div>

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
            {gettext('Back')}
          </button>
        </div>
      </div>
    </>
  )
}

Buttons.propTypes = {
  page: PropTypes.object.isRequired,
  help: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired
}

export default Buttons
