<template>
<q-card>
  <q-card-section>
    <div class="row">
      <q-btn flat
             dense
             no-wrap
             text-color="primary"
             type="a"
             :href="props.restaurantBase.homepage.length ? props.restaurantBase.homepage : '#'"
             :icon-right="props.restaurantBase.homepage.length ? 'las la-external-link-alt' : ''"
             :label="props.restaurantBase.name" />
      <q-space />
      
      <q-btn @click="isFavourite = !isFavourite"
	     flat
	     dense
	     round
	     color="white"
	     text-color="primary"
	     :icon="isFavourite ? laHeartSolid : laHeart" />
    </div>
    <div v-if="loading"
         class="flex justify-center">
      <q-spinner-dots 
        color="info"
        size="2em"
        />
    </div>
    <div v-else-if="failed"
         class="justify-center">
      <q-avatar text-color="negative" icon="error" />
      Failed to retrieve data for {{ props.restaurantBase.name }}
    </div>
    <q-list v-else>
      <q-item
        v-for="menuEntry in store.menu[props.restaurantBase.identifier]"
        :key="menuEntry['dish']">
        {{ menuEntry['dish'] }}
      </q-item>
    </q-list>
  </q-card-section>
</q-card>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useMenuHelperStore } from '../stores/menu'
import { laHeartSolid, laHeart } from '@quasar/extras/line-awesome'

defineOptions({
  name: 'RestaurantEntry'
})

const store = useMenuHelperStore()
const props = defineProps(["restaurantBase"])

const favourites = computed(() => {
  return store.favourites
})

const isFavourite = computed({
  get() {
    return store.favourites.includes(props.restaurantBase.identifier)
  },
  set(newValue) {
    store.updateFavourite({
      'favourite': newValue,
      'restaurant': props.restaurantBase.identifier,
    })
  }
})

const dishes = ref([])
const loading = ref(false)
const failed = ref(false)
const restaurantData = ref({})

onMounted(() => {
  store.getRestaurant(props.restaurantBase.identifier)
  isFavourite.value = favourites.value.includes(props.restaurantBase.identifier);
  store.getRestaurant(props.restaurantBase.identifier)
})

</script>
