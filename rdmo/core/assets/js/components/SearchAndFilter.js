import React from 'react'
import PropTypes from 'prop-types'
import { debounce } from 'lodash'

const SearchField = ({ value, onChange, onSearch, placeholder, delay }) => {
  const handleSearch = debounce(() => {
    onSearch(value)
  }, delay ?? 300)

  const handleChange = (newValue) => {
    onChange(newValue)
  }

  const handleButtonClick = () => {
    onChange('')
    handleSearch()
  }

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      handleSearch()
    }
  }

  return (
    <div className="form-group mb-0">
      <div className="input-group">
        <input
          type="text"
          className="form-control"
          placeholder={placeholder}
          value={value}
          onChange={(e) => handleChange(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <span className="input-group-btn">
          <button className="btn btn-default" onClick={handleButtonClick}>
            <span className="fa fa-times"></span>
          </button>
          <button className="btn btn-primary" onClick={handleSearch}>
            Search
          </button>
        </span>
      </div>
    </div>
  )
}

SearchField.propTypes = {
  value: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  onSearch: PropTypes.func.isRequired,
  placeholder: PropTypes.string.isRequired,
  delay: PropTypes.number, // Optional: Specify the delay time in milliseconds
}

const TextField = ({ value, onChange, placeholder }) => {
  return (
    <div className="form-group mb-0">
      <div className="input-group">
        <input type="text" className="form-control" placeholder={placeholder}
               value={ value } onChange={e => onChange(e.target.value)}></input>
        <span className="input-group-btn">
          <button className="btn btn-default" onClick={() => onChange('')}>
            <span className="fa fa-times"></span>
          </button>
        </span>
      </div>
    </div>
  )
}

TextField.propTypes = {
  value: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  placeholder: PropTypes.string.isRequired
}

const Select = ({ value, options, onChange, placeholder }) => {
  return (
    <div className="form-group mb-0">
      <select className="form-control" value={value} onChange={e => onChange(e.target.value)}>
        <option value="">{placeholder}</option>
        {
          options.map((option, index) => <option value={option} key={index}>{option}</option>)
        }
      </select>
    </div>
  )
}

Select.propTypes = {
  value: PropTypes.string,
  options: PropTypes.array.isRequired,
  onChange: PropTypes.func,
  placeholder: PropTypes.string
}

export { SearchField, Select, TextField }
