<template>
  <div>
    <div class="form-group row">
      <label class="col-sm-1 col-form-label col-form-label-sm">Name:</label>
      <div class="col-sm-3">
        <input type="text" v-model="form.name">
        <small class="form-text text-muted">
          Required.
        </small>
      </div>
    </div>
    <hr/>

    <div class="form-group row">
      <label class="col-sm-1 col-form-label col-form-label-sm">Default:</label>
      <div class="col-sm-3">
        <input type="checkbox" v-model="form.is_default">
        <small class="form-text text-muted">
          Required.
        </small>
      </div>
    </div>
    <hr/>

   <fieldset class="form-fieldset">
    <h4>Phases</h4>
    <input-phase :phase="selectedItem"></input-phase>
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
          <th style="text-align: center;">actions</th>
        </tr>
      </thead>
      <tbody>
        <phase-item v-for="(phase, key) in phases" :index="key" :phase="phase" :key="key"></phase-item>
        <tr v-show="!phases.length" class="table-info">
          <td colspan="9" align="center">No phases.</td>
        </tr>
      </tbody>
    </table>
  </fieldset>

    <div class="card p-2 bg-light text-right">
      <div class="d-flex">
        <div class="ml-auto">
          <button @click.prevent="" type="submit" class="btn btn-primary">
            SAVE
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import InputPhase from "./InputPhase.vue";
import PhaseItem from "./PhaseItem";

export default {
  components: {
    PhaseItem,
    InputPhase
  },
  data() {
    return {
      errors: [],
      testGroupsOptions: [],
      form: {
        campaign: {},
        name: '',
        is_default: false,
      },
      phases: [
        {
          _id: this.$uuid.v1(),
          name: 'phase 1',
          has_test: true,
          is_drilling: true,
          duration: 24,
          start: {date: '2021-01-01', time: 2},
          end: {date: '2021-01-02', time: 2},
          test_groups: []
        },
        {
          _id: this.$uuid.v1(),
          name: 'phase 2',
          has_test: true,
          is_drilling: true,
          duration: 24,
          start: {date: '2021-01-02', time: 2},
          end: {date: '2021-01-03', time: 2},
          test_groups: []
        }
      ],
      selectedItem: {}
    };
  },
  methods: {
    addItem(item) {
      item._id = this.$uuid.v1();
      this.phases.push(item);
    },
    updateItem(item) {
      let index = this.phases.findIndex(phase => phase._id == item._id)
      this.phases[index] = item;

      // Deselect item
      this.selectedItem = null;

      // Update all phase's datetime
      this.resetDatetimeItems(index);
    },
    addItemBefore(index) {
      let prevPhase;

      if (index > 0) {
        prevPhase = this.phases[index - 1];
        this.phases.splice(index, 0, {
          _id: this.$uuid.v1(),
          name: '',
          has_test: false,
          is_drilling: false,
          duration: 24,
          start: prevPhase.end,
          end: {date: '', time: 0},
          test_groups: []
        });
      } else {
        this.phases.splice(index, 0, {
          _id: this.$uuid.v1(),
          start: {date: '', time: 0},
          end: {date: '', time: 0},
        });
      }

      this.selectItem(index);
    },
    addItemAfter(index) {
      let prevPhase;

      prevPhase = this.phases[index];

      this.phases.splice(index, 0, {
        _id: this.$uuid.v1(),
        start: prevPhase.end
      });

    },
    selectItem(index) {
      this.selectedItem = this.phases[index];
    },
    resetDatetimeItems(index) {

      let length = this.phases.length
      let phase;
      let prevPhase;

      if (length <= 1) return;

      index += 1
      for (index; index < length; index++) {
        prevPhase = this.phases[index - 1]
        phase = this.phases[index]

        let {date, time} = prevPhase.start
        let d = this.calcDateTime(date, time, prevPhase.duration)

        phase.start.date = this.toDateString(d)
        phase.start.time = d.getHours()

        d = this.calcDateTime(phase.start.date, phase.start.time, phase.duration)
        phase.end.date = this.toDateString(d)
        phase.end.time = d.getHours()

        this.phases[index] = phase
      }
    },
    // main action
    store() {
      const that = this;
      let formRequest = this.form;
    }
  },
  mounted() {
    const that = this;

    this.$bus.$on("phaseAdded", event => {
      let item = event.phase;
      if (item)
        this.addItem(item);
    });

    this.$bus.$on("phaseUpdated", event => {
      let item = event.phase;
      if (item)
        this.updateItem(item);
    });

    this.$bus.$on("phaseAddedBefore", event => {
      let index = event.index;
      this.addItemBefore(index);
    });

    this.$bus.$on("phaseSelected", event => {
      console.log('chegou aq', event.index)
      this.selectItem(event.index);
    });

    this.$bus.$on("phaseListChanged", event => {
      this.resetDatetimeItems(event.index);
    });
  },
}
</script>
