const initialState = {
  catalog: null,
  catalogs: []
}

export default function catalogReducer(state = initialState, action) {

  switch(action.type) {
    case 'questions/fetchCatalogSuccess':
      return Object.assign({}, state, { catalog: action.catalog })
    default:
      return state
  }

}
