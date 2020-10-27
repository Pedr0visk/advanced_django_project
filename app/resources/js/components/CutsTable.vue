<template>
  <div class="overflow-auto">

    <p class="mt-3">Current Page: {{ currentPage }}</p>
    <b-table
        id="my-table"
        :items="items"
        :per-page="perPage"
        :current-page="currentPage"
        small
    ></b-table>

    <p class="mt-3">Current Page: {{ currentPage }}</p>
    <b-pagination
        v-model="currentPage"
        :total-rows="rows"
        :per-page="perPage"
        aria-controls="my-table"
    ></b-pagination>

  </div>
</template>

<script>
export default {
  data() {
    return {
      perPage: 15,
      currentPage: 1,
      items: []
    }
  },
  mounted() {
    this.items = JSON.parse(document.getElementById('json_data').textContent)
  },
  computed: {
    rows() {
      return this.items.length
    }
  }
}
</script>
