import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { isNil } from 'lodash'

import { Html } from 'rdmo/core/assets/js/components'

import { submitImport } from '../../../actions/importActions'
import { navigateDashboard } from '../../../actions/navigationActions'
import { fetchProject } from '../../../actions/projectActions'

const Import = () => {
  const dispatch = useDispatch()

  const current = useSelector((state) => state.import.current)
  const label = useSelector((state) => state.import.importList?.[current?.key]?.label) ?? current?.key

  const handleSubmit = (event) => {
    event.preventDefault()

    // the submitter adds the name of the clicked button, e.g. cancel, to the form data
    const formData = new FormData(event.target, event.nativeEvent.submitter)

    dispatch(submitImport(current.key, formData))
      .then((response) => {
        // the import is done (or was cancelled), the project might have changed
        if (response?.success) {
          dispatch(fetchProject()).catch(() => {})
          dispatch(navigateDashboard({ area: 'transfer' }))
        }
      })
  }

  // wait until the import is fetched
  return !isNil(current) && (
    <div className="project-import">
      <div className="d-flex justify-content-between align-items-center mb-5">
        <h1 className="mb-0">{label}</h1>
      </div>

      <div onSubmit={handleSubmit}>
        <Html html={current.html} />
      </div>
    </div>
  )
}

export default Import
