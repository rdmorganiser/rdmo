import React from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap'
import get from 'lodash/get'

import Checkbox from './common/Checkbox'
import JsonField from './common/JsonField'
import Number from './common/Number'
import Select from './common/Select'
import Text from './common/Text'
import Textarea from './common/Textarea'
import UriPrefix from './common/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/Buttons'
import { ReadOnlyIcon } from '../common/Icons'

import PluginInfo from '../info/PluginInfo'
import DeletePluginModal from '../modals/DeletePluginModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditPlugin = ({ config, plugin, elements, elementActions}) => {

  const { sites, groups } = config
  const { elementAction, catalogs } = elements

  const updatePlugin = (key, value) => elementActions.updateElement(plugin, {[key]: value})
  const storePlugin = (back) => elementActions.storeElement('plugins', plugin, elementAction, back)
  const deletePlugin = () => elementActions.deleteElement('plugins', plugin)

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <PluginInfo plugin={plugin} elements={elements} />

  const pluginModel = plugin.model || 'config.plugin'
  const pythonPathOptions = get(config, ['meta', pluginModel, 'python_path', 'choices'], [])
    .map(([value, label]) => ({id: value, name: label}))

  return (
    <div className="panel panel-default panel-edit">
      <div className="panel-heading">
        <div className="pull-right">
          <ReadOnlyIcon title={gettext('This plugin is read only')} show={plugin.read_only} />
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storePlugin} disabled={plugin.read_only} />
          <SaveButton elementAction={elementAction} onClick={storePlugin} disabled={plugin.read_only} back={true}/>
        </div>
        {
          plugin.id ? <>
            <strong>{gettext('Plugin')}{': '}</strong>
            <code className="code-config">{plugin.uri}</code>
          </> : <strong>{gettext('Create plugin')}</strong>
        }
      </div>

      {
        plugin.id && <div className="panel-body panel-border">
          { info }
        </div>
      }

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={plugin} field="uri_prefix"
                       onChange={updatePlugin} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={plugin} field="uri_path"
                  onChange={updatePlugin} />
          </div>
        </div>

        <Text config={config} element={plugin} field="url_name"
              onChange={updatePlugin} />

        <Textarea config={config} element={plugin} field="comment"
                  rows={4} onChange={updatePlugin} />

        <div className="row">
          <div className="col-sm-4">
            <Checkbox config={config} element={plugin} field="locked"
                      onChange={updatePlugin} />
          </div>
          <div className="col-sm-4">
            <Checkbox config={config} element={plugin} field="available"
                      onChange={updatePlugin} />
          </div>
          <div className="col-sm-4">
            <Number config={config} element={plugin} field="order"
                    onChange={updatePlugin} />
          </div>
        </div>

        <Select config={config} element={plugin} field="python_path"
                options={pythonPathOptions} onChange={updatePlugin} />

        <Tabs id="#plugin-tabs" defaultActiveKey={0} animation={false}>
          {
            config.settings && config.settings.languages.map(([lang_code, lang], index) => (
              <Tab className="pt-10" key={index} eventKey={index} title={lang}>
                <Text config={config} element={plugin} field={`title_${lang_code }`}
                      onChange={updatePlugin} />
              </Tab>
            ))
          }
        </Tabs>

        <Select config={config} element={plugin} field="catalogs"
                options={catalogs} onChange={updatePlugin} isMulti />

        {get(config, 'settings.groups') && <Select config={config} element={plugin} field="groups"
                                                   options={groups} onChange={updatePlugin} isMulti />}

        {get(config, 'settings.multisite') && <Select config={config} element={plugin} field="sites"
                                                      options={sites} onChange={updatePlugin} isMulti />}

        {get(config, 'settings.multisite') && <Select config={config} element={plugin} field="editors"
                                                      options={sites} onChange={updatePlugin} isMulti />}

        <JsonField config={config} element={plugin} field="plugin_settings"
                   onChange={updatePlugin} />
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storePlugin} disabled={plugin.read_only} />
          <SaveButton elementAction={elementAction} onClick={storePlugin} disabled={plugin.read_only} back={true}/>
        </div>
        {plugin.id && <DeleteButton onClick={openDeleteModal} disabled={plugin.read_only} />}
      </div>

      <DeletePluginModal plugin={plugin} info={info} show={showDeleteModal}
                         onClose={closeDeleteModal} onDelete={deletePlugin} />
    </div>
  )
}

EditPlugin.propTypes = {
  config: PropTypes.object.isRequired,
  plugin: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default EditPlugin
