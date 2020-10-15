import Vue from "vue";
import {uuid} from 'vue-uuid';
import Axios from "axios";
import VueSweetalert2 from 'vue-sweetalert2';

import {DatetimePicker} from '@livelybone/vue-datepicker';

Vue.prototype.$http = Axios;
Vue.prototype.$uuid = uuid;

Vue.use(VueSweetalert2);

// import components
Vue.component('datetime-picker', DatetimePicker);
Vue.component(
    "demo-component",
    require("./components/DemoComponent.vue").default
);
Vue.component(
    "schema-form",
    require("./components/SchemaForm.vue").default
);
Vue.component(
    "schema-update",
    require("./components/SchemaUpdate.vue").default
);

/*
 * By extending the Vue prototype with a new '$bus' property
 * we can easily access our global event bus from any child component.
 */
Object.defineProperty(Vue.prototype, '$bus', {
    get() {
        return this.$root.bus;
    }
});

window.bus = new Vue({});

let vue = new Vue({
    data() {
        return {
            bus: bus
        }
    },
    components: {DatetimePicker},

}).$mount("#app");
