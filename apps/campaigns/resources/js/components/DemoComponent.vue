<template>
  <div class="px-3">
    <div class="form-add-phase row">
      <div class="col-2">
        <input
            v-model="phase.name"
            placeholder="phase name"
            type="text"
            class="form-control form-control-sm">
        <small>phase name</small>
      </div>
      <div class="col-3">
        <datetime-picker
            :placeholder="placeholder"
            :dayStr="dayStr"
            :btnStr="btnStr"
            timeType="hour"
            v-model="phase.start_date"
            @input="log"
            :popperProps="popperProps"
            :timeStr="timeStr"
        />
        <small>format: Year-Month-Day Hour</small>
      </div>
      <div class="col-1">
        <input
            v-model="phase.duration"
            type="number"
            class="form-control form-control-sm">
        <small>duration</small>
      </div>
      <div class="col-1">
        <input type="checkbox" v-model="phase.has_test">
        <small>has test</small>
      </div>
      <div class="col-1">
        <input type="checkbox" v-model="phase.is_drilling">
        <small>is drilling</small>
      </div>
      <div class="col-2" v-show="phase.has_test">
        <select
            v-model="phase.test_groups"
            multiple
            class="form-control form-control-sm">
          <option
              v-for="group in testGroups"
              :value="group._id"
          >{{ group.name }}
          </option>
        </select>
        <small>step</small>
      </div>
      <div class="col-1">
        <button
            type="submit"
            class="btn-standard"
            @click.prevent="addPhase">save
        </button>
      </div>
    </div>
    <hr>
    <form class="phase-list">
      <tbody>
      <tr v-for="(phase, key) in phases" :key="key">
        <td><input type="text" v-model="phase.name" disabled></td>
        <td><input type="text" v-model="phase.start_date" disabled></td>
        <td><input type="text" v-model="phase.duration" disabled></td>
        <td><input type="text" v-model="phase.step" disabled></td>
        <td>
          <a
              v-on:click="selectPhase(key, $event)"
              href="" class="px-2"><i class="fa fa-pencil-alt text-warning"></i></a>
        </td>
        <td><a href="" class="px-2"><i class="fa fa-times text-danger"></i></a></td>
      </tr>
      </tbody>
    </form>
  </div>
</template>

<script>
const popperProps = {
  popperOptions: {
    modifiers: {
      preventOverflow: {
        padding: 20
      }
    },
    // onUpdate: function (data) {
    //   console.log(JSON.stringify(data.attributes))
    // }
  }
}

const formatDate = (date) => {
  let nextYear = date.getFullYear()
  let nextMonth = ("0" + (date.getMonth())).slice(-2)
  let nextDay = ("0" + (date.getDay() + 1)).slice(-2)
  let nextHour = ("0" + (date.getHours())).slice(-2)

  return `${nextYear}-${nextMonth}-${nextDay} ${nextHour}`
}

const nextDate = (start_date, duration) => {
  let full_date = start_date.split(' ')
  let date = full_date[0].split('-')
  const year = parseInt(date[0]),
      month = parseInt(date[1]),
      day = parseInt(date[2]),
      hour = parseInt(full_date[1])

  start_date = new Date(year, month, day, hour)
  let nextDate = new Date(start_date.getTime() + (duration * 60 * 60 * 1000))
  nextDate = formatDate(nextDate)
  return nextDate
}

export default {
  data() {
    return {
      timeStr: ['hour'],
      isM: false,
      popperProps: popperProps,
      testGroups: [],
      btnStr: 'pick',
      placeholder: "start date",
      dayStr: ['S', 'M', 'T', 'W', 'T', 'F', 'S'],
      phases: [],
      phase: {
        name: '',
        step: null,
        has_test: false,
        is_drilling: false,
        duration: null,
        start_date: formatDate(new Date()),
        test_groups: []
      }
    };
  },
  mounted() {
    let bopId = document.getElementById('bopId').value
    this.$http
      .get(`/api/bops/${bopId}/test-groups/`)
      .then(response => console.log(response))

    this.testGroups = [
      {_id: 1, name: 'test group 1'},
      {_id: 2, name: 'test group 2'}
    ]
  },
  methods: {
    log: function (val) {
      this.date = val
      console.log(val)
    },
    addPhase() {
      let newPhases = [...this.phases, this.phase]
      this.phases = newPhases
      this.clear()
    },
    selectPhase(index, event) {
      event.preventDefault()
      this.phase = {...this.phases[index]}
    },
    displayTests(e) {
      let {value} = e.target
      if (value == 5)
        return this.hasTest = true

      return this.hasTest = false
    },
    clear() {
      const lastPhase = this.phases[this.phases.length - 1]
      const {start_date, duration} = lastPhase
      const nex_date = nextDate(start_date, duration)

      this.phase = {
        name: '',
        step: null,
        duration: null,
        start_date: nex_date,
        test_groups: []
      }
    }
  },
};
</script>
