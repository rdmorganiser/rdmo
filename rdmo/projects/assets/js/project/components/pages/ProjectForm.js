import React, { useState } from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'
import AsyncSelect from 'react-select/async'
import { useDebouncedCallback } from 'use-debounce'
import { isEmpty } from 'lodash'

import Html from 'rdmo/core/assets/js/components/Html'
import Input from 'rdmo/core/assets/js/components/forms/Input'
import Textarea from 'rdmo/core/assets/js/components/forms/Textarea'

import { updateProject } from '../../actions/projectActions'
import { useFieldErrors } from '../../hooks/useFieldErrors'

import ProjectApi from '../../api/ProjectApi'

const ProjectForm = ({ disabled }) => {
  const { project, catalogs } = useSelector((state) => state.project.project)
  const templates = useSelector((state) => state.templates)
  const dispatch = useDispatch()
  const errors = useFieldErrors()

  const [formData, setFormData] = useState(project || {})
  const [enableParent, setEnableParent] = useState(!!project.parent)
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

  // Fetch a first page only when the menu is opened and nothing is selected/loaded yet
  const handleMenuOpen = () => {
    if (enableParent) {
      ProjectApi.fetchProjects({ search: '' }).then(({ results }) => {
        const options = results
          .filter(p => !project?.id || p.id !== project.id)
          .map(p => ({ value: p.id, label: p.title }))
          console.log('fetched projects for parent select', options)
        setParentOptions(options)
      })
    }
  }

  return (
    <form className="container mt-3">

      <Input
        className="mb-3 form-label fw-bold"
        label={gettext('Title')}
        help={gettext('The title for this project.')}
        value={formData.title || ''}
        onChange={(value) => handleChange('title', value)}
        errors={errors.title}
        isDisabled={disabled}
      />

      <Textarea
        className="mb-3 form-label fw-bold"
        label={gettext('Description')}
        help={gettext('A description of the project (optional).')}
        rows={4}
        value={formData.description || ''}
        onChange={(value) => handleChange('description', value)}
        errors={errors.description}
        isDisabled={disabled}
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
        errors={errors.phase}
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
              disabled={disabled}
            />
            <label className="form-check-label" htmlFor={`catalog-${catalog.id}`}>
              {catalog.title}
            </label>
          </div>
        ))}
        {errors.catalog?.map((err, i) => (
          <div key={i} className="text-danger mt-1">{err}</div>
        ))}
      </div>

      <div className="mb-3">
        <div className="form-check form-switch">
          <input
            type="checkbox"
            className="form-check-input"
            id="parentToggle"
            checked={enableParent}
            disabled={disabled}
            onChange={(e) => setEnableParent(e.target.checked)}
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
              defaultOptions={parentOptions}
              value={isEmpty(parentOptions) ? {
                value: project.parent,
                label: project.parent_title
              } : parentOptions.find(p => p.value === formData.parent)}
              onChange={(option) => handleChange('parent', option ? option.value : null)}
              getOptionValue={(project) => project.value}
              getOptionLabel={(project) => project.label}
              isDisabled={!enableParent || disabled}
              loadOptions={handleLoadProjects}
              onMenuOpen={handleMenuOpen}
              isClearable
              backspaceRemovesValue={true}
        />

        {errors.parent?.map((err, i) => (
          <div key={i} className="text-danger mt-1">{err}</div>
        ))}

        {/* <div className="form-check mt-2">
          <input
            type="checkbox"
            className="form-check-input"
            id="inheritDefaults"
            checked={!!formData.inheritDefaults}
            onChange={(e) => handleChange('inheritDefaults', e.target.checked)}
            disabled={!enableParent}
          />
          <label
            className={`form-check-label ${!enableParent ? 'text-muted' : ''}`}
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
  disabled: PropTypes.bool
}

export default ProjectForm
