import React, { useState } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import PropTypes from 'prop-types'
import { useFormattedDateTime } from 'rdmo/core/assets/js/hooks'
import { language } from 'rdmo/core/assets/js/utils'

import { useModal } from 'rdmo/core/assets/js/hooks'

import { setLocation } from '../../actions/projectActions'
import SnapshotModal from './SnapshotModal'
import { buildLocationForView } from '../../utils/buildLocationForView'
import SnapshotRollbackModal from './SnapshotRollbackModal'

const SnapshotsTable = ({ snapshots }) => {
  const dispatch = useDispatch()
  const { project } = useSelector((state) => state.project.project) || {}
  const perms = project?.permissions || {}

  const { show: showUpdate, open: openUpdate, close: closeUpdate } = useModal()
  const { show: showRollback, open: openRollback, close: closeRollback } = useModal()
  const [selectedSnapshot, setSelectedSnapshot] = useState(null)

  console.log('selectedtSnapshot', selectedSnapshot)
  const handleShowAnswers = (snapshotId) => {
    const location = buildLocationForView('answers', snapshotId)
    dispatch(setLocation({
      ...location,
      origin: 'snapshots'
    }))
  }

  const openRollbackModal = (snapshot) => {
    setSelectedSnapshot(snapshot)
    openRollback()
  }

  const openUpdateModal = (snapshot) => {
    setSelectedSnapshot(snapshot)
    openUpdate()
  }

  const closeUpdateModal = () => {
    setSelectedSnapshot(null)
    closeUpdate()
  }

  return (
    <div>
      <table className="table border align-middle">
        <thead className="table-light">
          <tr>
            <th style={{ width: '35%' }}>{gettext('Snapshot').toUpperCase()}</th>
            <th style={{ width: '40%' }}>{gettext('Description').toUpperCase()}</th>
            <th style={{ width: '15%' }}>{gettext('Created').toUpperCase()}</th>
            <th style={{ width: '10%' }}></th>
          </tr>
        </thead>
        <tbody>
          {snapshots?.map((snapshot) => {
            return (
              <tr key={snapshot.id}>
                <td>{snapshot.title}</td>
                <td>
                  {snapshot.description}
                </td>
                <td>
                  {useFormattedDateTime(snapshot.created, language)}
                </td>
                <td className="text-end">
                  {perms.can_view_snapshot && (
                    <button
                      type="button"
                      className="btn btn-link p-0"
                      aria-label={gettext('View answers')}
                      title={gettext('View answers')}
                      onClick={() => handleShowAnswers(snapshot.id)}
                    >
                      <i
                        className={'bi bi-eye'}
                        aria-hidden="true" />
                    </button>
                  )}
                  {perms.can_change_snapshot && (
                    <button
                      type="button"
                      className="btn btn-link p-0"
                      aria-label={gettext('Update snapshot')}
                      title={gettext('Update snapshot')}
                      onClick={() => openUpdateModal(snapshot)}
                    >
                      <i
                        className={'bi bi-pencil'}
                        aria-hidden="true" />
                    </button>
                  )}
                  {perms.can_rollback_snapshot && (
                    <button
                      type="button"
                      className="btn btn-link p-0"
                      aria-label={gettext('Rollback to snapshot')}
                      title={gettext('Rollback to snapshot')}
                      onClick={() => openRollbackModal(snapshot)}
                    >
                      <i
                        className={'bi bi-reply-fill'}
                        aria-hidden="true" />
                    </button>
                  )}
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
      {
        selectedSnapshot && (
          <>
            <SnapshotModal show={showUpdate} onClose={closeUpdateModal} snapshot={selectedSnapshot} />
            <SnapshotRollbackModal show={showRollback} onClose={closeRollback} snapshot={selectedSnapshot} />
          </>
        )
      }
    </div>
  )
}

SnapshotsTable.propTypes = {
  snapshots: PropTypes.array.isRequired,
}

export default SnapshotsTable
