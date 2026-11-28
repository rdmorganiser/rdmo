import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { isNil } from 'lodash'

import { Html } from 'rdmo/core/assets/js/components'

import { submitExport } from '../../../actions/exportActions'
import { navigateDashboard } from '../../../actions/navigationActions'

const Export = () => {
  const dispatch = useDispatch()

  const current = useSelector((state) => state.export.current)
  const label = useSelector((state) => state.export.exportList?.[current?.key]?.label) ?? current?.key

  const handleSubmit = (event) => {
    event.preventDefault()

    // the submitter adds the name of the clicked button, e.g. cancel, to the form data
    const formData = new FormData(event.target, event.nativeEvent.submitter)

    dispatch(submitExport(current.key, formData))
      .then((response) => {
        // the export is done (or was cancelled)
        if (response?.success) {
          dispatch(navigateDashboard({ area: 'transfer' }))
        }
      })
  }

  // wait until the export is fetched
  return !isNil(current) && (
    <div className="project-export">
      <div className="d-flex justify-content-between align-items-center mb-5">
        <h1 className="mb-0">{label}</h1>
      </div>

      <div onSubmit={handleSubmit}>
        <Html html={current.html} />
      </div>
    </div>
  )
}

export default Export
