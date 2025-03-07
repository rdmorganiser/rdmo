import React, { useState } from 'react'
import { Form, Field } from 'react-final-form'
import { useSelector } from 'react-redux'

const ProjectForm = () => {
  const projectData = useSelector((state) => state.project.project)
  console.log('Project Data:', projectData)
  const { project } = projectData
  const catalogs = useSelector((state) => state.catalogs?.catalogs || [])
  // const allProjects = useSelector((state) => state.project.allProjects || [])
  const allProjects = useSelector(state => state.project.allProjects, (prev, next) => prev === next)

  console.log('All projects:', allProjects)

  console.log('Project:', project)
  console.log('Catalogs:', catalogs)

  // State for the switch, initialized based on parent field value
  const [isParentSwitchOn, setIsParentSwitchOn] = useState(false)
  // const [titleLength, setTitleLength] = useState(10) // Default minimum size

  return (
    <Form
      initialValues={project}
      onSubmit={() => {}}
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
            {/* <Field
              name="title"
              component="input"
              type="text"
              className="form-control"
              placeholder="Title"
              size={Math.max(10, titleLength)} // Dynamically adjust width
              onChange={(e) => setTitleLength(e.target.value.length)} // Track length
            /> */}
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

          {/* Catalog Section */}
          <div className="mb-2">
            <label className="form-label fw-bold">Katalog</label>
            <div className="form-text">
              Der Fragenkatalog, der für dieses Projekt verwendet wird.
            </div>
            {catalogs?.map((catalog) => (
              <div key={catalog.id} className="form-check">
                <Field
                  name="catalog"
                  component="input"
                  type="radio"
                  className="form-check-input"
                  id={`catalog-${catalog.id}`}
                  value={catalog.id}
                  initialValue={project.catalog}
                />
                <label className="form-check-label" htmlFor={`catalog-${catalog.id}`}>
                  {catalog.title}
                </label>
              </div>
            ))}
          </div>


          {/* Übergeordnetes Projekt auswählen Section */}
          <div className="mb-3">
            <div className="form-check form-switch">
              <input
                type="checkbox"
                className="form-check-input"
                id="parentToggle"
                checked={isParentSwitchOn}
                onChange={(e) => setIsParentSwitchOn(e.target.checked)}
              />
              <label className="form-label fw-bold m-0" htmlFor="parentToggle">
                Übergeordnetes Projekt auswählen
              </label>
            </div>
            <div className="form-text mb-2">
              Durch die Verknüpfung mit einem übergeordneten Projekt, können ...
            </div>

            <Field
              name="parent"
              component="select"
              className={`form-select ${!isParentSwitchOn ? 'bg-light text-muted' : ''}`}
              disabled={!isParentSwitchOn}
              initialValue={project.parent} // Keeps the correct pre-selected value
            >
              {!project.parent && <option value="">Übergeordnetes Projekt auswählen</option>}
              {allProjects
                ?.filter((p) => p.id !== project.id) // Exclude the current project
                .map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.title}
                  </option>
                ))}
            </Field>

            <div className="form-check mt-2">
              <Field
                name="inheritDefaults"
                component="input"
                type="checkbox"
                className="form-check-input"
                id="inheritDefaults"
                disabled={!isParentSwitchOn}
              />
              <label
                className={`form-check-label ${!isParentSwitchOn ? 'text-muted' : ''}`}
                htmlFor="inheritDefaults"
              >
                Default-Werte aus übergeordnetem Projekt übernehmen
              </label>
            </div>
          </div>

          {/* <div className="mb-3">
            <div className="form-check form-switch">
              <input
                type="checkbox"
                className="form-check-input"
                id="parentToggle"
                checked={isParentSwitchOn}
                onChange={(e) => {
                  const checked = e.target.checked
                  setIsParentSwitchOn(checked)
                }}
              />
              <label className="form-label fw-bold m-0" htmlFor="parentToggle">
                Übergeordnetes Projekt auswählen
              </label>
            </div>
            <div className="form-text mb-2">
              Durch die Verknüpfung mit einem übergeordneten Projekt, können ...
            </div>

            <Field
              name="parent"
              component="select"
              className={`form-select ${!isParentSwitchOn ? 'bg-light text-muted' : ''}`}
              disabled={!isParentSwitchOn}
              initialValue={project.parent} // Preselect if project.parent exists
            >
              {!project.parent && <option value="">Übergeordnetes Projekt auswählen</option>}
              {allProjects
                ?.filter((p) => p.id !== project.id) // Exclude the current project
                .map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.title}
                  </option>
                ))}
            </Field>

            <div className="form-check mt-2">
              <Field
                name="inheritDefaults"
                component="input"
                type="checkbox"
                className="form-check-input"
                id="inheritDefaults"
                disabled={!isParentSwitchOn}
              />
              <label
                className={`form-check-label ${!isParentSwitchOn ? 'text-muted' : ''}`}
                htmlFor="inheritDefaults"
              >
                Default-Werte aus übergeordnetem Projekt übernehmen
              </label>
            </div>
          </div> */}
        </form>
      )}
    />
  )
}

// ProjectForm.propTypes = {
//   // onSave: PropTypes.func, // .isRequired Auto-save function (to be implemented)
// }

export default ProjectForm
