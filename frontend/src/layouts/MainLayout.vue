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
             :icon="$q.dark.isActive ? laSunSolid : laMoonSolid"
             @click="toggleDark" />
      
      <q-btn flat
             round
             dense
             :icon="laGithub"
             type="a"
             href="https://github.com/talavis/lunch-menu" />
    </q-toolbar>
  </q-header>
  <q-page-container>
    <router-view />
  </q-page-container>
</q-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { laSunSolid, laMoonSolid, laGithub } from '@quasar/extras/line-awesome'

defineOptions({
  name: 'MainLayout'
})

const version = ref(process.env.VERSION)
const today = ref('')

onMounted(() => {
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday']
  const months = ['January', 'February', 'March',
                  'April', 'May', 'June',
                  'July', 'August', 'September',
                  'October', 'November', 'December']
  let day = new Date()
  today.value = days[day.getDay()] + ' ' + day.getDate() + ' ' + months[day.getMonth()]
})

const $q = useQuasar()

function toggleDark () {
  $q.dark.toggle();
}

</script>
