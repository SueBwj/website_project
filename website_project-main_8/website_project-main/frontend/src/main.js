import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';

// bootstrap
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap';


// Vuetify
import 'vuetify/styles';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';


const vuetify = createVuetify({
    components,
    directives,
});


createApp(App)
    .use(store)
    .use(router)
    .use(vuetify)
    .mount('#app');
