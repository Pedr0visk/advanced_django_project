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
    <input-phase :phase="selectedItem" :testGroups="testGroupsOptions"></input-phase>
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
          <button v-show="!form.id" @click.prevent="store" type="submit" class="btn btn-primary">
            SAVE
          </button>
          <button v-show="form.id" @click.prevent="update" type="submit" class="btn btn-primary">
            UPDATE
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
        id: null,
        campaign: null,
        name: '',
        is_default: false,
      },
      phases: [],
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
      this.selectedItem = {};
      console.log('logging index at', item, index);
      // Update all phase's datetime
      this.resetDatetimeItems(index);
    },
    addItemBefore(index) {
      let prevPhase;

      if (index > 0) {
        prevPhase = this.phases[index - 1];
        this.phases.splice(index, 0, Object.assign({...this.$defaultSchema()}, {
          _id: this.$uuid.v1(),
          start: prevPhase.end
        }));
      } else {
        console.log('equal 0')
        this.phases.splice(index, 0, Object.assign({...this.$defaultSchema()}, {
          _id: this.$uuid.v1(),
        }));
      }
      this.selectItem(index);
    },
    addItemAfter(index) {
      let prevPhase;

      prevPhase = this.phases[index];

      this.phases.splice(index + 1, 0, Object.assign({...this.$defaultSchema()}, {
        _id: this.$uuid.v1(),
        start: prevPhase.end
      })); 

      this.selectItem(index + 1);
    },
    selectItem(index) {
      this.selectedItem = this.phases[index];
    },
    resetDatetimeItems(index) {

      let length = this.phases.length
      let phase;
      let prevPhase;

      index += 1
      for (index; index < length; index++) {
        prevPhase = this.phases[index - 1];
        phase = this.phases[index];

        phase.start = prevPhase.end;

        let d = this.calcDateTime(phase.start.date, phase.start.time, phase.duration);
        phase.end.date = this.toDateString(d);
        phase.end.time = d.getHours();

        this.phases[index] = phase;
      }
    },
    clearForm() {
      this.phases = [];
      this.form = {
        campaign: null,
        name: '',
        is_default: false,
      }
    },
    // main action
    store() {
      const that = this;
      const config = {
        headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value},
      }

      let formRequest = this.form;
      
      formRequest.phases = this.phases.map(phase => {
        let start_date = this.formatDate(phase.start.date, phase.start.time),
            end_date = this.formatDate(phase.end.date, phase.end.time);

        return {...phase, start_date, end_date}
      });

      axios.post('/api/schemas/', formRequest, config)
        .then(response => {
          that
            .$swal({
              title: "Schema created successfully!",
              text: 'go to campaign dashboard to see it',
              type: "success",
              showConfirmButton: false,
              timer: 1500
            })
            .then(swalRes => {
              this.clearForm();
            });
          })
    },
    update() {
      const that = this;

      let formRequest = this.form;
      
      formRequest.phases = this.phases.map(phase => {
        let start_date = this.formatDate(phase.start.date, phase.start.time),
            end_date = this.formatDate(phase.end.date, phase.end.time);

        return {...phase, start_date, end_date}
      });

      const config = {
        method: 'put',
        url: `/api/schemas/${this.form.id}/`,
        headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value},
        data: formRequest
      }

      this.$http(config)
        .then(response => {
          console.log(response)
          that
            .$swal({
              title: "Schema successfully updated!",
              text: 'go to campaign list to see it',
              type: "success",
              showConfirmButton: false,
              timer: 1500
            })
            .then(swalRes => {
              // window.location.href =  ;
            });
        })

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

    this.$bus.$on("phaseAddedAfter", event => {
      let index = event.index;
      this.addItemAfter(index);
    });

    this.$bus.$on("phaseSelected", event => {
      this.selectItem(event.index);
    });

    this.$bus.$on("phaseListChanged", event => {
      this.resetDatetimeItems(event.index);
    });


    //
    const bopId = document.getElementById('bopId').value;
    const schemaId = document.getElementById('schemaId').value;
    const campaignId = document.getElementById('campaignId').value;

    this.form.id = schemaId;
    this.form.campaign = campaignId;
    
    axios
        .get(`/api/bops/${bopId}/test-groups/`)
        .then(response => {
          console.log(response.data)
          this.testGroupsOptions = response.data
        });

    if (schemaId) {
      this.$http
        .get(`/api/schemas/${schemaId}/`)
        .then(response => {
          this.form.name = response.data.name
          this.form.is_default = response.data.is_default
          this.phases = response.data.phases.map(phase => {
            let start = {
              date: this.toDateString(new Date(phase.start_date)),
              time: new Date(phase.start_date).getHours()
            }

            let d = this.calcDateTime(start.date, start.time, phase.duration)

            let end = {
              date: this.toDateString(d),
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
          });

          this.$bus.$emit("schemaLoaded", {});
        })
    }
    
  },
}
</script>
