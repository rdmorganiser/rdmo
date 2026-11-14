import React from 'react'
import { useSelector } from 'react-redux'
import { isEmpty } from 'lodash'

const Pending = () => {
  const pending = useSelector((state) => state.pending)

  return (
    !isEmpty(pending.items) && (
      <span className="spinner-border spinner-border-sm" aria-hidden="true"></span>
    )
  )
}

export default Pending
