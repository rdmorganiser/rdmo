export const findById = (node, id) => {
  if (node.id === id) {
    return node
  }

  if (node.children && node.children.length > 0) {
    for (const child of node.children) {
      const found = findById(child, id)
      if (found) return found
    }
  }

  return null
}
