import { isNil, toNumber } from 'lodash'

class SetFactory {

  static create({ set_prefix, set_index, element }) {
    return {
      set_prefix: isNil(set_prefix) ? '' : set_prefix,
      set_index: isNil(set_index) ? 0 : toNumber(set_index),
      element,
      attributes: (
        isNil(element.attribute) ? [] : [element.attribute]
      ) + (element.questions || []).filter(e => !isNil(e.attribute)).map(e => e.attribute)
    }
  }

}

export default SetFactory
