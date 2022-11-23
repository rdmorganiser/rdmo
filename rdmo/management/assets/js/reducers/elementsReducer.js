const initialState = {
  current: null,
  error: null,
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
        error: null
      })
    case 'elements/fetchElementsSuccess':
      return Object.assign({}, state, {
        [action.resourceType]: action.elements
      })
    case 'elements/fetchElementsError':
      return Object.assign({}, state, {
        error: action.error
      })
    case 'elements/fetchElement':
      return Object.assign({}, state, {
        current: action.element
      })
    default:
      return state
  }
}
