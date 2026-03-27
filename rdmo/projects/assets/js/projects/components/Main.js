import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { get, isEmpty } from 'lodash'

import { Modal } from 'rdmo/core/assets/js/_bs53/components'
import * as configActions from 'rdmo/core/assets/js/actions/configActions'
import { Link, SearchField } from 'rdmo/core/assets/js/components'
import { useFormattedDateTime, useModal, useScrollToTop } from 'rdmo/core/assets/js/hooks'
import { language } from 'rdmo/core/assets/js/utils'
import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

import * as projectsActions from '../actions/projectsActions'
import { HEADER_FORMATTERS, SORTABLE_COLUMNS } from '../utils'

import ProjectDeleteModal from '../../project/components/areas/information/ProjectDeleteModal'
import ProjectForm from '../../project/components/areas/information/ProjectForm'

import { PendingInvitations, ProjectFilters, ProjectImport, Table } from './helper'

const Main = () => {
  const dispatch = useDispatch()

  const config = useSelector(state => state.config)
  const projectsObject = useSelector(state => state.projects)
  const currentUserObject = useSelector(state => state.currentUser)

  const [selectedProject, setSelectedProject] = useState(null)

  const { showTopButton, scrollToTop } = useScrollToTop()

  const { show: showInvitations, open: openInvitations, close: closeInvitations } = useModal()
  const { show: showImport, open: openImport, close: closeImport } = useModal()
  const { show: showEdit, open: openEdit, close: closeEdit } = useModal()
  const { show: showCreate, open: openCreate, close: closeCreate } = useModal()
  const { show: showDelete, open: openDelete, close: closeDelete } = useModal()
  const { show: showCopy, open: openCopy, close: closeCopy } = useModal()

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

  const createModalProps = {
    title: gettext('Create new project'),
    size: 'modal-lg',
    show: showCreate,
    onClose: closeCreate,
    onSubmit: () => { },
    submitLabel: gettext('Create project'),
    submitProps: {
      type: 'submit',
      form: 'project-create-form'
    }
  }

  const handleCloseCopy = () => {
    setSelectedProject(null)
    closeCopy()
  }

  const copyModalProps = {
    title: gettext('Copy project'),
    size: 'modal-lg',
    show: showCopy,
    onClose: handleCloseCopy,
    onSubmit: () => { },
    submitLabel: gettext('Copy project'),
    submitProps: {
      type: 'submit',
      form: 'project-copy-form'
    }
  }

  const handleCloseEdit = () => {
    setSelectedProject(null)
    closeEdit()
  }

  const editModalProps = {
    title: gettext('Update project'),
    size: 'modal-lg',
    show: showEdit,
    onClose: handleCloseEdit,
    onSubmit: () => { },
    submitLabel: gettext('Update project'),
    submitProps: {
      type: 'submit',
      form: 'project-edit-form'
    }
  }

  const handleCloseDelete = () => {
    setSelectedProject(null)
    closeDelete()
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

  const handleImport = (file) => {
    dispatch(projectsActions.uploadProject('/projects/import/', file))
  }

  const buildAncestorLink = (ancestors) => {
    if (!Array.isArray(ancestors) || ancestors.length === 0) return null

    const current = ancestors[ancestors.length - 1]
    const href = `${baseUrl}/projects/${current.id}`

    const parts = ancestors.map((ancestor, ancestorIndex) => {
      const content = ancestorIndex === ancestors.length - 1? <span className="fw-bold">{ancestor.title}</span>: ancestor.title

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
            <div className="text-secondary">{catalog.title}</div>
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
      <div className="d-flex position-relative">
        {
          projects.length > 0 && showTopButton &&
          <button type="button" className="btn btn-light btn-rounded font-small" onClick={scrollToTop}
            title={gettext('Scroll to top')} aria-label={gettext('Scroll to top')}>
            <i className="bi bi-arrow-up" aria-hidden="true"></i>
          </button>
        }
        {
          hasNext &&
          <button type="button" onClick={loadMore}
            className="btn btn-light btn-rounded font-small position-absolute start-50 translate-middle-x">
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
  const visibleColumns = myProjects? ['title', 'progress', 'role', 'last_changed', 'actions']: ['title', 'progress', 'owner', 'created', 'last_changed', 'actions']

  const columnWidths = myProjects? ['40%', '16%', '20%', '18%', '6%']: ['30%', '16%', '16%', '16%', '16%', '6%']

  const cellFormatters = {
    title: (_content, row) => renderTitle(row),
    role: (_content, row) => {
      const highestRoleString = (row.highest_role && row.highest_role.project_id != row.id) ? (
        <>
          {interpolate(gettext('%s of '), [row.highest_role.role_display])}
          <a href={`${baseUrl}/projects/${row.highest_role.project_id}`}>
            {row.highest_role.project_title}
          </a>
        </>
      ) : null

      return <>
        {
          row.current_role && <div>{row.current_role.role_display}</div>
        }
        {
          row.highest_role && <div className="text-secondary">{highestRoleString}</div>
        }
        {
          row.visibility && <div className="text-secondary">{row.visibility}</div>
        }
      </>
    },
    owner: (_content, row) => (
      <>
        <div>
          {row.owners.map(owner => owner.full_name).join('; ')}
        </div>
        {
          row.visibility && <div className="text-secondary">{row.visibility}</div>
        }
      </>
    ),
    progress: (_content, row) => getProgressString(row),
    created: content => useFormattedDateTime(content, language),
    last_changed: content => useFormattedDateTime(content, language),
    actions: (_content, row) => {
      const perms = row.permissions || {}
      return (
        <div className="d-flex align-items-center gap-1">
          <Link
            className="bi bi-copy"
            title={labels.copy}
            onClick={
              () => {
                setSelectedProject(row)
                openCopy()
              }
            }
          />
          {
            perms.can_change_project &&
            <Link
              className="bi bi-pencil"
              title={labels.update}
              onClick={
                () => {
                  setSelectedProject(row)
                  openEdit()
                }
              }
            />
          }
          {
            perms.can_delete_project &&
            <Link
              className="bi bi-trash"
              title={labels.delete}
              onClick={
                () => {
                  setSelectedProject(row)
                  openDelete()
                }
              }
            />
          }
        </div>
      )
    }
  }

  return (
    <div className="px-4 py-5">
      <div className="container gx-0">
        <div className="projects">
          <div className="d-flex align-items-center gap-3 mb-3">
            <h1 className="me-auto mb-0">{headline}</h1>
            {
              !isEmpty(invites) && myProjects && (
                <button type="button" className="link" onClick={openInvitations}>
                  <div className="d-flex align-items-center gap-1">
                    <span className="badge rounded-pill text-bg-primary">
                      {invites.length}
                    </span>
                    {gettext('Pending invitations')}
                  </div>
                </button>
              )
            }
            {
              isAdminOrSiteManager && (
                <button type="button" className="link font-small" onClick={handleView}>
                  {viewLinkText}
                </button>
              )
            }
            <button type="button" className="link font-small" onClick={openImport}>
              <i className="bi bi-download" aria-hidden="true"></i> {gettext('Import project')}
            </button>
            <button type="button" className="link font-small" onClick={openCreate}>
              <i className="bi bi-plus" aria-hidden="true"></i> {gettext('New project')}
            </button>
          </div>

          <div className="projects-form my-5">
            <div className="text-muted mb-3">
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
          <Modal {...editModalProps}>
            {
              selectedProject && (
                <ProjectForm
                  key={`edit-${selectedProject.id}`}
                  disabled={false}
                  formId="project-edit-form"
                  submitMode="submit"
                  mode="edit"
                  currentProject={selectedProject}
                  catalogs={catalogs ?? []}
                  onSaved={
                    () => {
                      handleCloseEdit()
                      dispatch(projectsActions.refetchLoadedPages())
                    }
                  }
                />
              )
            }
          </Modal>
          <Modal {...copyModalProps}>
            {
              selectedProject && (
                <ProjectForm
                  key={`copy-${selectedProject.id}`}
                  disabled={false}
                  formId="project-copy-form"
                  submitMode="submit"
                  mode="copy"
                  currentProject={selectedProject}
                  catalogs={catalogs ?? []}
                  onSaved={handleCloseCopy}
                />
              )
            }
          </Modal>
          <Modal {...createModalProps}>
            <ProjectForm
              key={`create-${showCreate}`}
              disabled={false}
              formId="project-create-form"
              submitMode="submit"
              mode="create"
              catalogs={catalogs ?? []}
              onSave={closeCreate}
            />
          </Modal>
          <ProjectDeleteModal
            project={selectedProject}
            id={selectedProject?.id}
            show={showDelete}
            onClose={handleCloseDelete}
            onDeleted={() => dispatch(projectsActions.refetchLoadedPages())}
          />
        </div>
      </div>
    </div>
  )
}

export default Main
