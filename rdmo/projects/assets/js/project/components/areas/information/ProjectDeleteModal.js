import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch } from 'react-redux'

import Modal from 'rdmo/core/assets/js/_bs53/components/Modal'
import Html from 'rdmo/core/assets/js/components/Html'

import { deleteProject } from '../../../actions/projectActions'

const ProjectDeleteModal = ({
  project = null,
  id = null,
  show,
  onClose,
  onDeleted = () => { },
}) => {
  const dispatch = useDispatch()

  const handleDelete = () => {
    const action = id ? deleteProject(id) : deleteProject()

    return dispatch(action).then(() => {
      onClose()
      onDeleted()
    })
  }

  return (
    <Modal
      title={gettext('Delete project')}
      show={show}
      onClose={onClose}
      onSubmit={handleDelete}
      submitLabel={gettext('Delete project')}
      submitProps={{ className: 'btn btn-danger' }}
    >
      <Html
        html={
          interpolate(
            gettext('Are you sure you want to delete the project <b>%s</b>?'),
            [project?.title ?? '']
          )
        }
      />
      <p>{gettext('This action cannot be undone.')}</p>
    </Modal>
  )
}

ProjectDeleteModal.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  id: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
  project: PropTypes.shape({
    title: PropTypes.string,
  }),
  onDeleted: PropTypes.func,
}

export default ProjectDeleteModal
