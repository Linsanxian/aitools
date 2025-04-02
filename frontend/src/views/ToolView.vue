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
            <!-- 菜系选择 -->
            <div class="space-y-2">
              <label class="text-sm font-medium text-gray-700">选择菜系</label>
              <div class="flex flex-wrap gap-2">
                <button 
                  v-for="type in foodTypes" 
                  :key="type"
                  @click="preferences.type = type"
                  :class="[
                    'btn',
                    preferences.type === type ? 'btn-primary' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  ]"
                >
                  {{ type }}
                </button>
              </div>
            </div>

            <!-- 饮食限制 -->
            <div class="space-y-2">
              <label class="text-sm font-medium text-gray-700">饮食限制（可多选）</label>
              <div class="flex flex-wrap gap-2">
                <button 
                  v-for="restriction in dietaryRestrictions" 
                  :key="restriction"
                  @click="toggleDietary(restriction)"
                  :class="[
                    'btn',
                    preferences.dietary?.includes(restriction) ? 'btn-primary' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  ]"
                >
                  {{ restriction }}
                </button>
              </div>
            </div>

            <!-- 辣度选择 -->
            <div class="space-y-2">
              <label class="text-sm font-medium text-gray-700">辣度偏好</label>
              <div class="flex flex-wrap gap-2">
                <button 
                  v-for="level in spiceLevels" 
                  :key="level"
                  @click="preferences.spiciness = level"
                  :class="[
                    'btn',
                    preferences.spiciness === level ? 'btn-primary' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  ]"
                >
                  {{ level }}
                </button>
              </div>
            </div>

            <!-- 价格区间 -->
            <div class="space-y-2">
              <label class="text-sm font-medium text-gray-700">价格区间</label>
              <div class="flex flex-wrap gap-2">
                <button 
                  v-for="range in priceRanges" 
                  :key="range"
                  @click="preferences.price = range"
                  :class="[
                    'btn',
                    preferences.price === range ? 'btn-primary' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  ]"
                >
                  {{ range }}
                </button>
              </div>
            </div>

            <!-- 思考过程 -->
            <div v-if="thinking" 
                 class="p-4 bg-primary-50 rounded-lg border border-primary-100 transition-all duration-300"
                 :class="{'max-h-[500px] overflow-y-auto': showThinking, 'max-h-12 overflow-hidden': !showThinking && response}"
                 @click="showThinking = !showThinking"
            >
              <div class="flex items-center justify-between mb-2 cursor-pointer">
                <div class="flex items-center space-x-2">
                  <div class="w-4 h-4 rounded-full bg-primary-200" :class="{'animate-pulse': !response}"></div>
                  <h3 class="text-sm font-medium text-primary-700">AI 思考过程</h3>
                </div>
                <button v-if="response" 
                        class="text-primary-600 text-sm hover:text-primary-700"
                        @click.stop="showThinking = !showThinking"
                >
                  {{ showThinking ? '收起' : '展开' }}
                </button>
              </div>
              <p class="text-sm text-primary-600 whitespace-pre-line">{{ thinking }}</p>
            </div>

            <!-- 推荐结果 -->
            <div v-if="response" 
                 class="p-6 bg-white rounded-lg border border-gray-200 shadow-sm"
                 :class="{'mt-2': thinking}"
            >
              <div class="prose prose-primary max-w-none">
                <div class="space-y-4 whitespace-pre-line" v-html="formatResponse(response)"></div>
              </div>
            </div>

            <button 
              @click="getFoodRecommendation" 
              class="btn btn-primary w-full"
              :disabled="loading || !preferences.type"
            >
              {{ loading ? '思考中...' : '获取推荐' }}
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
import { marked } from 'marked'

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
const dietaryRestrictions = ['素食', '不吃辣', '不吃海鲜', '清淡', '低脂']
const spiceLevels = ['不辣', '微辣', '中辣', '重辣']
const priceRanges = ['经济', '适中', '高端']

const preferences = ref({
  type: '',
  dietary: [] as string[],
  spiciness: '',
  price: ''
})

const toggleDietary = (restriction: string) => {
  const index = preferences.value.dietary?.indexOf(restriction) ?? -1
  if (index === -1) {
    preferences.value.dietary = [...(preferences.value.dietary || []), restriction]
  } else {
    preferences.value.dietary = preferences.value.dietary?.filter(r => r !== restriction)
  }
}

const getFoodRecommendation = async () => {
  try {
    await toolsStore.getFoodRecommendation(preferences.value)
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
const thinking = computed(() => toolsStore.thinking)
const response = computed(() => toolsStore.response)

const formatResponse = (text: string) => {
  // 使用 marked 将 Markdown 转换为 HTML
  const html = marked.parse(text, {
    gfm: true,
    breaks: true
  }) as string
  
  // 添加自定义样式
  return html
    .replace(/<h2>/g, '<h2 class="text-xl font-bold text-primary-600 mb-4">')
    .replace(/<h3>/g, '<h3 class="text-lg font-semibold text-gray-700 mt-4">')
    .replace(/<p>/g, '<p class="text-gray-600 ml-4 my-2">')
}

// 添加控制思考过程显示的状态
const showThinking = ref(true)
</script>

<style>
.prose h2 {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
}

.prose h3 {
  margin-top: 1.25rem;
  margin-bottom: 0.75rem;
}

.prose p {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}

.prose ul {
  margin-left: 1.5rem;
  list-style-type: disc;
}

.prose li {
  margin-top: 0.25rem;
  margin-bottom: 0.25rem;
}
</style> 