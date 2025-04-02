<template>
  <div class="card group cursor-pointer" @click="$emit('click')">
    <div class="flex items-center space-x-4">
      <div class="flex-shrink-0">
        <div class="w-12 h-12 rounded-lg bg-primary-100 flex items-center justify-center group-hover:bg-primary-200 transition-colors duration-300">
          <component :is="icon" class="w-6 h-6 text-primary-600" />
        </div>
      </div>
      <div class="flex-1">
        <h3 class="text-lg font-semibold text-gray-900">{{ title }}</h3>
        <p class="text-sm text-gray-500 mt-1">{{ description }}</p>
      </div>
      <div class="flex-shrink-0">
        <ChevronRightIcon class="w-5 h-5 text-gray-400 group-hover:text-primary-500 transition-colors duration-300" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ChevronRightIcon } from '@heroicons/vue/24/outline'

defineProps<{
  title: string
  description: string
  icon: any
}>()

defineEmits<{
  (e: 'click'): void
}>()
</script> 