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
    <td><a href="">show</a></td>

    <td align="center">
      <a
        @click.prevent="addItemBefore(index)"
        href="" class="btn-standard px-2"><i class="fas fa-arrow-circle-up text-success"></i> insert up</a>
      <a
        @click.prevent="onSelect(index)"
        href="" class="btn-standard px-2"><i class="fas fa-arrow-circle-down text-success"></i> insert down</a>
      <a
        @click.prevent="onSelect(index)"
        href="" class="btn-standard px-2"><i class="fa fa-pencil-alt text-warning"></i> edit</a>
      <a
        @click.prevent="deleteItem(phase)"
        href="" class="btn-standard px-2"><i class="fa fa-times text-danger"></i> remove</a>
    </td>
  </tr>
</template>

<script>
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
      if (this.$parent.selectedItem)
        return {
          active: this.$parent.selectedItem._id === item._id
        };

      return {
        active: false
      }
    }
  }
}
</script>

<style>
tr.active {
  background-color: #ffdb9b;
}
</style>
