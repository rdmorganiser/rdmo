import SetFactory from '../factories/SetFactory'

const initSets = (values) => {
  return values.reduce((acc, cur) => {
    if (!acc.find((valueset) => (cur.set_prefix == valueset.set_prefix &&
                                 cur.set_index == valueset.set_index))) {
      acc.push(SetFactory.create({
        set_prefix: cur.set_prefix,
        set_index: cur.set_index
      }))
    }

    return acc
  }, [])
}

export { initSets }
