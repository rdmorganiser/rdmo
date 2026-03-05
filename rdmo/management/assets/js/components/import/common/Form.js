import React from 'react'
import { useDispatch } from 'react-redux'
import PropTypes from 'prop-types'
import isUndefined from 'lodash/isUndefined'

import { updateElement } from '../../../actions/importActions'

import Key from './Key'
import UriPath from './UriPath'
import UriPrefix from './UriPrefix'

const Form = ({ element }) => {
  const dispatch = useDispatch()

  const handleChange = (key, value) => dispatch(updateElement(element, {[key]: value}))

  return (
    <div className="row">
      <div className="col-sm-6">
        <UriPrefix element={element} onChange={handleChange} />
      </div>
      <div className="col-sm-6">
        {
          isUndefined(element.uri_path) ? <Key element={element} onChange={handleChange} />
                                        : <UriPath element={element} onChange={handleChange} />
        }
      </div>
    </div>
  )
}

Form.propTypes = {
  element: PropTypes.object.isRequired
}

export default Form
