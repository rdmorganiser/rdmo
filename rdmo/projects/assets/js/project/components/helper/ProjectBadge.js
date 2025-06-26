import React from 'react'
import { useSelector } from 'react-redux'

const ProjectBadge = () => {
  const { project } = useSelector((state) => state.project.project || {})

  if (!project?.title) return null

  return (
    <div className="mb-3 px-3 py-2 rounded">
      <strong>{project.title}</strong>
      {project?.phase && (
        <div style={{ fontSize: '0.75rem', color: 'var(--bs-gray-500)' }}>
          {project.phase}
        </div>
      )}
    </div>
  )
}

export default ProjectBadge
