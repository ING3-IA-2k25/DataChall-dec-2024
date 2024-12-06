<template>
  <v-container >
    <v-card class="d-flex align-center pa-4 h-16" color="#232634" elevation="8">
      <v-card-text class="font-weight-bold">
        {{ name }}

        <v-chip
          :color="online ? 'green' : 'red'"
          small
          class="ml-2"
        >
          {{ online ? 'Online' : 'Offline' }}
        </v-chip>

      </v-card-text>

      <v-spacer></v-spacer>

      <v-chip
        :color="selected ? 'blue' : 'gray'"
        small
        class="ml-2"
        @click="$emit('emit-select')"
      >
        {{ selected ? 'Selected' : 'Not selected' }}
      </v-chip>

    </v-card>
  </v-container>
</template>

<script setup lang="ts">
// props
import { defineProps } from 'vue';

const props = defineProps({
  name: {
    type: String,
    default: '--',
  },

  online: {
    type: Boolean,
    default: false,
  },

  selected: {
    type: Boolean,
    default: false,
  },
});


</script>

<style scoped>

.custom_checkbox {
  width: 2rem;
  height: 2rem;
  background-color: #fff;
  border: 1px solid #000;
  /* border-radius: 50%; */
}

</style>
