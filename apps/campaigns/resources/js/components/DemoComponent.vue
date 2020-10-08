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
        <input
            v-model="phase.start_date"
            type="datetime-local"
            class="form-control form-control-sm">
        <small>start date</small>
      </div>
      <div class="col-1">
        <input
            v-model="phase.duration"
            type="number"
            class="form-control form-control-sm">
        <small>duration</small>
      </div>
      <div class="col-2">
        <select
            v-on:change="displayTests($event)"
            v-model="phase.step"
            class="form-control form-control-sm">
          <option
              v-for="step in steps"
              :value="step.value"
          >{{ step.text }}
          </option>
        </select>
        <small>step</small>
      </div>
      <div class="col-2" v-show="hasTest">
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
        <td><input type="datetime-local" v-model="phase.start_date" disabled></td>
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
export default {
  data() {
    return {
      hasTest: false,
      steps: [
        {value: 1, text: 'descend'},
        {value: 2, text: 'connect'},
        {value: 3, text: 'drilling'},
        {value: 4, text: 'disconnect'},
        {value: 5, text: 'test'}
      ],
      testGroups: [],
      phases: [],
      phase: {
        name: '',
        step: null,
        duration: null,
        start_date: '2020-02-02 20:00',
        test_groups: []
      }
    };
  },
  mounted() {
    this.testGroups = [
      {_id: 1, name: 'test group 1'},
      {_id: 2, name: 'test group 2'}
    ]
  },
  methods: {
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
      let date = new Date(lastPhase.start_date).getMilliseconds() + (lastPhase.duration * 60 * 60)
      this.phase = {
        name: '',
        step: null,
        duration: null,
        start_date: new Date(date),
        test_groups: []
      }
    }
  }
};
</script>
