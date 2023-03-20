import React, { useState } from 'react'

const useDeleteModal = () => {
  const [showDeleteModal, toggleDeleteModal] = useState(false);
  const openDeleteModal = () => toggleDeleteModal(true)
  const closeDeleteModal = () => toggleDeleteModal(false)

  return [showDeleteModal, openDeleteModal, closeDeleteModal]
}

export default useDeleteModal
