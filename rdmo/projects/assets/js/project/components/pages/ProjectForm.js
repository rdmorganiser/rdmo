import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'
import AsyncSelect from 'react-select/async'
import { useDebouncedCallback } from 'use-debounce'

import Html from 'rdmo/core/assets/js/components/Html'
import Input from 'rdmo/core/assets/js/components/forms/Input'
import Textarea from 'rdmo/core/assets/js/components/forms/Textarea'
import ProjectApi from '../../api/ProjectApi'
import { updateProject } from '../../actions/projectActions'
import { getFieldErrors } from '../../utils/getFieldErrors'

const ProjectForm = ({ allowed }) => {
  const { project, catalogs } = useSelector((state) => state.project.project)
  const templates = useSelector((state) => state.templates)
  const dispatch = useDispatch()

  const [formData, setFormData] = useState(project || {})
  const [isParentSwitchOn, setIsParentSwitchOn] = useState(!!project.parent)
  const [parentOptions, setParentOptions] = useState([])

  const saveProject = (newFormData) => {
    dispatch(updateProject(newFormData))
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
    if (formData.parent && !parentOptions.some(p => p.value === formData.parent)) {
      ProjectApi.fetchProject(formData.parent).then((project) => {
        const option = { value: project.id, label: project.title }
        setParentOptions((prev) => [...prev, option])
      })
    }
  }, [formData.parent, parentOptions])

  return (
    // <form onSubmit={handleSubmit} className="container mt-3">
    <form className="container mt-3">

      <Input
        className="mb-3 form-label fw-bold"
        label={gettext('Title')}
        help={gettext('The title for this project.')}
        value={formData.title || ''}
        onChange={(value) => handleChange('title', value)}
        errors={getFieldErrors('title')}
        isDisabled={!allowed}
      />

      <Textarea
        className="mb-3 form-label fw-bold"
        label={gettext('Description')}
        help={gettext('A description of the project (optional).')}
        rows={4}
        value={formData.description || ''}
        onChange={(value) => handleChange('description', value)}
        errors={getFieldErrors('description')}
        isDisabled={!allowed}
      />

      {/* TODO feature project phase */}
      {/*
      <Select
        className="mb-3 form-label fw-bold"
        label={gettext('Project phase')}
        help={gettext('The phase of the project at this time.')}
        // "Die Phase, in der sich Ihr Projekt zum aktuellen Zeitpunkt befindet."
        isClearable={true}
        options={[
          { value: 'antragstellung', label: 'Antragstellung' },
          { value: 'durchführung', label: 'Durchführung' },
          { value: 'abschluss', label: 'Abschluss' }
        ]}
        value={formData.phase || ''}
        onChange={(value) => handleChange('phase', value)}
        errors={getFieldErrors('phase')}
        placeholder={gettext('Select project phase')}
      />
      */}

      <div className="mb-3">
        <label className="form-label fw-bold">{gettext('Catalog')}</label>
        <div className="form-text">{gettext('The catalog used for this project.')}</div>
        {catalogs?.filter(catalog => catalog.available).map((catalog) => (
          <div key={catalog.id} className="form-check">
            <input
              type="radio"
              className="form-check-input"
              id={`catalog-${catalog.id}`}
              name="catalog"
              value={catalog.id}
              checked={formData.catalog == catalog.id}
              onChange={(e) => handleChange('catalog', e.target.value)}
              disabled={!allowed}
            />
            <label className="form-check-label" htmlFor={`catalog-${catalog.id}`}>
              {catalog.title}
            </label>
          </div>
        ))}
        {getFieldErrors('catalog').map((err, i) => (
          <div key={i} className="text-danger mt-1">{err}</div>
        ))}
      </div>

      <div className="mb-3">
        <div className="form-check form-switch">
          <input
            type="checkbox"
            className="form-check-input"
            id="parentToggle"
            checked={isParentSwitchOn}
            disabled={!allowed}
            onChange={(e) => setIsParentSwitchOn(e.target.checked)}
          />
          <label className="form-label fw-bold m-0" htmlFor="parentToggle">
            {gettext('Select parent project')}
          </label>
        </div>
        <div className="form-text">
          <Html html={templates.project_view_parent_help} />
        </div>

        <AsyncSelect
              classNamePrefix='react-select'
              className='react-select mt-10'
              placeholder={gettext('Search projects ...')}
              noOptionsMessage={() => gettext('No projects matching your search.')}
              loadingMessage={() => gettext('Loading ...')}
              options={parentOptions}
              value={parentOptions.find(p => p.value === formData.parent) || null}
              onChange={(option) => handleChange('parent', option ? option.value : null)}
              getOptionValue={(project) => project.value}
              getOptionLabel={(project) => project.label}
              isDisabled={!isParentSwitchOn || !allowed}
              loadOptions={handleLoadProjects}
              isClearable
              backspaceRemovesValue={true}
        />

        {getFieldErrors('parent').map((err, i) => (
          <div key={i} className="text-danger mt-1">{err}</div>
        ))}

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

      {/* <button type="submit" className="btn btn-primary" onClick={handleSubmit}>{gettext('Submit')}</button> */}
    </form>
  )
}

ProjectForm.propTypes = {
  allowed: PropTypes.bool
}

export default ProjectForm
