import React, { useRef } from 'react'
import { useDrag, useDrop } from 'react-dnd'
import PropTypes from 'prop-types'
import classNames from 'classnames'

const Drag = ({ element, show=true }) => {
  const dragRef = useRef(null)

  const [{}, drag] = useDrag(() => ({
    type: element.model,
    item: element
  }), [element])

  drag(dragRef)

  return show && <span className="element-link drag">
    <i className="fa fa-arrows drag" ref={dragRef}></i>
  </span>
}

Drag.propTypes = {
  element: PropTypes.object.isRequired,
  show: PropTypes.bool
}

const Drop = ({ element, elementActions, indent=0, mode='in', children=null }) => {
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
      elementActions.dropElement(item, element, mode)
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
    return <div className={dropClassName} ref={dropRef} style={{ marginLeft: 30 * indent }}></div>
  }
}

Drop.propTypes = {
  element: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired,
  mode: PropTypes.string,
  indent: PropTypes.number,
  children: PropTypes.oneOfType([PropTypes.arrayOf(PropTypes.node), PropTypes.node])
}

export { Drag, Drop }
