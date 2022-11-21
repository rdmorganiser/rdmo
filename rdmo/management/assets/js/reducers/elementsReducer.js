const initialState = {
  current: null,
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
    case 'elements/fetchElementsSuccess':
      return Object.assign({}, state, {
        [action.resourceType]: action.elements
      })
    case 'elements/fetchElement':
      return Object.assign({}, state, {
        current: action.element
      })
    default:
      return state
  }

}
