import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import Select from 'rdmo/core/assets/js/components/forms/Select'

import {
  deleteProjectVisibility,
  updateProjectVisibility
} from '../../../actions/projectActions'

const ProjectVisibilityForm = ({ projectId, disabled = false}) => {
  const dispatch = useDispatch()
  const visibility = useSelector((state) => state.project.visibility)
  const sites = useSelector((state) => state.sites)

  const [siteIds, setSiteIds] = useState(visibility?.sites || [])

  console.log('sites', sites)
  console.log('visibility', visibility)

  useEffect(() => {
    setSiteIds(visibility?.sites || [])
  }, [visibility])

  const siteOptions = sites ? Object.values(sites).map((site) => ({
    value: site.id,
    label: site.current ? `${site.domain} (${gettext('current')})` : site.domain
  })) : []

  const handleSave = () => {
    const data = new FormData()
    siteIds.forEach((siteId) => data.append('sites', siteId))
    dispatch(updateProjectVisibility(data))
  }

  const handleDelete = () => {
    setSiteIds([])
    dispatch(deleteProjectVisibility())
  }

  if (!projectId) {
    return null
  }

  return (
    <div>
      <div className="d-flex align-items-center justify-content-between mb-2">
        <h3 className="mb-0">{gettext('Project visibility')}</h3>
        <span className="text-muted small">
          {visibility ? gettext('Configured') : gettext('Not set')}
        </span>
      </div>

      {/* <p className="text-muted mb-3">
        {gettext('Select the sites that may access this project.')}
      </p> */}

      <Select
        className="mb-3"
        label={gettext('Sites')}
        placeholder={gettext('Select sites')}
        isClearable={true}
        isDisabled={disabled}
        isMulti={true}
        options={siteOptions}
        value={siteIds}
        onChange={(value) => setSiteIds(value || [])}
      />

      <div className="d-flex gap-2">
        <button
          type="button"
          className="btn btn-primary"
          disabled={disabled}
          onClick={handleSave}
        >
          <i className="bi bi-save me-1" aria-hidden="true" />
          {visibility ? gettext('Update visibility') : gettext('Make visible')}
        </button>

        {
          visibility && (
            <button
              type="button"
              className="btn btn-outline-danger"
              disabled={disabled}
              onClick={handleDelete}
            >
              <i className="bi bi-trash me-1" aria-hidden="true" />
              {gettext('Remove visibility')}
            </button>
          )
        }
      </div>
    </div>
  )
}

ProjectVisibilityForm.propTypes = {
  projectId: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  disabled: PropTypes.bool
}

export default ProjectVisibilityForm
