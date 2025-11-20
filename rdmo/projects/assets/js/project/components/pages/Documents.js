import React from 'react'
import { useSelector } from 'react-redux'

// import { baseUrl } from 'rdmo/core/assets/js/utils/meta'
import Html from 'rdmo/core/assets/js/components/Html'
import { Tile } from '../helper'

const Documents = () => {
  const { projectViews } = useSelector((state) => state.project) ?? {}
  const { project, snapshots } = useSelector((state) => state.project.project) ?? {}
  const perms = project?.permissions ?? {}

  const renderView = (view) => {
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
          <div className="fw-bold mb-1">{view.title}</div>

          {view.help && (
            <div className="text-muted small mb-2">
              <Html html={view.help} />
            </div>
          )}

          <a href="#" className="text-decoration-none mt-auto">
            {gettext('Download')} <i className="bi bi-chevron-down" />
          </a>
        </div>
      </div>
    )
  }

  return (
    <>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2 className="mb-0">{gettext('Documents')}</h2>
        {perms.can_view_snapshot && (
          <span className="dropdown">
            <button type="button" className="link link bi" data-bs-toggle="dropdown"
              title={gettext('Snapshots')} aria-label={gettext('Snapshots')}>  {gettext('Snapshots')}</button>
            <ul className="dropdown-menu dropdown-menu-end">
              <li key="current">
                <a
                  // href={`${baseUrl}/projects/${project.id}/views/${view.id}`}
                  href="#"
                  rel="noreferrer"
                  className="dropdown-item"
                >
                  {gettext('Current')}
                </a>
              </li>
              {snapshots.map((snapshot) => (
                <li key={snapshot.id}>
                  <a
                    href="#"
                    rel="noreferrer"
                    className="dropdown-item"
                  >
                    {snapshot.title}
                  </a>
                </li>
              ))}
            </ul>
          </span>
        )}
      </div>
      {projectViews.length > 0 && (
        <div className="container-fluid">
          <h3 className="mb-3">{gettext('Data management plans')}</h3>
          <div className="row">
            {projectViews.map((view) => (
              <Tile key={view.id} size={'compact'}>
                {renderView(view)}
              </Tile>
            ))}
          </div>
        </div >
      )}
      {/* TODO: answers */}
    </>
  )
}

export default Documents
