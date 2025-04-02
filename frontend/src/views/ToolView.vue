<template>
  <div class="min-h-screen bg-gray-50 py-12">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-8">
        <button @click="router.back()" class="flex items-center text-gray-600 hover:text-primary-600">
          <ArrowLeftIcon class="w-5 h-5 mr-2" />
          返回
        </button>
      </div>
      
      <div class="card">
        <div class="flex items-center space-x-4 mb-6">
          <div class="w-12 h-12 rounded-lg bg-primary-100 flex items-center justify-center">
            <component :is="tool.icon" class="w-6 h-6 text-primary-600" />
          </div>
          <div>
            <h1 class="text-2xl font-bold text-gray-900">{{ tool.title }}</h1>
            <p class="text-gray-600">{{ tool.description }}</p>
          </div>
        </div>
        
        <div class="space-y-6">
          <!-- 今天吃什么 -->
          <div v-if="toolId === 'what-to-eat'" class="space-y-4">
            <div class="flex space-x-4">
              <button 
                v-for="type in foodTypes" 
                :key="type"
                @click="selectedType = type"
                :class="[
                  'btn',
                  selectedType === type ? 'btn-primary' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                ]"
              >
                {{ type }}
              </button>
            </div>
            <div v-if="result" class="p-4 bg-gray-50 rounded-lg">
              <h3 class="text-lg font-semibold mb-2">推荐：</h3>
              <p class="text-xl text-primary-600">{{ result }}</p>
            </div>
            <button 
              @click="getFoodRecommendation" 
              class="btn btn-primary w-full"
              :disabled="loading"
            >
              {{ loading ? '获取中...' : '获取推荐' }}
            </button>
            <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>
          </div>
          
          <!-- 开心一下 -->
          <div v-if="toolId === 'happy-moment'" class="space-y-4">
            <div v-if="joke" class="p-4 bg-gray-50 rounded-lg">
              <p class="text-lg">{{ joke }}</p>
            </div>
            <button 
              @click="getJoke" 
              class="btn btn-primary w-full"
              :disabled="loading"
            >
              {{ loading ? '获取中...' : '获取新笑话' }}
            </button>
            <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>
          </div>
          
          <!-- 其他工具 -->
          <div v-else class="text-center text-gray-500">
            该功能正在开发中...
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeftIcon } from '@heroicons/vue/24/outline'
import {
  SparklesIcon,
  FaceSmileIcon,
  QuestionMarkCircleIcon,
  ChatBubbleLeftRightIcon,
  DocumentTextIcon,
  PhotoIcon
} from '@heroicons/vue/24/outline'
import { useToolsStore } from '../stores/tools'

const route = useRoute()
const router = useRouter()
const toolsStore = useToolsStore()

type ToolId = keyof typeof tools
const toolId = computed(() => route.params.id as ToolId)

const tools = {
  'what-to-eat': {
    title: '今天吃什么？',
    description: '让AI帮你解决选择困难症',
    icon: QuestionMarkCircleIcon
  },
  'happy-moment': {
    title: '开心一下',
    description: '获取一个有趣的笑话或故事',
    icon: FaceSmileIcon
  },
  'chat': {
    title: '智能对话',
    description: '与AI助手进行自然对话',
    icon: ChatBubbleLeftRightIcon
  },
  'text-generator': {
    title: '文本生成',
    description: '生成文章、故事或创意内容',
    icon: DocumentTextIcon
  },
  'image-generator': {
    title: '图像生成',
    description: '将文字转换为图像',
    icon: PhotoIcon
  },
  'ai-assistant': {
    title: 'AI助手',
    description: '全能AI助手，解决各种问题',
    icon: SparklesIcon
  }
}

const tool = computed(() => tools[toolId.value])

// 今天吃什么
const foodTypes = ['中餐', '西餐', '日料', '韩餐', '快餐']
const selectedType = ref('中餐')
const result = ref('')

const getFoodRecommendation = async () => {
  try {
    result.value = await toolsStore.getFoodRecommendation(selectedType.value)
  } catch (e) {
    console.error(e)
  }
}

// 开心一下
const joke = ref('')

const getJoke = async () => {
  try {
    joke.value = await toolsStore.getJoke()
  } catch (e) {
    console.error(e)
  }
}

// 计算属性
const loading = computed(() => toolsStore.loading)
const error = computed(() => toolsStore.error)
</script> 