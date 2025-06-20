import React from 'react'
import PropTypes from 'prop-types'
import { get, isEmpty } from 'lodash'

import { Link, Modal, SearchField } from 'rdmo/core/assets/js/components'
import { useFormattedDateTime, useModal, useScrollToTop }  from 'rdmo/core/assets/js/hooks'
import { language } from 'rdmo/core/assets/js/utils'
import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

import { PendingInvitations, ProjectFilters, ProjectImport, Table } from '../helper'
import { getTitlePath, getUserRoles, userIsManager, HEADER_FORMATTERS, SORTABLE_COLUMNS } from '../../utils'

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

  const displayMessage = interpolate(gettext('%s of %s projects are displayed'), [projects.length > projectsCount ? projectsCount : projects.length, projectsCount])

  const getProgressString = (row) => {
    return (row.progress_total ?  interpolate(gettext('%s of %s'), [row.progress_count ?? 0, row.progress_total]) : null)
  }

  const currentUserId = currentUser.id
  const isManager = userIsManager(currentUser)

  const searchString = get(config, 'params.search', '')
  const updateSearchString = (value) => {
    value ? configActions.updateConfig('params.search', value) : configActions.deleteConfig('params.search')
  }

  const viewLinkText = myProjects ? gettext('View all projects') : gettext('View my projects')
  const headline = myProjects ? gettext('My projects') : gettext('All projects')

  // inlining the title attributes caused problems with django's translation system
  const labels = {
    copy: gettext('Copy project'),
    update: gettext('Update project'),
    delete: gettext('Delete project')
  }

  const handleView = () => {
    configActions.updateConfig('myProjects', !myProjects)
    projectsActions.fetchProjects()
  }

  const handleNew = () => {
    window.location.href = `${baseUrl}/projects/create/`
  }

  const handleImport = (file) => {
    projectsActions.uploadProject('/projects/import/', file)
  }

  const renderTitle = (title, row) => {
    const pathArray = getTitlePath(projects, title, row).split(' / ')
    const lastChild = pathArray.pop()

    const catalog = catalogs.find(c => c.id === row.catalog)

    return (
      <div>
        <a href={`${baseUrl}/projects/${row.id}/`}>
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

  const loadMore = () => {
    const page = get(config, 'params.page') ?? 1
    configActions.updateConfig('params.page', (parseInt(page) + 1).toString())
    projectsActions.fetchProjects(false)
  }

  const renderLoadButtons = () => {
    return (
          <div className="icon-container ml-auto">
            {projects.length > 0 && showTopButton &&
              <button type="button" className="elliptic-button" onClick={scrollToTop}
                      title={gettext('Scroll to top')} aria-label={gettext('Scroll to top')}>
                <i className="fa fa-arrow-up" aria-hidden="true"></i>
              </button>
            }
            {hasNext &&
            <button type="button" onClick={loadMore} className="elliptic-button">
              {gettext('Load more')}
            </button>
            }
          </div>
    )
  }

  /* order of elements in 'visibleColumns' corresponds to order of columns in table */
  let visibleColumns = ['title', 'progress', 'last_changed', 'actions']
  let columnWidths

  if (myProjects) {
    visibleColumns.splice(2, 0, 'role')
    columnWidths = ['40%', '18%', '18%', '18%', '6%']
  } else {
    visibleColumns.splice(2, 0, 'created')
    visibleColumns.splice(2, 0, 'owner')
    columnWidths = ['30%', '10%', '18%', '18%', '18%', '6%']
  }

  const cellFormatters = {
    title: (content, row) => renderTitle(content, row),
    role: (_content, row) => {
      const { rolesString } = getUserRoles(row, currentUserId)
      return <>
        {
          rolesString && <p>{rolesString}</p>
        }
        {
          row.visibility && <p className="text-muted">{row.visibility}</p>
        }
      </>
    },
    owner: (_content, row) => (
      <>
        <p>
          {row.owners.map(owner => owner.full_name).join('; ')}
        </p>
        {
          row.visibility && <p className="text-muted">{row.visibility}</p>
        }
      </>
    ),
    progress: (_content, row) => getProgressString(row),
    created: content => useFormattedDateTime(content, language),
    last_changed: content => useFormattedDateTime(content, language),
    actions: (_content, row) => {
      const rowUrl = `${baseUrl}/projects/${row.id}`
      const params = `?next=${window.location.pathname}`
      const { isProjectManager, isProjectOwner } = getUserRoles(row, currentUserId, ['managers', 'owners'])

      return (
        <div className="icon-container">
          <Link
            href={`${rowUrl}/copy/`}
            className="fa fa-copy"
            title={labels.copy}
            onClick={() => window.location.href = `${rowUrl}/copy/${params}`}
          />
          {(isProjectManager || isProjectOwner || isManager) &&
            <Link
              href={`${rowUrl}/update/`}
              className="fa fa-pencil"
              title={labels.update}
              onClick={() => window.location.href = `${rowUrl}/update/${params}`}
            />
          }
          {(isProjectOwner || isManager) &&
            <Link
              href={`${rowUrl}/delete/`}
              className="fa fa-trash"
              title={labels.delete}
              onClick={() => window.location.href = `${rowUrl}/delete/${params}`}
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
              <button type="button" className="btn btn-link" onClick={openInvitations}>
                <span className="badge badge-primary badge-invitations">
                  {invites.length}
                </span>
                {gettext('Pending invitations')}
              </button>
            )
          }
          {
            isManager && (
              <button type="button" className="btn btn-link" onClick={handleView}>
                {viewLinkText}
              </button>
            )
          }
          <button type="button" id="import-project" className="btn btn-link" onClick={openImport}>
            <i className="fa fa-download" aria-hidden="true"></i> {gettext('Import project')}
          </button>
          <button type="button" id="create-project" className="btn btn-link" onClick={handleNew}>
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
            onSearch={() => projectsActions.fetchProjects()}
            placeholder={gettext('Search projects')}
            className="search-field"
          />
        </div>
        <ProjectFilters
          catalogs={catalogs ?? []}
          config={config}
          configActions={configActions}
          isManager={isManager}
          projectsActions={projectsActions}
        />
      </div>
      <Table
        cellFormatters={cellFormatters}
        columnWidths={columnWidths}
        config={config}
        configActions={configActions}
        data={projects}
        headerFormatters={HEADER_FORMATTERS}
        projectsActions={projectsActions}
        sortableColumns={SORTABLE_COLUMNS}
        visibleColumns={visibleColumns}
      />

      {renderLoadButtons()}

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
