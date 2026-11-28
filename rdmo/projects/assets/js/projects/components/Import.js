import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { isNil } from 'lodash'

import { Html } from 'rdmo/core/assets/js/components'

import Errors from 'rdmo/core/assets/js/components/Errors'

import { navigateImport, submitImport } from '../actions/importActions'

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
        // the import is done (or was cancelled), return to the list of projects
        if (response?.success) {
          dispatch(navigateImport(null))
        }
      })
  }

  return (
    <div className="px-4 py-5">
      <div className="container gx-0">
        <Errors />
        {
          !isNil(current) && (
            <div className="projects-import">
              <div className="d-flex justify-content-between align-items-center mb-5">
                <h1 className="mb-0">{label}</h1>
              </div>

              <div onSubmit={handleSubmit}>
                <Html html={current.html} />
              </div>
            </div>
          )
        }
      </div>
    </div>
  )
}

export default Import
