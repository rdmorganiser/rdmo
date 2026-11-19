import React, { useState } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'

const Tabs = ({ labels, tabs }) => {
  const [activeTab, setActiveTab] = useState(0)

  return (
    <div className="mb-3">
      <ul className="nav nav-tabs">
        {
          labels.map((label, index) => (
            <li key={index} className="nav-item">
              <button
                className={classNames('nav-link', {'active': index === activeTab})}
                onClick={() => setActiveTab(index)}>{label}</button>
            </li>
          ))
        }
      </ul>

      <div className="border-start border-end border-bottom rounded-bottom-2 p-3 pb-0 mb-3">
        {tabs[activeTab]}
      </div>
    </div>
  )
}

Tabs.propTypes = {
  labels: PropTypes.array,
  tabs: PropTypes.array
}

export default Tabs
