import React from 'react'
import { useSelector } from 'react-redux'
import PropTypes from 'prop-types'
import { useFormattedDateTime } from 'rdmo/core/assets/js/hooks'
import { language } from 'rdmo/core/assets/js/utils'


// import { useModal } from 'rdmo/core/assets/js/hooks'

// import Select from 'rdmo/core/assets/js/components/Select'

// import { updateProjectMember, updateProjectInvite } from '../../actions/projectActions'

// import MembershipDeleteModal from './MembershipDeleteModal'

const SnapshotsTable = ({ snapshots }) => {
  // const dispatch = useDispatch()
  // const currentUser = useSelector((state) => state.user.currentUser)
  const { project } = useSelector((state) => state.project.project) || {}
  const perms = project?.permissions || {}
  console.log('perms', perms)

  // const { show: showConfirm, open: openConfirm, close: closeConfirm } = useModal()
  // const [modalState, setModalState] = useState(null)

  // const isAdminOrSiteManager = currentUser?.is_superuser || currentUser?.is_site_manager

  // const openDeleteModal = (person, isCurrentUser) => {
  //   setModalState({ person, isCurrentUser })
  //   openConfirm()
  // }

  // const closeDeleteModal = () => {
  //   setModalState(null)
  //   closeConfirm()
  // }

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
          {snapshots?.map((snapshot, index) => {

            return (
              <tr key={index}>
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
                    // onClick={() => openDeleteModal(person, isCurrentUser)}
                    >
                      <i
                        className={'bi bi-eye'}
                        aria-hidden="true"
                      />
                    </button>
                  )}
                  {perms.can_change_snapshot && (
                    <button
                      type="button"
                      className="btn btn-link p-0"
                      aria-label={gettext('Update snapshot')}
                      title={gettext('Update snapshot')}
                    // onClick={() => openDeleteModal(person, isCurrentUser)}
                    >
                      <i
                        className={'bi bi-pencil'}
                        aria-hidden="true"
                      />
                    </button>
                  )}
                  {perms.can_rollback_snapshot && (
                    <button
                      type="button"
                      className="btn btn-link p-0"
                      aria-label={gettext('Rollback to snapshot')}
                      title={gettext('Rollback to snapshot')}
                    // onClick={() => openDeleteModal(person, isCurrentUser)}
                    >
                      <i
                        className={'bi bi-reply-fill'}
                        aria-hidden="true"
                      />
                    </button>
                  )}
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

SnapshotsTable.propTypes = {
  snapshots: PropTypes.array.isRequired,
}

export default SnapshotsTable
