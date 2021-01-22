<template>
  <form>
    <div class="form-row">
      <div class="form-group col-md-3">
        <label>Name</label>
        <input v-model="form.name" type="text" class="form-control form-control-sm" />
      </div>
      <div class="form-group col-md-2">
        <label>Start Date</label>
        <input
            :min="this.toDateString(new Date())"
            v-model="form.start.date"
            type="date"
            class="form-control form-control-sm"
        />
      </div>
      <div class="form-group col-auto">
        <label>Start Time</label>
        <select v-model="form.start.time" class="form-control form-control-sm">
          <option :key="hour" v-for="hour in 24" :value="hour-1">{{ ("0" + (hour - 1)).slice(-2) }}:00</option>
        </select>
      </div>
      <div class="form-group col-auto" style="max-width: 7rem;">
        <label>Duration</label>
        <input 
        v-model="form.duration" 
        type="number" 
        class="form-control form-control-sm" />
      </div>
      <div class="form-group col-auto">
        <label>Finish at</label>
        <input :value="this.formatDate(form.end.date, form.end.time)" disabled type="text"
               class="form-control form-control-sm" />
      </div>
      <div class="form-group col-12">
        <div class="form-check">
          <input
            v-model="form.is_drilling"
            class="form-check-input"
            type="checkbox" />
          <label class="form-check-label">
            Drilling
          </label>
        </div>
      </div>
      <div class="col-6" v-show="form.has_test">
        <label for="">Select one or more Test Groups bellow.</label>
        <select
            v-model="form.test_groups"
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
      <div class="form-group col-12">
        <div class="form-check">
          <input
            v-model="form.has_test"
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
    <button @click.prevent="cancel(form)" class="btn-standard">Cancel</button>
  </form>
</template>

<script>
export default {
  props: ['testGroups', 'phase'],
  data() {
    return {
      form: {...this.$defaultSchema()}
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
    cancel(item) {
      this.clearForm();
      this.$parent.selectedItem = {};
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
  mounted() {
    this.$bus.$on("schemaLoaded", event => {
      this.clearForm();
    });
  },
  // validations
  watch: {
    'form.duration': function (val, oldVal) {
      if (val !== null || oldVal !== null) {
        if (!val) {
          this.form.end = {
            date: '',
            time: ''
          }
          return;
        };

        console.log('[LOGGER] out of if', val)

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
      if (newItem._id) this.form = Object.assign({...this.form}, newItem)
    }
  },
}
</script>
