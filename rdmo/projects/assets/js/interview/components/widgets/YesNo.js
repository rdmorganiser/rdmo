import React from 'react'
import PropTypes from 'prop-types'

const YesNo = ({ question }) => {
  console.log(question)

  return (
    <div>

    </div>
  )
}

YesNo.propTypes = {
  question: PropTypes.object.isRequired
}

export default YesNo
