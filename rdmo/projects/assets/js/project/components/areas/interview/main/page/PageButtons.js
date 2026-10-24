import React from 'react'
import { useDispatch, useSelector } from 'react-redux'

import useModal from 'rdmo/core/assets/js/hooks/useModal'

import { navigateDashboard } from '../../../../../actions/navigationActions'

import PageDoneModal from './PageDoneModal'

const PageButtons = () => {
  const dispatch = useDispatch()
  const page = useSelector((state) => state.interview.page)

  const doneModal = useModal()

  return (
    <>
      <div className="project-interview-page-buttons">
        <div className="d-flex">
          {
            page.prev_page && (
              <button
                type="button"
                onClick={() => dispatch(navigateDashboard({ area: 'interview', pageId: page.prev_page}, true))}
                disabled={!page.prev_page}
                className="btn btn-outline-primary"
              >
                {gettext('Back')}
              </button>
            )
          }
          {
            page.next_page ? (
              <button
                type="button"
                onClick={() => dispatch(navigateDashboard({ area: 'interview', pageId: page.next_page}))}
                className="btn btn-primary ms-auto"
              >
                {gettext('Proceed')}
              </button>
            ) : (
              <button
                type="button"
                onClick={() => doneModal.open()}
                className="btn btn-primary ms-auto"
              >
                {gettext('Complete questionnaire')}
              </button>
            )
          }
        </div>
      </div>
      <PageDoneModal
        show={doneModal.show}
        onClose={doneModal.close}
        onSubmit={() => dispatch(navigateDashboard({ area: 'documents'}))}
      />
    </>
  )
}

export default PageButtons
