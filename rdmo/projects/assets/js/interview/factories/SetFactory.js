import { isNil, toNumber } from 'lodash'

class SetFactory {

  static create({ set_prefix, set_index }) {
    return {
      set_prefix: isNil(set_prefix) ? '' : set_prefix,
      set_index: isNil(set_index) ? 0 : toNumber(set_index),
    }
  }

}

export default SetFactory
