import React from 'react'
import PropTypes from 'prop-types'

import { Modal } from 'rdmo/core/assets/js/_bs53/components'

import ProjectForm from '../../project/components/areas/information/ProjectForm'

const CopyProjectModal = ({
  catalogs,
  onClose,
  project,
  show
}) => {
  const modalProps = {
    title: gettext('Copy project'),
    size: 'modal-lg',
    show,
    onClose,
    onSubmit: () => {},
    submitLabel: gettext('Copy project'),
    submitProps: {
      type: 'submit',
      form: 'project-copy-form'
    }
  }

  return (
    <Modal {...modalProps}>
      {
        project && (
          <ProjectForm
            key={`copy-${project.id}`}
            disabled={false}
            formId="project-copy-form"
            submitMode="submit"
            mode="copy"
            currentProject={project}
            catalogs={catalogs}
            onSave={onClose}
          />
        )
      }
    </Modal>
  )
}

CopyProjectModal.propTypes = {
  catalogs: PropTypes.array,
  onClose: PropTypes.func.isRequired,
  project: PropTypes.object,
  show: PropTypes.bool.isRequired
}

export default CopyProjectModal
