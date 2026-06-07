# Vibe Coding 实战任务方案（2～3 小时）

> **Class19 配套练习**

---

## 一、课程目标

本节课的目标只有一句话：

> **在 2～3 小时内，借助 AI，从零做出一个「别人 clone 下来能跑」的 GitHub 小项目。**

---

## 二、能力与预期

### 2.1 本课你将练到的能力

1. **拆需求**：把模糊想法拆成 3～5 个可执行小目标
2. **写 Prompt**：向 AI 描述约束（语言、框架、输入输出、时间上限）
3. **快速验证**：每 20～30 分钟必须有一次「能跑」的里程碑
4. **工程习惯**：`README`、依赖文件、`.gitignore`、最小测试
5. **GitHub 交付**：初始化仓库、提交、推送、写项目说明

### 2.2 本课不追求什么

- ❌ 不追求代码完美、架构宏大
- ❌ 不追求覆盖所有边界情况
- ❌ 不追求 UI 精美（除非选了前端方向且时间够）
- ✅ **追求：能演示、能复现、能说清楚做了什么**

---

## 三、参考项目方向

原则：**范围小到能做完，价值大到能写进 README**。


### 方向 C：数据处理小工具（零基础友好）

**一句话**：读入一份 CSV，完成清洗/统计/导出，全程命令行。

**适合谁**：数据分析入门、不想碰 Web 的学员

**题目示例**：

3. **个人记账**：读 `expenses.csv`，按类别汇总当月支出

**最小可运行（MVP）**：

- `python main.py --input data/sample.csv`
- 终端打印汇总结果
- 仓库自带 **小样本 CSV**（≤100 行）

**2 小时版**：1 种统计 + 1 种导出

**3 小时版**：+ 简单 matplotlib 图表保存为 PNG

**技术建议**：Python + pandas

**验收亮点**：样本数据随仓库提供，无需学员自己找数据

---

---


**禁止选题（超时预警）**：

- 完整用户登录系统、支付、微服务集群
- 需要申请 API Key 且审核耗时的云服务（除非课前已备好 Key）
- 训练大模型、爬取需登录的社交媒体

---

## 五、标准仓库结构

所有方向通用：

```text
your-project/
├── README.md           # 必需：项目说明、安装、运行、截图
├── requirements.txt    # 或 pyproject.toml
├── .gitignore          # 忽略 .venv、__pycache__、.env
├── .env.example        # 若有配置项（不要提交真实 .env）
├── src/                # 或根目录 main.py（小项目可扁平）
│   └── ...
├── data/               # 样本数据（方向 C/D）
│   └── sample.csv
├── tests/              # 3 小时版建议有 1 个测试
│   └── test_basic.py
└── LICENSE             # 可选：MIT
```

---

## 六、Vibe Coding 工作流

### Step 1：用 AI 写「项目一页纸」（10 min）

把下面模板发给 Cursor / Codex / CC，**填好你的方向**：

```markdown
我要在 2.5 小时内完成一个可运行的 GitHub 项目。

【方向】：（A/B/C/D）
【具体题目】：（例：Ollama 命令行问答工具）
【技术栈】：Python 3.10+，只用 requests + argparse，不要 Django
【MVP 范围】：
1. ...
2. ...
3. ...
【不做】：登录、数据库、前端框架
【交付】：requirements.txt、README、main 入口

请输出：
1. 目录结构
2. 分 3 个阶段的实现顺序（每阶段约 40 分钟）
3. 每个文件的职责一句话说明
不要一次生成全部代码，先给计划。
```

### Step 2：按阶段要代码，不要一次要完

**阶段 1 Prompt（搭骨架）**：

```text
按刚才的计划实现阶段 1：只创建目录、requirements.txt、入口文件。
要求：运行 python main.py --help 不报错。
不要实现业务逻辑。改完后告诉我怎么验证。
```

**阶段 2 Prompt（主流程）**：

```text
实现阶段 2 的核心功能：[具体描述 happy path]。
保持单文件或少文件，优先跑通。
如果依赖 Ollama，请写 health check 和友好报错。
```

**阶段 3 Prompt（文档与健壮）**：

```text
请帮我写 README.md（中文），包含：项目介绍、环境要求、安装步骤、
运行示例、常见问题。并补 .gitignore 和 .env.example（如需要）。
```

### Step 3：报错时这样问

```text
我运行 `python main.py --input data/sample.csv` 报错如下：

【完整报错粘贴】

【我期望的行为】
【相关文件】@main.py @utils.py

请最小改动修复，并说明原因。不要重构无关代码。
```

### Step 4：GitHub 推送（最后 20 min 必做）

```powershell
git init
git add .
git commit -m "feat: initial runnable MVP for [项目名]"
# 在 GitHub 新建仓库后：
git remote add origin https://github.com/你的用户名/仓库名.git
git branch -M main
git push -u origin main
```

---

## 七、README 最低要求

学员 README（说明报告）**必须包含**以下 6 块（可让 AI 按此生成）：

1. **项目名称 + 一句话介绍**
2. **功能列表**（3～5 条，与 MVP 一致）
3. **环境要求**（Python 版本、是否需 Ollama 等）
4. **安装步骤**（复制即用的命令）
5. **运行示例**（含预期输出或截图）
6. **项目结构说明**（主要文件职责）

**额外要求**：

- 附演示相关截图
- 说明**主要功能 + 实现方式**
