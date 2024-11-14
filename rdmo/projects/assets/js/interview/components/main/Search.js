import React from 'react'
import PropTypes from 'prop-types'
import AsyncSelect from 'react-select/async'
import { useDebouncedCallback } from 'use-debounce'
import { isEmpty, isNil, pick, truncate } from 'lodash'

import ProjectApi from '../../api/ProjectApi'
import ValueApi from '../../api/ValueApi'

const Search = ({ page, attribute, values, setValues, collection = false }) => {
  // create a key for the first AsyncSelect, to reset the loaded values when project or snapshot changes
  const key = (values.project ? values.project.id : '') + (values.snapshot ? '-all' : '')

  const handleLoadValues = useDebouncedCallback((search, callback) => {
    ValueApi.searchValues({
      attribute,
      set_attribute: page && page.is_collection && page.attribute,
      search,
      project: values.project ? values.project.id : '',
      snapshot: values.snapshot ? 'all' : '',
      collection
    }).then(response => {
      if (collection) {
        // if the search component is used from QuestionReuseValues/CheckboxWidget
        // the list of values from the server needs to be reduced to show only one entry
        // for each set_prefix/set_index combination
        callback(response.reduce((collections, value) => {
          // look if a value for the same project/snapshot/set_prefix/set_index already exists in values_list
          const collection = isNil(collections) ? null : collections.find(v => (
            (v.project == value.project) &&
            (v.snapshot == value.snapshot) &&
            (v.set_prefix == value.set_prefix) &&
            (v.set_index == value.set_index)
          ))
          if (isNil(collection)) {
            // append the value
            return [...collections, { ...value, values: [value] }]
          } else {
            // update the value_title and the values array of the existing value
            collection.value_label += '; ' + value.value_label
            collection.values.push(value)
            return collections
          }
        }, []))
      } else {
        callback(response)
      }
    })
  }, 500)

  const handleLoadProjects = useDebouncedCallback((search, callback) => {
    ProjectApi.fetchProjects({ search })
              .then(response => callback(response.results.map(project => pick(project, 'id', 'title'))))
  }, 500)

  return <>
    <AsyncSelect
      key={key}
      classNamePrefix="react-select"
      className='react-select'
      placeholder={gettext('Search for project or snapshot title, or answer text ...')}
      noOptionsMessage={() => gettext(
        'No answers match your search.'
      )}
      loadingMessage={() => gettext('Loading ...')}
      options={[]}
      value={values.value}
      onChange={(value) => setValues({ ...values, value })}
      getOptionValue={(value) => value}
      getOptionLabel={(value) => value.value_label}
      formatOptionLabel={(value) => (
        <div>
          {gettext('Project')} <strong>{value.project_label}</strong>
          {
            value.snapshot_label && <>
              <span className="mr-5 ml-5">&rarr;</span>
              {gettext('Snapshot')} <strong>{value.snapshot_label}</strong>
            </>
          }
          {
            value.set_label && <>
              <span className="mr-5 ml-5">&rarr;</span>
              <strong>{value.set_label}</strong>
            </>
          }
          <span className="mr-5 ml-5">&rarr;</span>
          {truncate(value.value_label, {
            'length': 256,
            'omission': ' [...]'
          })}
        </div>
      )}
      loadOptions={handleLoadValues}
      defaultOptions
      isClearable
      backspaceRemovesValue={true}
    />

    <AsyncSelect
      classNamePrefix='react-select'
      className='react-select mt-10'
      placeholder={gettext('Restrict the search to a particular project ...')}
      noOptionsMessage={() => gettext(
        'No projects matching your search.'
      )}
      loadingMessage={() => gettext('Loading ...')}
      options={[]}
      value={values.project}
      onChange={(project) => setValues({
        ...values,
        value: (isEmpty(project) || project == values.project) ? values.value : '',  // reset value
        project: project
      })}
      getOptionValue={(project) => project}
      getOptionLabel={(project) => project.title}
      loadOptions={handleLoadProjects}
      defaultOptions
      isClearable
      backspaceRemovesValue={true}
    />

    <div className="checkbox">
      <label>
        <input
          type="checkbox"
          checked={values.snapshot}
          onChange={() => setValues({
            ...values,
            value: values.snapshot ? '' : values.value,  // reset value
            snapshot: !values.snapshot })}
        />
        <span>{gettext('Include snapshots in the search')}</span>
      </label>
    </div>
  </>
}

Search.propTypes = {
  page: PropTypes.number.isRequired,
  attribute: PropTypes.number.isRequired,
  setAttribute: PropTypes.number,
  values: PropTypes.object.isRequired,
  setValues: PropTypes.func.isRequired,
  collection: PropTypes.bool
}

export default Search
