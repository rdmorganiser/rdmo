import React, { Component} from 'react'
import PropTypes from 'prop-types'

import Section from './Section'

const Catalog = ({ catalog }) => {
    return (
        <div>
            <h2>{catalog.title}</h2>
            <p>{catalog.help}</p>
            {
                catalog.sections.map((section, index) => (
                    <Section section={section} key={index} />
                ))
            }
        </div>
    )
}

Catalog.propTypes = {
  catalog: PropTypes.object.isRequired
}

export default Catalog
