import React, { Component } from 'react'
import PropTypes from 'prop-types'

import { ExtendLink } from '../common/Links'

import useBool from '../../hooks/useBool'

const OptionInfo = ({ option, elements }) => {

  const [extendConditions, toggleConditions] = useBool(false)

  const conditions = elements.conditions.filter(e => option.conditions.includes(e.id))

  return (
    <div className="element-info">
      <p dangerouslySetInnerHTML={{
        __html: interpolate(ngettext(
          'This option is used for <b>%s values</b> in <b>one project</b>.',
          'This option is used for <b>%s values</b> in <b>%s projects</b>.',
          option.projects_count), [option.values_count, option.projects_count])}} />
      {
        conditions.length > 0 && <>
          <p>
            <span dangerouslySetInnerHTML={{
              __html: interpolate(ngettext(
                'This option is used in <b>one condition</b>.',
                'This option is used in <b>%s conditions</b>.',
                conditions.length
              ), [conditions.length])}} />
            <ExtendLink extend={extendConditions} onClick={toggleConditions} />
          </p>
          {
            extendConditions && conditions.map((condition, index) => (
              <p key={index}>
                <code className="code-conditions">{condition.uri}</code>
              </p>
            ))
          }
        </>
      }
    </div>
  )
}

OptionInfo.propTypes = {
  option: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired
}

export default OptionInfo
