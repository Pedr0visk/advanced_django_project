<template>
  <tr :class="[activeClass(phase), inactiveClass(editable)]">
    <td>{{ phase.name }}</td>
    <td>
      {{ this.formatDate(phase.start.date, phase.start.time) }}
    </td>
    <td>
      {{ this.formatDate(phase.end.date, phase.end.time) }}
    </td>
    <td>{{ phase.duration }}h</td>
    <td><img v-if="phase.has_test" src="/static/img/icon-yes.svg" alt=""></td>
    <td><img v-if="phase.is_drilling" src="/static/img/icon-yes.svg" alt=""></td>
    <td>
      <a
          href=""
          v-show="phase._id"
          @click.prevent="displayTestGroups(phase)">
        show <i class="fas fa-external-link-alt"></i>
      </a>
    </td>

    <td align="center">
      <div v-show="phase._id != this.$parent.selectedItem._id && editable">
      <a
        @click.prevent="addItemBefore(index)"
        href="" class="btn-standard px-2"><i class="fas fa-arrow-circle-up text-success"></i> insert up</a>
      <a
        @click.prevent="addItemAfter(index)"
        href="" class="btn-standard px-2"><i class="fas fa-arrow-circle-down text-success"></i> insert down</a>
      <a
        @click.prevent="onSelect(index)"
        href="" class="btn-standard px-2"><i class="fa fa-pencil-alt text-warning"></i> edit</a>
      <a
        @click.prevent="deleteItem(phase)"
        href="" class="btn-standard px-2"><i class="fa fa-times text-danger"></i> remove</a>
      </div>
    </td>
  </tr>
</template>

<script>

export default {
  props: ['index', 'phase'],
  data() {
    return {
      editable: true
    };
  },
  methods: {
    addItemBefore(index) {
      this.$bus.$emit("phaseAddedBefore", {
        index
      });
    },

    addItemAfter(index) {
      this.$bus.$emit("phaseAddedAfter", {
        index
      });
    },

    onSelect(index) {
      this.$bus.$emit("phaseSelected", {
        index
      });
    },

    deleteItem(item) {
      let index = _.findIndex(this.$parent.phases, function(i) {
        return i._id == item._id;
      });
      this.$parent.phases.splice(index, 1);

      this.$bus.$emit("phaseListChanged", {index: 0});
    },

    activeClass(item) {
      return {
        active: this.$parent.selectedItem._id == item._id
      };
    },

    inactiveClass() {
      return {
        disabled: !this.editable
      }
    },

    displayTestGroups(item) {
      let tbody = ''

      this.$parent.testGroupsOptions.map(i => {
        let failureModesPack = '';

        if (item.test_groups.includes(i.id)) {
          let fmList = i.failure_modes.slice(0, 99);
          fmList.map(el => {
            failureModesPack += `<small>${el.code}, </small>`
          });
        }

        tbody += `<tr>
          <td>${i.name}</td>
          <td width="10%">${i.start_date}</td>
          <td width="50%">
          ${failureModesPack}
          </td>
          <td align="left">
          ${JSON.stringify(i.tests)}
          </td>
        </tr>`
      });

      let table = `
      <div class="table-responsive table-scroll">
        <table class="table m-0 table-hover dnv-table dnv-table-admin" id="campaignsTable">
          <thead>
            <tr>
              <th scope="col">name</th>
              <th scope="col">start date</th>
              <th scope="col">failure modes</th>
              <th scope="col">tests <small>(interval, coverage)</small></th>
            </tr>
          </thead>
          
          <tbody>
            ${tbody}
          </tbody>
        </table>
      </div>`;

      this.$swal.fire({
        title: '<strong>Test Groups</strong>',
        width: 1200,
        padding: '1rem',
        html: table,
        showCloseButton: true,
        showCancelButton: false,
        confirmButtonText:
          '<i class="fa fa-thumbs-up"></i> Okay!',
        confirmButtonAriaLabel: 'Thumbs up, great!',
      })
    }
  },
  mounted() {
    let date = new Date(this.formatDate(this.phase.end.date, this.phase.end.time)),
        currDate = new Date();

    if (currDate > date) this.editable = false;
  }
}
</script>

<style>
tr.active {
  background-color: #ffdb9b!important;
}
tr.disabled {
  background-color: #e3e3e3!important;
}
</style>
