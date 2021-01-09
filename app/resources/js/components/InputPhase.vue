<template>
  <form>
    <div class="form-row">
      <div class="form-group col-md-3">
        <label>Name</label>
        <input v-model="form.name" type="text" class="form-control form-control-sm" />
      </div>
      <div class="form-group col-md-2">
        <label>Start Date</label>
        <input v-model="form.start.date" type="date" class="form-control form-control-sm" />
      </div>
      <div class="form-group col-auto">
        <label>Start Time</label>
        <select v-model="form.start.time" class="form-control form-control-sm">
          <option value="1">1h</option>
          <option value="2">2h</option>
        </select>
      </div>
      <div class="form-group col-auto" style="max-width: 7rem;">
        <label>Duration</label>
        <input v-model="form.duration" type="number" class="form-control form-control-sm" />
      </div>
      <div class="form-group col-auto">
        <label>Finish at</label>
        <input :value="this.formatDate(form.end.date, form.end.time)" disabled type="text"
               class="form-control form-control-sm" />
      </div>
      <div class="form-group col-12">
        <div class="form-check">
          <input
            class="form-check-input"
            type="checkbox" />
          <label class="form-check-label">
            Drilling
          </label>
        </div>
      </div>
      <div class="form-group col-12">
        <div class="form-check">
          <input
            class="form-check-input"
            type="checkbox">
          <label class="form-check-label">
            Test
          </label>
        </div>
      </div>
    </div>

    <button
      v-show="!form._id"
      class="btn-standard"
      @click.prevent="submit">
      <i class="fa fa-plus text-success"></i> Add phase
    </button>
    <button
      v-show="form._id"
      class="btn-standard"
      @click.prevent="submit">
      <i class="fa fa-pencil-alt text-warning"></i> Update
    </button>
    <button class="btn-standard">Cancel</button>
  </form>
</template>

<script>
export default {
  props: ['test-groups', 'phase'],
  data() {
    return {
      form: {
        _id: null,
        name: '',
        has_test: false,
        is_drilling: false,
        duration: null,
        start: {date: '', time: 12},
        end: {date: '', time: 0},
        test_groups: []
      }
    }
  },
  methods: {
    submit() {
      if (!this.form._id) {
        this.$bus.$emit("phaseAdded", {
          phase: this.form
        });
      } else {
        this.$bus.$emit("phaseUpdated", {
          phase: this.form
        });
      }

      this.clearForm();
    },
    clearForm() {
      // clear data input and set some default
      // values to start dante and time
      const lastPhase = this.$parent.phases[this.$parent.phases.length - 1];

      this.form = {
        _id: null,
        name: '',
        duration: null,
        has_test:  false,
        is_drilling: false,
        start: lastPhase.end,
        end: {date: '', time: 0},
        test_groups: []
      }
    }
  },
  // validations
  watch: {
    'form.duration': function (val, oldVal) {
      if (val !== null && oldVal !== null) {
        let {date, time} = this.form.start;
        let d = this.calcDateTime(date, time, this.form.duration);

        this.form.end = {
          date: this.toDateString(d),
          time: d.getHours()
        }
      }
    },
    'form.start.time': function (val, oldVal) {
      if (val !== null && oldVal !== null) {
        let {date, time} = this.form.start
        let {duration} = this.form

        if (duration == '' || duration == null)
          return

        let d = this.calcDateTime(date, time, duration)

        this.form.end = {
          date: `${d.getFullYear()}-${("0" + (d.getMonth() + 1)).slice(-2)}-${("0" + (d.getDate())).slice(-2)}`,
          time: d.getHours()
        }
      }
    },
    'form.has_test': function (val, oldVal) {
      if (val !== null && oldVal !== null) {
        if (this.form.has_test) {
          this.form.is_drilling = false
        }
      }
    },
    'form.is_drilling': function (val, oldVal) {
      if (val !== null && oldVal !== null) {
        if (this.form.is_drilling) {
          this.form.has_test = false
          this.form.test_groups = []
        }
      }
    },

    phase: function(newItem, oldItem) {
      if (newItem) this.form = newItem
    }
  },
}
</script>
