# Context Package Template

## 1. 文件作用

本模板用于任务开始前，由 Agent 根据长期上下文文件生成本次任务专用的 `task_context/CONTEXT_PACKAGE.md`。

它的目标是：

```text
让 Agent 在执行任务前先看对上下文、明确目标、识别约束、知道相关文件和验证标准。
```

Context Package 不是长期知识库，而是每次任务的临时上下文包。

---

# 2. 生成规则

Agent 每次处理复杂任务前，必须：

```text
1. 读取 skills/CONTEXT_ENGINEERING_SKILL.md
2. 读取 skills/PROMPT_ENGINEERING_SKILL.md
3. 读取 context/PROJECT_CONTEXT.md
4. 读取 context/USER_PREFERENCES.md
5. 读取 context/DECISION_LOG.md
6. 读取 context/TODO.md
7. 根据任务类型读取 TEST_COMMANDS.md / CHANGELOG.md / EXPERIMENT_LOG.md
8. 根据任务需要读取相关源码、文档、配置或数据文件
9. 按本模板生成 task_context/CONTEXT_PACKAGE.md
10. 再基于 Context Package 生成高质量任务 Prompt
```

对于简单解释类问题，可以不生成完整 Context Package，但仍应遵守用户偏好和高优先级规则。

---

# 3. Context Package 标准模板

```markdown
# Context Package

## 1. 当前任务

### 用户原始需求

```text
【填写用户这次提出的原始任务】
```

### 任务类型

```text
【代码生成 / 代码修复 / 项目优化 / 文档整理 / 实验设计 / 论文写作 / FPGA部署 / Prompt优化 / Skill生成 / 其他】
```

### 本次任务目标

```text
【明确本次最终要交付什么】
```

### 本次任务边界

```text
本次要做：
1. 【事项 1】
2. 【事项 2】
3. 【事项 3】

本次不做：
1. 【不做事项 1】
2. 【不做事项 2】
```

---

## 2. 项目背景摘要

从 `context/PROJECT_CONTEXT.md` 中提取与本次任务相关的信息。

```text
项目名称：
【填写项目名称】

项目长期目标：
【填写长期目标】

当前阶段：
【填写当前阶段】

技术路线：
【填写技术路线】

软硬件环境：
【填写环境】

长期固定限制：
【填写固定限制】
```

如果没有 `PROJECT_CONTEXT.md`，写：

```text
未找到 PROJECT_CONTEXT.md，需要先创建项目背景文件，或基于当前对话临时推断项目背景。
```

---

## 3. 用户偏好摘要

从 `context/USER_PREFERENCES.md` 中提取与本次任务相关的偏好。

```text
回答风格偏好：
【例如：直接讲原理、流程、例子，少寒暄】

技术偏好：
【例如：FPGA 方案不默认 HLS，优先纯 Verilog】

输出格式偏好：
【例如：Markdown、表格、步骤、文件】

Agent 行为偏好：
【例如：先读项目结构，再制定计划，不要一上来改代码】
```

如果没有 `USER_PREFERENCES.md`，写：

```text
未找到 USER_PREFERENCES.md，本次仅依据当前用户指令执行。
```

---

## 4. 历史决策摘要

从 `context/DECISION_LOG.md` 中提取与本次任务相关的历史决策。

```text
相关决策 1：
- 日期：
- 决策：
- 原因：
- 影响：

相关决策 2：
- 日期：
- 决策：
- 原因：
- 影响：
```

如果没有相关历史决策，写：

```text
暂无与本次任务直接相关的历史决策。
```

如果历史决策和当前用户指令冲突，写：

```text
发现上下文冲突：
- 冲突来源：
- 冲突内容：
- 采用规则：
当前用户明确指令 > 项目规则文件 > 当前任务文件 > PROJECT_CONTEXT > USER_PREFERENCES > DECISION_LOG > Skill 文件 > README/历史文档 > 旧笔记。
- 本次采用：
【说明采用哪个版本】
```

---

## 5. 当前状态

从 `context/TODO.md`、`context/CHANGELOG.md`、`context/EXPERIMENT_LOG.md` 中提取当前状态。

```text
当前已完成：
1. 【已完成事项 1】
2. 【已完成事项 2】

当前正在做：
1. 【正在做事项 1】

当前阻塞点：
1. 【阻塞点 1】

下一步计划：
1. 【下一步 1】
2. 【下一步 2】
```

如果缺少状态文件，写：

```text
未找到完整状态文件，本次根据当前对话临时判断项目状态。
```

---

## 6. 相关文件

列出本次任务需要读取、参考、修改或生成的文件。

```text
需要读取：
1. 【文件路径】 - 【为什么需要读取】
2. 【文件路径】 - 【为什么需要读取】

需要修改：
1. 【文件路径】 - 【为什么需要修改】

需要生成：
1. 【文件路径】 - 【生成目的】

可选参考：
1. 【文件路径】 - 【参考价值】
```

如果相关文件不存在，写：

```text
未找到以下文件：
1. 【文件路径】

处理方式：
- 【创建新文件 / 请求用户提供 / 暂时跳过 / 基于当前信息生成草案】
```

---

## 7. 相关命令

从 `context/TEST_COMMANDS.md` 中提取本次任务需要使用的命令。

```bash
# 安装依赖
【命令】

# 运行项目
【命令】

# 测试
【命令】

# 格式检查
【命令】

# 构建 / 仿真 / 实验复现
【命令】
```

如果本次任务不是代码任务，写：

```text
本次任务不涉及代码运行或测试命令。
```

如果暂无验证命令，写：

```text
暂无明确验证命令，本次任务需要在输出中补充可行的验证方式。
```

---

## 8. 关键约束

本次任务必须遵守：

```text
1. 【约束 1】
2. 【约束 2】
3. 【约束 3】
```

本次任务禁止：

```text
1. 【禁止事项 1】
2. 【禁止事项 2】
3. 【禁止事项 3】
```

优先级：

```text
1. 【最高优先级事项】
2. 【次优先级事项】
3. 【低优先级事项】
```

冲突处理规则：

```text
当前用户明确指令 > 项目根目录规则文件 > 当前任务相关文件 > PROJECT_CONTEXT > USER_PREFERENCES > DECISION_LOG > Skill 文件 > README/历史文档 > 旧笔记。
```

---

## 9. 输出要求与完成标准

### 最终输出格式

```text
【Markdown / 代码 / 表格 / JSON / 文件 / 报告 / PPT / 其他】
```

### 最终交付物

```text
1. 【交付物 1】
2. 【交付物 2】
3. 【交付物 3】
```

### 完成标准

```text
1. 【标准 1】
2. 【标准 2】
3. 【标准 3】
```

### 验证方法

```text
1. 【如何检查输出是否正确】
2. 【如何运行测试】
3. 【如何确认没有破坏现有内容】
```

### 风险点

```text
1. 【风险 1】
2. 【风险 2】
3. 【风险 3】
```
```

---

# 4. Agent 生成 Context Package 后的下一步

生成 `task_context/CONTEXT_PACKAGE.md` 后，Agent 必须继续执行：

```text
1. 基于 Context Package 总结任务理解
2. 基于 PROMPT_ENGINEERING_SKILL.md 生成高质量任务 Prompt
3. 制定执行计划
4. 明确将读取/修改/生成哪些文件
5. 执行任务
6. 验证结果
7. 任务结束后执行 TASK_CLOSING_CHECKLIST.md
```

---

# 5. Context Package 质量检查

Agent 生成 Context Package 后，应检查：

```text
1. 是否明确当前任务？
2. 是否包含项目背景？
3. 是否包含用户偏好？
4. 是否提取相关历史决策？
5. 是否说明当前状态？
6. 是否列出相关文件？
7. 是否列出相关命令？
8. 是否明确关键约束？
9. 是否明确输出要求和完成标准？
10. 是否标记上下文冲突或不确定点？
```

如果任一关键项缺失，Agent 必须在 Context Package 中说明：

```text
缺失项：
原因：
临时假设：
是否需要用户补充：
```

---

# 6. 最终原则

```text
Context Package 不是复制所有资料。
Context Package 是把当前任务需要的信息压缩成一份可执行上下文。
```

目标：

> 让 Agent 在开始执行任务前，已经知道“我要做什么、为什么做、基于什么做、不能做什么、怎么判断完成”。
