import React, { Component, useRef } from 'react'
import { useDrag, useDrop } from 'react-dnd'
import PropTypes from 'prop-types'
import classNames from 'classnames'

import { dragAndDropTypes } from '../../constants/elements'
import { compareElements } from '../../utils/elements'

const Drag = ({ element }) => {
  const dragRef = useRef(null)

  const [{}, drag] = useDrag(() => ({
    type: element.model,
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

const DropAfter = ({ element, elementActions, indent=0 }) => {
  const dropRef = useRef(null)

  const dropTypes = {
    'questions.section': ['questions.section'],
    'questions.page': ['questions.page'],
    'questions.questionset': ['questions.questionset', 'questions.question'],
    'questions.question': ['questions.questionset', 'questions.question']
  }[element.model]

  const [{ isDragging, isOver }, drop] = useDrop(() => ({
    accept: dropTypes,
    collect: (monitor) => ({
      isDragging: dropTypes.includes(monitor.getItemType()),
      isOver: monitor.isOver()
    }),
    drop: (item, monitor) => {
      elementActions.dropAfterElement(item, element);
    },
  }), [element])

  drop(dropRef)

  const dropClassName = classNames({
    'drop-after': true,
    'show': isDragging,
    'over': isOver
  })

  return <div className={dropClassName} ref={dropRef} style={{ marginLeft: 30 * indent }}></div>
}

DropAfter.propTypes = {
  element: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  indent: PropTypes.number
}

const DropIn = ({ element, elementActions, children }) => {
  const dropRef = useRef(null)

  const dropTypes = {
    'questions.section': ['questions.page'],
    'questions.page': ['questions.questionset', 'questions.question'],
    'questions.questionset': ['questions.questionset', 'questions.question']
  }[element.model]

  const [{ isDragging, isOver }, drop] = useDrop(() => ({
    accept: dropTypes,
    collect: (monitor) => ({
      isDragging: dropTypes.includes(monitor.getItemType()),
      isOver: monitor.isOver()
    }),
    drop: (item, monitor) => {
      elementActions.dropInElement(item, element);
    },
  }), [element])

  drop(dropRef)

  const dropClassName = classNames({
    'drop-in': true,
    'show': isDragging,
    'over': isOver
  })

  return <div className={dropClassName} ref={dropRef}>{children}</div>
}

DropIn.propTypes = {
  element: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export { Drag, DropAfter, DropIn }
