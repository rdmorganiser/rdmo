import React from 'react'
import PropTypes from 'prop-types'
import { useSelector } from 'react-redux'

const SendIssueDropdowns = ({
  formData,
  setField,
  onCheckboxChange,
  formats
}) => {
  const answers = useSelector((state) => state.project.project.answers) ?? {}
  const views = useSelector((state) => state.project.project.views) ?? []
  const snapshots = useSelector((state) => state.project.project.snapshots) ?? []
  const snapshotOptions = [
    { id: 'current', title: gettext('Current') },
    ...snapshots
  ]
  const files = []

  return (
    <div className="d-flex justify-content-end gap-3 mb-3">
      <div className="dropdown">
        <button
          type="button"
          className="link text-nowrap"
          data-bs-toggle="dropdown"
          data-bs-popper-config='{"strategy":"fixed"}'
          aria-expanded="false"
          title={gettext('Attachments')}
        >
          {gettext('Attachments')} <i className="bi bi-caret-down-fill ms-1" />
        </button>

        <div className="dropdown-menu p-3" style={{ minWidth: '280px' }}>
          {
            answers.html && (
              <div className="mb-3">
                <div className="fw-bold mb-2">
                  {gettext('Answers')}
                </div>

                <div className="form-check">
                  <input
                    id="id_attachments_answers"
                    name="attachments_answers"
                    type="checkbox"
                    className="form-check-input"
                    value="project_answers"
                    checked={formData.attachments_answers.includes('project_answers')}
                    onChange={
                      (event) => onCheckboxChange(
                        'attachments_answers',
                        'project_answers',
                        event.target.checked
                      )
                    }
                  />
                  <label
                    className="form-check-label fw-normal"
                    htmlFor="id_attachments_answers"
                  >
                    {/* TODO: use a template for that? */}
                    {gettext('Attach the output of "View answers".')}
                  </label>
                </div>
              </div>
            )
          }
          {
            views.length > 0 && (
              <div className="mb-3">
                <div className="fw-bold mb-2">{gettext('Views')}</div>
                {
                  views.map((view) => (
                    <div className="form-check" key={view.id}>
                      <input
                        id={`id_attachments_views_${view.id}`}
                        name="attachments_views"
                        type="checkbox"
                        className="form-check-input"
                        value={view.id}
                        checked={formData.attachments_views.includes(view.id)}
                        onChange={
                          (event) => onCheckboxChange('attachments_views', view.id, event.target.checked)
                        }
                      />
                      <label
                        className="form-check-label fw-normal"
                        htmlFor={`id_attachments_views_${view.id}`}>
                        {view.title}
                      </label>
                    </div>
                  ))
                }
              </div>
            )
          }

          {
            files.length > 0 && (
              <div className="mb-3">
                <div className="fw-bold mb-2">{gettext('Files')}</div>
                {
                  files.map((file) => (
                    <div className="form-check" key={file.id}>
                      <input
                        id={`id_attachments_files_${file.id}`}
                        name="attachments_files"
                        type="checkbox"
                        className="form-check-input"
                        value={file.id}
                        checked={formData.attachments_files.includes(file.id)}
                        onChange={
                          (event) => onCheckboxChange('attachments_files', file.id, event.target.checked)
                        }
                      />
                      <label
                        className="form-check-label fw-normal"
                        htmlFor={`id_attachments_files_${file.id}`}>
                        {file.file_name}
                      </label>
                    </div>
                  ))
                }
              </div>
            )
          }

          <div>
            <div className="fw-bold mb-2">{gettext('Snapshot')}</div>
            {
              snapshotOptions.map((snapshot) => (
                <div className="form-check" key={snapshot.id}>
                  <input
                    id={`id_attachments_snapshot_${snapshot.id}`}
                    name="attachments_snapshot"
                    type="radio"
                    className="form-check-input"
                    value={snapshot.id}
                    checked={formData.attachments_snapshot === snapshot.id}
                    onChange={() => setField('attachments_snapshot', snapshot.id)}
                  />
                  <label
                    className="form-check-label fw-normal"
                    htmlFor={`id_attachments_snapshot_${snapshot.id}`}
                  >
                    {snapshot.title}
                  </label>
                </div>
              ))
            }
          </div>
        </div>
      </div>
      <div className="dropdown">
        <button
          type="button"
          className="link text-nowrap"
          data-bs-toggle="dropdown"
          data-bs-popper-config='{"strategy":"fixed"}'
          aria-expanded="false"
          title={gettext('Format')}
        >
          {gettext('Format')} <i className="bi bi-caret-down-fill ms-1" />
        </button>

        <div className="dropdown-menu p-3" style={{ minWidth: '220px' }}>
          {
            formats.map(([format, label]) => (
              <div className="form-check" key={format}>
                <input
                  id={`id_attachments_format_${format}`}
                  name="attachments_format"
                  type="radio"
                  className="form-check-input"
                  value={format}
                  checked={formData.attachments_format === format}
                  onChange={() => setField('attachments_format', format)}
                />
                <label
                  className="form-check-label fw-normal"
                  htmlFor={`id_attachments_format_${format}`}
                >
                  {label}
                </label>
              </div>
            ))
          }
        </div>
      </div>
    </div>
  )
}

SendIssueDropdowns.propTypes = {
  formData: PropTypes.object.isRequired,
  setField: PropTypes.func.isRequired,
  onCheckboxChange: PropTypes.func.isRequired,
  formats: PropTypes.array.isRequired
}

export default SendIssueDropdowns
