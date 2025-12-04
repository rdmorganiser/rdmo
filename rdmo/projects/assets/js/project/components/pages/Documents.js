import React, { useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'
import { Tile } from '../helper'
import { clearCurrentView, downloadDocument, openViewInContext, setLocation } from '../../actions/projectActions'
import { buildApiPath, buildLocationForView } from '../../utils/buildPaths'
import { isEmpty } from 'lodash'

const Documents = () => {
  const dispatch = useDispatch()
  const { project, projectAnswers, projectViews, snapshots } = useSelector((state) => state.project.project) ?? {}
  const { page, pageId, action, actionId, origin } = useSelector((state) => state.config)

  const selectedSnapshotId = page === 'snapshots' && pageId ? pageId : null

  const exportFormats = useSelector((state) => state.settings.export_formats) ?? {}
  const perms = project?.permissions ?? {}
  const currentView = useSelector((state) => state.project.currentView)
  const showTiles = !currentView && origin !== 'snapshots'

  const answerView = !isEmpty(projectAnswers)
    ? {
      id: 'answers',
      title: gettext('Project answers'),
      ...projectAnswers,
    }
    : null

  useEffect(() => {
    if (currentView) return
    if (!action) return

    let snapshotId = null
    let viewId = null

    if (page === 'documents') {
      if (action === 'answers') {
        viewId = 'answers'
      } else if (action === 'views' && actionId) {
        viewId = actionId
      }
    } else if (page === 'snapshots' && pageId) {
      snapshotId = pageId

      if (action === 'answers') {
        viewId = 'answers'
      } else if (action === 'views' && actionId) {
        viewId = actionId
      }
    }

    if (!viewId) return

    dispatch(openViewInContext({
      viewId,
      snapshotId,
      projectAnswers: viewId === 'answers' && !snapshotId ? answerView : undefined,
    }))
  }, [page, pageId, action, actionId, currentView, answerView, dispatch])

  const handleBack = () => {
    dispatch(clearCurrentView())

    if (origin === 'snapshots') {
      dispatch(setLocation({
        page: 'snapshots',
        pageId: undefined,
        action: undefined,
        actionId: undefined,
      }))
    } else if (page === 'snapshots' && pageId) {
      dispatch(setLocation({
        page: 'snapshots',
        pageId: String(pageId),
        action: undefined,
        actionId: undefined,
      }))
    } else {
      dispatch(setLocation({
        page: 'documents',
        pageId: undefined,
        action: undefined,
        actionId: undefined,
      }))
    }
  }

  const buildApiPathForView = (viewId, snapshotId) => {
    if (viewId === 'answers') {
      return snapshotId == null
        ? buildApiPath('answers')
        : buildApiPath('snapshots', snapshotId, 'answers')
    }

    return snapshotId == null
      ? buildApiPath('views', viewId)
      : buildApiPath('snapshots', snapshotId, 'views', viewId)
  }

  const handleSelectSnapshot = (snapshotId) => {
    const viewId = currentView?.id || 'answers'
    if (currentView) {
      dispatch(openViewInContext({
        viewId,
        snapshotId,
        answerView,
      }))

      const location = buildLocationForView(viewId, snapshotId)
      dispatch(setLocation(location))
    } else {
      if (snapshotId == null) {
        dispatch(setLocation({
          page: 'documents',
          pageId: undefined,
          action: undefined,
          actionId: undefined,
        }))
      } else {
        dispatch(setLocation({
          page: 'snapshots',
          pageId: String(snapshotId),
          action: undefined,
          actionId: undefined,
        }))
      }
    }
  }

  const handleTileClick = (viewId, answerView = {}) => {
    const snapshotId = selectedSnapshotId

    dispatch(openViewInContext({
      viewId,
      snapshotId,
      projectAnswers: answerView
    }))

    const location = buildLocationForView(viewId, snapshotId)
    dispatch(setLocation({
      ...location,
      origin: 'documents'
    }))
  }

  const handleDownload = (path, format) => {
    dispatch(downloadDocument(path, format))
  }

  const renderExportFormatMenuItems = (viewId) => {
    const apiPath = buildApiPathForView(viewId, selectedSnapshotId)
    if (!Array.isArray(exportFormats) || exportFormats.length === 0) {
      return (
        <li className="dropdown-item text-muted">
          {gettext('No export formats available')}
        </li>
      )
    }

    return exportFormats.map(([value, label]) => (
      <li key={value}>
        <button
          type="button"
          className="dropdown-item"
          onClick={(event) => {
            event.stopPropagation()  // prevent Tile onClick
            handleDownload(apiPath, value)
          }}
        >
          {label}
        </button>
      </li>
    ))
  }

  const renderViewTile = (view) => {
    return (
      <div className="d-flex">
        <div
          className="d-flex align-items-center justify-content-center me-3 flex-shrink-0"
          style={{
            width: '48px',
            height: '48px',
            backgroundColor: '#a8d5c2',
            borderRadius: '8px',
          }}
        >
          <i
            className="bi bi-file-earmark-text"
            style={{ fontSize: '24px', color: '#fff' }}
          />
        </div>

        <div className="flex-grow-1 d-flex flex-column">
          <div className="d-flex justify-content-between align-items-start mb-1">
            <div className="fw-bold">{view.title}</div>
            <div className="dropdown ms-2">
              <button
                type="button"
                className="btn btn-link p-0 text-decoration-none"
                data-bs-toggle="dropdown"
                aria-expanded="false"
                onClick={(event) => event.stopPropagation()}
                title={gettext('Download')}
              >
                <i className="bi bi-download" style={{ fontSize: '1.1rem' }} />
              </button>

              <ul className="dropdown-menu dropdown-menu-end">
                {renderExportFormatMenuItems(view.id)}
              </ul>
            </div>
          </div>

          {view.help && (
            <div className="text-muted small mb-2">
              <Html html={view.help} />
            </div>
          )}
        </div>
      </div>
    )
  }

  return (
    <>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2 className="mb-0">{gettext('Documents')}</h2>
        <div className="d-flex align-items-center gap-2">
          {currentView && <span className="dropdown">
            <button type="button" className="link link bi" data-bs-toggle="dropdown"
              title={gettext('Export')} aria-label={gettext('Export')}>
              {gettext('Export')}
              <i className="bi bi-caret-down-fill ms-1" />
            </button>
            <ul className="dropdown-menu dropdown-menu-end">
              {renderExportFormatMenuItems(currentView?.id || 'answers')}
            </ul>
          </span>}
          {perms.can_view_snapshot && (
            <span className="dropdown">
              <button type="button" className="link link bi" data-bs-toggle="dropdown"
                title={gettext('Snapshots')} aria-label={gettext('Snapshots')}>
                {gettext('Snapshots')}
                <i className="bi bi-caret-down-fill ms-1" />
              </button>
              <ul className="dropdown-menu dropdown-menu-end">
                <li key="current">
                  <a
                    rel="noreferrer"
                    className="dropdown-item"
                    onClick={() => handleSelectSnapshot(null)}
                  >
                    {selectedSnapshotId === null && (
                      <i
                        className="bi bi-arrow-right me-1"
                        aria-hidden="true"
                      />
                    )}
                    {gettext('Current')}
                  </a>
                </li>
                {snapshots?.map((snapshot) => (
                  <li key={String(snapshot.id)}>
                    <a
                      rel="noreferrer"
                      className="dropdown-item"
                      onClick={() => handleSelectSnapshot(String(snapshot.id))}
                    >
                      {selectedSnapshotId === String(snapshot.id) && (
                        <i
                          className="bi bi-arrow-right me-1"
                          aria-hidden="true"
                        />
                      )}
                      {snapshot.title}
                    </a>
                  </li>
                ))}
              </ul>
            </span>
          )}
        </div>
      </div>
      {showTiles ? (
        <>
          {!isEmpty(projectAnswers) &&
            <Tile key={answerView.id} size={'compact'} onClick={() => handleTileClick(answerView.id, answerView)}>
              {renderViewTile(answerView)}
            </Tile>}
          {projectViews?.length > 0 && (
            <div className="container-fluid">
              <h3 className="mb-3">{gettext('Data management plans')}</h3>
              <div className="row">
                {projectViews.map((view) => (
                  <Tile key={view.id} size={'compact'} onClick={() => handleTileClick(view.id)}>
                    {renderViewTile(view)}
                  </Tile>
                ))}
              </div>
            </div>
          )}
        </>
      ) : (
        <div className="mt-3">
          <button
            type="button"
            className="btn btn-link p-0 mb-3"
            onClick={handleBack}
          >
            <i className="bi bi-arrow-left me-1" />
            {gettext('Back')}
          </button>

          {currentView ? (
            <>
              <Html html={currentView.html} />
            </>
          ) : (
            <div className="text-muted">
              {gettext('Loading view …')}
            </div>
          )}
        </div>
      )}
    </>
  )
}

export default Documents
