import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'
import Modal from 'rdmo/core/assets/js/_bs53/components/Modal'

import { userIsManager } from 'rdmo/projects/assets/js/common/utils'

import { deleteProjectMember, deleteProjectInvite, leaveProject } from '../../actions/projectActions'
import { useFieldErrors } from '../../hooks/useFieldErrors'

const MembershipDeleteModal = ({ show, onClose, person, isMember = false, isCurrentUser = false }) => {
  const dispatch = useDispatch()
  const { project } = useSelector((state) => state.project.project) ?? {}
  const { perms } = useSelector((state) => state.project)
  console.log('perms', perms)
  console.log('project', project)
  console.log('person', person )
  const errors = useFieldErrors()

  const isManager = userIsManager(useSelector((state) => state.user.currentUser))

  const name =
    [person.user.first_name, person.user.last_name].filter(Boolean).join(' ').trim() ||
    person.user.email || ''

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
            isCurrentUser ?
            await dispatch(leaveProject(
              person.id,
              !isManager && { redirect: true })) :
            await dispatch(deleteProjectMember(person.id))
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
  isMember: PropTypes.bool,
  isCurrentUser: PropTypes.bool,
  person: PropTypes.shape({
    id: PropTypes.number.isRequired,
    user: PropTypes.shape({
      first_name: PropTypes.string,
      last_name: PropTypes.string,
      email: PropTypes.string,
    })
  })
}

export default MembershipDeleteModal
