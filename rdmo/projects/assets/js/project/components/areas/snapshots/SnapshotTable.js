import React, { useState } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import PropTypes from 'prop-types'

import { useFormattedDateTime } from 'rdmo/core/assets/js/hooks'
import { useModal } from 'rdmo/core/assets/js/hooks'
import { language } from 'rdmo/core/assets/js/utils'
import { Link } from 'rdmo/core/assets/js/components'

import { navigateDashboard } from '../../../actions/projectActions'
import { buildPath } from '../../../utils/location'

import SnapshotModal from './SnapshotModal'
import SnapshotRollbackModal from './SnapshotRollbackModal'
import SnapshotDeleteModal from './SnapshotDeleteModal'

const SnapshotTable = ({ snapshots }) => {
  const dispatch = useDispatch()
  const { project } = useSelector((state) => state.project.project) || {}
  const perms = project?.permissions || {}

  const updateModal = useModal()
  const rollbackModal = useModal()
  const deleteModal = useModal()
  const [selectedSnapshot, setSelectedSnapshot] = useState(null)

  const openRollbackModal = (snapshot) => {
    setSelectedSnapshot(snapshot)
    rollbackModal.open()
  }

  const openUpdateModal = (snapshot) => {
    setSelectedSnapshot(snapshot)
    updateModal.open()
  }

  const openDeleteModal = (snapshot) => {
    setSelectedSnapshot(snapshot)
    deleteModal.open()
  }

  return (
    <div>
      <table className="table">
        <thead>
          <tr>
            <th style={{ width: '35%' }}>{gettext('Snapshot')}</th>
            <th style={{ width: '40%' }}>{gettext('Description')}</th>
            <th style={{ width: '15%' }}>{gettext('Created')}</th>
            <th style={{ width: '10%' }}></th>
          </tr>
        </thead>
        <tbody>
          {snapshots?.map((snapshot) => {
            const documentsLocation = { area: 'snapshots', snapshotId: snapshot.id }
            return (
              <tr key={snapshot.id}>
                <td>
                  <strong>{snapshot.title}</strong>
                </td>
                <td>
                  {snapshot.description}
                </td>
                <td>
                  {useFormattedDateTime(snapshot.created, language)}
                </td>
                <td>
                  <div className="d-flex justify-content-end align-items-center gap-1">
                    {perms.can_view_snapshot && (
                      <Link
                        title={gettext('View documents')}
                        href={buildPath(documentsLocation)}
                        onClick={() => dispatch(navigateDashboard(documentsLocation))}
                      >
                        <i className={'bi bi-file-text'} aria-hidden="true" />
                      </Link>
                    )}
                    {perms.can_change_snapshot && (
                      <button
                        type="button"
                        className="link"
                        aria-label={gettext('Update snapshot')}
                        title={gettext('Update snapshot')}
                        onClick={() => openUpdateModal(snapshot)}
                      >
                        <i className={'bi bi-pencil'} aria-hidden="true" />
                      </button>
                    )}
                    {perms.can_rollback_snapshot && (
                      <button
                        type="button"
                        className="link"
                        aria-label={gettext('Rollback to snapshot')}
                        title={gettext('Rollback to snapshot')}
                        onClick={() => openRollbackModal(snapshot)}
                      >
                        <i className={'bi bi-reply-fill'} aria-hidden="true" />
                      </button>
                    )}
                    {perms.can_delete_snapshot && (
                      <button
                        type="button"
                        className="link"
                        aria-label={gettext('Delete snapshot')}
                        title={gettext('Delete snapshot')}
                        onClick={() => openDeleteModal(snapshot)}
                      >
                        <i className={'bi bi-trash'} aria-hidden="true" />
                      </button>
                    )}
                  </div>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
      {
        selectedSnapshot && (
          <>
            <SnapshotModal
              show={updateModal.show}
              onClose={updateModal.close}
              snapshot={selectedSnapshot} />
            <SnapshotRollbackModal
              show={rollbackModal.show}
              onClose={rollbackModal.close}
              snapshot={selectedSnapshot} />
            <SnapshotDeleteModal
              show={deleteModal.show}
              onClose={deleteModal.close}
              snapshot={selectedSnapshot} />
          </>
        )
      }
    </div>
  )
}

SnapshotTable.propTypes = {
  snapshots: PropTypes.array.isRequired,
}

export default SnapshotTable
