import React from 'react'
import PropTypes from 'prop-types'
import { Dropdown } from 'bootstrap'
import { useSelector } from 'react-redux'

const ExportsDropdown = ({ onExport }) => {

  const exportFormats = useSelector((state) => state.settings.export_formats) ?? {}


  const handleClick = (event, format) => {
    event.stopPropagation()
    onExport(format)

    // ensure that the dropdown is closed
    const dropdownElement = event.currentTarget.closest('.dropdown')?.querySelector('[data-bs-toggle="dropdown"]')
    const dropdown = Dropdown.getInstance(dropdownElement)
    dropdown?.hide()
  }

  return (
    <div className="dropdown dropdown-menu-end">
      <button
        type="button"
        className="link text-nowrap"
        data-bs-toggle="dropdown"
        data-bs-popper-config='{"strategy":"fixed"}'
        aria-expanded="false"
        onClick={(event) => event.stopPropagation()}
        title={gettext('Download')}
      >
        {gettext('Download')} <i className="bi bi-caret-down-fill ms-1" />
      </button>

      <ul className="dropdown-menu">
        {
          exportFormats.map(([format, label]) => (
            <li key={format}>
              <button className="dropdown-item" onClick={(event) => handleClick(event, format)}>
                {label}
              </button>
            </li>
          ))
        }
      </ul>
    </div>
  )
}

ExportsDropdown.propTypes = {
  onExport: PropTypes.func,
  title: PropTypes.bool,
}

export default ExportsDropdown
