import React, { useState, useMemo } from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'
import AsyncSelect from 'react-select/async'
import { useDebouncedCallback } from 'use-debounce'
import { isEmpty } from 'lodash'

import Html from 'rdmo/core/assets/js/components/Html'
import Input from 'rdmo/core/assets/js/components/forms/Input'
import Textarea from 'rdmo/core/assets/js/components/forms/Textarea'
import Select from 'rdmo/core/assets/js/components/forms/Select'

import { createProject, updateProject } from '../../../actions/projectActions'
import { useFieldErrors } from '../../../hooks/useFieldErrors'

import ProjectApi from '../../../api/ProjectApi'

const ProjectForm = ({ disabled, submitMode = 'auto', mode = 'edit', initialProject = null,
  catalogs: catalogsProp = null, formId = 'project-form', onSaved }) => {
  const dispatch = useDispatch()
  const errors = useFieldErrors()
  const templates = useSelector((state) => state.templates)
  const selectCatalog = useSelector((state) => state.settings?.project_select_catalog)
  const storeData = useSelector((state) => state.project?.project)

  const project = initialProject ?? storeData?.project
  const catalogs = catalogsProp ?? storeData?.catalogs

  const [formData, setFormData] = useState(project || {})
  const [enableParent, setEnableParent] = useState(!!project?.parent)
  const [parentOptions, setParentOptions] = useState([])

  const catalogOptions = useMemo(
    () => (catalogs || [])
      .filter(c => c.available)
      .map(c => ({ value: c.id, label: c.title })),
    [catalogs]
  )

  const saveProject = (newFormData) => {
    return dispatch(
      mode === 'create'
        ? createProject(newFormData)
        : updateProject(newFormData)
    )
  }

  const debouncedSaveShort = useDebouncedCallback(saveProject, 500)
  const debouncedSaveLong = useDebouncedCallback(saveProject, 1500)

  const handleChange = (key, value) => {
    const updatedFormData = { ...formData, [key]: value }
    setFormData(updatedFormData)

    if (submitMode !== 'auto' || mode !== 'edit') return

    if (key === 'description') {
      debouncedSaveLong(updatedFormData)
    } else {
      debouncedSaveShort(updatedFormData)
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    saveProject({ ...formData })?.then(() => onSaved?.())
  }

  const handleLoadProjects = useDebouncedCallback((search, callback) => {
    ProjectApi.fetchProjects({ search })
      .then(response => {
        const options = response.results
          .filter(p => !project?.id || p.id !== project?.id)
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
          .filter(p => !project?.id || p.id !== project?.id)
          .map(p => ({ value: p.id, label: p.title }))
        setParentOptions(options)
      })
    }
  }

  return (
    <form id={formId} className="container mt-3" onSubmit={submitMode === 'submit' ? handleSubmit : undefined}>
      <Input
        className="mb-3 form-label fw-bold"
        label={gettext('Title')}
        help={<Html html={templates.project_view_title_help} />}
        value={formData.title || ''}
        onChange={(value) => handleChange('title', value)}
        errors={errors.title}
        isDisabled={disabled}
      />

      <Textarea
        className="mb-3 form-label fw-bold"
        label={gettext('Description')}
        help={<Html html={templates.project_view_description_help} />}
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

        {selectCatalog == 'select' ? (
          <Select
            className="mt-2"
            placeholder={gettext('Select catalog')}
            isClearable={false}
            isDisabled={disabled}
            options={catalogOptions}
            value={formData.catalog}
            onChange={(value) => handleChange('catalog', value)}
          />
        ) : (
          catalogOptions.map((opt) => (
            <div key={opt.value} className="form-check">
              <input
                type="radio"
                className="form-check-input"
                id={`catalog-${opt.value}`}
                name="catalog"
                value={opt.value}
                checked={formData.catalog === opt.value}
                onChange={(e) => handleChange('catalog', Number(e.target.value))}
                disabled={disabled}
              />
              <label className="form-check-label" htmlFor={`catalog-${opt.value}`}>
                {opt.label}
              </label>
            </div>
          ))
        )}

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
          value={isEmpty(parentOptions) ? (
            project ? {
              value: project.parent,
              label: project.parent_title
            } : null
          ) : parentOptions.find(p => p.value === formData.parent)}
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
    </form>
  )
}

ProjectForm.propTypes = {
  catalogs: PropTypes.array,
  disabled: PropTypes.bool,
  formId: PropTypes.string,
  initialProject: PropTypes.object,
  mode: PropTypes.oneOf(['create', 'edit']),
  submitMode: PropTypes.oneOf(['auto', 'submit']),
  onSaved: PropTypes.func
}

export default ProjectForm
