<template>
<div class="justify-center">
  <div class="flex justify-center">
    <q-list class="flex-center">
      <q-item v-for="restaurant in store.visibleRestaurants"
              :key="restaurant.identifier">
        <q-item-section>
          <RestaurantEntry :restaurantBase="restaurant" />
        </q-item-section>
      </q-item>
    </q-list>

    <q-inner-loading :showing="loading">
      <q-spinner-dots color="primary"
                      size="2em" />
    </q-inner-loading>
  </div>
</div>
</template>

<script setup>
import RestaurantEntry from 'components/RestaurantEntry.vue'

import { ref, onMounted } from 'vue'
import { useMenuHelperStore } from '../stores/menu'

const store = useMenuHelperStore()

const loading = ref(false)

defineOptions({
  name: 'MenuList',
})

onMounted(() => {
  store.getRestaurants()
})

</script>
