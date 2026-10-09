import React from 'react'
import PropTypes from 'prop-types'

import { useModal } from 'rdmo/core/assets/js/hooks'

import CopyProjectModal from '../../../../common/components/CopyProjectModal'

const CopyProject = ({ project }) => {
  const { show, open, close } = useModal()

  const handleOpen = () => open()
  const handleClose = () => close()

  return (
    <>
      <button type="button" className="btn link small" onClick={handleOpen}>
        <i className="bi bi-copy" aria-hidden="true"></i> {gettext('Copy project')}
      </button>

      <CopyProjectModal
        onClose={handleClose}
        project={project}
        show={show}
      />
    </>
  )
}

CopyProject.propTypes = {
  project: PropTypes.object
}

export default CopyProject
