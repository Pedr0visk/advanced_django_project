<template>
  <div>
    <div class="form-group row">
      <label class="col-sm-1 col-form-label col-form-label-sm">Name:</label>
      <div class="col-sm-3">
        <input type="text" v-model="campaign.name">
        <small class="form-text text-muted">
          Required.
        </small>
      </div>
    </div>
    <hr/>

    <div class="form-group row">
      <label class="col-sm-1 col-form-label col-form-label-sm">Description:</label>
      <div class="col-sm-3">
        <textarea name="" id="" cols="30" rows="10">{{ campaign.description }}</textarea>
        <small class="form-text text-muted">
          Optional.
        </small>
      </div>
    </div>
    <hr/>

    <div class="form-group row">
      <label class="col-sm-1 col-form-label col-form-label-sm">Active:</label>
      <div class="col-sm-3">
        <input type="checkbox" v-model="campaign.active">
        <small class="form-text text-muted">
          Required.
        </small>
      </div>
    </div>
    <hr/>

    <div class="form-group row">
      <label class="col-sm-1 col-form-label col-form-label-sm">Start Date:</label>
      <div class="col-sm-2">
        <input type="date" v-model="campaign.start_date">
        <small class="form-text text-muted">
          Note: you are 3 hours behind server time.
        </small>
      </div>
    </div>
    <hr/>

    <div class="form-group row">
      <label class="col-sm-1 col-form-label col-form-label-sm">End Date:</label>
      <div class="col-sm-2">
        <input type="date" v-model="campaign.end_date">
        <small class="form-text text-muted">
          Note: you are 3 hours behind server time.
        </small>
      </div>
    </div>
    <hr/>

    <div class="form-group row">
      <label class="col-sm-1 col-form-label col-form-label-sm">Well Name:</label>
      <div class="col-sm-3">
        <input type="text" v-model="campaign.well_name">
        <small class="form-text text-muted">
          Required.
        </small>
      </div>
    </div>
    <hr/>

    <fieldset class="form-fieldset">
      <h4>Phases</h4>

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
            <small>duration</small>
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
            <th>duration</th>
            <th>Test</th>
            <th>is drilling</th>
            <th>test groups</th>
            <th></th>
            <th></th>
          </tr>
          </thead>
          <tbody>

          <tr v-for="(phase, key) in phases" :key="key">
            <td>{{ phase.name }}</td>
            <td>{{ phase.start_date }}</td>
            <td>{{ phase.end_date }}</td>
            <td>{{ phase.duration }}</td>
            <td>{{ phase.has_test }}</td>
            <td>{{ phase.is_drilling }}</td>
            <td>{{ phase.test_groups }}</td>
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
          </tr>
          </tbody>
        </table>
      </div>
    </fieldset>

    <div class="card p-2 bg-light text-right">
      <div class="d-flex">
        <div>
          <a href="{% url 'bops:index' bop_pk %}" class="btn btn-danger">Cancel</a>
        </div>
        <div class="ml-auto">
          <button type="submit" class="btn btn-secondary">
            Save and add another
          </button>
          <button @click.prevent="createCampaign" type="submit" class="btn btn-primary">
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

const formatDate = (date) => {
  let nextYear = date.getFullYear()
  let nextMonth = ("0" + (date.getMonth())).slice(-2)
  let nextDay = ("0" + (date.getDate())).slice(-2)
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
      isUpdate: false,
      popperProps: popperProps,
      testGroups: [],
      btnStr: 'pick',
      dayStr: ['S', 'M', 'T', 'W', 'T', 'F', 'S'],
      campaign: {
        name: '',
        active: true,
        description: '',
        start_date: '',
        end_date: '',
        well_name: '',
      },
      phases: [],
      phase: {
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
    this.$http
        .get(`/api/bops/${bopId}/test-groups/`)
        .then(response => this.testGroups = response.data)

    this.testGroups = [
      {_id: 1, name: 'test group 1'},
      {_id: 2, name: 'test group 2'}
    ]
  },
  methods: {
    add() {
      this.phase._id = this.$uuid.v1()
      let newPhases = [...this.phases, this.phase]
      this.phases = newPhases
      this.clear()
    },
    update(id) {
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
        name: '',
        duration: null,
        start_date: next_date,
        end_date: '',
        test_groups: [],
        has_test: false,
        is_drilling: false,
      }
    },
    toggleAction() {
      this.isUpdate = !this.isUpdate
      this.clear()
    },
    createCampaign() {
      let that = this
      this.$http
          .post('api/campaigns')
          .then(response => {
            that
                .$swal({
                  title: "Campaign created successfully!",
                  text: 'go to campaign list to see it',
                  type: "success",
                  showConfirmButton: false,
                  timer: 1500
                })
                .then(swalRes => {
                });
          })
    },
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
