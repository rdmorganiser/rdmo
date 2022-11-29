const initialState = {
  elementType: null,
  elementId: null,
  errors: [],
  catalogs: [],
  sections: [],
  pages: [],
  questionsets: [],
  questions: [],
  optionsets: [],
  options: [],
  conditions: [],
  tasks: [],
  views: []
}

export default function elementsReducer(state = initialState, action) {
  switch(action.type) {
    case 'elements/fetchElementsInit':
      return Object.assign({}, state, {
        elementType: action.elementType,
        elementId: null,
        errors: []
      })
    case 'elements/fetchElementsSuccess':
      return Object.assign({}, state, {
        [state.elementType]: action.elements
      })
    case 'elements/fetchElementsError':
      return Object.assign({}, state, {
        errors: action.errors
      })
    default:
      return state
  }
}
