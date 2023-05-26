import React, { Component, useRef } from 'react'
import { useDrag, useDrop } from 'react-dnd'
import PropTypes from 'prop-types'
import classNames from 'classnames'

import { dragAndDropTypes } from '../../constants/elements'
import { compareElements } from '../../utils/elements'

const Drag = ({ element }) => {
  const dragRef = useRef(null)
  const dragType = dragAndDropTypes[element.model]

  const [{}, drag] = useDrag(() => ({
    type: dragAndDropTypes[element.model],
    item: element
  }), [element])

  drag(dragRef)

  return <span className="element-link drag">
    <i className="fa fa-arrows drag" ref={dragRef}></i>
  </span>
}

Drag.propTypes = {
  element: PropTypes.object.isRequired
}

const Drop = ({ element, elementActions, indent=0 }) => {
  const dropRef = useRef(null)
  const dropType = dragAndDropTypes[element.model]

  const [{ isDragging, isOver }, drop] = useDrop(() => ({
    accept: dropType,
    collect: (monitor) => ({
      isDragging: monitor.getItemType() == dropType,
      isOver: monitor.isOver()
    }),
    drop: (item, monitor) => {
      elementActions.moveElement(item, element);
    },
  }), [element])

  drop(dropRef)

  const dropClassName = classNames({
    'drop': true,
    'show': isDragging,
    'over': isOver
  })

  return <div className={dropClassName} ref={dropRef} style={{ marginLeft: 30 * indent }}></div>
}

Drop.propTypes = {
  element: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  indent: PropTypes.number
}

export { Drag, Drop }
