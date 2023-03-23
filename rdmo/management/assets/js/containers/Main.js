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
    const { config, elements, configActions, elementActions } = this.props
    const { element, elementType, elementId, elementAction, errors } = elements

    // check if anything was loaded yet
    if (isNil(elementType)) {
      return null
    }

    // check if an an error occured
    if (!isNil(errors.api)) {
      return <ApiErrors errors={errors.api} />
    }

    // check if the nested components should be displayed
    if (!isNil(element) && elementAction == 'nested') {
      switch (elementType) {
        case 'catalogs':
          return <NestedCatalog config={config} catalog={element} elementActions={elementActions} />
        case 'sections':
          return <NestedSection config={config} section={element} elementActions={elementActions} />
        case 'pages':
          return <NestedPage config={config} page={element} elementActions={elementActions} />
        case 'questionsets':
          return <NestedQuestionSet config={config} questionset={element} elementActions={elementActions} />
        case 'attributes':
          return <NestedAttribute config={config} attribute={element} elementActions={elementActions} />
        case 'optionsets':
          return <NestedOptionSet config={config} optionset={element} elementActions={elementActions} />
      }
    }

    // check if the edit components should be displayed
    if (!isNil(element)) {
      switch (elementType) {
        case 'catalogs':
          return <EditCatalog config={config} catalog={element} elements={elements} elementActions={elementActions} />
        case 'sections':
          return <EditSection config={config} section={element} elements={elements} elementActions={elementActions} />
        case 'pages':
          return <EditPage config={config} page={element} elements={elements} elementActions={elementActions} />
        case 'questionsets':
          return <EditQuestionSet config={config} questionset={element} elements={elements} elementActions={elementActions} />
        case 'questions':
          return <EditQuestion config={config} question={element} elements={elements} elementActions={elementActions} />
        case 'attributes':
          return <EditAttribute config={config} attribute={element} elements={elements} elementActions={elementActions} />
        case 'optionsets':
          return <EditOptionSet config={config} optionset={element} elements={elements} elementActions={elementActions} />
        case 'options':
          return <EditOption config={config} option={element} elements={elements} elementActions={elementActions} />
        case 'conditions':
          return <EditCondition config={config} condition={element} elements={elements} elementActions={elementActions} />
        case 'tasks':
          return <EditTask config={config} task={element} elements={elements} elementActions={elementActions} />
        case 'views':
          return <EditView config={config} view={element} elements={elements} elementActions={elementActions} />
      }
    }

    // check if the list components should be displayed
    if (isNil(elementId) && isNil(elementAction) && !isEmpty(elements[elementType])) {
      switch (elementType) {
        case 'catalogs':
          return <Catalogs config={config} catalogs={elements.catalogs}
                           configActions={configActions} elementActions={elementActions} />
        case 'sections':
          return <Sections config={config} sections={elements.sections}
                           configActions={configActions} elementActions={elementActions} />
        case 'pages':
          return <Pages config={config} pages={elements.pages}
                        configActions={configActions} elementActions={elementActions} />
        case 'questionsets':
          return <QuestionSets config={config} questionsets={elements.questionsets}
                               configActions={configActions} elementActions={elementActions} />
        case 'questions':
          return <Questions config={config} questions={elements.questions}
                            configActions={configActions} elementActions={elementActions} />
        case 'attributes':
          return <Attributes config={config} attributes={elements.attributes}
                             configActions={configActions} elementActions={elementActions} />
        case 'optionsets':
          return <OptionSets config={config} optionsets={elements.optionsets}
                             configActions={configActions} elementActions={elementActions} />
        case 'options':
          return <Options config={config} options={elements.options}
                          configActions={configActions} elementActions={elementActions} />
        case 'conditions':
          return <Conditions config={config} conditions={elements.conditions}
                             configActions={configActions} elementActions={elementActions} />
        case 'tasks':
          return <Tasks config={config} tasks={elements.tasks}
                        configActions={configActions} elementActions={elementActions} />
        case 'views':
          return <Views config={config} views={elements.views}
                        configActions={configActions} elementActions={elementActions} />
      }
    }

    // fetching the data is not complete yet, or no action was invoked yet
    return null
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
