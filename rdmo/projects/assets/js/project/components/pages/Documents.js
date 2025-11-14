import React from 'react'
import { useSelector } from 'react-redux'
// import { isEmpty } from 'lodash'
import { Tile } from '../helper'

const Documents = () => {
  const { projectViews } = useSelector((state) => state.project) ?? {}
  const { project, snapshots } = useSelector((state) => state.project.project) ?? {}
  const perms = project?.permissions ?? {}

  // const renderView = (view) => {
  //   return (
  //     <div className="p-2">
  //       <div className="fw-bold mb-1">{view.title}</div>

  //       {view.description && (
  //         <div className="text-muted small mb-2">
  //           {view.description}
  //         </div>
  //       )}

  //       <a href="#" className="text-decoration-none">
  //         {gettext('Download')} <i className="bi bi-chevron-down"></i>
  //       </a>
  //     </div>
  //   )
  // }

  const renderView = (view) => {
    return (
      <div className="d-flex">
        <div
          className="d-flex align-items-center justify-content-center"
          style={{
            width: '64px',
            backgroundColor: '#a8d5c2',
            borderRadius: '4px 0 0 4px',
          }}
        >
          <i className="bi bi-file-earmark-text" style={{ fontSize: '32px', color: '#fff' }}></i>
        </div>
        <div className="p-3 flex-grow-1">
          <div className="fw-bold mb-1">{view.title}</div>
          {view.description && (
            <div className="text-muted small mb-2">
              {view.description}
            </div>
          )}
          <a href="#" className="text-decoration-none">
            {gettext('Download')} <i className="bi bi-chevron-down"></i>
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
            {projectViews.map((view, index) => (
              // <Tile key={index} size={projectViews.length <= 8 ? 'normal' : 'compact'}>
              <Tile key={index} size={'normal'}>
                {renderView(view)}
              </Tile>
            ))}
          </div>
        </div >
      )}
      {'Work in progress: Documents Page '}
    </>
  )
}

export default Documents
