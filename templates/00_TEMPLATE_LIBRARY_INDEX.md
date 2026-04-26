# Template Library Index

## 1. 文件作用

本文件是模板库总入口，用于记录当前模板库中已有的模板文件、每个模板的用途、推荐放置位置、生成目标文件，以及 Agent 使用这些模板的基本流程。

注意：

```text
本文件是模板库说明文件，不是具体项目上下文文件。
它不绑定任何具体项目、具体技术方向或具体用户任务。
```

它主要回答：

```text
当前模板库有哪些模板？
每个模板用来生成什么文件？
这些模板应该放在哪里？
Agent 初始化项目时应该按什么顺序读取模板？
后续 Project Bootstrap Skill 应该如何调用这些模板？
```

---

# 2. 模板库定位

本模板库用于帮助 Agent 在任意项目中快速生成一套基础工程上下文文件。

它服务于以下目标：

```text
1. 标准化项目上下文文件
2. 标准化用户偏好文件
3. 标准化长期决策记录
4. 标准化任务清单
5. 标准化验证命令记录
6. 标准化任务开始前的 Context Package
7. 标准化任务结束后的 Closing Checklist
8. 为后续 Project Bootstrap Skill 提供模板输入
```

---

# 3. 推荐目录结构

建议模板库放置结构如下：

```text
templates/
├── 00_TEMPLATE_LIBRARY_INDEX.md
├── PROJECT_CONTEXT_TEMPLATE.md
├── USER_PREFERENCES_TEMPLATE.md
├── DECISION_LOG_TEMPLATE.md
├── TODO_TEMPLATE.md
├── TEST_COMMANDS_TEMPLATE.md
├── CONTEXT_PACKAGE_TEMPLATE.md
└── TASK_CLOSING_CHECKLIST.md
```

在具体项目中，Agent 可根据这些模板生成：

```text
context/
├── PROJECT_CONTEXT.md
├── USER_PREFERENCES.md
├── DECISION_LOG.md
├── TODO.md
└── TEST_COMMANDS.md

task_context/
└── CONTEXT_PACKAGE.md
```

---

# 4. 当前模板清单

## 4.1 PROJECT_CONTEXT_TEMPLATE.md

### 模板用途

用于生成：

```text
context/PROJECT_CONTEXT.md
```

### 目标文件作用

记录项目长期背景、长期目标、当前阶段、技术路线、关键环境和长期约束。

### 适合记录

```text
1. 项目是什么
2. 为什么做
3. 长期目标是什么
4. 当前阶段是什么
5. 技术路线是什么
6. 长期限制是什么
7. 什么时候需要更新本文件
```

### 不适合记录

```text
1. 单次任务细节
2. 临时聊天内容
3. 详细 TODO
4. 详细变更记录
5. 具体实验结果
```

---

## 4.2 USER_PREFERENCES_TEMPLATE.md

### 模板用途

用于生成：

```text
context/USER_PREFERENCES.md
```

### 目标文件作用

记录用户长期稳定偏好，包括回答风格、输出格式、技术路线偏好、禁止默认项、Agent 行为偏好和验证偏好。

### 适合记录

```text
1. 长期回答风格偏好
2. 长期输出格式偏好
3. 长期技术偏好
4. 长期禁止默认项
5. Agent 执行任务时应遵守的长期习惯
```

### 不适合记录

```text
1. 单次任务要求
2. 临时格式要求
3. 未经确认的猜测
4. 具体项目 TODO
5. 单次实验结果
```

---

## 4.3 DECISION_LOG_TEMPLATE.md

### 模板用途

用于生成：

```text
context/DECISION_LOG.md
```

### 目标文件作用

记录项目推进过程中已经确认的重要长期决策，避免后续任务反复推翻已确定方向。

### 适合记录

```text
1. 技术路线决策
2. 工具链选择决策
3. 文件组织方式决策
4. 工作流决策
5. 验证方式决策
6. 重要取舍决策
```

### 不适合记录

```text
1. 普通 TODO
2. 单次临时想法
3. 单次报错
4. 单次实验结果
5. 详细代码 diff
```

---

## 4.4 TODO_TEMPLATE.md

### 模板用途

用于生成：

```text
context/TODO.md
```

### 目标文件作用

记录项目任务状态，包括正在做、下一步、未来待办、阻塞、待确认、已完成和已放弃任务。

### 适合记录

```text
1. 当前正在执行的任务
2. 下一步任务
3. 未来待办任务
4. 已完成任务
5. 被阻塞任务
6. 待确认任务
7. 任务优先级和依赖关系
```

### 不适合记录

```text
1. 项目长期背景
2. 用户长期偏好
3. 详细技术决策
4. 详细文件变更记录
5. 实验完整数据
```

---

## 4.5 TEST_COMMANDS_TEMPLATE.md

### 模板用途

用于生成：

```text
context/TEST_COMMANDS.md
```

### 目标文件作用

记录项目可复用的运行命令、测试命令、构建命令、格式检查命令、验证命令和复现命令。

### 适合记录

```text
1. 环境准备命令
2. 依赖安装命令
3. 项目运行命令
4. 测试命令
5. 构建命令
6. Lint / Format / Type Check 命令
7. 文档生成命令
8. 手动验证步骤
9. 高风险命令说明
```

### 不适合记录

```text
1. 项目背景
2. 用户长期偏好
3. 技术决策解释
4. 详细 TODO
5. 与验证无关的长篇说明
```

---

## 4.6 CONTEXT_PACKAGE_TEMPLATE.md

### 模板用途

用于生成或刷新：

```text
task_context/CONTEXT_PACKAGE.md
```

### 目标文件作用

在每次复杂任务开始前，由 Agent 根据长期上下文文件生成当前任务专用的上下文包。

### 适合记录

```text
1. 当前任务
2. 项目背景摘要
3. 用户偏好摘要
4. 历史决策摘要
5. 当前状态
6. 相关文件
7. 相关命令
8. 关键约束
9. 输出要求与完成标准
```

### 不适合记录

```text
1. 长期完整知识库
2. 所有项目文件全文
3. 与当前任务无关的信息
4. 没有压缩的长日志
5. 无关历史聊天
```

---

## 4.7 TASK_CLOSING_CHECKLIST.md

### 模板用途

用于任务结束后检查哪些长期文件需要更新。

### 目标作用

帮助 Agent 在任务结束后判断：

```text
1. 是否需要更新 PROJECT_CONTEXT.md
2. 是否需要更新 USER_PREFERENCES.md
3. 是否需要更新 DECISION_LOG.md
4. 是否需要更新 TODO.md
5. 是否需要更新 TEST_COMMANDS.md
6. 是否需要更新 CHANGELOG.md
7. 是否需要更新 EXPERIMENT_LOG.md
8. 是否需要更新对应 Skill 文件
```

### 适合记录

```text
1. 任务完成检查规则
2. 文件更新触发条件
3. 哪些文件不需要更新
4. Task Closing Report 输出格式
```

### 不适合记录

```text
1. 具体项目任务内容
2. 具体项目长期背景
3. 具体用户偏好
4. 具体实验结果
```

---

# 5. 模板之间的关系

这些模板不是孤立文件，而是组成一个任务闭环。

```text
PROJECT_CONTEXT_TEMPLATE.md
USER_PREFERENCES_TEMPLATE.md
DECISION_LOG_TEMPLATE.md
TODO_TEMPLATE.md
TEST_COMMANDS_TEMPLATE.md
        ↓
生成长期上下文文件 context/*.md
        ↓
CONTEXT_PACKAGE_TEMPLATE.md
        ↓
生成 task_context/CONTEXT_PACKAGE.md
        ↓
Agent 执行任务
        ↓
TASK_CLOSING_CHECKLIST.md
        ↓
判断是否更新长期上下文文件
```

---

# 6. 推荐初始化流程

当 Agent 进入一个新项目时，推荐执行以下流程：

```text
1. 读取 templates/00_TEMPLATE_LIBRARY_INDEX.md
2. 读取 templates/PROJECT_CONTEXT_TEMPLATE.md
3. 读取 templates/USER_PREFERENCES_TEMPLATE.md
4. 读取 templates/DECISION_LOG_TEMPLATE.md
5. 读取 templates/TODO_TEMPLATE.md
6. 读取 templates/TEST_COMMANDS_TEMPLATE.md
7. 扫描当前项目 README、目录结构和配置文件
8. 根据实际情况生成 context/*.md
9. 读取 templates/CONTEXT_PACKAGE_TEMPLATE.md
10. 根据当前任务生成 task_context/CONTEXT_PACKAGE.md
11. 执行任务
12. 任务结束后读取 templates/TASK_CLOSING_CHECKLIST.md
13. 输出 Task Closing Report
14. 按需更新长期文件
```

---

# 7. 后续 Project Bootstrap Skill 的调用方式

后续可以新增一个 Skill：

```text
skills/PROJECT_BOOTSTRAP_SKILL.md
```

该 Skill 应使用本模板库完成项目初始化。

预期工作流：

```text
Agent 读取 PROJECT_BOOTSTRAP_SKILL.md
  ↓
Agent 读取 templates/00_TEMPLATE_LIBRARY_INDEX.md
  ↓
Agent 扫描当前项目
  ↓
Agent 读取所有必要模板
  ↓
Agent 生成 context/PROJECT_CONTEXT.md
  ↓
Agent 生成 context/USER_PREFERENCES.md
  ↓
Agent 生成 context/DECISION_LOG.md
  ↓
Agent 生成 context/TODO.md
  ↓
Agent 生成 context/TEST_COMMANDS.md
  ↓
Agent 生成初始化报告
```

注意：

```text
PROJECT_BOOTSTRAP_SKILL.md 暂未在本阶段生成。
本文件只记录模板库和未来 Bootstrap Skill 的调用关系。
```

---

# 8. 模板使用原则

Agent 使用模板时必须遵守：

```text
1. 模板文件只能提供结构，不能直接当成项目事实。
2. 生成具体项目文件时，必须根据真实项目信息填写。
3. 信息不足时，必须标记“待补充”或“暂无明确记录”。
4. 不得编造项目背景、命令、决策或用户偏好。
5. 不得把具体项目内容写回模板文件。
6. 模板更新应保持通用性。
7. 具体项目内容应写入 context/ 或 task_context/。
```

---

# 9. 模板库更新规则

当发生以下情况时，可以更新本模板库：

```text
1. 模板结构需要改进
2. 新增通用模板
3. 删除不再使用的模板
4. 某个模板职责边界需要调整
5. 多个项目复用后发现通用问题
6. Project Bootstrap Skill 需要新的模板输入
```

不应因为以下情况更新模板库：

```text
1. 某个具体项目产生临时需求
2. 某个具体项目新增 TODO
3. 某个具体项目修改技术路线
4. 某个具体项目新增测试命令
5. 某个具体项目产生实验结果
```

这些内容应写入具体项目的：

```text
context/
task_context/
docs/
reports/
```

而不是写入模板库。

---

# 10. 当前模板库状态

当前模板库 V1 包含：

```text
已完成：
- PROJECT_CONTEXT_TEMPLATE.md
- USER_PREFERENCES_TEMPLATE.md
- DECISION_LOG_TEMPLATE.md
- TODO_TEMPLATE.md
- TEST_COMMANDS_TEMPLATE.md
- CONTEXT_PACKAGE_TEMPLATE.md
- TASK_CLOSING_CHECKLIST.md

待生成：
- PROJECT_BOOTSTRAP_SKILL.md
- 其他可选高级模板
```

---

# 11. 后续可选模板

后续可根据需要添加：

```text
CHANGELOG_TEMPLATE.md
EXPERIMENT_LOG_TEMPLATE.md
AGENT_LESSONS_TEMPLATE.md
RETROSPECTIVE_TEMPLATE.md
VERIFICATION_SKILL_TEMPLATE.md
DOCUMENTATION_SKILL_TEMPLATE.md
WORKFLOW_TEMPLATE.md
```

这些属于扩展模板，不是 V1 必须文件。

---

# 12. 最终原则

```text
模板库负责提供结构。
具体项目文件负责记录事实。
Agent Skill 负责调用模板并生成项目文件。
```

一句话总结：

> 本模板库是 Agent 初始化项目上下文系统的基础输入。它不保存具体项目事实，只提供可复用的文件结构和生成规范。
