import React from 'react'
import { useSelector } from 'react-redux'
import { Dropdown } from 'bootstrap'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { isNil } from 'lodash'

const SnapshotsDropdown = ({ onChange }) => {
  const { snapshotId } = useSelector((state) => state.config)
  const { snapshots } = useSelector((state) => state.project?.project)

  const handleClick = (event, snapshot) => {
    event.stopPropagation()

    onChange(snapshot)

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
        title={gettext('Snapshots')}
      >
        {gettext('Snapshot')} <i className="bi bi-caret-down-fill ms-1" />
      </button>

      <ul className="dropdown-menu">
        <button className={classNames('dropdown-item', { active: isNil(snapshotId) })}
                onClick={(event) => handleClick(event, null)}>
          {gettext('Current')}
        </button>
        {
          snapshots.map((snapshot) => (
            <li key={snapshot.id}>
              <button className="dropdown-item" onClick={(event) => handleClick(event, snapshot)}>
                {snapshot.title}
              </button>
            </li>
          ))
        }
      </ul>
    </div>
  )
}

SnapshotsDropdown.propTypes = {
  onChange: PropTypes.func
}

export default SnapshotsDropdown
