<template>
  <div class="min-h-screen bg-gray-50 py-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">AI 工具集</h1>
        <p class="text-xl text-gray-600">探索智能工具，让生活更简单</p>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <ToolCard
          v-for="tool in tools"
          :key="tool.id"
          :title="tool.title"
          :description="tool.description"
          :icon="tool.icon"
          @click="navigateToTool(tool.id)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import ToolCard from '../components/ToolCard.vue'
import {
  SparklesIcon,
  FaceSmileIcon,
  QuestionMarkCircleIcon,
  ChatBubbleLeftRightIcon,
  DocumentTextIcon,
  PhotoIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()

const tools = [
  {
    id: 'what-to-eat',
    title: '今天吃什么？',
    description: '让AI帮你解决选择困难症',
    icon: QuestionMarkCircleIcon
  },
  {
    id: 'happy-moment',
    title: '开心一下',
    description: '获取一个有趣的笑话或故事',
    icon: FaceSmileIcon
  },
  {
    id: 'chat',
    title: '智能对话',
    description: '与AI助手进行自然对话',
    icon: ChatBubbleLeftRightIcon
  },
  {
    id: 'text-generator',
    title: '文本生成',
    description: '生成文章、故事或创意内容',
    icon: DocumentTextIcon
  },
  {
    id: 'image-generator',
    title: '图像生成',
    description: '将文字转换为图像',
    icon: PhotoIcon
  },
  {
    id: 'ai-assistant',
    title: 'AI助手',
    description: '全能AI助手，解决各种问题',
    icon: SparklesIcon
  }
]

const navigateToTool = (toolId: string) => {
  router.push(`/tool/${toolId}`)
}
</script> 