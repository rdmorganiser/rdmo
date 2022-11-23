import React, { Component} from 'react'
import PropTypes from 'prop-types'

const Sections = ({ sections }) => {
  return (
    <div className="sections">
      <div className="panel panel-default">
        <div className="panel-body">
          <strong>Sections</strong>
        </div>
      </div>
      {
        sections.map((section, index) => {
          return (
            <div key={index} className="panel panel-default">
              <div className="panel-heading">
                <strong>Section</strong> {section.title}
              </div>
              <div className="panel-body">
                <code className="code-questions">{section.uri}</code>
              </div>
            </div>
          )
        })
      }
    </div>
  )
}

Sections.propTypes = {
  sections: PropTypes.array.isRequired
}

export default Sections
