<template>
<q-page class="justify-center">
  <div class="flex justify-center">
    <q-btn-toggle class="q-ma-md"
                  v-model="selectedRegion"
                  :options="regionChoices" />
  </div>
  <div v-if="selectedRegion != 'favourites'">
    <div class="flex justify-center">
      <q-btn-toggle
        v-model="showMapList"
        rounded
        unelevated
        toggle-color="primary"
        color="white"
        text-color="primary"
        :options="[
          {label: 'Map', value: 'map'},
          {label: 'List', value: 'list'}
          ]"
        />
    </div>
    <div v-if="showMapList === 'map'" class="q-my-lg q-mx-md">
      <MenuMap />
    </div>
    <div v-show="showMapList === 'list'" class="q-my-lg q-mx-md">
      <MenuList />
    </div>
  </div>
  <MenuList v-else/>
</q-page>
</template>

<script setup>
import MenuList from 'components/MenuList.vue'
import MenuMap from 'components/MenuMap.vue'

import { laHeartSolid } from '@quasar/extras/line-awesome'

import { ref, computed, onMounted } from 'vue'
import { useMenuHelperStore } from '../stores/menu'

defineOptions({
  name: 'IndexPage',
})

const store = useMenuHelperStore()

const regionChoices = computed(() => {
  let regions = [];
  for (let entry of store.restaurants)
    if (!regions.includes(entry.region.toLowerCase()))
      regions.push(entry.region.toLowerCase())
  regions = regions.sort()
  regions.forEach(function (value, i) {
    regions[i] = {label: value, value: value}
  });
  regions.push({icon: laHeartSolid, value: 'favourites'})
  return regions;
})

const selectedRegion = computed({
  get() {
    return store.currentRegion
  },
  set(newValue) {
    store.updateRegion(newValue)
  }
})

const showMapList = computed({
  get () {
    return store.showMapList
  },
  set (newValue) {
    store.showMapList = newValue
  }
})

const error = ref(false)
const loading = ref(false)

onMounted(() => {
  loading.value = true
  store.getRestaurants()
    .catch(() => {
      error.value = true
    })
    .finally(() => {
      loading.value = false
    })
  store.loadRegion()
})

</script>
