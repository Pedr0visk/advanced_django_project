require('./bootstrap');
import Vue from "vue";
import 'bootstrap-vue/dist/bootstrap-vue.css'
import {uuid} from 'vue-uuid';
import Axios from "axios";
import VueSweetalert2 from 'vue-sweetalert2';
import {BootstrapVue, IconsPlugin} from 'bootstrap-vue'
import {DatetimePicker} from '@livelybone/vue-datepicker';

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.prototype.$http = Axios;
Vue.prototype.$uuid = uuid;

Vue.use(VueSweetalert2);

// setup axios interceptor
window.axios.interceptors.response.use(function (response) {
    // Do something before request is sent
    return response;
}, function (error) {

    if (error.response.status == 400) {
        let errorMessages = []

        for (let err in error.response.data) {
            errorMessages.push(`${err} - ${error.response.data[err]}`)
        }

        Vue.swal({
            title: 'Validation Failed!',
            html: errorMessages.join('<br>'),
            type: 'error',
        })
    } else if (error.response.status == 500) {
        Vue.swal({
            type: 'error',
            title: 'Oops...',
            text: 'Something went wrong!',
        })
    } else if (error.response.status == 401) {
        // window.location = '/login'
    }

    return Promise.reject(error.response);
});

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
Vue.component(
    "cuts-table",
    require("./components/CutsTable.vue").default
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