<template>
  <div class="form-group">
    <div class="input-group date datepicker" id="datetimepicker1">
      <input type="text" class="form-control form-control-sm" v-on:focus="datepick_dialog_open" v-on:blur="select_by_lose_focus">
      <div class="input-group-append" data-target="#datetimepicker1" data-toggle="datetimepicker">
        <div class="input-group-text"><i class="fa fa-calendar"></i></div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      date: ''
    }
  },
  mounted() {
    
  },
  methods: {
    datepick_dialog_open() {
      this.$el.firstChild.children[1].click();
      console.log('YAHOOY')
    },
    select_by_lose_focus(e) {
      console.log('AHOY!');
      console.log(e.target.value);
    }
  }
};
</script>
