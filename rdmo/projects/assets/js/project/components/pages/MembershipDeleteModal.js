import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'
import Modal from 'rdmo/core/assets/js/_bs53/components/Modal'

import { deleteProjectMember, deleteProjectInvite } from '../../actions/projectActions'
import { useFieldErrors } from '../../hooks/useFieldErrors'

const MembershipDeleteModal = ({ show, onClose, person, isManager = false,
                                 isMember = false, isCurrentUser = false }) => {
  const dispatch = useDispatch()
  const { project } = useSelector((state) => state.project.project) ?? {}
  const errors = useFieldErrors()

  const name =
    [person.first_name, person.last_name].filter(Boolean).join(' ').trim() ||
    person.email || ''

  const text = !isMember ? gettext('Delete invite') : (
    isCurrentUser ? gettext('Leave project') : gettext('Delete membership')
  )

  return (
    <Modal
      title={text}
      show={show}
      onClose={onClose}
      onSubmit={async () => {
        try {
          if (isMember) {
            await dispatch(
              deleteProjectMember(
                person.id,
                isCurrentUser && !isManager ? { redirect: true } : {}
              )
            )
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
                gettext('You are about to leave the project <b>%s</b>. If you want to access this project again, somebody will need to invite you!'),
                [project?.title ?? '']
              )
            : isMember
            ? interpolate(
                gettext('You are about to remove the user <b>%s</b> from the project <b>%s</b>.'),
                [name, project?.title ?? '']
              )
            : interpolate(
                gettext('You are about to remove the invite of <b>%s</b> from the project <b>%s</b>.'),
                [name, project?.title ?? '']
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
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  isManager: PropTypes.bool,
  isMember: PropTypes.bool,
  isCurrentUser: PropTypes.bool,
  person: PropTypes.shape({
    id: PropTypes.number.isRequired,
    first_name: PropTypes.string,
    last_name: PropTypes.string,
    email: PropTypes.string,
  })
}

export default MembershipDeleteModal
