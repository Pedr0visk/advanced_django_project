module.exports = schema = () => {
  return {
    _id: null,
    name: '',
    duration: 0,
    start: {date: '', time: 0},
    end: {date: '', time: 0},
    has_test: false,
    is_drilling: false,
    test_groups: []
  }
}