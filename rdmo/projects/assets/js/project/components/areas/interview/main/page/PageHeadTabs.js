import React, { useLayoutEffect, useRef, useState } from 'react'
import PropTypes from 'prop-types'
import { useDispatch } from 'react-redux'
import classNames from 'classnames'
import { isNil } from 'lodash'

import { activateSet } from '../../../../../actions/interviewActions'

const PageHeadTabs = ({ sets, values, currentSet }) => {
  const dispatch = useDispatch()

  const ref = useRef(null)
  const listRef = useRef(null)
  const listWidthRef = useRef(0)
  const listLabelsRef = useRef(null)

  const [collapsed, setCollapsed] = useState(false)
  const [availableWidth, setAvailableWidth] = useState(0)

  const getLabel = (set) => {
    const setValue = values.find((value) => (
      value.set_prefix == set.set_prefix && value.set_index == set.set_index
    ))
    return isNil(setValue) ? `#${set.set_index + 1}` : setValue.text
  }

  // the sets and values arrays change on every render, so the labels are used as dependency
  const labels = sets.map(getLabel).join('\n')

  useLayoutEffect(() => {
    // compare the width of the full list of tabs with the available width,
    // when the list is collapsed, the last measured width is used
    const update = () => {
      if (listRef.current) {
        listWidthRef.current = listRef.current.scrollWidth
        listLabelsRef.current = labels
      } else if (listLabelsRef.current != labels) {
        // the tabs have changed, show the full list again, so that it can be measured
        setCollapsed(false)
        return
      }
      setCollapsed(listWidthRef.current > ref.current.clientWidth)
      setAvailableWidth(ref.current.clientWidth)
    }

    update()

    const resizeObserver = new ResizeObserver(update)
    resizeObserver.observe(ref.current)

    return () => resizeObserver.disconnect()
  }, [collapsed, labels])

  const isActive = (set) => set.set_index == currentSet.set_index

  const handleActivate = (set) => {
    if (!isActive(set)) {
      dispatch(activateSet(set))
    }
  }

  const currentLabel = getLabel(currentSet)

  return (
    <div ref={ref} className="flex-grow-1" style={{ minWidth: 0 }}>
      {
        collapsed ? (
          <ul className="nav nav-underline flex-nowrap">
            <li className="nav-item dropdown" style={{ minWidth: 0 }}>
              <button
                type="button"
                title={currentLabel}
                className="nav-link dropdown-toggle active d-flex align-items-center w-100 px-3"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                <span className="text-truncate">{currentLabel}</span>
              </button>
              <ul className="dropdown-menu" style={{ minWidth: availableWidth }}>
                {
                  sets.map((set, setIndex) => (
                    <li key={setIndex}>
                      <button
                        type="button"
                        className={classNames('dropdown-item text-wrap', {active: isActive(set)})}
                        onClick={() => handleActivate(set)}
                      >
                        {getLabel(set)}
                      </button>
                    </li>
                  ))
                }
              </ul>
            </li>
          </ul>
        ) : (
          <ul ref={listRef} className="nav nav-underline flex-nowrap text-nowrap gap-0">
            {
              sets.map((set, setIndex) => {
                const setLabel = getLabel(set)
                return (
                  <li key={setIndex} className="nav-item flex-shrink-0">
                    <button
                      type="button"
                      title={setLabel}
                      className={classNames('nav-link px-3', {active: isActive(set)})}
                      onClick={() => handleActivate(set)}
                    >
                      {setLabel}
                    </button>
                  </li>
                )
              })
            }
          </ul>
        )
      }
    </div>
  )
}

PageHeadTabs.propTypes = {
  sets: PropTypes.array.isRequired,
  values: PropTypes.array.isRequired,
  currentSet: PropTypes.object.isRequired
}

export default PageHeadTabs
