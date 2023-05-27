import React from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap'

import Checkbox from './common/Checkbox'
import OrderedMultiSelect from './common/OrderedMultiSelect'
import Text from './common/Text'
import Textarea from './common/Textarea'
import UriPrefix from './common/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/Buttons'

import SectionInfo from '../info/SectionInfo'
import DeleteSectionModal from '../modals/DeleteSectionModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditSection = ({ config, section, elements, elementActions }) => {

  const { elementAction, parent, pages } = elements

  const updateSection = (key, value) => elementActions.updateElement(section, {[key]: value})
  const storeSection = (back) => elementActions.storeElement('sections', section, back)
  const deleteSection = () => elementActions.deleteElement('sections', section)

  const editPage = (value) => elementActions.fetchElement('pages', value.page)
  const createPage = () => elementActions.createElement('pages', { section })

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <SectionInfo section={section} elements={elements} elementActions={elementActions} />

  return (
    <div className="panel panel-default">
      <div className="panel-heading">
        <div className="pull-right">
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeSection} />
          <SaveButton elementAction={elementAction} onClick={storeSection} back={true}/>
        </div>
        {
          section.id ? <>
            <strong>{gettext('Section')}{': '}</strong>
            <code className="code-questions">{section.uri}</code>
          </> : <strong>{gettext('Create section')}</strong>
        }
      </div>

      {
        parent && parent.catalog && <div className="panel-body panel-border">
          <p dangerouslySetInnerHTML={{
            __html:interpolate(gettext('This section will be added to the catalog <code class="code-questions">%s</code>.'), [parent.catalog.uri])
          }} />
        </div>
      }

      {
        section.id && <div className="panel-body panel-border">
          { info }
        </div>
      }

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={section} field="uri_prefix"
                       onChange={updateSection} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={section} field="uri_path"
                  onChange={updateSection} />
          </div>
        </div>

        <Textarea config={config} element={section} field="comment"
                  rows={4} onChange={updateSection} />

        <Checkbox config={config} element={section} field="locked"
                  onChange={updateSection} />

        <Tabs id="#section-tabs" defaultActiveKey={0} animation={false}>
          {
            config.settings && config.settings.languages.map(([lang_code, lang], index) => (
              <Tab key={index} eventKey={index} title={lang}>
                <Text config={config} element={section} field={`title_${lang_code }`}
                      onChange={updateSection} />
              </Tab>
            ))
          }
        </Tabs>

        <OrderedMultiSelect config={config} element={section} field="pages"
                            options={pages} verboseName="page"
                            onChange={updateSection} onCreate={createPage} onEdit={editPage} />
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storeSection} />
          <SaveButton elementAction={elementAction} onClick={storeSection} back={true}/>
        </div>
          {section.id && <DeleteButton onClick={openDeleteModal} />}
      </div>

      <DeleteSectionModal section={section} info={info} show={showDeleteModal}
                          onClose={closeDeleteModal} onDelete={deleteSection} />
    </div>
  )
}

EditSection.propTypes = {
  config: PropTypes.object.isRequired,
  section: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default EditSection
