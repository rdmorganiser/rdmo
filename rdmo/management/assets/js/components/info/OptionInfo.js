import React from 'react'
import PropTypes from 'prop-types'
import { useDispatch, useSelector } from 'react-redux'

import Html from 'rdmo/core/assets/js/components/Html'

import { fetchElement } from '../../actions/elementActions'
import useBool from '../../hooks/useBool'

import { CodeLink, ExtendLink } from '../common/Links'

const OptionInfo = ({ option }) => {
  const dispatch = useDispatch()

  const elements = useSelector((state) => state.elements)

  const [extendConditions, toggleConditions] = useBool(false)

  const conditions = elements.conditions.filter(e => option.conditions.includes(e.id))

  const fetchCondition = (condition) => dispatch(fetchElement('conditions', condition.id))

  return (
    <div className="mb-2">
      <p className="mb-1">
        <Html html={
          interpolate(ngettext(
            'This option is used for <b>%s values</b> in <b>one project</b>.',
            'This option is used for <b>%s values</b> in <b>%s projects</b>.',
            option.projects_count), [option.values_count, option.projects_count])
        } />
      </p>
      <p className="mb-1">
        <Html html={
          interpolate(ngettext(
            'This option is used in <b>one condition</b>.',
            'This option is used in <b>%s conditions</b>.',
            conditions.length
          ), [conditions.length])
        } />
        {conditions.length > 0 && <ExtendLink extend={extendConditions} onClick={toggleConditions} />}
      </p>
      {
        extendConditions && conditions.map((condition, index) => (
          <p className="mb-1" key={index}>
            <CodeLink type="conditions" uri={condition.uri} onClick={() => fetchCondition(condition)} />
          </p>
        ))
      }
    </div>
  )
}

OptionInfo.propTypes = {
  option: PropTypes.object.isRequired
}

export default OptionInfo
