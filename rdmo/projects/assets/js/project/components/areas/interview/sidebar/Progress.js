import React from 'react'
import { useSelector } from 'react-redux'
import { isNil } from 'lodash'

const Progress = () => {
  const progress = useSelector((state) => state.project.progress)

  if (isNil(progress)) {
    return
  }

  const low = progress.ratio <= 0.25
  const width = progress.ratio * 100
  const label = interpolate(gettext('%s of %s'), [progress.count, progress.total])

  return (
    <>
      <h3>{gettext('Progress')}</h3>

      <div className="project-interview-progress mb-3">
        {low && <div className="interview-progress-count">{label}</div>}

        <div className="progress">
          <div className="progress-bar" role="progressbar" style={{width: `${width}%`}}>
            {!low && <span>{label}</span>}
          </div>
        </div>
      </div>
    </>
  )
}

export default Progress
