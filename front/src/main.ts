import './assets/main.css'

import App from './App.vue'
import router from './router'

/* -------------------------------------------------------------- */

/* -------------------------------------------------------------- */

// pinia
import { createApp } from 'vue'
import { createPinia } from 'pinia'

/* -------------------------------------------------------------- */

//unocss
import 'virtual:uno.css'

/* -------------------------------------------------------------- */


// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

const vuetify = createVuetify({
    icons: {
        defaultSet: 'mdi',
        aliases,
        sets: {
            mdi,
        },
    },
    components,
    directives,
})

/* -------------------------------------------------------------- */

import Vue3Toasity, { type ToastContainerOptions } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

const toastconfig: ToastContainerOptions = {
    autoClose: 3000,
}

/* -------------------------------------------------------------- */


createApp(App)
  .use(createPinia())
  .use(router)
  .use(vuetify)
  .use(Vue3Toasity, toastconfig)
  .mount('#app')
