import React from 'react'
import PropTypes from 'prop-types'
import { PendingInvitations, ProjectFilters, ProjectImport, Table } from '../helper'
import { Link, Modal, SearchField } from 'rdmo/core/assets/js/components'
import { useFormattedDateTime, useModal, useScrollToTop }  from 'rdmo/core/assets/js/hooks'
import useDatePicker from '../../hooks/useDatePicker'
import { language } from 'rdmo/core/assets/js/utils'
import { getTitlePath, getUserRoles, userIsManager, HEADER_FORMATTERS, SORTABLE_COLUMNS } from '../../utils'
import { get, isEmpty } from 'lodash'

const Projects = ({ config, configActions, currentUserObject, projectsActions, projectsObject }) => {
  const { allowedTypes, catalogs, importUrls, invites, projects, projectsCount, hasNext } = projectsObject

  const { currentUser } = currentUserObject
  const { myProjects } = config

  const { showTopButton, scrollToTop } = useScrollToTop()

  const { show: showInvitations, open: openInvitations, close: closeInvitations } = useModal()
  const { show: showImport, open: openImport, close: closeImport } = useModal()

  const invitationsModalProps = {
    title: gettext('Pending invitations'),
    show: showInvitations,
    onClose: closeInvitations
  }

  const importModalProps = {
    title: gettext('Import project'),
    show: showImport,
    onClose: closeImport
  }

  const { setStartDate, setEndDate } = useDatePicker()

  const displayMessage = interpolate(gettext('%s of %s projects are displayed'), [projects.length > projectsCount ? projectsCount : projects.length, projectsCount])

  const getProgressString = (row) => {
    return (row.progress_total ?  interpolate(gettext('%s of %s'), [row.progress_count ?? 0, row.progress_total]) : null)
  }

  const currentUserId = currentUser.id
  const isManager = userIsManager(currentUser)

  const showFilters = get(config, 'showFilters', false)
  const toggleFilters = () => configActions.updateConfig('showFilters', !showFilters)

  const searchString = get(config, 'params.search', '')
  const updateSearchString = (value) => {
    value ? configActions.updateConfig('params.search', value) : configActions.deleteConfig('params.search')
    configActions.updateConfig('params.page', '1')
  }

  const viewLinkText = myProjects ? gettext('View all projects') : gettext('View my projects')
  const headline = myProjects ? gettext('My projects') : gettext('All projects')

  const handleView = () => {
    configActions.updateConfig('myProjects', !myProjects)
    myProjects ? configActions.deleteConfig('params.user') : configActions.updateConfig('params.user', currentUserId)
    configActions.updateConfig('params.page', '1')
    projectsActions.fetchProjects()
  }

  const handleNew = () => {
    window.location.href = '/projects/create'
  }

  const handleImport = (file) => { projectsActions.uploadProject('/projects/import/', file) }

  const renderTitle = (title, row) => {
    const pathArray = getTitlePath(projects, title, row).split(' / ')
    const lastChild = pathArray.pop()

    const catalog = catalogs.find(c => c.id === row.catalog)

    return (
      <div>
        <a href={`/projects/${row.id}`}>
          {pathArray.map((path, index) => (
            <span key={index}>{path} / </span>
          ))}
          <b>{lastChild}</b>
        </a>
        {
          catalog && (
            <div className='text-muted' dangerouslySetInnerHTML={{ __html: catalog.title }} ></div>
          )
        }
      </div>
    )
  }

  const resetAllFilters = () => {
    configActions.deleteConfig('params.catalog')
    configActions.deleteConfig('params.created_after')
    setStartDate('created', null)
    configActions.deleteConfig('params.created_before')
    setEndDate('created', null)
    configActions.deleteConfig('params.last_changed_after')
    setStartDate('last_changed', null)
    configActions.deleteConfig('params.last_changed_before')
    setEndDate('last_changed', null)
    projectsActions.fetchProjects()
  }

  /* order of elements in 'visibleColumns' corresponds to order of columns in table */
  let visibleColumns = ['title', 'progress', 'last_changed', 'actions']
  let columnWidths

  if (myProjects) {
    visibleColumns.splice(2, 0, 'role')
    columnWidths = ['35%', '20%', '20%', '20%', '5%']
  } else {
    visibleColumns.splice(2, 0, 'created')
    visibleColumns.splice(2, 0, 'owner')
    columnWidths = ['35%', '10%', '20%', '20%', '20%', '5%']
  }

  const cellFormatters = {
    title: (content, row) => renderTitle(content, row),
    role: (_content, row) => {
      const { rolesString } = getUserRoles(row, currentUserId)
      return rolesString
    },
    owner: (_content, row) => row.owners.map(owner => `${owner.first_name} ${owner.last_name}`).join('; '),
    progress: (_content, row) => getProgressString(row),
    created: content => useFormattedDateTime(content, language),
    last_changed: content => useFormattedDateTime(content, language),
    actions: (_content, row) => {
      const rowUrl = `/projects/${row.id}`
      const path = `?next=${window.location.pathname}`
      const { isProjectManager, isProjectOwner } = getUserRoles(row, currentUserId, ['managers', 'owners'])
      return (
        <div className="icon-container">
          {(isProjectManager || isProjectOwner || isManager) &&
          <Link
            href={`${rowUrl}/update`}
            className="element-link fa fa-pencil"
            title={row.title}
            onClick={() => window.location.href = `${rowUrl}/update/${path}`}
          />
          }
          {(isProjectOwner || isManager) &&
          <Link
            href={`${rowUrl}/delete`}
            className="element-link fa fa-trash"
            title={row.title}
            onClick={() => window.location.href = `${rowUrl}/delete/${path}`}
          />
          }
        </div>
      )
    }
  }

  return (
    <div className="projects">
      <div className="projects-header-container">
        <h1>{headline}</h1>
        <div className="projects-header-buttons">
          {
            !isEmpty(invites) && myProjects && (
              <button className="btn btn-link" onClick={openInvitations}>
                <span className="badge badge-primary badge-invitations">
                  {invites.length}
                </span>
                {gettext('Pending invitations')}
              </button>
            )
          }
          {
            isManager && (
              <button className="btn btn-link" onClick={handleView}>
                {viewLinkText}
              </button>
            )
          }
          <button id="import-project" className="btn btn-link" onClick={openImport}>
            <i className="fa fa-download" aria-hidden="true"></i> {gettext('Import project')}
          </button>
          <button id="create-project" className="btn btn-link" onClick={handleNew}>
            <i className="fa fa-plus" aria-hidden="true"></i> {gettext('New project')}
          </button>
        </div>
      </div>
      <div className="projects-form">
        <div className="text-muted mb-10">
          {displayMessage}
        </div>
        <div className="search-container">
          <SearchField
            value={searchString}
            onChange={updateSearchString}
            onSearch={projectsActions.fetchProjects}
            placeholder={gettext('Search projects')}
            className="search-field"
          />
        </div>
        {
          showFilters && (
            <ProjectFilters
              catalogs={catalogs ?? []}
              config={config}
              configActions={configActions}
              isManager={isManager}
              projectsActions={projectsActions}
            />
          )
        }
        <div className="pull-right mt-5">
          {
            showFilters && (
              <Link className="element-link mr-10 mb-10" onClick={resetAllFilters}>
                {gettext('Reset all filters')}
              </Link>
            )
          }
          <Link className="element-link mb-10" onClick={toggleFilters}>
            {showFilters ? gettext('Hide filters') : gettext('Show filters')}
          </Link>
        </div>
      </div>
      <Table
        cellFormatters={cellFormatters}
        columnWidths={columnWidths}
        config={config}
        configActions={configActions}
        data={projects}
        hasNext={hasNext}
        headerFormatters={HEADER_FORMATTERS}
        projectsActions={projectsActions}
        showTopButton={showTopButton}
        scrollToTop={scrollToTop}
        sortableColumns={SORTABLE_COLUMNS}
        visibleColumns={visibleColumns}
      />
      <Modal {...invitationsModalProps}>
        <PendingInvitations invitations={invites} />
      </Modal>
      <Modal {...importModalProps}>
        <ProjectImport
          allowedTypes={allowedTypes}
          handleImport={handleImport}
          importUrls={importUrls ?? []} />
      </Modal>
    </div>
  )
}

Projects.propTypes = {
  config: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  currentUserObject: PropTypes.object.isRequired,
  projectsActions: PropTypes.object.isRequired,
  projectsObject: PropTypes.object.isRequired,
}

export default Projects
