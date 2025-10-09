import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'
import Modal from 'rdmo/core/assets/js/_bs53/components/Modal'

import { deleteProjectMember, deleteProjectInvite, leaveProject } from '../../actions/projectActions'
import { useFieldErrors } from '../../hooks/useFieldErrors'

const MembershipDeleteModal = ({ type, show, person, onClose, isAdminOrSiteManager = false,
                                 isCurrentUser = false }) => {
  const dispatch = useDispatch()
  const { project } = useSelector((state) => state.project.project) ?? {}
  const errors = useFieldErrors()

  const name = person.user?.full_name || person.email || ''

  const text = (type == 'memberships') ? (
    isCurrentUser ? gettext('Leave project') : gettext('Delete membership')
  ) : gettext('Delete invite')

  return (
    <Modal
      title={text}
      show={show}
      onClose={onClose}
      onSubmit={async () => {
        try {
          if (type == 'memberships') {
            isCurrentUser ? await dispatch(leaveProject(person.id, { redirect: !isAdminOrSiteManager }))
                          : await dispatch(deleteProjectMember(person.id))
          } else {
            await dispatch(deleteProjectInvite(person.id))
          }
          onClose()
        } catch {
          // keep modal open on error
        }
      }}
      submitLabel={text}
      submitProps={{ className: 'btn btn-danger' }}
      size="modal-md"
    >
      <Html
        html={
          isCurrentUser
            ? interpolate(
              gettext('You are about to leave the project <b>%s</b>. If you want to access this project again, ' +
                      'somebody will need to invite you!'),
              [project?.title ?? '']
            ) : (
              (type == 'memberships')
              ? interpolate(
                  gettext('You are about to remove the user <b>%s</b> from the project <b>%s</b>.'),
                  [name, project?.title ?? '']
                )
              : interpolate(
                  gettext('You are about to remove the invite of <b>%s</b> from the project <b>%s</b>.'),
                  [name, project?.title ?? '']
                )
            )
        }
      />
      {errors.non_field_errors?.map((err, i) => (
        <div key={i} className="text-danger mt-1">{err}</div>
      ))}
    </Modal>
  )
}

MembershipDeleteModal.propTypes = {
  type: PropTypes.oneOf(['memberships', 'invites']),
  show: PropTypes.bool.isRequired,
  person: PropTypes.shape({
    id: PropTypes.number.isRequired,
    user: PropTypes.shape({
      first_name: PropTypes.string,
      last_name: PropTypes.string,
      full_name: PropTypes.string,
      email: PropTypes.string,
    }),
    email: PropTypes.string,
  }),
  onClose: PropTypes.func.isRequired,
  isAdminOrSiteManager: PropTypes.bool,
  isMember: PropTypes.bool,
  isCurrentUser: PropTypes.bool,
}

export default MembershipDeleteModal
