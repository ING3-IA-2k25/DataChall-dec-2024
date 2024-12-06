<script setup lang="ts">
/* eslint-disable*/
import { onMounted, ref } from 'vue';
import "leaflet/dist/leaflet.css";
import L from 'leaflet'
import { LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";

// const zoom = ref(12)
// const center = ref([48.869438881659114, 2.3086074935262557])

// import metrograph.ts store
import { useMetrographStore } from '@/stores/metrograph';

const metroGraphStore = useMetrographStore();

onMounted(() => {
  metroGraphStore.loadGraph();
  // metroGraphStore.fetchProducers();
})

import { useMetroMap } from '@/composables/useMetroMap';


const { initMap } = useMetroMap();

onMounted(() => {
  initMap('map');
});




</script>

<template>
  <main>
    <div class="flex flex-row justify-center bg-ctp-frappe-base h-screen mt--16 pt-16  ">
      <!-- Left colone -->
      <div id="left-col" class="h-full w-100 relative">

        <!-- div pour la map center -->
        <div class="absolute p-15! h-full w-full">
          <div class="bg-ctp-latte-mauve h-full w-full" ref="mapDiv" id="map">
          </div>
        </div>
      </div>

    </div>
  </main>
</template>
