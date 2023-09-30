import React from 'react'
import PropTypes from 'prop-types'
import { Tabs, Tab } from 'react-bootstrap'
import get from 'lodash/get'
import isUndefined from 'lodash/isUndefined'
import orderBy from 'lodash/orderBy'

import Checkbox from './common/Checkbox'
import MultiSelect from './common/MultiSelect'
import OrderedMultiSelect from './common/OrderedMultiSelect'
import Select from './common/Select'
import Text from './common/Text'
import Textarea from './common/Textarea'
import UriPrefix from './common/UriPrefix'

import { BackButton, SaveButton, DeleteButton } from '../common/Buttons'
import { ReadOnlyIcon } from '../common/Icons'

import PageInfo from '../info/PageInfo'
import DeletePageModal from '../modals/DeletePageModal'

import useDeleteModal from '../../hooks/useDeleteModal'

const EditPage = ({ config, page, elements, elementActions }) => {

  const { sites } = config
  const { elementAction, parent, attributes, conditions } = elements

  const elementValues = orderBy(page.questions.concat(page.questionsets), ['order', 'uri'])
  const elementOptions = elements.questions.map(question => ({
    value: 'question-' + question.id,
    label: interpolate(gettext('Question: %s'), [question.uri])
  })).concat(elements.questionsets.map(questionset => ({
    value: 'questionset-' + questionset.id,
    label: interpolate(gettext('Question set: %s'), [questionset.uri])
  })))

  const updatePage = (key, value) => {
    if (key == 'elements') {
      elementActions.updateElement(page, {
        questions: value.filter(e => !isUndefined(e.question)),
        questionsets: value.filter(e => !isUndefined(e.questionset))
      })
    } else {
      elementActions.updateElement(page, { [key]: value })
    }
  }
  const storePage = (back) => elementActions.storeElement('pages', page, back)
  const deletePage = () => elementActions.deleteElement('pages', page)

  const editElement = (value) => {
    if (value.questionset) {
      elementActions.fetchElement('questionsets', value.questionset)
    } else if (value.question) {
      elementActions.fetchElement('questions', value.question)
    }
  }
  const createQuestionSet = () => elementActions.createElement('questionsets', { page })
  const createQuestion = () => elementActions.createElement('questions', { page })

  const editCondition = (condition) => elementActions.fetchElement('conditions', condition)
  const createCondition = () => elementActions.createElement('conditions', { page })

  const editAttribute = (attribute) => elementActions.fetchElement('attributes', attribute)
  const createAttribute = () => elementActions.createElement('attributes', { page })

  const [showDeleteModal, openDeleteModal, closeDeleteModal] = useDeleteModal()

  const info = <PageInfo page={page} elements={elements} elementActions={elementActions} />

  return (
    <div className="panel panel-default panel-edit">
      <div className="panel-heading">
        <div className="pull-right">
          <ReadOnlyIcon title={gettext('This page is read only')} show={page.read_only} />
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storePage} disabled={page.read_only} />
          <SaveButton elementAction={elementAction} onClick={storePage} disabled={page.read_only} back={true}/>
        </div>
        {
          page.id ? <>
            <strong>{gettext('Page')}{': '}</strong>
            <code className="code-questions">{page.uri}</code>
          </> : <strong>{gettext('Create page')}</strong>
        }
      </div>

      {
        parent && parent.section && <div className="panel-body panel-border">
          <p dangerouslySetInnerHTML={{
            __html:interpolate(gettext('This page will be added to the section <code class="code-questions">%s</code>.'), [parent.section.uri])
          }} />
        </div>
      }

      {
        page.id && <div className="panel-body panel-border">
          { info }
        </div>
      }

      <div className="panel-body">
        <div className="row">
          <div className="col-sm-6">
            <UriPrefix config={config} element={page} field="uri_prefix"
                  onChange={updatePage} />
          </div>
          <div className="col-sm-6">
            <Text config={config} element={page} field="uri_path"
                  onChange={updatePage} />
          </div>
        </div>

        <Textarea config={config} element={page} field="comment"
                  rows={4} onChange={updatePage} />

        <div className="row">
          <div className="col-sm-6">
            <Checkbox config={config} element={page} field="locked"
                      onChange={updatePage} />
          </div>
          <div className="col-sm-6">
            <Checkbox config={config} element={page} field="is_collection"
                      onChange={updatePage} />
          </div>
        </div>

        <Tabs id="#page-tabs" defaultActiveKey={0} animation={false}>
          {
            config.settings && config.settings.languages.map(([lang_code, lang], index) => (
              <Tab key={index} eventKey={index} title={lang}>
                <Text config={config} element={page} field={`title_${lang_code }`}
                      onChange={updatePage} />
                <Textarea config={config} element={page} field={`help_${lang_code }`}
                          rows={4} onChange={updatePage} />
                <Text config={config} element={page} field={`verbose_name_${lang_code }`}
                      onChange={updatePage} />
              </Tab>
            ))
          }
        </Tabs>

        <Select config={config} element={page} field="attribute" verboseName={gettext('attribute')}
                options={attributes} onChange={updatePage} onCreate={createAttribute} onEdit={editAttribute} />

        <OrderedMultiSelect config={config} element={page} field="elements"
                            values={elementValues} options={elementOptions} verboseName={gettext('element')}
                            verboseNameCreate={gettext('question')} verboseNameAltCreate={gettext('question set')}
                            onChange={updatePage} onCreate={createQuestion} onAltCreate={createQuestionSet}
                            onEdit={editElement} />

        <MultiSelect config={config} element={page} field="conditions"
                     options={conditions} verboseName="condition"
                     onChange={updatePage} onCreate={createCondition} onEdit={editCondition} />

        {get(config, 'settings.multisite') && <Select config={config} element={page} field="editors"
                                                      options={sites} onChange={updatePage} isMulti />}
      </div>

      <div className="panel-footer">
        <div className="pull-right">
          <BackButton />
          <SaveButton elementAction={elementAction} onClick={storePage} disabled={page.read_only} />
          <SaveButton elementAction={elementAction} onClick={storePage} disabled={page.read_only} back={true}/>
        </div>
        {page.id && <DeleteButton onClick={openDeleteModal} disabled={page.read_only} />}
      </div>

      <DeletePageModal page={page} info={info} show={showDeleteModal}
                       onClose={closeDeleteModal} onDelete={deletePage} />
    </div>
  )
}

EditPage.propTypes = {
  config: PropTypes.object.isRequired,
  page: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

export default EditPage
