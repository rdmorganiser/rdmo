import React from 'react'
import PropTypes from 'prop-types'
import Tile from './Tile'

const TileGrid = ({ tiles, size = 'normal' }) => {
  return (
    <div className="container-fluid">
      <div className="row">
        {tiles.map((tile, index) => (
          <Tile key={index} title={tile.title} size={size}>
            {tile.content}
          </Tile>
        ))}
      </div>
    </div>
  )
}

TileGrid.propTypes = {
  tiles: PropTypes.arrayOf(
    PropTypes.shape({
      title: PropTypes.string.isRequired,
      content: PropTypes.node.isRequired,
    })
  ).isRequired,
  size: PropTypes.oneOf(['compact', 'normal', 'fullWidth']),
}

export default TileGrid
