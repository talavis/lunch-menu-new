import { defineStore } from 'pinia'
import { LocalStorage } from 'quasar'
import axios from 'axios'

export const useMenuHelperStore = defineStore('menuHelper', {
  state: () => ({
    restaurants: [],
    visibleRestaurants: [],
    currentRegion: 'solna',
    favourites: [],
    showMapList: 'list',
    menu: {},
  }),
  actions: {
    getRestaurant (identifier) {
      return new Promise((resolve, reject) => {
	axios
	  .get('/api/restaurant/' + identifier)
	  .then((response) => {
	    this.menu[identifier] = response.data.restaurant.menu
	    resolve(response);
	  })
	  .catch((err) => {
	    reject(err)
	  });
      })
    },
    getRestaurants() {
      return new Promise((resolve, reject) => {
	if (this.restaurants.length === 0) {
	  axios
	    .get('/api/restaurant')
	    .then((response) => {
	      this.restaurants = response.data.restaurants
	      this.updateVisible()
	      resolve(response)
	    })
	    .catch((err) => {
	      reject(err)
	    })
	}
	else {
	  resolve({})
	}
      })
    },
    loadRegion() {
      let savedRegion = LocalStorage.getItem('currentRegion')
      if (savedRegion !== null) {
	this.currentRegion = savedRegion
      }
    },
    updateRegion(newRegion) {
      this.currentRegion = newRegion
      LocalStorage.set('currentRegion', newRegion)
      this.updateVisible()
    },
    updateVisible() {
      let current = JSON.parse(JSON.stringify(this.restaurants))
      if (this.currentRegion === "favourites") {
	current = current.filter((entry) => this.favourites.includes(entry.identifier))
      }
      else {
	current = current.filter((value) => value.region.toLowerCase() === this.currentRegion)
      }
      this.visibleRestaurants = current.sort((a,b) => {
	return (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0)
      })
    },
    updateFavourite(payload) {
      let index = this.favourites.indexOf(payload.restaurant);
      if (payload.favourite) {
	if (index === -1) {
	  this.favourites.push(payload.restaurant);
	}
      }
      else {
	if (index > -1) {
	  this.favourites.splice(index, 1);
	}
      }
    },
  }
})
