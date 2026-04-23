# 🦞 智慧龙虾开发工作流指南

## 快速开始

### 1. 日常开发流程

```bash
# 1. 写代码...

# 2. 格式化代码
python scripts/dev_workflow.py format

# 3. 代码检查
python scripts/dev_workflow.py lint

# 4. 运行测试
python scripts/dev_workflow.py test

# 5. 一键检查全部（推荐）
python scripts/dev_workflow.py check

# 6. 推送到 GitHub
python scripts/dev_workflow.py sync
```

### 2. 同步到主机

**虚拟机端（写完代码后）：**
```bash
python scripts/dev_workflow.py sync
# 输入提交信息，例如："添加微信连接器"
```

**主机端（获取最新代码）：**
```bash
cd smart-lobster
git pull origin main
```

## 命令详解

| 命令 | 说明 | 使用场景 |
|------|------|---------|
| `format` | 代码格式化 (black) | 代码写完后 |
| `lint` | 代码风格检查 (flake8) | 提交前 |
| `test` | 运行测试 (pytest) | 提交前 |
| `check` | 格式化+检查+测试 | 提交前（推荐） |
| `push` | Git 提交并推送 | 手动控制时 |
| `sync` | check + push 组合 | 日常开发（最推荐） |

## 项目结构

```
smart-lobster/
├── .github/workflows/    # CI/CD 配置
├── connectors/           # 渠道连接器（微信、钉钉）
├── core/                 # 核心引擎
│   ├── message-router/   # 消息路由
│   └── analysis-engine/  # AI 分析
├── docs/                 # 文档
├── frontend/             # 前端界面
├── scripts/              # 工具脚本
│   └── dev_workflow.py   # ⭐ 开发工作流
├── smart_lobster/        # 主包
│   ├── __init__.py
│   └── server.py         # 服务入口
├── tests/                # 测试
├── .env.example          # 环境变量模板
├── Makefile              # 快捷命令
├── pyproject.toml        # 工具配置
└── requirements.txt      # 依赖
```

## 代码规范

### Python 代码风格
- 使用 **black** 格式化，行宽 100
- 使用 **flake8** 检查
- 所有函数添加类型注解
- 公共函数必须写 docstring

### Git 提交规范
```
类型: 简短描述

详细说明（可选）

类型说明：
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式（不影响功能）
- refactor: 重构
- test: 测试相关
- chore: 构建/工具相关

示例：
feat: 添加微信消息接收接口
fix: 修复百度API token过期问题
docs: 更新部署文档
```

## 开发环境配置

### 1. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 填入你的配置
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 验证安装
```bash
python scripts/dev_workflow.py check
```

## 常用快捷命令

### 使用 Makefile
```bash
make install      # 安装依赖
make format       # 格式化
make lint         # 检查
make test         # 测试
make check        # 全部检查
make clean        # 清理缓存
make run          # 运行服务
```

### 使用 Python 脚本
```bash
python -m smart_lobster.server          # 启动服务
python core/fraud_detector.py           # 测试反诈模块
python scripts/get_baidu_token.py       # 获取百度token
```

## CI/CD 流程

每次推送到 GitHub 会自动运行：
1. ✅ 代码格式化检查
2. ✅ flake8 风格检查
3. ✅ pytest 单元测试
4. ✅ 覆盖率报告

## 故障排除

### 问题：black 格式化失败
```bash
# 手动运行
python -m black . --line-length 100
```

### 问题：flake8 报错太多
```bash
# 查看具体问题
python -m flake8 . --max-line-length 100
```

### 问题：测试失败
```bash
# 详细输出
python -m pytest tests/ -v --tb=long
```

### 问题：Git 推送失败
```bash
# 检查远程仓库
git remote -v

# 重新设置远程（如果需要）
git remote set-url origin https://github.com/Lihgttt/smart-lobster.git
```

## 团队协作

### 分支策略
```bash
# 开发新功能
git checkout -b feature/wechat-connector
# ... 开发 ...
git push origin feature/wechat-connector
# 创建 Pull Request

# 修复bug
git checkout -b fix/api-timeout
# ... 修复 ...
git push origin fix/api-timeout
```

### 代码审查清单
- [ ] 代码已通过 `make check`
- [ ] 新增功能有对应测试
- [ ] 文档已更新
- [ ] 提交信息符合规范

---

**💡 提示：日常使用只需要记住 `python scripts/dev_workflow.py sync`**