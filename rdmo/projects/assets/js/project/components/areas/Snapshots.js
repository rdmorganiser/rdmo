import React from 'react'
import { useSelector } from 'react-redux'
import { isEmpty } from 'lodash'

import { useModal } from 'rdmo/core/assets/js/hooks'

import SnapshotModal from './snapshots/SnapshotModal'
import SnapshotTable from './snapshots/SnapshotTable'

const Snapshots = () => {
  const { show: showSnapshot, open: openSnapshot, close: closeSnapshot } = useModal()

  const { snapshots, project } = useSelector((state) => state.project.project) ?? {}
  const perms = project?.permissions ?? {}

  return (
    <div className="project-snapshots">
      <div className="d-lg-flex justify-content-between align-items-center mb-5">
        <h1 className="mb-lg-0">{gettext('Snapshots')}</h1>
        {
          perms.can_add_snapshot && (
            <button type="button" className="btn link small" onClick={openSnapshot}>
              <i className="bi bi-plus" aria-hidden="true"></i> {gettext('Create snapshot')}
            </button>
          )
        }
      </div>
      {
        !isEmpty(snapshots) && perms.can_view_snapshot && (
          <SnapshotTable snapshots={snapshots} />
        )
      }
      <SnapshotModal show={showSnapshot} onClose={closeSnapshot} />
    </div>
  )
}

export default Snapshots
