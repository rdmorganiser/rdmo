import React from 'react'
import { useDispatch, useSelector } from 'react-redux'

import { get, isEmpty } from 'lodash'

import { Link, Modal, SearchField } from 'rdmo/core/assets/js/components'
import { useFormattedDateTime, useModal, useScrollToTop } from 'rdmo/core/assets/js/hooks'
import { language } from 'rdmo/core/assets/js/utils'
import { baseUrl } from 'rdmo/core/assets/js/utils/meta'
import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import * as projectsActions from '../actions/projectsActions'

import { PendingInvitations, ProjectFilters, ProjectImport, Table } from './helper'
import { HEADER_FORMATTERS, SORTABLE_COLUMNS } from '../utils'
import { roleOptions } from '../../common/constants/roles'

const Projects = () => {
  const dispatch = useDispatch()

  const config = useSelector(state => state.config)
  const projectsObject = useSelector(state => state.projects)
  const currentUserObject = useSelector(state => state.currentUser)

  const { showTopButton, scrollToTop } = useScrollToTop()

  const { show: showInvitations, open: openInvitations, close: closeInvitations } = useModal()
  const { show: showImport, open: openImport, close: closeImport } = useModal()

  if (!projectsObject.ready) return null
  const { allowedTypes, catalogs, importUrls, invites, projects, projectsCount, hasNext } = projectsObject
  const { currentUser } = currentUserObject
  const { myProjects } = config

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
    return (row.progress_total ? interpolate(gettext('%s of %s'), [row.progress_count ?? 0, row.progress_total]) : null)
  }

  const isAdminOrSiteManager = currentUser.is_superuser || currentUser.is_site_manager

  const searchString = get(config, 'params.search', '')
  const updateSearchString = (value) => {
    value ? dispatch(configActions.updateConfig('params.search', value)) : dispatch(configActions.deleteConfig('params.search'))
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
    dispatch(configActions.updateConfig('myProjects', !myProjects))
    dispatch(projectsActions.fetchProjects())
  }

  const handleNew = () => {
    window.location.href = `${baseUrl}/projects/create/`
  }

  const handleImport = (file) => {
    dispatch(projectsActions.uploadProject('/projects/import/', file))
  }

  const buildAncestorLink = (ancestors) => {
    if (!Array.isArray(ancestors) || ancestors.length === 0) return null

    const current = ancestors[ancestors.length - 1]
    const href = `${baseUrl}/projects/${current.id}`

    const parts = ancestors.map((ancestor, ancestorIndex) => {
      const content = ancestorIndex === ancestors.length - 1
        ? <span className="fw-bold">{ancestor.title}</span>
        : ancestor.title

      return (
        <React.Fragment key={ancestorIndex}>
          {ancestorIndex > 0 && ' / '}
          {content}
        </React.Fragment>
      )
    })

    return <a href={href}>{parts}</a>
  }

  const renderTitle = (row) => {
    const catalog = catalogs.find(c => c.id === row.catalog)

    return (
      <div>
        {buildAncestorLink(row.ancestors)}
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
    dispatch(configActions.updateConfig('params.page', (parseInt(page) + 1).toString()))
    dispatch(projectsActions.fetchProjects(false))
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

  const ordering = get(config, 'params.ordering')
  const sortOrder = ordering ? (ordering.startsWith('-') ? 'desc' : 'asc') : undefined
  const sortColumn = ordering ? (ordering.startsWith('-') ? ordering.substring(1) : ordering) : undefined

  const handleHeaderClick = (column) => {
    if (sortColumn === column) {
      if (sortOrder === 'asc') {
        dispatch(configActions.updateConfig('params.ordering', `-${column}`))
      } else if (sortOrder === 'desc') {
        dispatch(configActions.deleteConfig('params.ordering'))
      } else {
        dispatch(configActions.updateConfig('params.ordering', column))
      }
    } else {
      dispatch(configActions.updateConfig('params.ordering', column))
    }
    dispatch(projectsActions.fetchProjects())
  }

  /* order of elements in 'visibleColumns' corresponds to order of columns in table */
  const visibleColumns = myProjects
    ? ['title', 'progress', 'role', 'last_changed', 'actions']
    : ['title', 'progress', 'owner', 'created', 'last_changed', 'actions']

  const columnWidths = myProjects
    ? ['40%', '18%', '18%', '18%', '6%']
    : ['30%', '10%', '18%', '18%', '18%', '6%']

  const cellFormatters = {
    title: (_content, row) => renderTitle(row),
    role: (_content, row) => {
      const rolesString = roleOptions.find(option => option.value == row.current_role)?.label || ''

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
      const perms = row.permissions || {}
      return (
        <div className="icon-container">
          <Link
            href={`${rowUrl}/copy/`}
            className="fa fa-copy"
            title={labels.copy}
            onClick={() => window.location.href = `${rowUrl}/copy/${params}`}
          />
          {perms.can_change_project &&
            <Link
              href={`${rowUrl}/update/`}
              className="fa fa-pencil"
              title={labels.update}
              onClick={() => window.location.href = `${rowUrl}/update/${params}`}
            />
          }
          {perms.can_delete_project &&
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
            isAdminOrSiteManager && (
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
            onSearch={() => dispatch(projectsActions.fetchProjects())}
            placeholder={gettext('Search projects')}
            className="search-field"
          />
        </div>
        <ProjectFilters
          catalogs={catalogs ?? []}
          isAdminOrSiteManager={isAdminOrSiteManager}
        />
      </div>
      <Table
        cellFormatters={cellFormatters}
        columnWidths={columnWidths}
        data={projects}
        headerFormatters={HEADER_FORMATTERS}
        onHeaderClick={handleHeaderClick}
        sortableColumns={SORTABLE_COLUMNS}
        sortColumn={sortColumn}
        sortOrder={sortOrder}
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

export default Projects
