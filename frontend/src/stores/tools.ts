import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useToolsStore = defineStore('tools', () => {
  const loading = ref(false)
  const error = ref<string | null>(null)

  // 获取食物推荐
  const getFoodRecommendation = async (type: string) => {
    loading.value = true
    error.value = null
    try {
      // TODO: 调用后端API
      const foods = {
        '中餐': ['宫保鸡丁', '麻婆豆腐', '水煮鱼', '回锅肉', '糖醋排骨'],
        '西餐': ['意大利面', '披萨', '牛排', '汉堡', '沙拉'],
        '日料': ['寿司', '拉面', '天妇罗', '刺身', '咖喱饭'],
        '韩餐': ['石锅拌饭', '部队锅', '炸鸡', '烤肉', '泡菜汤'],
        '快餐': ['肯德基', '麦当劳', '必胜客', '汉堡王', '赛百味']
      }
      
      const randomFood = foods[type][Math.floor(Math.random() * foods[type].length)]
      return randomFood
    } catch (e) {
      error.value = '获取推荐失败'
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
    getFoodRecommendation,
    getJoke
  }
}) 