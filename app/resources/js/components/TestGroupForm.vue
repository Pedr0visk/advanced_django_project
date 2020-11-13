<template>
  <div class="container-fluid">
    <div class="test-list">
      <table class="dnv-table">
        <thead>
        <tr>
          <th>coverage</th>
          <th>interval (Day)</th>
          <th></th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(test, index) in tests">
          <td>{{test.coverage}}</td>
          <td>{{test.interval}} days</td>
          <td>
            <button
                class="btn"
                @click.prevent="remove(test)">
              <i class="fa fa-times text-danger"></i>
            </button>
          </td>
        </tr>
        <tr>
          <td>
            <input
                v-model="test.coverage"
                type="number"
                placeholder="coverage">
            <small>min: 0 and max: 1</small>
          </td>
          <td>
            <input
                v-model="test.interval"
                type="number"
                placeholder="interval">
            <small>Days</small>
          </td>
          <td>
            <button
                :disabled="!enable"
                class="btn-standard"
                @click.prevent="add">add
            </button>
          </td>
        </tr>
        <tr v-if="errors.length">
          <td v-for="error in errors" colspan="3">
            <div class="d-flex">
              <img src="/static/img/icon-no.svg" alt="">
              <p class="text-danger ml-2">
                {{ error }}
              </p>
            </div>
          </td>
        </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script>
export default {
  data() {
    return {
      enable: true,
      errors: [],
      tests: [],
      test: {
        coverage: null,
        interval: null,
      }
    }
  },
  mounted () {
    let form = document.getElementById('testGroup')
    this.tests = JSON.parse(form.tests.value) || []
  },
  methods: {
    add() {
      if (!this.checkForm()) return
      this.tests = [...this.tests, this.test]
      this.test = {
        coverage: 1,
        interval: null,
      }
    },
    remove(test) {
      this.tests = this.tests.filter(item => item != test)
    },
    checkForm() {
      this.errors = []

      let {coverage, interval} = this.test
      let len = this.tests.length

      if (coverage > 1)
        this.errors.push("coverage cannot be greater than 1.")

      if (len == 1) {

        if (this.tests[0].coverage == 1 && coverage == 1)
          this.errors.push("you already have a test with coverage equals 1. Try deleting all tests and add new ones.")

        if (coverage < 1)
          this.errors.push("you must add a test with coverage 1.")
      }

      if (len == 2)
        this.errors.push("you reached the limit of tests.")


      if (this.errors.length > 0)
        return false
      return true
    }
  },
   watch: {
    'tests': function (val, oldVal) {
      let len = this.tests.length

      let form = document.getElementById('testGroup')
      form.tests.value = JSON.stringify(this.tests)
    }
  }
}
</script>

