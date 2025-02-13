import React from 'react'
import { Form, Field } from 'react-final-form'
import { useSelector } from 'react-redux'

const ProjectForm = () => {

  const projectData = useSelector((state) => state.project.project)

  const { project } = projectData
  console.log('Project:', project)

  return (
    <Form
      initialValues={project}
      onSubmit={() => {}} // No explicit submit needed
      render={({ handleSubmit }) => (
        <form onSubmit={handleSubmit} className="container mt-3">
          <div className="mb-2">
            <label className="form-label fw-bold">Title</label>
            <Field
              name="title"
              component="input"
              type="text"
              className="form-control"
              placeholder="Title"
            />
            <div className="form-text">Der Title für dieses Projekt.</div>
          </div>

          <div className="mb-2">
            <label className="form-label fw-bold">Beschreibung</label>
            <Field
              name="description"
              component="textarea"
              className="form-control"
              placeholder="Beschreibung"
            />
            <div className="form-text">Eine Beschreibung für dieses Projekt (optional).</div>
          </div>

          <div className="mb-2">
            <label className="form-label fw-bold">Projektphase</label>
            <Field name="phase" component="select" className="form-select">
              <option value="antragstellung">Antragstellung</option>
              <option value="durchführung">Durchführung</option>
              <option value="abschluss">Abschluss</option>
            </Field>
            <div className="form-text">
              Die Phase, in der sich Ihr Projekt zum aktuellen Zeitpunkt befindet.
            </div>
          </div>
        </form>
      )}
    />
  )
}

// ProjectForm.propTypes = {
//   // onSave: PropTypes.func, // .isRequired Auto-save function (to be implemented)
// }

export default ProjectForm
