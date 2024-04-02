import React from 'react'
import PropTypes from 'prop-types'

const Text = ({ question }) => {
  console.log(question)

  return (
    <div>

    </div>
  )
}

Text.propTypes = {
  question: PropTypes.object.isRequired
}

export default Text
