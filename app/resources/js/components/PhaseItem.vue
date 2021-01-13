<template>
  <tr :class="activeClass(phase)">
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
    <td><a href="" v-show="phase._id" @click.prevent="displayTestGroups(phase)">show <i class="fas fa-external-link-alt"></i></a></td>

    <td align="center">
      <div v-show="phase._id != this.$parent.selectedItem._id">
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
import Modal from "./Modal.vue";

export default {
  props: ['index', 'phase'],
  data() {
    return {};
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

    displayTestGroups(item) {
      let body = '';

      this.$parent.testGroupsOptions.map(i => {
        let items = JSON.parse(JSON.stringify(item.test_groups))
        if (items.includes(i.id)) {
          body = `
            <table class="table m-0 table-hover dnv-table dnv-table-admin">
              <thead>
              <tr>
                <th scope="col">name</th>
                <th scope="col">start date</th>
                <th scope="col">failure modes</th>
                <th scope="col">tests <small>(interval, coverage)</small></th>
                <td></td>
                <td></td>
              </tr>
              </thead>
              <tbody>
                <tr>
                  <td>test group 1</td>
                  <td width="10%"></td>
                  <td width="50%">
                    
                  </td>
                  <td align="left">
                    level 1 <b>168, 0.2</b><br>
                  </td>
                </tr>
              </tbody>
            </table>
          `
        }
      });

      this.$swal.fire({
        title: '<strong>Showing Test Groups</strong>',
        width: 1200,
        padding: '0.5rem',
        html: body,
        showCloseButton: true,
        showCancelButton: false,
        confirmButtonText:
          '<i class="fa fa-thumbs-up"></i> Okay!',
        confirmButtonAriaLabel: 'Thumbs up, great!',
      })
    }
  }
}
</script>

<style>
tr.active {
  background-color: #ffdb9b!important;
}
</style>
