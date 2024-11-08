import React from 'react'
import PropTypes from 'prop-types'
import AsyncSelect from 'react-select/async'
import { useDebouncedCallback } from 'use-debounce'

import ValueApi from '../../api/ValueApi'

const Search = ({ attribute, values, setValues }) => {

  const handleLoadOptions = useDebouncedCallback((search, snapshot, callback) => {
    ValueApi.searchValues({ attribute, search, snapshot }).then(response => {
      callback(response)
    })
  }, 500)

  return <>
    <AsyncSelect
      classNamePrefix="react-select"
      backspaceRemovesValue={false}
      placeholder={gettext('Search for project or snapshot title, or answer text ...')}
      noOptionsMessage={() => gettext(
        'No answers match your search.'
      )}
      loadingMessage={() => gettext('Loading ...')}
      options={[]}
      value={values.copySetValue}
      onChange={(id) => setValues({ ...values, copySetValue: id })}
      getOptionValue={(value) => value}
      getOptionLabel={(value) => value.value_title}
      formatOptionLabel={(value) => (
        <div>
          {gettext('Project')} <strong>{value.project_title}</strong>
          {
            value.snapshot && <>
              <span className="mr-5 ml-5">&rarr;</span>
              {gettext('Snapshot')} <strong>{value.snapshot_title}</strong>
            </>
          }
          <span className="mr-5 ml-5">&rarr;</span>
          {value.value_and_unit}
        </div>
      )}
      loadOptions={(search, callback) => {
        handleLoadOptions(search, values.snapshot ? 'all' : '', callback)
      }}
      defaultOptions={[]}
    />

    <div className="checkbox">
      <label>
        <input
          type="checkbox"
          checked={values.snapshot}
          onChange={() => setValues({ ...values, snapshot: !values.snapshot })}
        />
        <span>{gettext('Include snapshots in the search')}</span>
      </label>
    </div>
  </>
}

Search.propTypes = {
  attribute: PropTypes.number.isRequired,
  values: PropTypes.object.isRequired,
  setValues: PropTypes.func.isRequired
}

export default Search
