import React, { Component} from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import isEmpty from 'lodash/isEmpty';
import * as configActions from '../actions/configActions'
import * as elementActions from '../actions/elementActions'
import isNil from 'lodash/isNil'

import ApiErrors from '../components/ApiErrors'

import Attributes from '../components/elements/Attributes'
import Catalogs from '../components/elements/Catalogs'
import Conditions from '../components/elements/Conditions'
import Options from '../components/elements/Options'
import OptionSets from '../components/elements/OptionSets'
import Pages from '../components/elements/Pages'
import Questions from '../components/elements/Questions'
import QuestionSets from '../components/elements/QuestionSets'
import Sections from '../components/elements/Sections'
import Tasks from '../components/elements/Tasks'
import Views from '../components/elements/Views'

import EditAttribute from '../components/edit/EditAttribute'
import EditCatalog from '../components/edit/EditCatalog'
import EditCondition from '../components/edit/EditCondition'
import EditOption from '../components/edit/EditOption'
import EditOptionSet from '../components/edit/EditOptionSet'
import EditPage from '../components/edit/EditPage'
import EditQuestion from '../components/edit/EditQuestion'
import EditQuestionSet from '../components/edit/EditQuestionSet'
import EditSection from '../components/edit/EditSection'
import EditTask from '../components/edit/EditTask'
import EditView from '../components/edit/EditView'

import NestedAttribute from '../components/nested/NestedAttribute'
import NestedCatalog from '../components/nested/NestedCatalog'
import NestedOptionSet from '../components/nested/NestedOptionSet'
import NestedPage from '../components/nested/NestedPage'
import NestedQuestionSet from '../components/nested/NestedQuestionSet'
import NestedSection from '../components/nested/NestedSection'

class Main extends Component {

  constructor(props) {
    super(props)
  }

  render() {
    const { config, elements, errors, elementActions } = this.props

    if (!isNil(elements.errors) && !isNil(elements.errors.api)) {
      return <ApiErrors errors={elements.errors.api} />
    } else {
      const element = elements.element

      switch (elements.elementType) {
        case 'catalogs':
          if (isNil(elements.element)) {
            return <Catalogs config={config} catalogs={elements.catalogs} elementActions={elementActions} />
          } else if (elements.elementAction == 'nested') {
            return <NestedCatalog config={config} catalog={element} elementActions={elementActions} />
          } else {
            return <EditCatalog config={config} catalog={element} sites={elements.sites}
                                groups={elements.groups} sections={elements.sections}
                                elementActions={elementActions} />
          }
        case 'sections':
          if (isNil(elements.element)) {
            return <Sections config={config} sections={elements.sections} elementActions={elementActions} />
          } else if (elements.elementAction == 'nested') {
            return <NestedSection config={config} section={element} elementActions={elementActions} />
          } else {
            return <EditSection config={config} section={element} pages={elements.pages}
                                elementActions={elementActions} />
          }
        case 'pages':
          if (isNil(elements.element)) {
            return <Pages config={config} pages={elements.pages} elementActions={elementActions} />
          } else if (elements.elementAction == 'nested') {
            return <NestedPage config={config} page={element} elementActions={elementActions} />
          } else {
            return <EditPage config={config} page={element} attributes={elements.attributes}
                             conditions={elements.conditions} questionsets={elements.questionsets}
                             questions={elements.questions} elementActions={elementActions} />
          }
        case 'questionsets':
          if (isNil(elements.element)) {
            return <QuestionSets config={config} questionsets={elements.questionsets}
                                 elementActions={elementActions} />
          } else if (elements.elementAction == 'nested') {
            return <NestedQuestionSet config={config} questionset={element} elementActions={elementActions} />
          } else {
            return <EditQuestionSet config={config} questionset={element} attributes={elements.attributes}
                                    conditions={elements.conditions} questionsets={elements.questionsets}
                                    questions={elements.questions} elementActions={elementActions} />
          }
        case 'questions':
          if (isNil(elements.element)) {
            return <Questions config={config} questions={elements.questions} elementActions={elementActions} />
          } else {
            return <EditQuestion config={config} question={element} attributes={elements.attributes}
                                 conditions={elements.conditions} optionsets={elements.optionsets}
                                 options={elements.options} widgetTypes={elements.widgetTypes}
                                 valueTypes={elements.valueTypes} elementActions={elementActions} />
          }
        case 'attributes':
          if (isNil(elements.element)) {
            return <Attributes config={config} attributes={elements.attributes} elementActions={elementActions} />
          } else if (elements.elementAction == 'nested') {
            return <NestedAttribute config={config} attribute={element} elementActions={elementActions} />
          } else {
            return <EditAttribute config={config} attribute={element} attributes={elements.attributes}
                                  elementActions={elementActions} />
          }
        case 'optionsets':
          if (isNil(elements.element)) {
            return <OptionSets config={config} optionsets={elements.optionsets}
                               elementActions={elementActions} />
          } else if (elements.elementAction == 'nested') {
            return <NestedOptionSet config={config} optionset={element} elementActions={elementActions} />
          } else {
            return <EditOptionSet config={config} optionset={element} options={elements.options}
                                  providers={elements.providers} elementActions={elementActions} />
          }
        case 'options':
          if (isNil(elements.element)) {
            return <Options config={config} options={elements.options} elementActions={elementActions} />
          } else {
            return <EditOption config={config} option={element} elementActions={elementActions} />
          }
        case 'conditions':
          if (isNil(elements.element)) {
            return <Conditions config={config} conditions={elements.conditions} elementActions={elementActions} />
          } else {
            return <EditCondition config={config} condition={element} relations={elements.relations}
                                  attributes={elements.attributes} options={elements.options}
                                  elementActions={elementActions} />
          }
        case 'tasks':
          if (isNil(elements.element)) {
            return <Tasks config={config} tasks={elements.tasks} elementActions={elementActions} />
          } else {
            return <EditTask config={config} task={element} attributes={elements.attributes}
                             conditions={elements.conditions} catalogs={elements.catalogs}
                             groups={elements.groups} sites={elements.sites}
                             elementActions={elementActions} />
          }
        case 'views':
          if (isNil(elements.element)) {
            return <Views config={config} views={elements.views} elementActions={elementActions} />
          } else {
            return <EditView config={config} view={element} catalogs={elements.catalogs}
                             groups={elements.groups} sites={elements.sites}
                             elementActions={elementActions} />
          }
        default:
          return null
      }
    }
  }

}

Main.propTypes = {
  config: PropTypes.object.isRequired,
  elements: PropTypes.object.isRequired,
  configActions: PropTypes.object.isRequired,
  elementActions: PropTypes.object.isRequired
}

function mapStateToProps(state, props) {
  return {
    config: state.config,
    elements: state.elements
  }
}

function mapDispatchToProps(dispatch) {
  return {
    configActions: bindActionCreators(configActions, dispatch),
    elementActions: bindActionCreators(elementActions, dispatch)
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Main)
