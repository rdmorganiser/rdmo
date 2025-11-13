import React from 'react'
import { useSelector } from 'react-redux'
// import { isEmpty } from 'lodash'
import { Tile } from '../helper'

const Documents = () => {
  const { projectViews } = useSelector((state) => state.project) ?? {}
  const { project } = useSelector((state) => state.project.project) ?? {}
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
      <header className="d-flex justify-content-between align-items-center mb-3">
        <h5 className="mb-0">{gettext('Documents')}</h5>
        {/* <button
          type="button"
          id="snapshot-select"
          className="btn btn-link text-decoration-none"
        // onClick={openSnapshotDropdown}
        >
          <i className="bi bi-plus" aria-hidden="true"></i> {gettext('Snapshots')}
        </button> */}
        {/* <span className="dropdown">
              <button type="button" className="element-btn-link btn-link fa fa-plus" data-toggle="dropdown"
                title={gettext('Create snapshot')} aria-label={gettext('Create snapshot')}>
              </button>
              <ul className="dropdown-menu">
                <li onClick={() => null}>
                  <Link href="" onClick={() => null}>{'dummy1'}</Link>
                </li>
                <li onClick={() => null}>
                  <Link href="" onClick={() => null}>{'dummy2'}</Link>
                </li>
              </ul>
            </span> */}
        {perms.can_view_snapshot && (
          <span className="dropdown">
            <button
              type="button"
              id="snapshot-select"
              className="btn btn-link text-decoration-none"
              data-toggle="dropdown"
            // onClick={openSnapshot}
            >
              {gettext('Snapshots')}
            </button>
          </span>
        )}
      </header>
      <div className="container-fluid">
        <div className="row">
          {projectViews.map((view, index) => (
            // <Tile key={index} size={projectViews.length <= 8 ? 'normal' : 'compact'}>
            <Tile key={index} size={'normal'}>
              {renderView(view)}
            </Tile>
          ))}
        </div>
      </div >
      {'Work in progress: Documents Page '}
    </>
  )
}

export default Documents
