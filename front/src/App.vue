<script setup lang="ts">
import { RouterView } from 'vue-router'
import HeaderBase from './components/HeaderBase.vue';
</script>

<template class="static w-full h-screen max-h-dvh">
  <v-app class="bg-ctp-frappe-base! block!">
    <HeaderBase />
    <div class="relative">
      <RouterView />
    </div>
  </v-app>

</template>

<style scoped>


div {

  height: 75%;
}
</style>
