import React from 'react'
import PropTypes from 'prop-types'

const Sidebar = ({ menuItems, onNavigate, activePage }) => {
  return (
    <div className="d-flex flex-column flex-shrink-0 p-3 bg-light" style={{ width: '250px', height: '100vh'}}>
      <h5 className="fw-bold">TU dmo</h5>
      <hr />

      <ul className="nav nav-pills flex-column mb-auto">
        {menuItems.map((section) => (
          <div key={section.title}>
            {section.title && <h6 className="text-muted mt-3 mb-2">{section.title}</h6>}

            {section.items.map((item) => (
              <li key={item.id} className="nav-item">
                <button
                  className={`nav-link w-100 text-start d-flex align-items-center gap-2 ${activePage === item.id ? 'active' : 'text-dark'}`}
                  onClick={() => onNavigate(item.id)}
                  style={{ paddingLeft: '0.5rem' }}
                >
                  <i className={`bi ${item.icon}`}></i>
                  {item.name}
                </button>
              </li>
            ))}
          </div>
        ))}
      </ul>

      {/* Keep "Zur Projektübersicht" as a direct link */}
      <div className="mt-auto pt-3">
        <a
          href="/projects"
          className="nav-link text-dark w-100 text-start d-flex align-items-center gap-2"
          style={{ paddingLeft: '0.5rem' }}
        >
          <i className="bi bi-arrow-left"></i> Zur Projektübersicht
        </a>
      </div>
    </div>
  )
}

Sidebar.propTypes = {
  menuItems: PropTypes.arrayOf(
    PropTypes.shape({
      title: PropTypes.string,
      items: PropTypes.arrayOf(
        PropTypes.shape({
          id: PropTypes.string.isRequired,
          name: PropTypes.string.isRequired,
          icon: PropTypes.string,
        })
      ).isRequired,
    })
  ).isRequired,
  onNavigate: PropTypes.func.isRequired,
  activePage: PropTypes.string.isRequired, // ✅ Added to track selected item
}

export default Sidebar
