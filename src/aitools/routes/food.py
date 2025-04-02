from flask import Blueprint, request, Response, stream_with_context
import json
from openai import OpenAI
import re
from src.aitools.config import Config

food_bp = Blueprint('food', __name__, url_prefix='/api/')

client = OpenAI(api_key=Config.DASHSCOPE_API_KEY,
                base_url=Config.DASHSCOPE_BASE_URL)


def generate_food_recommendation(preferences):
    """生成食物推荐"""
    # 构建提示词
    prompt = f"""作为一个专业的美食推荐专家，请根据以下用户偏好推荐合适的美食：

用户偏好：
- 菜系：{preferences['type']}
- 饮食限制：{', '.join(preferences.get('dietary', [])) if preferences.get('dietary') else '无'}
- 辣度偏好：{preferences.get('spiciness', '不限')}
- 价格区间：{preferences.get('price', '不限')}

请分两个步骤回答，并使用特定格式：

1. 首先用 <think> 标签包裹你的思考过程
2. 然后给出具体推荐（使用 Markdown 格式）：

示例格式：
<think>
[在这里写下你的分析思考过程]
</think>

## 🍽️ 推荐菜品

### 📝 菜品描述
[菜品的详细描述]

### ✨ 推荐理由
[推荐理由]

### 💰 价格参考
[价格范围]

### 🏠 推荐餐厅
[餐厅推荐]
"""

    # 创建流式响应
    stream = client.chat.completions.create(
        model="qwq-32b",
        messages=[
            {"role": "system", "content": "你是一个专业的美食推荐专家，善于根据用户偏好推荐合适的食物。你的回答应该既专业又温暖，让用户感受到你的专业性和关心。"},
            {"role": "user", "content": prompt}
        ],
        stream=True
    )

    buffer = ""
    in_thinking = False
    thinking_content = ""

    for chunk in stream:
        if not chunk.choices:
            continue
        
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            buffer += content

            # 检查是否包含完整的思考标签
            think_match = re.search(r'<think>(.*?)</think>', buffer, re.DOTALL)
            
            if think_match and not in_thinking:
                # 发现完整的思考内容
                in_thinking = True
                thinking_content = think_match.group(1).strip()
                yield json.dumps({
                    "type": "thinking",
                    "content": thinking_content
                }) + "\n"
                # 从 buffer 中移除思考内容
                buffer = buffer.replace(think_match.group(0), '').strip()
            elif '<think>' in buffer and not in_thinking:
                # 开始收集思考内容
                in_thinking = True
            elif '</think>' in buffer and in_thinking:
                # 结束思考内容
                think_end_pos = buffer.find('</think>')
                thinking_content = buffer[:think_end_pos].replace('<think>', '').strip()
                yield json.dumps({
                    "type": "thinking",
                    "content": thinking_content
                }) + "\n"
                # 从 buffer 中移除思考内容
                buffer = buffer[think_end_pos + 8:].strip()
                in_thinking = False
            elif in_thinking:
                # 继续收集思考内容
                yield json.dumps({
                    "type": "thinking",
                    "content": content
                }) + "\n"
            else:
                # 发送响应内容
                yield json.dumps({
                    "type": "response",
                    "content": content
                }) + "\n"

@food_bp.route('/food-recommendation', methods=['POST'])
def food_recommendation():
    """处理食物推荐请求"""
    try:
        preferences = request.get_json()
        
        # 验证必要参数
        if not preferences or 'type' not in preferences:
            return Response(
                json.dumps({"error": "缺少必要参数"}),
                status=400,
                mimetype='application/json'
            )

        # 返回流式响应
        return Response(
            stream_with_context(generate_food_recommendation(preferences)),
            mimetype='text/event-stream'
        )

    except Exception as e:
        return Response(
            json.dumps({"error": str(e)}),
            status=500,
            mimetype='application/json'
        )
