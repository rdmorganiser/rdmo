import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import { siteId } from 'rdmo/core/assets/js/utils/meta'

import Select from 'rdmo/core/assets/js/components/forms/Select'
import Html from 'rdmo/core/assets/js/components/Html'

import {
  deleteProjectVisibility,
  updateProjectVisibility
} from '../../../actions/projectActions'

const ProjectVisibilityForm = () => {
  const dispatch = useDispatch()
  const visibility = useSelector((state) => state.project.visibility)
  const project = useSelector((state) => state.project.project.project) || {}
  const groups = useSelector((state) => state.groups)
  const settings = useSelector((state) => state.settings)
  const sites = useSelector((state) => state.sites)
  const templates = useSelector((state) => state.templates)
  const currentUser = useSelector((state) => state.user.currentUser)
  const isSubmitting = useSelector((state) => (
    state.pending.items.includes('updateProjectVisibility') ||
    state.pending.items.includes('deleteProjectVisibility') ||
    state.pending.items.includes('fetchProjectVisibility')
  ))

  const projectPerms = project?.permissions || {}
  const userPerms = currentUser?.permissions || {}

  const ownSite = !userPerms.can_change_visibility &&
    currentUser?.role?.manager?.find((site) => site.id === siteId)

  const ownSiteIsVisible = Boolean(
    ownSite && visibility && (
      visibility.sites.length === 0 ||
      visibility.sites.includes(ownSite.id)
    )
  )

  const [siteIds, setSiteIds] = useState(visibility?.sites || [])
  const [groupIds, setGroupIds] = useState(visibility?.groups || [])

  useEffect(() => {
    if (visibility?.sites.length === 0) {
      setSiteIds(Object.values(sites || {}).map((site) => site.id))
    } else {
      setSiteIds(visibility?.sites || [])
    }
    if (visibility?.groups.length === 0) {
      setGroupIds(Object.values(groups || {}).map((group) => group.id))
    } else {
      setGroupIds(visibility?.groups || [])
    }
  }, [visibility, sites, groups])

  const canUpdateVisibility = visibility && userPerms.can_change_visibility && (settings.multisite || settings.groups)
  const canSetVisibility = !visibility && userPerms.can_add_visibility
  const canAddOwnSite = visibility ? projectPerms.can_change_visibility : projectPerms.can_add_visibility

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
      const selectedSiteIds = siteIds.length === siteOptions.length ? [] : siteIds
      selectedSiteIds.forEach((selectedSiteId) => data.append('sites', selectedSiteId))
    }
    if (settings.groups) {
      const selectedGroupIds = groupIds.length === groupOptions.length ? [] : groupIds
      selectedGroupIds.forEach((selectedGroupId) => data.append('groups', selectedGroupId))
    }
    dispatch(updateProjectVisibility(data))
  }

  const handleDelete = () => {
    dispatch(deleteProjectVisibility())
  }

  if (!project.id) {
    return null
  }

  return (
    <div>
      <div className="d-flex align-items-center justify-content-between mb-2">
        <h3 className="mb-0">{gettext('Project visibility')}</h3>
        <span className="text-muted small">
          {
            visibility ? visibility.help_display : gettext('Not set')
          }
        </span>
      </div>
      <Html html={templates?.project_view_visibility_help} />

      {
        userPerms?.can_change_visibility ? (
          <>
            {
              settings.multisite && (
                <Select
                  className="mb-3"
                  label={gettext('Sites')}
                  placeholder={gettext('Select sites')}
                  isClearable={false}
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
                  isClearable={false}
                  isMulti={true}
                  options={groupOptions}
                  value={groupIds}
                  onChange={(value) => setGroupIds(value || [])}
                />
              )
            }

            <div className="d-flex gap-2">
              {
                (canUpdateVisibility || canSetVisibility) && (
                  <button
                    type="button"
                    className="btn btn-primary"
                    disabled={isSubmitting}
                    onClick={handleSave}
                  >
                    {
                      canUpdateVisibility ? gettext('Update visibility') : gettext('Make visible')
                    }
                  </button>
                )
              }

              {
                visibility && userPerms.can_delete_visibility && (
                  <button
                    type="button"
                    className="btn btn-danger"
                    disabled={isSubmitting}
                    onClick={handleDelete}
                  >
                    {gettext('Remove visibility')}
                  </button>
                )
              }
            </div>
          </>
        ) : ownSite ? (
          <div className="mb-3">
            {
              ownSiteIsVisible ? (
                projectPerms.can_delete_visibility && (
                  <button
                    type="button"
                    className="btn btn-danger"
                    disabled={isSubmitting}
                    onClick={handleDelete}
                  >
                    {interpolate(gettext('Remove %s'), [ownSite.name])}
                  </button>
                )
              ) : (
                canAddOwnSite && (
                  <button
                    type="button"
                    className="btn btn-primary"
                    disabled={isSubmitting}
                    onClick={handleSave}
                  >
                    {interpolate(gettext('Make %s visible'), [ownSite.name])}
                  </button>
                )
              )
            }
          </div>
        ) : null

      }

    </div>
  )
}

export default ProjectVisibilityForm
