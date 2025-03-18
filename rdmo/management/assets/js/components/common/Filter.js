import React from 'react'
import PropTypes from 'prop-types'

const FilterString = ({ value, onChange, label }) => {
  return (
    <div className="form-group mb-0">
      <div className="input-group">
        <input type="text" className="form-control" placeholder={label} aria-label={label}
               value={ value } onChange={e => onChange(e.target.value)}></input>
        <span className="input-group-btn">
          <button className="btn btn-default" onClick={() => onChange('')}
                  title={gettext('Reset')} aria-label={gettext('Reset')}>
            <span className="fa fa-times"></span>
          </button>
        </span>
      </div>
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
    <div className="form-group mb-0">
      <select className="form-control" value={value} aria-label={gettext('Filter URI prefix')}
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
    <div className="form-group mb-0">
      <select className="form-control" value={value} aria-label={label}
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

export { FilterString, FilterUriPrefix, FilterSite }
