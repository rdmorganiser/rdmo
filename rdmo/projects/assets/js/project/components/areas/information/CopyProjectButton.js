import React, { useState } from 'react'
import PropTypes from 'prop-types'

import { useModal } from 'rdmo/core/assets/js/hooks'

import CopyProjectModal from '../../../../common/components/CopyProjectModal'

const CopyProjectButton = ({ project }) => {
  const [selectedProject, setSelectedProject] = useState(null)

  const { show, open, close } = useModal()

  const handleOpen = () => {
    setSelectedProject(project)
    open()
  }

  const handleClose = () => {
    setSelectedProject(null)
    close()
  }

  return (
    <>
      <button type="button" className="btn btn-primary" onClick={handleOpen}>
        {gettext('Copy project')}
      </button>

      <CopyProjectModal
        onClose={handleClose}
        project={selectedProject}
        show={show}
      />
    </>
  )
}

CopyProjectButton.propTypes = {
  project: PropTypes.object
}

export default CopyProjectButton
