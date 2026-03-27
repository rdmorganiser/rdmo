import React, { useRef } from 'react'
import PropTypes from 'prop-types'
import { useDrag, useDrop } from 'react-dnd'
import { useDispatch } from 'react-redux'
import classNames from 'classnames'

import { dropElement } from '../../actions/elementActions'

const Drag = ({ element, show=true }) => {
  const dragRef = useRef(null)

  const [{}, drag] = useDrag(() => ({
    type: element.model,
    item: element
  }), [element])

  drag(dragRef)

  const className = classNames('bi bi-arrows-move drag', {
    'disabled': element.read_only
  })

  return show && <span className="drag">
    <i className={className} ref={dragRef} aria-hidden="true"></i>
  </span>
}

Drag.propTypes = {
  element: PropTypes.object.isRequired,
  show: PropTypes.bool
}

const Drop = ({ element, indent=0, mode='in', children=null }) => {
  const dispatch = useDispatch()

  const dropRef = useRef(null)

  let accept
  if (mode == 'in') {
    accept = {
      'questions.section': ['questions.page'],
      'questions.page': ['questions.questionset', 'questions.question'],
      'questions.questionset': ['questions.questionset', 'questions.question']
    }[element.model]
  } else {
    accept = {
      'questions.section': ['questions.section'],
      'questions.page': ['questions.page'],
      'questions.questionset': ['questions.questionset', 'questions.question'],
      'questions.question': ['questions.questionset', 'questions.question']
    }[element.model]
  }

  const [{ isDragging, isOver }, drop] = useDrop(() => ({
    accept: accept,
    collect: (monitor) => ({
      isDragging: accept.includes(monitor.getItemType()),
      isOver: monitor.isOver()
    }),
    drop: (item) => {
      dispatch(dropElement(item, element, mode))
    },
  }), [element])

  drop(dropRef)

  const dropClassName = classNames({
    'drop-in': mode == 'in',
    'drop': mode != 'in',
    'show': isDragging,
    'over': isOver
  })

  if (mode == 'in') {
    return <div className={dropClassName} ref={dropRef}>{children}</div>
  } else {
    return <div className={dropClassName} ref={dropRef} style={{ marginLeft: `${indent}rem` }}></div>
  }
}

Drop.propTypes = {
  element: PropTypes.object.isRequired,
  mode: PropTypes.string,
  indent: PropTypes.number,
  children: PropTypes.oneOfType([PropTypes.arrayOf(PropTypes.node), PropTypes.node])
}

export { Drag, Drop }
