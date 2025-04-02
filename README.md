# 卡片展示网站

这是一个使用Flask、Vue和MySQL构建的卡片展示网站，支持用户注册、登录和卡片管理功能。

## 功能特点

- 用户注册和登录
- 流式卡片展示
- 创建新卡片
- 响应式设计

## 技术栈

- 后端：Flask + MySQL
- 前端：Vue 3 + Element Plus
- 数据库：MySQL

## 安装说明

### 后端设置

1. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置数据库：
- 创建MySQL数据库：`aitools`
- 修改 `app.py` 中的数据库连接信息

4. 运行后端服务：
```bash
python app.py
```

### 前端设置

1. 进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
```

3. 运行开发服务器：
```bash
npm run dev
```

## 使用说明

1. 访问 http://localhost:3000
2. 注册新账号或登录已有账号
3. 在首页查看卡片列表
4. 点击"创建新卡片"按钮添加新卡片

## 注意事项

- 确保MySQL服务已启动
- 后端服务运行在 http://localhost:5000
- 前端服务运行在 http://localhost:3000 