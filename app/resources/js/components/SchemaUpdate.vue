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

    <div class="form-group row">
      <label class="col-sm-1 col-form-label col-form-label-sm">Default:</label>
      <div class="col-sm-3">
        <input type="checkbox" v-model="schema.is_default">
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
          <li :key="index" v-for="(error, index) in errors" class="text-danger">{{ error }}</li>
        </ul>
      </div>
      <div class="px-3">
        <div class="form-add-phase row mb-3">
          <!-- name -->
          <div class="col-4">
            <input
                v-model="phase.name"
                placeholder="phase name"
                type="text"
                class="form-control form-control-sm ">
            <small>phase name</small>
          </div>

          <!-- datetime picker -->
          <div class="col-auto">
            <div class="d-flex flex-column">
              <input 
              :disabled="phases.length > 0"
              type="date" 
              v-model="phase.start.date" 
              :max="bop.last_certification.end_date"/>
              <small>mm/dd/YYYY</small>
            </div>
          </div>

           <!-- time select -->
          <div class="col-1">
            <select 
            :disabled=" phases.length > 0"
            v-model="phase.start.time" 
            class="form-control form-control-sm">
              <option :key="hour" v-for="hour in 24" :value="hour-1">{{ ("0" + (hour - 1)).slice(-2) }}:00</option>
            </select>
          </div>

          <!-- duration -->
          <div class="col-1">
            <input
              v-model="phase.duration"
              type="number"
              :disabled="phase.start.date == ''"
              class="form-control form-control-sm">
            <small>duration (h)</small>
          </div>

          <!-- datetime picker -->
          <div class="col-auto">
            <input type="text" disabled :value="formatDate(phase.end.date, phase.end.time)">
          </div>
        </div>
        <div class="row">
          <!-- test -->
          <div class="col-12">
            <div class="form-group">
              <div class="form-check">
                <input 
                  v-model="phase.has_test"
                  class="form-check-input" 
                  type="checkbox" 
                  id="gridCheck">
                <label class="form-check-label" for="gridCheck">
                  Test
                </label>
              </div>
            </div>
          </div>

          <div class="col-6" v-show="phase.has_test">
            <label for="">Select one or more Test Groups bellow.</label>
            <select
                v-model="phase.test_groups"
                multiple
                class="form-control form-control-sm">
              <option
                  v-for="group in testGroups"
                  :key="group.id"
                  :value="group.id"
              >{{ group.name }}
              </option>
            </select>
            <small>test groups</small>
          </div>

          <!-- drilling -->
          <div class="col-12">
            <div class="form-group">
              <div class="form-check">
                <input 
                  v-model="phase.is_drilling"
                  class="form-check-input" 
                  type="checkbox" 
                  id="gridCheck">
                <label class="form-check-label" for="gridCheck">
                  Drilling
                </label>
              </div>
            </div>
          </div>

          <div class="col-12">
            <button
                v-show="!isUpdate"
                type="submit"
                class="btn-standard"
                @click.prevent="add">add
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
            <th>test</th>
            <th>drilling</th>
            <th>test groups</th>
            <th></th>
            <th></th>
          </tr>
          </thead>
          <tbody>

          <tr v-for="(item, key) in phases" :key="key">
            <td>{{ item.name }}</td>
            <td>{{ formatDate(item.start.date, item.start.time) }}</td>
            <td>{{ formatDate(item.end.date, item.end.time) }}</td>
            <td>{{ item.duration }}h</td>
            <td><img v-if="item.has_test" src="/static/img/icon-yes.svg" alt=""></td>
            <td><img v-if="item.is_drilling" src="/static/img/icon-yes.svg" alt=""></td>
            <td>
              <span 
              :key="tg.code"
              v-for="tg in item.test_groups" 
              class="badge badge-success mr-1 text-uppercase">{{ showTestGroup(tg) }}</span>
            </td>
            <td width="5%">
              <a
                  @click.prevent="select(key)"
                  href="" class="px-2"><i class="fa fa-pencil-alt text-warning"></i></a>
            </td>
            <td width="5%">
              <a
                  @click.prevent="remove(item._id)"
                  href="" class="px-2"><i class="fa fa-times text-danger"></i></a>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </fieldset>

    <div class="card p-2 bg-light text-right">
      <div class="d-flex">
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
/**
 *
 * @param start_date:Date
 * @param time:Int
 * @param duration:Int
 * @return new_date:Date
 */

function calcDateTime(start_date, hour, duration) {
  let delay = (parseInt(duration) + parseInt(hour)) * 60 ** 2 * 1000
  let new_date = new Date(new Date(start_date.split('-')).getTime() + delay)
  return new_date
}

function toDateString(date) {
  return `${date.getFullYear()}-${("0" + (date.getMonth() + 1)).slice(-2)}-${("0" + (date.getDate())).slice(-2)}`
}

export default {

  data() {
    return {
      bop: {name: '', model: '', last_certification: {end_date: ''}},
      isLoading: true,
      errors: [],
      isUpdate: false,
      testGroups: [],
      phases: [],
      schema: {
        name: '',
        is_default: false,
      },
      phase: {
        _id: null,
        name: '',
        has_test: false,
        is_drilling: false,
        duration: null,
        start: {date: '', time: 12},
        end: {date: '', time: 0},
        test_groups: []
      }
    };
  },
  mounted() {
    let bopId = document.getElementById('bopId').value
    let schemaId = document.getElementById('schemaId').value
    this.$http
        .get(`/api/bops/${bopId}/test-groups/`)
        .then(response => {
          console.log(response.data)
          this.testGroups = response.data
        })

    this.$http
        .get(`/api/schemas/${schemaId}/`)
        .then(response => {
          this.schema.name = response.data.name
          this.schema.is_default = response.data.is_default
          this.phases = response.data.phases.map(phase => {
            let start = {
              date: toDateString(new Date(phase.start_date)),
              time: new Date(phase.start_date).getHours()
            }

            let d = calcDateTime(start.date, start.time, phase.duration)

            let end = {
              date: toDateString(d),
              time: d.getHours()
            }

            return {
              _id: this.$uuid.v1(),
              name: phase.name,
              has_test: phase.has_test,
              is_drilling: phase.is_drilling,
              duration: phase.duration,
              start: start,
              end: end,
              test_groups: phase.test_groups
            }
          })

          this.isLoading = false
          this.phase.start = this.phases[this.phases.length - 1].end
        })
  },
  methods: {
    updateSchema() {
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      let schemaId = document.getElementById('schemaId').value

      const payload = {
        campaign: parseInt(document.getElementById('campaignId').value),
        name: this.schema.name,
        is_default: this.schema.is_default,
        phases: this.phases.map(phase => {
          return {
            name: phase.name,
            has_test: phase.has_test,
            is_drilling: phase.is_drilling,
            duration: phase.duration,
            start_date: this.formatDate(phase.start.date, phase.start.time),
            end_date: this.formatDate(phase.end.date, phase.end.time),
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
                  title: "Schema updated successfully!",
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
      if (!this.checkForm()) return
      
      this.phase._id = this.$uuid.v1()
      let newPhases = [...this.phases, this.phase]
      this.phases = newPhases
      this.clear()
    },
    update(id) {
      if (!this.checkForm()) return

      let index = this.phases.findIndex(phase => phase._id == id)
      this.phases[index] = this.phase

      let length = this.phases.length
      let phase;
      let prevPhase;

      index += 1
      for (index; index < length; index++) {
        prevPhase = this.phases[index - 1]
        phase = this.phases[index]

        let {date, time} = prevPhase.start
        let d = calcDateTime(date, time, prevPhase.duration)

        phase.start.date = toDateString(d)
        phase.start.time = d.getHours()

        d = calcDateTime(phase.start.date, phase.start.time, phase.duration)
        phase.end.date = toDateString(d)
        phase.end.time = d.getHours()

        this.phases[index] = phase
      }

      if (this.phase.is_drilling)
        this.phase.test_groups = []

      this.toggleAction()
    },
    addBefore(index) {
      let prevPhase = this.phases[index - 1]
      this.phases.splice(index, 0, Object.assign(this.phase, {
        _id: this.$uuid.v1(),
        start: prevPhase.end
      }))
      this.select(index)
    },
    addAfter(index) {
      let prevPhase = this.phases[index]
      this.phases.splice(index + 1, 0, Object.assign(this.phase, {
        _id: this.$uuid.v1(),
        start: prevPhase.end
      }))
      this.select(index + 1)
    },
    remove(id) {
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

      this.phase = {
        _id: '',
        name: '',
        duration: null,
        start: lastPhase.end,
        end: {date: '', time: 0},
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
      let {name, duration, start: {date, time}, is_drilling, has_test } = this.phase

      let phaseEndDate = calcDateTime(date, time, duration)
      let certExpiryDate = calcDateTime(this.bop.last_certification.end_date, 23, 1)

      if(phaseEndDate > certExpiryDate)
        this.errors.push('this phase duration exceed the bop\'s certification period')
      if (!name)
        this.errors.push('the field name is required')
      if (!duration)
        this.errors.push('the field duration is required')
      if (!date || !time)
        this.errors.push('the field start date is required')
      if (is_drilling && has_test)
        this.errors.push('The phase cannot be set as both drilling and test, you \
        can choose just one.')

      if (this.errors.length > 0)
        return false;

      return true
    },
    formatDate(date, hour) {
      if (!date) return

      let d = new Date(date.split('-')),
          month = '' + (d.getMonth() + 1),
          day = '' + d.getDate(),
          year = d.getFullYear();

      if (month.length < 2)
        month = '0' + month;
      if (day.length < 2)
        day = '0' + day;

      return `${[year, month, day].join('-')} ${("0" + hour).slice(-2)}:00:00`;
    },
    showTestGroup(id) {
      let items = this.testGroups.filter((item) => item.id == id)
      if (items.length > 0) 
        return `${items[0].name}`
      return ''
    }
  },
  watch: {
    'phase.duration': function (val, oldVal) {
      let {date, time} = this.phase.start
      let d = calcDateTime(date, time, this.phase.duration)

      this.phase.end = {
        date: `${d.getFullYear()}-${("0" + (d.getMonth() + 1)).slice(-2)}-${("0" + (d.getDate())).slice(-2)}`,
        time: d.getHours()
      }
    },
    'phase.start.time': function (val, oldVal) {
      if (val !== null && oldVal !== null) {
        let {date, time} = this.phase.start
        let {duration} = this.phase

        if (duration == '' || duration == null) 
          return
          
        let d = calcDateTime(date, time, duration)

        this.phase.end = {
          date: `${d.getFullYear()}-${("0" + (d.getMonth() + 1)).slice(-2)}-${("0" + (d.getDate())).slice(-2)}`,
          time: d.getHours()
        }
      }
    }
  }
};
</script>
