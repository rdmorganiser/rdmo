import React from 'react'
import PropTypes from 'prop-types'

const PageButtons = ({ page, fetchPage }) => {
  return (
    <>
      <div className="interview-buttons">
        <div className="pull-right">
          <button type="button" onClick={() => fetchPage(page.prev_page, true)} disabled={!page.prev_page}
                  className="btn btn-default">
            {gettext('Back')}
          </button>
          {' '}
          {
            page.next_page ? (
              <button type="button" onClick={() => fetchPage(page.next_page)}
                      className="btn btn-primary">
                {gettext('Proceed')}
              </button>
            ) : (
              <button type="button" onClick={() => fetchPage('done')}
                      className="btn btn-primary">
                {gettext('Complete questionnaire')}
              </button>
            )
          }
        </div>
      </div>
    </>
  )
}

PageButtons.propTypes = {
  page: PropTypes.object.isRequired,
  fetchPage: PropTypes.func.isRequired
}

export default PageButtons
