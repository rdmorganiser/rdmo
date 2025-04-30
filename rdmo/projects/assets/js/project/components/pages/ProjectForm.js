import React, { useEffect, useState } from 'react'
import { useSelector } from 'react-redux'
import AsyncSelect from 'react-select/async'
import { useDebouncedCallback } from 'use-debounce'

import Input from 'rdmo/core/assets/js/components/forms/Input'
import Select from 'rdmo/core/assets/js/components/forms/Select'
import Textarea from 'rdmo/core/assets/js/components/forms/Textarea'
import ProjectApi from '../../api/ProjectApi'

const ProjectForm = () => {
  const { project, catalogs } = useSelector((state) => state.project.project)
  const [formData, setFormData] = useState(project || {})
  // const [errors, setErrors] = useState({})
  const errors = useSelector((state) => state.project.errors)
  const [isParentSwitchOn, setIsParentSwitchOn] = useState(!!project.parent)
  const [parentOptions, setParentOptions] = useState([])

  const saveProject = (newFormData) => {
    ProjectApi.updateProject(project.id, newFormData)
  }

  const debouncedSaveShort = useDebouncedCallback(saveProject, 500)
  const debouncedSaveLong = useDebouncedCallback(saveProject, 1500)

  const handleChange = (key, value) => {
    const updatedFormData = { ...formData, [key]: value }
    setFormData(updatedFormData)

    if (key === 'description') {
      debouncedSaveLong(updatedFormData)
    } else {
      debouncedSaveShort(updatedFormData)
    }
  }
  console.log('parentOptions %o', parentOptions)

  const handleLoadProjects = useDebouncedCallback((search, callback) => {
    ProjectApi.fetchProjects({ search })
      .then(response => {
        const options = response.results
        .filter(p => !project?.id || p.id !== project.id)
        .map(project => ({
          value: project.id,
          label: project.title
        }))
        setParentOptions(options)
        callback(options)
      })
  }, 500)

  useEffect(() => {
    if (formData.parent && parentOptions.length === 0) {
      ProjectApi.fetchProject(formData.parent).then(project => {
        const option = { value: project.id, label: project.title }
        setParentOptions([option])
      })
    }
  }, [formData.parent, parentOptions.length])

  const handleSubmit = (e) => {
    e.preventDefault()
    console.log('Form Data:', formData)
    console.log('submit!')
  }

  return (
    <form onSubmit={handleSubmit} className="container mt-3">

      <Input
        className="mb-3"
        label="Title"
        help="Der Title für dieses Projekt."
        value={formData.title || ''}
        onChange={(value) => handleChange('title', value)}
        errors={errors.title}
      />

      <Textarea
        className="mb-3"
        label="Beschreibung"
        help="Eine Beschreibung für dieses Projekt (optional)."
        rows={4}
        value={formData.description || ''}
        onChange={(value) => handleChange('description', value)}
        errors={errors.description}
      />

      <Select
        className="mb-3"
        label="Projektphase"
        help="Die Phase, in der sich Ihr Projekt zum aktuellen Zeitpunkt befindet."
        isClearable={true}
        options={[
          { value: 'antragstellung', label: 'Antragstellung' },
          { value: 'durchführung', label: 'Durchführung' },
          { value: 'abschluss', label: 'Abschluss' }
        ]}
        value={formData.phase || ''}
        onChange={(value) => handleChange('phase', value)}
        errors={errors.phase}
        placeholder="Projektphase auswählen"
      />

      <div className="mb-3">
        <label className="form-label fw-bold">Katalog</label>
        <div className="form-text">Der Fragenkatalog, der für dieses Projekt verwendet wird.</div>
        {catalogs?.map((catalog) => (
          <div key={catalog.id} className="form-check">
            <input
              type="radio"
              className="form-check-input"
              id={`catalog-${catalog.id}`}
              name="catalog"
              value={catalog.id}
              checked={formData.catalog == catalog.id}
              onChange={(e) => handleChange('catalog', e.target.value)}
            />
            <label className="form-check-label" htmlFor={`catalog-${catalog.id}`}>
              {catalog.title}
            </label>
          </div>
        ))}
      </div>

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
        <div className="form-text">
          Durch die Verknüpfung mit einem übergeordneten Projekt, können ...
        </div>

        <AsyncSelect
              classNamePrefix='react-select'
              className='react-select mt-10'
              placeholder={gettext('Search projects ...')}
              noOptionsMessage={() => gettext(
                'No projects matching your search.'
              )}
              loadingMessage={() => gettext('Loading ...')}
              options={parentOptions}
              value={parentOptions.find(p => p.value === formData.parent) || null}
              onChange={(option) => handleChange('parent', option ? option.value : null)}
              getOptionValue={(project) => project.value}
              getOptionLabel={(project) => project.label}
              isDisabled={!isParentSwitchOn}
              loadOptions={handleLoadProjects}
              defaultOptions
              isClearable
              backspaceRemovesValue={true}
        />

        {/* <div className="form-check mt-2">
          <input
            type="checkbox"
            className="form-check-input"
            id="inheritDefaults"
            checked={!!formData.inheritDefaults}
            onChange={(e) => handleChange('inheritDefaults', e.target.checked)}
            disabled={!isParentSwitchOn}
          />
          <label
            className={`form-check-label ${!isParentSwitchOn ? 'text-muted' : ''}`}
            htmlFor="inheritDefaults"
          >
            Default-Werte aus übergeordnetem Projekt übernehmen
          </label>
        </div> */}
      </div>

      <button type="submit" className="btn btn-primary" onClick={handleSubmit}>{gettext('Submit')}</button>
    </form>
  )
}

export default ProjectForm
