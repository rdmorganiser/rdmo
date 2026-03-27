import React, { useState } from 'react'
import { TileGrid } from '../helper'

import Tooltip from 'rdmo/core/assets/js/_bs53/components/Tooltip'

import PluginForm from '../helper/PluginForm'

const Dashboard = () => {
  const [tileSize, setTileSize] = useState('normal')

  const toggleSize = () => {
    setTileSize((prevSize) => {
      if (prevSize === 'compact') return 'normal'
      if (prevSize === 'normal') return 'fullWidth'
      return 'compact'
    })
  }

  const tiles = [
    { title: 'Tile 1', content: <p>Content 1</p> },
    { title: 'Tile 2', content: <p>Content 2</p> },
    { title: 'Tile 3', content: <p>Content 3</p> },
    { title: 'Tile 4', content: <p>Content 4</p> },
    { title: 'Tile 5', content: <p>Content 5</p> },
    { title: 'Tile 6', content: <p>Content 6</p> },
  ]

  const html = '<form><input class="form-control mb-3" type="text" name="input" /><button type="submit" class="btn btn-primary">Submit</button></form>'

  return (
    <div>
      <h1>{gettext('Dashboard')}</h1>

      <div className="mt-5">
        <button className="btn btn-primary mb-3" onClick={toggleSize}>
              Toggle Tile Size (Current: {tileSize})
        </button>

        <TileGrid tiles={tiles} size={tileSize} />

        <div>
          <Tooltip title={<>TITLE</>} placement="top">
            <span>TOOLTIP</span>
          </Tooltip>
        </div>

        <PluginForm html={html} />
      </div>
    </div>
  )
}

export default Dashboard
