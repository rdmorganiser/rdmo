import React from 'react'
import PropTypes from 'prop-types'

const PluginInfo = ({ plugin }) => {
  return (
    <div className="element-info">
      <p>
        <strong>{gettext('Plugin type')}</strong>{': '}
        <code className="code-config">{plugin.plugin_type || gettext('Unknown')}</code>
      </p>
      <p>
        <strong>{gettext('Python path')}</strong>{': '}
        <code className="code-config">{plugin.python_path}</code>
      </p>
    </div>
  )
}

PluginInfo.propTypes = {
  plugin: PropTypes.object.isRequired
}

export default PluginInfo
