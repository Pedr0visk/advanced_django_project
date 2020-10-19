<template>
  <div>
    <div class="form-group row">
      <label class="col-sm-1 col-form-label col-form-label-sm">Name:</label>
      <div class="col-sm-3">
        <input type="text" v-model="schema.name">
        <small class="form-text text-muted">
          Required.
        </small>
      </div>
    </div>
    <hr/>

    <fieldset class="form-fieldset">
      <h4>Phases</h4>
      <div v-if="errors.length">
        <ul>
          <li v-for="error in errors" class="text-danger">{{ error }}</li>
        </ul>
      </div>
      <div class="px-3">
        <div class="form-add-phase row">
          <!-- name -->
          <div class="col-2">
            <input
                v-model="phase.name"
                placeholder="phase name"
                type="text"
                class="form-control form-control-sm">
            <small>phase name</small>
          </div>
          <!-- datetime picker -->
          <div class="col-3">
            <datetime-picker
                placeholder="start date"
                :dayStr="dayStr"
                :btnStr="btnStr"
                timeType="hour"
                v-model="phase.start_date"
                :popperProps="popperProps"
                :timeStr="timeStr"
            />
            <small>format: Year-Month-Day Hour</small>
          </div>
          <!-- datetime picker -->
          <div class="col-3">
            <datetime-picker
                placeholder="end date"
                :dayStr="dayStr"
                :btnStr="btnStr"
                timeType="hour"
                v-model="phase.end_date"
                :popperProps="popperProps"
                :timeStr="timeStr"
            />
            <small>format: Year-Month-Day Hour</small>
          </div>
          <!-- duration -->
          <div class="col-1">
            <input
                v-model="phase.duration"
                type="number"
                class="form-control form-control-sm">
            <small>duration (h)</small>
          </div>
          <!-- has_test -->
          <div class="col-1">
            <input type="checkbox" v-model="phase.has_test">
            <small>Test</small>
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
                  :value="group.id"
              >{{ group.name }}
              </option>
            </select>
            <small>step</small>
          </div>
          <div class="col-1">
            <button
                v-show="!isUpdate"
                type="submit"
                class="btn-standard"
                @click.prevent="add">save
            </button>
            <div class="d-flex">
              <button
                  v-show="isUpdate"
                  type="submit"
                  class="btn-standard mr-2"
                  @click.prevent="update(phase._id)">update
              </button>
              <button
                  v-show="isUpdate"
                  type="submit"
                  class="btn-standard"
                  @click.prevent="toggleAction">cancel
              </button>
            </div>
          </div>
        </div>
        <hr>
        <table class="phase-list table m-0 dnv-table">
          <thead>
          <tr>
            <th>name</th>
            <th>start date</th>
            <th>end date</th>
            <th>duration (h)</th>
            <th>Test</th>
            <th>is drilling</th>
            <th>test groups</th>
            <th></th>
            <th></th>
            <th></th>
            <th></th>
          </tr>
          </thead>
          <tbody>

          <tr
              v-for="(item, key) in phases"
              :key="key"
              v-bind:class="{selected: item._id === phase._id }">
            <td>{{ item.name }}</td>
            <td>{{ item.start_date }}</td>
            <td>{{ item.end_date }}</td>
            <td>{{ item.duration }}h</td>
            <td>{{ item.has_test }}</td>
            <td>{{ item.is_drilling }}</td>
            <td>{{ item.test_groups }}</td>
            <td width="5%">
              <a
                  @click.prevent="select(key)"
                  href="" class="px-2"><i class="fa fa-pencil-alt text-warning"></i></a>
            </td>
            <td width="5%">
              <a
                  @click.prevent="remove(phase._id)"
                  href="" class="px-2"><i class="fa fa-times text-danger"></i></a>
            </td>
            <td width="10%">
              <a
                  @click.prevent="addBefore(key)"
                  href="" class="px-2">add before</a>
            </td>
            <td width="10%">
              <a
                  @click.prevent="addAfter(key)"
                  href="" class="px-2">add after</a>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </fieldset>

    <div class="card p-2 bg-light text-right">
      <div class="d-flex">
        <div>
          <a href="" class="btn btn-danger">Cancel</a>
        </div>
        <div class="ml-auto">
          <button @click.prevent="updateSchema" type="submit" class="btn btn-primary">
            SAVE
          </button>
        </div>
      </div>
    </div>
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

const parseDateTime = (datetime) => {
  let full_date = datetime.split(' ')
  let date = full_date[0].split('-')
  const year = parseInt(date[0]),
      month = parseInt(date[1]),
      day = parseInt(date[2]),
      hour = parseInt(full_date[1])

  return new Date(year, month, day, hour)
}

const formatDate = (date) => {
  let nextYear = date.getFullYear()
  let nextMonth = ("0" + (date.getMonth() + 1)).slice(-2)
  let nextDay = ("0" + (date.getDate())).slice(-2)
  let nextHour = ("0" + (date.getHours())).slice(-2)

  return `${nextYear}-${nextMonth}-${nextDay} ${nextHour}`
}

const nextDate = (start_date, duration) => {
  const parsed_date = parseDateTime(start_date)
  let nextDate = new Date(parsed_date.getTime() + (duration * 60 * 60 * 1000))
  nextDate = formatDate(nextDate)
  return nextDate
}

export default {

  data() {
    return {
      errors: [],
      timeStr: ['hour'],
      isM: false,
      isUpdate: false,
      popperProps: popperProps,
      testGroups: [],
      btnStr: 'pick',
      dayStr: ['S', 'M', 'T', 'W', 'T', 'F', 'S'],
      phases: [],
      schema: {
        name: ''
      },
      phase: {
        _id: null,
        name: '',
        has_test: false,
        is_drilling: false,
        duration: null,
        start_date: '',
        end_date: '',
        test_groups: []
      }
    };
  },
  mounted() {
    let bopId = document.getElementById('bopId').value
    let schemaId = document.getElementById('schemaId').value
    this.$http
        .get(`/api/bops/${bopId}/test-groups/`)
        .then(response => this.testGroups = response.data)

    this.$http
        .get(`/api/schemas/${schemaId}/`)
        .then(response => {
          this.schema.name = response.data.name
          console.log(response)
          this.phases = response.data.phases.map(phase => ({
            _id: this.$uuid.v1(),
            name: phase.name,
            has_test: phase.has_test,
            is_drilling: phase.is_drilling,
            duration: phase.duration,
            start_date: formatDate(new Date(phase.start_date)),
            end_date: nextDate(formatDate(new Date(phase.start_date)), phase.duration),
            test_groups: phase.test_groups
          }))
          this.phase.start_date = this.phases[this.phases.length - 1].end_date
        })
  },
  methods: {
    updateSchema() {
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      let schemaId = document.getElementById('schemaId').value

      const payload = {
        campaign: parseInt(document.getElementById('campaignId').value),
        name: this.schema.name,
        phases: this.phases.map(phase => {
          return {
            name: phase.name,
            has_test: phase.has_test,
            is_drilling: phase.is_drilling,
            duration: phase.duration,
            start_date: phase.start_date + ':00:00',
            end_date: phase.end_date + ':00:00',
            test_groups: phase.test_groups
          }
        })
      }

      const config = {
        method: 'put',
        url: `/api/schemas/${schemaId}/`,
        headers: {'X-CSRFToken': csrftoken},
        data: payload
      }

      let that = this
      this.$http(config)
          .then(response => {
            console.log(response)
            that
                .$swal({
                  title: "Campaign updated successfully!",
                  text: 'go to campaign list to see it',
                  type: "success",
                  showConfirmButton: false,
                  timer: 1500
                })
                .then(swalRes => {

                });
          })
    },
    add() {
      if (!this.checkForm())
        return

      this.phase._id = this.$uuid.v1()
      let newPhases = [...this.phases, this.phase]
      this.phases = newPhases
      this.clear()
    },
    update(id) {
      if (!this.checkForm())
        return

      let index = this.phases.findIndex(phase => phase._id == id)
      this.phases[index] = this.phase

      let length = this.phases.length
      let phase;
      let prevPhase;

      index += 1
      for (index; index < length; index++) {
        prevPhase = this.phases[index - 1]
        phase = this.phases[index]
        phase.start_date = nextDate(prevPhase.start_date, prevPhase.duration)
        phase.end_date = nextDate(phase.start_date, phase.duration)
        this.phases[index] = phase
      }
      this.toggleAction()
    },
    addBefore(index) {
      let prevPhase = this.phases[index - 1]
      this.phases.splice(index, 0, Object.assign(this.phase, {
        _id: this.$uuid.v1(),
        start_date: prevPhase.end_date
      }))
      this.select(index)
    },
    addAfter(index) {
      let prevPhase = this.phases[index]
      this.phases.splice(index + 1, 0, Object.assign(this.phase, {
        _id: this.$uuid.v1(),
        start_date: prevPhase.end_date
      }))
      this.select(index + 1)
    },
    remove(id) {
      console.log('deleting')
      this.phases = this.phases.filter(phase => phase._id != id)
    },
    select(index) {
      this.isUpdate = true
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
      const next_date = nextDate(start_date, duration)

      this.phase = {
        _id: '',
        name: '',
        duration: null,
        start_date: next_date,
        end_date: '',
        test_groups: [],
        has_test: false,
        is_drilling: false,
      }
      this.errors = []
    },
    toggleAction() {
      this.isUpdate = !this.isUpdate
      this.clear()
    },
    checkForm() {
      this.errors = []
      let {name, duration, start_date} = this.phase

      if (!name)
        this.errors.push('the field name is required')
      if (!duration)
        this.errors.push('the field duration is required')
      if (!start_date)
        this.errors.push('the field start date is required')

      if (this.errors.length > 0)
        return false;
      return true;
    }

  },
  watch: {
    'phase.duration': function (val, oldVal) {
      if (val !== null && oldVal !== null) {
        this.phase.end_date = nextDate(this.phase.start_date, this.phase.duration)
      }
    }
  }
};
</script>
