# AGENT_LESSONS_TEMPLATE.md

## 1. 模板作用

本模板用于生成 Agent 经验教训记录文件：

```text
context/AGENT_LESSONS.md
```

该文件用于记录 Agent 在项目执行过程中出现的问题、错误、误判、规则缺口，以及后续应如何避免。

它主要回答：

```text
Agent 这次哪里做错了？
为什么会错？
是 Prompt 问题、Context 问题、Skill 问题、验证问题，还是工具使用问题？
以后应该怎么避免？
需要更新哪个规则文件或模板？
```

注意：

```text
本文件是通用模板，不绑定任何具体项目。
使用时，Agent 应根据当前项目实际情况，把【占位内容】替换为真实经验教训。
不要在模板中写入具体项目名称、具体技术路线或具体领域内容。
```

---

# 2. 使用方式

当 Agent 初始化一个项目，或用户要求建立 Agent 经验教训记录时，应读取本模板，并生成：

```text
context/AGENT_LESSONS.md
```

每次任务结束后，Agent 应根据 `templates/TASK_CLOSING_CHECKLIST.md` 判断是否需要更新本文件。

如果本次任务中 Agent 出现以下情况，通常应该更新本文件：

```text
1. 没有读取上下文就开始执行
2. 忽略用户明确要求
3. 忽略用户长期偏好
4. 编造不存在的文件、命令或结论
5. 修改了无关文件
6. 没有验证就声称完成
7. 没有识别上下文冲突
8. 输出过于泛泛
9. 任务边界理解错误
10. 工具调用顺序错误
11. 没有按模板生成项目文件
12. 没有按任务结束清单更新长期文件
```

---

# 3. 什么内容应该写入 AGENT_LESSONS.md

应该写入：

```text
1. Agent 出错的具体表现
2. 错误发生的任务场景
3. 错误原因分析
4. 应该遵守但没有遵守的规则
5. 需要新增或修改的规则
6. 需要更新的 Skill 文件
7. 需要更新的模板文件
8. 后续避免方法
9. 是否需要用户确认
10. 是否已经修复
```

不应该写入：

```text
1. 普通 TODO
2. 项目长期背景
3. 用户长期偏好
4. 详细代码 diff
5. 完整实验数据
6. 无明确复用价值的临时闲聊
7. 对 Agent 的情绪化评价但没有可执行改进
```

这些内容应分别放入：

```text
context/TODO.md
context/PROJECT_CONTEXT.md
context/USER_PREFERENCES.md
context/CHANGELOG.md
context/EXPERIMENT_LOG.md
task_context/CONTEXT_PACKAGE.md
```

---

# 4. Agent 问题分类

建议使用以下分类：

```text
Context Error：上下文读取、压缩、组装错误
Prompt Error：提示词生成或任务表达错误
Planning Error：任务计划错误
Execution Error：执行步骤错误
Tool Error：工具选择或调用错误
Verification Error：验证缺失或验证错误
File Operation Error：文件读写、修改、删除错误
Hallucination Error：编造信息、文件、命令或结论
Scope Error：任务边界错误，做多了或做少了
Format Error：输出格式不符合要求
Safety Error：执行了高风险操作或缺少确认
Memory Error：长期信息更新或读取错误
Template Error：模板使用错误
Skill Error：Skill 规则不完整或未遵守
```

---

# 5. 严重程度定义

建议使用以下严重程度：

```text
S1 Critical：
严重错误，可能导致文件丢失、错误修改、错误决策或明显破坏任务结果。

S2 Major：
重要错误，影响任务质量，需要修改规则或重新执行部分任务。

S3 Minor：
轻微错误，不影响主要结果，但需要记录以优化体验。

S4 Note：
观察项，不一定是错误，但值得后续改进。
```

---

# 6. 状态定义

建议使用以下状态：

```text
Open：已发现，尚未处理
Fixed：已修复
Mitigated：已缓解，但仍需观察
Needs User Confirmation：需要用户确认
Won't Fix：暂不处理
Superseded：已被新的规则或模板替代
```

---

# 7. AGENT_LESSONS.md 标准模板

复制下面内容，并根据当前项目实际情况填写。

```markdown
# Agent Lessons

## 1. 文件作用

本文件用于记录 Agent 在项目执行中的经验教训、错误模式和规则改进点。

Agent 在任务结束后，应读取 `TASK_CLOSING_CHECKLIST.md`，判断本次任务是否暴露了 Agent 行为问题。

本文件不记录普通任务清单、项目背景或详细变更记录。

---

## 2. 最新经验摘要

```text
最近一次记录日期：
【YYYY-MM-DD】

最近一次问题分类：
【Context Error / Prompt Error / Planning Error / Execution Error / Tool Error / Verification Error / File Operation Error / Hallucination Error / Scope Error / Format Error / Safety Error / Memory Error / Template Error / Skill Error】

严重程度：
【S1 Critical / S2 Major / S3 Minor / S4 Note】

当前状态：
【Open / Fixed / Mitigated / Needs User Confirmation / Won't Fix / Superseded】

摘要：
【用 1-3 句话概括本次经验教训】
```

---

## 3. 经验教训记录

### Lesson 【编号】：【标题】

#### 日期

```text
【YYYY-MM-DD】
```

#### 问题分类

```text
【Context Error / Prompt Error / Planning Error / Execution Error / Tool Error / Verification Error / File Operation Error / Hallucination Error / Scope Error / Format Error / Safety Error / Memory Error / Template Error / Skill Error】
```

#### 严重程度

```text
【S1 Critical / S2 Major / S3 Minor / S4 Note】
```

#### 当前状态

```text
【Open / Fixed / Mitigated / Needs User Confirmation / Won't Fix / Superseded】
```

#### 发生场景

```text
【说明是在什么任务、什么步骤、什么条件下发生的】
```

#### Agent 的错误表现

```text
1. 【错误表现 1】
2. 【错误表现 2】
3. 【错误表现 3】
```

#### 正确做法应该是

```text
1. 【正确做法 1】
2. 【正确做法 2】
3. 【正确做法 3】
```

#### 根因分析

```text
1. 【根因 1】
2. 【根因 2】
3. 【根因 3】
```

可选根因类型：

```text
- 上下文缺失
- 上下文过多或冲突
- Prompt 约束不清
- Skill 规则缺失
- 验证规则缺失
- 文件边界不清
- 用户需求理解不完整
- 工具权限或工具能力限制
- 模板职责边界不清
```

#### 需要更新的文件

```text
1. 【文件路径】 - 【为什么需要更新】
2. 【文件路径】 - 【为什么需要更新】
3. 【文件路径】 - 【为什么需要更新】
```

如果不需要更新文件，写：

```text
暂无需要更新的文件。
```

#### 新增或修正规则

```text
1. 【规则 1】
2. 【规则 2】
3. 【规则 3】
```

#### 后续避免方法

```text
1. 【避免方法 1】
2. 【避免方法 2】
3. 【避免方法 3】
```

#### 是否需要用户确认

```text
【是/否】
```

如果需要，写明问题：

```text
需要用户确认：
1. 【问题 1】
2. 【问题 2】
```

#### 是否已经修复

```text
【是/否/部分修复/待确认】
```

#### 相关任务 / 文件

```text
1. 【相关任务】
2. 【相关文件】
3. 【相关输出】
```

#### 备注

```text
【补充说明，可为空】
```

---

## 4. 常见错误模式

### 4.1 上下文相关错误

```text
- 【错误模式 1】
- 【错误模式 2】
```

### 4.2 提示词相关错误

```text
- 【错误模式 1】
- 【错误模式 2】
```

### 4.3 执行相关错误

```text
- 【错误模式 1】
- 【错误模式 2】
```

### 4.4 验证相关错误

```text
- 【错误模式 1】
- 【错误模式 2】
```

### 4.5 文件操作相关错误

```text
- 【错误模式 1】
- 【错误模式 2】
```

如果暂无记录，写：

```text
暂无已归纳的常见错误模式。
```

---

## 5. 已修复规则

用于记录已经根据经验教训更新过的规则。

| ID | 日期 | 原问题 | 修复方式 | 更新文件 | 状态 |
|---|---|---|---|---|---|
| FIX-001 | 【YYYY-MM-DD】 | 【原问题】 | 【修复方式】 | 【文件路径】 | 【Fixed / Mitigated】 |

如果暂无已修复规则，写：

```text
暂无已修复规则记录。
```

---

## 6. 待处理规则改进

| ID | 提出日期 | 问题 | 建议改进 | 影响文件 | 优先级 | 状态 |
|---|---|---|---|---|---|---|
| IMP-001 | 【YYYY-MM-DD】 | 【问题】 | 【建议改进】 | 【文件路径】 | 【P0/P1/P2/P3】 | 【Open/Needs User Confirmation】 |

如果暂无待处理规则改进，写：

```text
暂无待处理规则改进。
```

---

## 7. 何时更新本文件

以下情况发生时，应更新本文件：

```text
1. Agent 明显误解用户任务
2. Agent 忽略上下文或规则
3. Agent 编造文件、命令、数据或结论
4. Agent 没有验证就声称完成
5. Agent 修改了无关文件
6. Agent 没有遵守用户偏好
7. Agent 没有识别上下文冲突
8. Agent 错误使用模板
9. Agent 错误调用工具
10. Agent 暴露出可复用的规则缺口
```

以下情况通常不更新本文件：

```text
1. 普通任务完成
2. 没有出现 Agent 行为问题
3. 用户只是提问概念
4. 只是新增普通 TODO
5. 只是记录文件变更
```

---

## 8. 当前待确认问题

```text
1. 【待确认问题 1】
2. 【待确认问题 2】
3. 【待确认问题 3】
```

如果没有，写：

```text
暂无待确认问题。
```
```

---

# 8. Agent 更新 AGENT_LESSONS.md 的规则

Agent 在任务结束后，应根据 `TASK_CLOSING_CHECKLIST.md` 判断是否更新本文件。

更新条件：

```text
1. 本次任务暴露了 Agent 行为问题
2. 用户指出 Agent 的回答或执行方式有问题
3. Agent 发现当前 Skill 规则不够明确
4. Agent 发现模板职责边界不清
5. Agent 发现缺少验证规则
6. Agent 发现上下文读取或更新流程有问题
7. 本次任务产生了可复用的 Agent 改进经验
```

不要因为只是普通任务完成就更新本文件。

---

# 9. Agent 生成 AGENT_LESSONS.md 后的检查清单

生成后，Agent 必须检查：

```text
1. 是否记录了具体错误表现？
2. 是否说明发生场景？
3. 是否分析了根因？
4. 是否说明正确做法？
5. 是否提出后续避免方法？
6. 是否说明需要更新哪些文件？
7. 是否区分问题分类？
8. 是否标注严重程度？
9. 是否标注当前状态？
10. 是否没有写入具体项目内容到模板本身？
```

---

# 10. 最终原则

```text
AGENT_LESSONS.md 是 Agent 经验教训文件，不是任务清单文件，也不是变更日志文件。
```

它应该帮助 Agent 回答：

```text
我以前犯过什么错？
为什么会错？
现在应该遵守什么规则来避免再次犯错？
```

如果是任务清单，应写入：

```text
context/TODO.md
```

如果是文件变更，应写入：

```text
context/CHANGELOG.md
```

如果是长期决策，应写入：

```text
context/DECISION_LOG.md
```
