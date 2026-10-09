import React from 'react'
import PropTypes from 'prop-types'

const FilterString = ({ value, onChange, label }) => {
  return (
    <div className="input-group mb-2">
      <input
        type="text" className="form-control" placeholder={label} aria-label={label}
        value={value} onChange={e => onChange(e.target.value)}></input>
      <button
        className="btn btn-light border" onClick={() => onChange('')}
        title={gettext('Reset')} aria-label={gettext('Reset')}>
        <strong className="bi bi-x-lg"></strong>
      </button>
    </div>
  )
}

FilterString.propTypes = {
  value: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  label: PropTypes.string.isRequired
}

const FilterUriPrefix = ({ value, options, onChange }) => {
  return (
    <div className="form-group mb-2">
      <select
        className="form-select" value={value} aria-label={gettext('Filter URI prefix')}
        onChange={event => onChange(event.target.value)}>
        <option value="">{gettext('All URI prefixes')}</option>
        {
          options.map((option, index) => <option value={option} key={index}>{option}</option>)
        }
      </select>
    </div>
  )
}

FilterUriPrefix.propTypes = {
  value: PropTypes.string,
  options: PropTypes.array,
  onChange: PropTypes.func
}

const FilterSite = ({ value, options, onChange, label = 'Filter sites', allLabel = 'All sites' }) => {
  return (
    <div className="form-group mb-2">
      <select
        className="form-select" value={value} aria-label={label}
        onChange={event => onChange(event.target.value)}>
        <option value="">{gettext(allLabel)}</option>
        {
          options.map((option, index) => <option value={option.id} key={index}>{option.name}</option>)
        }
      </select>
    </div>
  )
}

FilterSite.propTypes = {
  value: PropTypes.string,
  options: PropTypes.array,
  onChange: PropTypes.func,
  label: PropTypes.string,
  allLabel: PropTypes.string
}

export { FilterSite, FilterString, FilterUriPrefix }
