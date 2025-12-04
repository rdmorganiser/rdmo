import React, { useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'
import { Tile } from '../helper'
import { clearCurrentView, downloadDocument, openViewInContext, setLocation } from '../../actions/projectActions'
import { buildLocationForView } from '../../utils/buildLocationForView'
import { isEmpty } from 'lodash'

const Documents = () => {
  const dispatch = useDispatch()
  const { project, projectAnswers, projectViews, snapshots } = useSelector((state) => state.project.project) ?? {}
  const { page, pageId, action, actionId, origin } = useSelector((state) => state.config)

  const selectedSnapshotId = page === 'snapshots' && pageId ? pageId : null

  const exportFormats = useSelector((state) => state.settings.export_formats) ?? {}
  const perms = project?.permissions ?? {}
  const currentView = useSelector((state) => state.project.currentView)
  const hasActions = (action === 'views' && !!actionId) || action === 'answers'
  const showTiles = !hasActions && origin !== 'snapshots'

  const answerView = !isEmpty(projectAnswers)
    ? {
      id: 'answers',
      title: gettext('Project answers'),
      ...projectAnswers,
    }
    : null

  useEffect(() => {
    if (!hasActions) return

    const snapshotId =
      page === 'snapshots' && pageId
        ? pageId
        : null

    const viewId = action === 'answers'
      ? 'answers'
      : actionId

    if (!viewId) return

    const answersViewForProject =
      viewId === 'answers' && !snapshotId
        ? answerView
        : undefined

    dispatch(openViewInContext({
      viewId,
      snapshotId,
      projectAnswers: answersViewForProject,
    }))
  }, [page, pageId, action, actionId, projectAnswers, dispatch])

  const handleBack = () => {
    dispatch(clearCurrentView())
    if (origin === 'snapshots') {
      dispatch(setLocation(
        buildLocationForView(null, null, { basePage: 'snapshots' })
      ))
    } else if (page === 'snapshots' && pageId) {
      dispatch(setLocation(
        buildLocationForView(null, pageId)
      ))
    } else {
      dispatch(setLocation(
        buildLocationForView(null, null)
      ))
    }
  }

  const handleSelectSnapshot = (snapshotId) => {
    if (hasActions) {
      const viewId = currentView?.id || 'answers'
      const location = buildLocationForView(viewId, snapshotId)
      dispatch(setLocation(location))
    } else {
      dispatch(setLocation(
        buildLocationForView(null, snapshotId)
      ))
    }
  }

  const handleTileClick = (viewId) => {
    const snapshotId = selectedSnapshotId
    const location = buildLocationForView(viewId, snapshotId)
    dispatch(setLocation({
      ...location,
      origin: 'documents'
    }))
  }

  const renderExportFormatMenuItems = () => {
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
            dispatch(downloadDocument(window.location.pathname, value))
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
                {renderExportFormatMenuItems()}
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
          {hasActions && <span className="dropdown">
            <button type="button" className="link link bi" data-bs-toggle="dropdown"
              title={gettext('Export')} aria-label={gettext('Export')}>
              {gettext('Export')}
              <i className="bi bi-caret-down-fill ms-1" />
            </button>
            <ul className="dropdown-menu dropdown-menu-end">
              {renderExportFormatMenuItems()}
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
            <Tile key={answerView.id} size={'compact'} onClick={() => handleTileClick(answerView.id)}>
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
