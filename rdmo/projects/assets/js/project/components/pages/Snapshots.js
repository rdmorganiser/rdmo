import React from 'react'
import { useSelector } from 'react-redux'
import { isEmpty } from 'lodash'

import { useModal } from 'rdmo/core/assets/js/hooks'

import SnapshotsTable from './SnapshotsTable'
import SnapshotModal from './SnapshotModal'

const Snapshots = () => {
  const { show: showSnapshot, open: openSnapshot, close: closeSnapshot } = useModal()

  const { snapshots, project } = useSelector((state) => state.project.project) ?? {}
  const perms = project?.permissions ?? {}

  return (
    <>
      <header className="d-flex justify-content-between align-items-center mb-3">
        <h5 className="mb-0">{gettext('Snapshots')}</h5>
        {perms.can_add_snapshot && (
          <>
            <button
              type="button"
              id="add-snapshot"
              className="btn btn-link text-decoration-none"
              onClick={openSnapshot}
            >
              <i className="bi bi-plus" aria-hidden="true"></i> {gettext('Create snapshot')}
            </button>
          </>
        )}
      </header>
      {
        !isEmpty(snapshots) && perms.can_view_snapshot && (
          <SnapshotsTable snapshots={snapshots} />
        )
      }
      <SnapshotModal show={showSnapshot} onClose={closeSnapshot} />
    </>
  )
}

export default Snapshots
