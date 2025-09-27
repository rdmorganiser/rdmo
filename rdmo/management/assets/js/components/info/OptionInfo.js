import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import PropTypes from 'prop-types'

import Html from 'rdmo/core/assets/js/components/Html'

import { fetchElement } from '../../actions/elementActions'

import { ExtendLink, CodeLink } from '../common/Links'

import useBool from '../../hooks/useBool'

const OptionInfo = ({ option }) => {
  const dispatch = useDispatch()

  const elements = useSelector((state) => state.elements)

  const [extendConditions, toggleConditions] = useBool(false)

  const conditions = elements.conditions.filter(e => option.conditions.includes(e.id))

  const fetchCondition = (condition) => dispatch(fetchElement('conditions', condition.id))

  return (
    <div className="element-info">
      <p>
        <Html html={interpolate(ngettext(
          'This option is used for <b>%s values</b> in <b>one project</b>.',
          'This option is used for <b>%s values</b> in <b>%s projects</b>.',
          option.projects_count), [option.values_count, option.projects_count])} />
      </p>
      <p>
        <Html html={interpolate(ngettext(
          'This option is used in <b>one condition</b>.',
          'This option is used in <b>%s conditions</b>.',
          conditions.length
        ), [conditions.length])} />
        {conditions.length > 0 && <ExtendLink extend={extendConditions} onClick={toggleConditions} />}
      </p>
      {
        extendConditions && conditions.map((condition, index) => (
          <p key={index}>
            <CodeLink className="code-conditions" uri={condition.uri} onClick={() => fetchCondition(condition)} />
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
