import Vue from "vue";
import { DatetimePicker } from '@livelybone/vue-datepicker';
import Axios from "axios";

Vue.prototype.$http = Axios

// import components
Vue.component('datetime-picker', DatetimePicker);
Vue.component(
    "demo-component",
    require("./components/DemoComponent.vue").default
);

let vue = new Vue({
 components:{ DatetimePicker }
}).$mount("#app");
