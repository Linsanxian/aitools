import { defineStore } from 'pinia'
import { ref } from 'vue'

const API_BASE_URL = 'http://localhost:5002/api'

export const useToolsStore = defineStore('tools', () => {
  const loading = ref(false)
  const error = ref<string | null>(null)
  const thinking = ref<string>('')
  const foodResponse = ref<string>('')

  // 获取食物推荐
  const getFoodRecommendation = async (preferences: {
    type: string
    dietary?: string[]
    spiciness?: string
    price?: string
  }) => {
    // 重置状态
    loading.value = true
    error.value = null
    thinking.value = ''
    foodResponse.value = ''

    try {
      const response = await fetch(`${API_BASE_URL}/food-recommendation`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream',
        },
        credentials: 'include',
        body: JSON.stringify(preferences)
      })

      console.log(response)

      if (!response.ok) {
        throw new Error('网络请求失败')
      }

      const reader = response.body?.getReader()
      if (!reader) {
        throw new Error('无法读取响应')
      }

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        // 将 Uint8Array 转换为字符串
        const chunk = new TextDecoder().decode(value)
        try {
          const data = JSON.parse(chunk)
          if (data.type === 'thinking') {
            thinking.value += data.content
          } else if (data.type === 'response') {
            // 当收到响应时，清空思考过程
            thinking.value = ''
            foodResponse.value += data.content
          }
        } catch (e) {
          console.error('解析响应失败:', e)
        }
      }

      return foodResponse.value
    } catch (e) {
      error.value = e instanceof Error ? e.message : '获取推荐失败'
      throw e
    } finally {
      loading.value = false
    }
  }

  // 获取笑话
  const getJoke = async () => {
    loading.value = true
    error.value = null
    try {
      // TODO: 调用后端API
      const jokes = [
        '为什么程序员总是分不清万圣节和圣诞节？因为 Oct 31 == Dec 25',
        '为什么程序员不喜欢户外活动？因为有太多的bug',
        '为什么程序员总是很冷？因为他们开着很多窗口',
        '为什么程序员总是很累？因为他们一直在处理异常',
        '为什么程序员总是很饿？因为他们一直在处理空值'
      ]
      
      return jokes[Math.floor(Math.random() * jokes.length)]
    } catch (e) {
      error.value = '获取笑话失败'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    thinking,
    response: foodResponse,
    getFoodRecommendation,
    getJoke
  }
}) 