<template>
  <div class="flex justify-center">
    <div ref="mapRoot" style="width: 100%; height: 50vh; max-height: 50em">
    </div>
    <RestaurantEntry v-if="selectedRestaurant.length > 0"
               class="q-my-md"
               :restaurantBase="selectedRestaurantBase" />
    <q-card v-else
            class="q-my-md">
      <q-card-section class="text-center text-weight-medium">
        Click a marker to show information about the restaurant
      </q-card-section>
    </q-card>
  </div>
</template>

<script setup>
import View from 'ol/View'
import Map from 'ol/Map'
import TileLayer from 'ol/layer/Tile'
import VectorLayer from 'ol/layer/Vector'
import OSM from 'ol/source/OSM'
import Vector from 'ol/source/Vector'
import Feature from 'ol/Feature'
import Point from 'ol/geom/Point'
import {fromLonLat} from 'ol/proj'
import {Icon, Style} from 'ol/style';
import {getDistance} from 'ol/sphere';
import 'ol/ol.css'

import { ref, computed, onMounted, watch } from 'vue'

import markerSelectUrl from 'assets/assets/map-marker-solid-sel.png'
import markerUrl from 'assets/assets/map-marker-solid-sel.png'

import { useMenuHelperStore } from '../stores/menu'
import RestaurantEntry from 'components/RestaurantEntry.vue'

const store = useMenuHelperStore()

defineOptions({
  name: 'MenuMap',
})

const mapObject = ref(null)
const selectedRestaurant = ref('')
const currRes = ref(null)
const resSource = ref(null)
const mapRoot = ref(null)

const selectedRestaurantBase = computed(() => {
  for (let entry of store.restaurants) {
    if (entry.identifier === selectedRestaurant.value)
      return entry
  }
  return null
})

const showMap = computed({
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

const updateResSource = () => {
  resSource.value.clear()
  for (let entry of store.visibleRestaurants) {
    resSource.value.addFeature(new Feature({
      geometry: new Point(fromLonLat([entry.coordinate[1], entry.coordinate[0]])),
      name: entry.identifier,
    }))
  }
}

const handleMapClick = (event) => {
  let res = resSource.value.getClosestFeatureToCoordinate(event.coordinate)
  if (currRes.value !== null)
    currRes.value.setStyle(undefined)
  currRes.value = res
  if (currRes.value !== null) {
    currRes.value.setStyle(new Style({
      image: new Icon({
        anchor: [0.5, 50],
        anchorXUnits: 'fraction',
        anchorYUnits: 'pixels',
        src: markerSelectUrl,
      })
    }))
    selectedRestaurant.value = res.get('name')
  }
  else
    this.selectedRestaurant = ''
}

watch(store.visibleRestaurants, () => {
  selectedRestaurant.value = '',
  currRes.value = null;
  updateResSource();
  if (resSource.value.getFeatures().length > 0)
    mapObject.value.getView().fit(this.resSource.getExtent(), {padding: [70, 70, 70, 70]});
  else
    mapObject.value.setView(new View({center: fromLonLat([18.02588, 59.34864]), zoom:15}))
})

onMounted(() => {
  mapObject.value = new Map({
    target: mapRoot.value,
    layers: [ new TileLayer({ source: new OSM() }) ],
    view: new View({center: fromLonLat([18.02588, 59.34864]), zoom:15})
  })
  resSource.value = new Vector({features: []});
  updateResSource()
  let layer = new VectorLayer({source: resSource.value,
                               style: new Style({
                                 image: new Icon({
                                   anchor: [0.5, 50],
                                   anchorXUnits: 'fraction',
                                   anchorYUnits: 'pixels',
                                   src: markerUrl,
                                 })
                               })
                              })
  mapObject.value.addLayer(layer);
  if (resSource.value.getFeatures().length > 0) {
    mapObject.value.getView().fit(resSource.value.getExtent(), {padding: [70, 70, 70, 70]});
  }
  mapObject.value.on('click', handleMapClick);
})

</script>
