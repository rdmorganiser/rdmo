import React from 'react'
import PropTypes from 'prop-types'
import { baseUrl } from 'rdmo/core/assets/js/utils/meta'

const HierarchyTree = ({ hierarchy }) => {
  const bulletStyle = { listStyleType: 'disc' }
  const isCurrentNode = (node) => node?.current === true || node?.current === 'true'

  const linkOrText = (node) => {
    const isCurrent = isCurrentNode(node)
    const content = (node?.permissions?.can_view_project && !isCurrent)
      ? <a href={`${baseUrl}/projects/${node.id}`}>{node.title}</a>
      : <>{node.title}</>

    return isCurrent ? <span className="fw-bold">{content}</span> : content
  }

  const renderFullSubtree = (node) => {
    if (!node?.children?.length) return null
    return (
      <ul style={bulletStyle}>
        {node.children.map(child => (
          <li key={child.id}>
            {linkOrText(child)}
            {renderFullSubtree(child)}
          </li>
        ))}
      </ul>
    )
  }

  const pathToCurrent = (node) => {
    if (!node) return null
    if (node.current) return [node]
    for (const child of (node.children || [])) {
      const path = pathToCurrent(child)
      if (path) return [node, ...path]
    }
    return null
  }

  const pathToCurrentFromRoot = (root) => {
    if (Array.isArray(root)) {
      for (const n of root) {
        const p = pathToCurrent(n)
        if (p) return p
      }
      return null
    }
    return pathToCurrent(root)
  }

  const path = pathToCurrentFromRoot(hierarchy)
  if (!path || path.length === 0) return null

  const renderPath = (idx) => {
    const node = path[idx]
    const isAtCurrentInPath = idx === path.length - 1

    if (idx === 0) {
      return (
        <>
          {linkOrText(node)}
          {isAtCurrentInPath
            ? renderFullSubtree(node)
            : <ul style={bulletStyle}>{renderPath(idx + 1)}</ul>}
        </>
      )
    }

    return (
      <li key={node.id}>
        {linkOrText(node)}
        {isAtCurrentInPath
          ? renderFullSubtree(node)
          : <ul style={bulletStyle}>{renderPath(idx + 1)}</ul>}
      </li>
    )
  }

  return (
    <div className="ms-2">{renderPath(0)}</div>
  )
}

const nodeShape = PropTypes.shape({
  id: PropTypes.oneOfType([PropTypes.number, PropTypes.string]).isRequired,
  title: PropTypes.string.isRequired,
  current: PropTypes.bool,
  permissions: PropTypes.shape({
    can_view_project: PropTypes.bool,
    can_change_project: PropTypes.bool,
    can_delete_project: PropTypes.bool
  }),
  children: PropTypes.array
})
  PropTypes.arrayOf(() => nodeShape)
HierarchyTree.propTypes = {
  hierarchy: PropTypes.oneOfType([
    nodeShape,
    PropTypes.arrayOf(nodeShape)
  ]).isRequired
}

export default HierarchyTree
