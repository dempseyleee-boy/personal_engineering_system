# 00_PERSONAL_ENGINEERING_OPTIMIZATION_PATH.md

## 1. 文件作用

本文件是“个人工程优化系统”的总入口文档。

它用于说明：

```text
这个系统是什么
为什么要建立这个系统
目录结构如何组织
每类文件的作用是什么
Agent 应该按什么流程读取和使用这些文件
如何从模板生成具体项目文件
任务开始前怎么准备上下文
任务结束后怎么沉淀信息
后续应该如何扩展
```

注意：

```text
本文件是系统总说明，不是具体项目的 PROJECT_CONTEXT。
具体项目背景应写入 context/PROJECT_CONTEXT.md。
```

---

# 2. 系统定位

本系统的目标是建立一套可复用的个人工程优化路径。

它不是从零开发一个新的 Agent，而是为现有 Agent 工具提供一套标准化文件体系，让 Agent 能够：

```text
1. 读取项目背景
2. 理解用户偏好
3. 读取历史决策
4. 生成当前任务上下文
5. 生成高质量 Prompt
6. 制定执行计划
7. 执行任务
8. 验证结果
9. 任务结束后沉淀经验
```

适用对象包括：

```text
Cursor Agent
Claude Code
Codex
OpenClaw
其他支持读取项目文件的 AI Agent
```

---

# 3. 当前优先方向

当前优先做的是：

```text
个人工程优化路径
```

当前暂不优先做的是：

```text
Agent 从零搭建路径
```

当前核心任务是：

```text
先建立一套可以放入项目中的规则文件、模板文件和上下文文件体系。
```

---

# 4. 核心思想

本系统由四层组成：

```text
Prompt Engineering
  ↓
Context Engineering
  ↓
Template / Skill System
  ↓
Task Execution & Reflection Loop
```

对应关系：

```text
Prompt Engineering：
解决“怎么把模糊需求变成高质量提示词”。

Context Engineering：
解决“Agent 在当前任务中应该看到什么上下文”。

Template System：
解决“如何根据模板生成标准项目文件”。

Skill System：
解决“Agent 应该按什么规则执行某类任务”。

Task Closing Loop：
解决“任务结束后哪些长期文件需要更新”。
```

---

# 5. 推荐目录结构

推荐最终目录结构如下：

```text
personal_engineering_system/
├── 00_PERSONAL_ENGINEERING_OPTIMIZATION_PATH.md
│
├── skills/
│   ├── PROMPT_ENGINEERING_SKILL.md
│   ├── CONTEXT_ENGINEERING_SKILL.md
│   ├── PROJECT_BOOTSTRAP_SKILL.md
│   └── VERIFICATION_SKILL.md
│
├── templates/
│   ├── 00_TEMPLATE_LIBRARY_INDEX.md
│   ├── context/
│   │   ├── 10_PROJECT_CONTEXT_TEMPLATE.md
│   │   ├── 11_USER_PREFERENCES_TEMPLATE.md
│   │   ├── 12_DECISION_LOG_TEMPLATE.md
│   │   ├── 13_TODO_TEMPLATE.md
│   │   ├── 14_TEST_COMMANDS_TEMPLATE.md
│   │   ├── 15_CHANGELOG_TEMPLATE.md
│   │   └── 16_AGENT_LESSONS_TEMPLATE.md
│   ├── task_context/
│   │   ├── 20_CONTEXT_PACKAGE_TEMPLATE.md
│   │   └── 21_TASK_CONTEXT_TEMPLATE.md
│   ├── closing/
│   │   └── 30_TASK_CLOSING_CHECKLIST.md
│   └── reports/
│       └── 40_RETROSPECTIVE_TEMPLATE.md
│
├── context/
│   ├── PROJECT_CONTEXT.md
│   ├── USER_PREFERENCES.md
│   ├── DECISION_LOG.md
│   ├── TODO.md
│   ├── TEST_COMMANDS.md
│   ├── CHANGELOG.md
│   └── AGENT_LESSONS.md
│
├── task_context/
│   ├── CONTEXT_PACKAGE.md
│   └── TASK_CONTEXT.md
│
└── reports/
    └── retrospectives/
        └── RETROSPECTIVE_YYYY_MM_DD.md
```

---

# 6. 各目录作用

## 6.1 skills/

`skills/` 用于存放 Agent 可读取的能力规则文件。

它告诉 Agent：

```text
面对某类任务时，应该按什么流程执行。
```

建议包含：

```text
PROMPT_ENGINEERING_SKILL.md
CONTEXT_ENGINEERING_SKILL.md
PROJECT_BOOTSTRAP_SKILL.md
VERIFICATION_SKILL.md
```

---

## 6.2 templates/

`templates/` 用于存放通用模板文件。

它们不记录具体项目内容，只提供结构。

Agent 读取这些模板后，根据当前项目实际情况生成：

```text
context/*.md
task_context/*.md
reports/*.md
```

模板文件不能写入具体项目事实。

---

## 6.3 context/

`context/` 用于存放具体项目的长期上下文文件。

这些文件由 Agent 根据 `templates/context/` 中的模板生成。

长期上下文文件用于记录：

```text
项目背景
用户偏好
历史决策
任务状态
验证命令
变更记录
Agent 经验教训
```

---

## 6.4 task_context/

`task_context/` 用于存放当前任务相关上下文。

它通常包含：

```text
CONTEXT_PACKAGE.md
TASK_CONTEXT.md
```

区别：

```text
CONTEXT_PACKAGE.md：
复杂任务开始前的完整上下文包。

TASK_CONTEXT.md：
单个任务的轻量任务说明。
```

---

## 6.5 reports/

`reports/` 用于存放阶段复盘、验证报告、实验报告等输出文件。

当前已规划：

```text
reports/retrospectives/
```

后续可扩展：

```text
reports/verification/
reports/experiments/
reports/task_reports/
```

---

# 7. 已完成文件

当前已经完成或生成过以下内容。

## 7.1 Skill 文件

```text
PROMPT_ENGINEERING_SKILL_FOR_AGENT.md
CONTEXT_ENGINEERING_SKILL_TEMPLATE.md
```

建议正式放置为：

```text
skills/PROMPT_ENGINEERING_SKILL.md
skills/CONTEXT_ENGINEERING_SKILL.md
```

---

## 7.2 模板库文件

当前模板库已整理为：

```text
templates/
├── 00_TEMPLATE_LIBRARY_INDEX.md
├── context/
│   ├── 10_PROJECT_CONTEXT_TEMPLATE.md
│   ├── 11_USER_PREFERENCES_TEMPLATE.md
│   ├── 12_DECISION_LOG_TEMPLATE.md
│   ├── 13_TODO_TEMPLATE.md
│   ├── 14_TEST_COMMANDS_TEMPLATE.md
│   ├── 15_CHANGELOG_TEMPLATE.md
│   └── 16_AGENT_LESSONS_TEMPLATE.md
├── task_context/
│   ├── 20_CONTEXT_PACKAGE_TEMPLATE.md
│   └── 21_TASK_CONTEXT_TEMPLATE.md
├── closing/
│   └── 30_TASK_CLOSING_CHECKLIST.md
└── reports/
    └── 40_RETROSPECTIVE_TEMPLATE.md
```

---

# 8. 模板编号规则

模板文件采用两位数编号：

```text
第一位：组优先级，从 0 开始
第二位：组内优先级，从 0 开始
```

组含义：

```text
0x：模板库入口
1x：长期上下文模板
2x：任务上下文模板
3x：任务结束检查模板
4x：报告 / 复盘模板
```

示例：

```text
00_TEMPLATE_LIBRARY_INDEX.md
10_PROJECT_CONTEXT_TEMPLATE.md
20_CONTEXT_PACKAGE_TEMPLATE.md
30_TASK_CLOSING_CHECKLIST.md
40_RETROSPECTIVE_TEMPLATE.md
```

---

# 9. Agent 标准启动流程

Agent 进入项目后，应按以下顺序执行：

```text
1. 读取 00_PERSONAL_ENGINEERING_OPTIMIZATION_PATH.md
2. 读取 templates/00_TEMPLATE_LIBRARY_INDEX.md
3. 读取 skills/PROMPT_ENGINEERING_SKILL.md
4. 读取 skills/CONTEXT_ENGINEERING_SKILL.md
5. 检查 context/ 目录是否存在长期上下文文件
6. 如果不存在，后续通过 PROJECT_BOOTSTRAP_SKILL.md 生成
7. 如果存在，则读取 PROJECT_CONTEXT.md、USER_PREFERENCES.md、DECISION_LOG.md、TODO.md、TEST_COMMANDS.md
8. 根据当前任务生成 task_context/CONTEXT_PACKAGE.md
9. 再根据 Prompt Skill 生成高质量任务 Prompt
10. 制定执行计划
11. 执行任务
12. 验证结果
13. 任务结束后执行 TASK_CLOSING_CHECKLIST
```

---

# 10. 项目初始化流程

当一个项目还没有 `context/` 文件时，后续应使用：

```text
skills/PROJECT_BOOTSTRAP_SKILL.md
```

进行初始化。

预期流程：

```text
读取 PROJECT_BOOTSTRAP_SKILL.md
  ↓
读取 templates/00_TEMPLATE_LIBRARY_INDEX.md
  ↓
扫描当前项目 README、目录结构、配置文件
  ↓
读取 templates/context/*.md
  ↓
生成 context/PROJECT_CONTEXT.md
  ↓
生成 context/USER_PREFERENCES.md
  ↓
生成 context/DECISION_LOG.md
  ↓
生成 context/TODO.md
  ↓
生成 context/TEST_COMMANDS.md
  ↓
按需生成 CHANGELOG.md 和 AGENT_LESSONS.md
  ↓
输出初始化报告
```

注意：

```text
PROJECT_BOOTSTRAP_SKILL.md 尚未生成，是后续最重要的待办之一。
```

---

# 11. 任务开始流程

每次复杂任务开始前，Agent 应执行：

```text
1. 读取 context/PROJECT_CONTEXT.md
2. 读取 context/USER_PREFERENCES.md
3. 读取 context/DECISION_LOG.md
4. 读取 context/TODO.md
5. 读取 context/TEST_COMMANDS.md
6. 根据任务类型读取 CHANGELOG.md 或 AGENT_LESSONS.md
7. 根据当前任务读取相关代码、文档、配置或数据
8. 使用 templates/task_context/20_CONTEXT_PACKAGE_TEMPLATE.md
9. 生成 task_context/CONTEXT_PACKAGE.md
10. 基于 CONTEXT_PACKAGE.md 生成任务执行 Prompt
```

对于轻量任务，可以使用：

```text
templates/task_context/21_TASK_CONTEXT_TEMPLATE.md
```

生成：

```text
task_context/TASK_CONTEXT.md
```

---

# 12. 任务执行流程

任务执行时，Agent 应遵守：

```text
1. 先确认任务目标
2. 明确本次做什么和不做什么
3. 明确输入和输出
4. 明确相关文件
5. 明确约束
6. 先制定计划
7. 再执行修改或生成
8. 执行后说明验证方式
9. 不确定时说明假设
10. 不编造不存在的文件、命令或结果
```

---

# 13. 任务结束流程

任务完成后，Agent 应读取：

```text
templates/closing/30_TASK_CLOSING_CHECKLIST.md
```

然后判断是否需要更新：

```text
context/PROJECT_CONTEXT.md
context/USER_PREFERENCES.md
context/DECISION_LOG.md
context/TODO.md
context/TEST_COMMANDS.md
context/CHANGELOG.md
context/AGENT_LESSONS.md
对应 Skill 文件
对应模板文件
```

任务结束时，Agent 应输出：

```text
1. 本次完成了什么
2. 未完成什么
3. 有哪些风险
4. 建议更新哪些长期文件
5. 哪些文件不需要更新
6. 下一步建议
```

---

# 14. 文件更新原则

## 14.1 不要因为读取文件就更新文件

```text
读取文件 = 获取上下文
产生长期影响 = 才需要更新文件
```

---

## 14.2 更新触发条件

```text
项目长期目标变化 → 更新 PROJECT_CONTEXT.md
用户长期偏好变化 → 更新 USER_PREFERENCES.md
重要决策产生 → 更新 DECISION_LOG.md
任务状态变化 → 更新 TODO.md
验证命令变化 → 更新 TEST_COMMANDS.md
文件发生变更 → 更新 CHANGELOG.md
Agent 发生可复用错误 → 更新 AGENT_LESSONS.md
任务开始前整理上下文 → 生成或更新 CONTEXT_PACKAGE.md
阶段性复盘 → 生成 RETROSPECTIVE 文件
```

---

# 15. 当前最重要的下一步

当前系统已经有：

```text
Prompt Skill
Context Skill
模板库
```

下一步最重要的是生成：

```text
skills/PROJECT_BOOTSTRAP_SKILL.md
```

原因：

```text
模板库已经存在，但还缺一个 Skill 来指挥 Agent 使用这些模板生成具体项目文件。
```

之后再生成：

```text
skills/VERIFICATION_SKILL.md
```

用于规范不同类型任务的验证标准。

---

# 16. 后续推荐路线

建议后续按以下顺序推进：

```text
1. 生成 PROJECT_BOOTSTRAP_SKILL.md
2. 生成 VERIFICATION_SKILL.md
3. 用一个测试项目试运行模板初始化流程
4. 根据试运行结果更新模板库
5. 增加 DOCUMENTATION_SKILL.md
6. 增加 EXPERIMENT_DESIGN_SKILL.md
7. 增加 WORKFLOW_ENGINEERING_SKILL.md
```

---

# 17. 当前系统的最小闭环

当前系统想要实现的最小闭环是：

```text
用户提出任务
  ↓
Agent 读取长期上下文
  ↓
Agent 生成 Context Package
  ↓
Agent 生成高质量 Prompt
  ↓
Agent 执行任务
  ↓
Agent 验证结果
  ↓
Agent 执行 Task Closing Checklist
  ↓
Agent 按需更新长期文件
```

---

# 18. 最终目标

本系统最终要实现：

```text
每一个项目都有清晰上下文
每一次任务都有明确任务包
每一次执行都有可验证结果
每一次完成都有经验沉淀
每一次失败都能更新规则
每一个模板都能复用
每一个 Agent 都能按文件规则工作
```

一句话总结：

> 个人工程优化系统的目标，是把用户的项目经验、提示词方法、上下文管理、任务执行、验证和复盘沉淀成一套可复用的 Agent 工作流体系。
