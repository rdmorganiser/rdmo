import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import Select from 'rdmo/core/assets/js/components/forms/Select'

import {
  deleteProjectVisibility,
  updateProjectVisibility
} from '../../../actions/projectActions'

const ProjectVisibilityForm = ({ projectId }) => {
  const dispatch = useDispatch()
  const visibility = useSelector((state) => state.project.visibility)
  const perms = useSelector((state) => state.project.project.project?.permissions) ?? {}
  const settings = useSelector((state) => state.settings)
  const sites = useSelector((state) => state.sites)
  const groups = useSelector((state) => state.groups)

  console.log('groups', groups)
  const [siteIds, setSiteIds] = useState(visibility?.sites || [])
  const [groupIds, setGroupIds] = useState(visibility?.groups || [])

  console.log('sites', sites)
  console.log('groups', groups)
  console.log('visibility', visibility)

  useEffect(() => {
    setSiteIds(visibility?.sites || [])
    setGroupIds(visibility?.groups || [])
  }, [visibility])

  const siteOptions = sites ? Object.values(sites).map((site) => ({
    value: site.id,
    label: site.current ? `${site.domain} (${gettext('current')})` : site.domain
  })) : []

  const groupOptions = groups ? Object.values(groups).map((group) => ({
    value: group.id,
    label: group.name
  })) : []

  const handleSave = () => {
    const data = new FormData()
    if (settings.multisite) {
      siteIds.forEach((siteId) => data.append('sites', siteId))
    }
    if (settings.groups) {
      groupIds.forEach((groupId) => data.append('groups', groupId))
    }
    dispatch(updateProjectVisibility(data))
  }

  const handleDelete = () => {
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
          {
            visibility ? (
              siteIds.length === 0 && groupIds.length === 0 ? (
                gettext('Visible to all users on all sites')
              ) : gettext('Restricted')
            ) : gettext('Not set')
          }
        </span>
      </div>

      {
        settings.multisite && (
          <Select
            className="mb-3"
            label={gettext('Sites')}
            placeholder={gettext('Select sites')}
            isClearable={true}
            isDisabled={!perms.can_change_visibility}
            isMulti={true}
            options={siteOptions}
            value={siteIds}
            onChange={(value) => setSiteIds(value || [])}
          />
        )
      }

      {
        settings.groups && (
          <Select
            className="mb-3"
            label={gettext('Groups')}
            placeholder={gettext('Select groups')}
            isClearable={true}
            isDisabled={!perms.can_change_visibility}
            isMulti={true}
            options={groupOptions}
            value={groupIds}
            onChange={(value) => setGroupIds(value || [])}
          />
        )
      }

      <div className="d-flex gap-2">
        {
          (visibility && perms.can_change_visibility) || perms.can_add_visibility && (
            <button
              type="button"
              className="btn btn-primary"
              onClick={handleSave}
            >
              <i className="bi bi-save me-1" aria-hidden="true" />
              {
                visibility && perms.can_change_visibility ? gettext('Update visibility') : (
                  perms.can_add_visibility ? gettext('Set visibility') : null)
              }
            </button>
          )
        }

        {
          visibility && perms.can_delete_visibility && (
            <button
              type="button"
              className="btn btn-outline-danger"
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
  projectId: PropTypes.oneOfType([PropTypes.string, PropTypes.number])
}

export default ProjectVisibilityForm
