<template>
<q-layout view="lHh Lpr lFf">
  <q-header elevated reveal>
    <q-toolbar>
      <q-toolbar-title>
	{{ today }}
      </q-toolbar-title>

      <q-space />

      <div class="q-mr-xl text-weight-bold text-caption">
	{{ version }}
      </div>
      <q-btn flat
             round
             dense
             :icon="$q.dark.isActive ? 'las la-sun' : 'las la-moon'"
             @click="toggleDark" />
      
      <q-btn flat
             round
             dense
             icon="lab la-github"
             type="a"
             href="https://github.com/talavis/lunch-menu" />
    </q-toolbar>
  </q-header>
  <q-page-container>
    <router-view />
  </q-page-container>
</q-layout>
</template>

<script>
import { setCssVar } from 'quasar'

export default {
  name: 'MainLayout',

  data () {
    return {
      today: '',
      version: process.env.VERSION,
    }
  },

  methods: {
    toggleDark () {
      console.log("here")
      this.$q.dark.toggle();
//      if (this.$q.dark.isActive)
//        setCssVar('info', '#A7C947');
//      else
//        setCssVar('info', '#3F3F3F');
    },
  },
  
  created () {
    if (this.$q.dark.isActive)
      setCssVar('info', '#A7C947');

    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
                  'Thursday', 'Friday', 'Saturday'];
    const months = ['January', 'February', 'March',
                    'April', 'May', 'June',
                    'July', 'August', 'September',
                    'October', 'November', 'December'];
    let day = new Date();
    this.today = days[day.getDay()] + ' ' + day.getDate() + ' ' + months[day.getMonth()];
  }
    
}
</script>
