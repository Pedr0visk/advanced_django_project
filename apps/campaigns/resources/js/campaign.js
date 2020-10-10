import Vue from "vue";
import { uuid } from 'vue-uuid';
import Axios from "axios";

import { DatetimePicker } from '@livelybone/vue-datepicker';

Vue.prototype.$http = Axios;
Vue.prototype.$uuid = uuid;

// import components
Vue.component('datetime-picker', DatetimePicker);
Vue.component(
    "demo-component",
    require("./components/DemoComponent.vue").default
);

let vue = new Vue({
 components:{ DatetimePicker }
}).$mount("#app");
