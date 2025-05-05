import React from 'react'
import { useSelector } from 'react-redux'

const ProjectBadge = () => {
  const { project } = useSelector((state) => state.project.project || {})

  if (!project?.title) return null
  const projectState = 'Antragstellung'

  return (
    <div
      className="mb-3 px-3 py-2 rounded"
      style={{
        backgroundColor: 'rgba(255, 255, 255, 0.08)', // Very subtle contrast over #003366
        fontSize: '0.875rem',
        lineHeight: '1.2',
        color: 'white', // Title color
      }}
    >
      <strong>{project.title}</strong>
      {projectState && (
        <div style={{ fontSize: '0.75rem', color: 'var(--bs-gray-500)' }}>
          {projectState}
        </div>
      )}
    </div>
  )
}

export default ProjectBadge
