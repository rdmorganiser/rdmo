const initialState = {
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
    case 'elemets/fetchCatalogs':
      return Object.assign({}, state, { catalogs: action.catalogs })
    default:
      return state
  }

}
