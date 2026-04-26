# CHANGELOG_TEMPLATE.md

## 1. 模板作用

本模板用于生成项目变更记录文件：

```text
context/CHANGELOG.md
```

该文件用于记录项目在推进过程中发生的实际变化，包括代码、文档、配置、模板、规则、目录结构、实验文件等的新增、修改或删除。

它主要回答：

```text
这次实际改了什么？
为什么改？
影响了哪些文件？
有没有验证？
是否带来后续影响？
```

注意：

```text
本文件是通用模板，不绑定任何具体项目。
使用时，Agent 应根据当前项目实际变更情况，把【占位内容】替换为真实信息。
不要在模板中写入具体项目名称、具体技术路线或具体领域内容。
```

---

# 2. 使用方式

当 Agent 初始化一个项目，或用户要求建立变更记录时，应读取本模板，并生成：

```text
context/CHANGELOG.md
```

每次任务结束后，Agent 应根据 `templates/TASK_CLOSING_CHECKLIST.md` 判断是否需要更新本文件。

如果本次任务创建、修改或删除了任何文件，通常都应该更新 `CHANGELOG.md`。

---

# 3. 什么内容应该写入 CHANGELOG.md

应该写入：

```text
1. 新增文件
2. 修改文件
3. 删除文件
4. 移动或重命名文件
5. 修改目录结构
6. 修改配置
7. 修改规则文件
8. 修改模板文件
9. 修改代码
10. 修改文档
11. 修改测试或验证方式
12. 修改实验相关文件
```

不应该写入：

```text
1. 项目长期目标
2. 用户长期偏好
3. 详细技术决策
4. 普通 TODO
5. 完整实验结果
6. 大段代码 diff
7. 单次聊天解释
8. 与项目文件无关的临时讨论
```

这些内容应分别放入：

```text
context/PROJECT_CONTEXT.md
context/USER_PREFERENCES.md
context/DECISION_LOG.md
context/TODO.md
context/EXPERIMENT_LOG.md
task_context/CONTEXT_PACKAGE.md
```

---

# 4. 变更类型定义

建议使用以下变更类型：

```text
Added：新增文件、功能、文档、模板或规则
Changed：修改已有内容
Fixed：修复问题
Removed：删除内容
Renamed：重命名文件或目录
Moved：移动文件或目录
Deprecated：标记为废弃
Security：安全相关变更
Docs：文档相关变更
Config：配置相关变更
Test：测试相关变更
Experiment：实验相关变更
Template：模板相关变更
Skill：Skill / Agent 规则相关变更
```

---

# 5. 验证状态定义

建议使用以下验证状态：

```text
Verified：已验证
Partially Verified：部分验证
Not Verified：未验证
Not Applicable：不适用
Failed：验证失败
Blocked：无法验证
```

---

# 6. CHANGELOG.md 标准模板

复制下面内容，并根据当前项目实际情况填写。

```markdown
# Changelog

## 1. 文件作用

本文件用于记录项目实际发生的文件、规则、配置、代码、文档、实验或模板变更。

Agent 在任务结束后，应读取 `TASK_CLOSING_CHECKLIST.md`，判断本次任务是否需要更新本文件。

本文件不记录长期项目背景、用户偏好、详细技术决策或普通任务清单。

---

## 2. 最新变更摘要

```text
最近一次变更日期：
【YYYY-MM-DD】

最近一次变更类型：
【Added / Changed / Fixed / Removed / Renamed / Moved / Deprecated / Security / Docs / Config / Test / Experiment / Template / Skill】

最近一次变更摘要：
【用 1-3 句话概括本次变更】

验证状态：
【Verified / Partially Verified / Not Verified / Not Applicable / Failed / Blocked】
```

---

## 3. 变更记录

### Change 【编号】：【变更标题】

#### 日期

```text
【YYYY-MM-DD】
```

#### 变更类型

```text
【Added / Changed / Fixed / Removed / Renamed / Moved / Deprecated / Security / Docs / Config / Test / Experiment / Template / Skill】
```

#### 变更摘要

```text
【简要说明本次变更做了什么】
```

#### 变更原因

```text
【说明为什么要做这个变更】
```

#### 涉及文件

```text
1. 【文件路径 1】 - 【新增/修改/删除/移动/重命名】
2. 【文件路径 2】 - 【新增/修改/删除/移动/重命名】
3. 【文件路径 3】 - 【新增/修改/删除/移动/重命名】
```

#### 具体变更内容

```text
1. 【变更点 1】
2. 【变更点 2】
3. 【变更点 3】
```

#### 影响范围

```text
1. 【影响范围 1】
2. 【影响范围 2】
3. 【影响范围 3】
```

如果影响范围很小，写：

```text
影响范围较小，仅影响上述文件。
```

#### 验证方式

```text
1. 【验证方式 1】
2. 【验证方式 2】
3. 【验证方式 3】
```

如果未验证，写：

```text
本次变更尚未验证。
原因：
【说明未验证原因】
```

如果不需要验证，写：

```text
本次变更不涉及可执行逻辑，验证状态为 Not Applicable。
```

#### 验证结果

```text
【Verified / Partially Verified / Not Verified / Not Applicable / Failed / Blocked】
```

#### 后续影响

```text
1. 【后续影响 1】
2. 【后续影响 2】
3. 【后续影响 3】
```

如果没有明显后续影响，写：

```text
暂无明显后续影响。
```

#### 是否需要更新其他长期文件

```text
PROJECT_CONTEXT.md：【是/否，原因】
USER_PREFERENCES.md：【是/否，原因】
DECISION_LOG.md：【是/否，原因】
TODO.md：【是/否，原因】
TEST_COMMANDS.md：【是/否，原因】
EXPERIMENT_LOG.md：【是/否，原因】
对应 Skill 文件：【是/否，原因】
```

#### 备注

```text
【补充说明，可为空】
```

---

## 4. 按类型汇总

### Added

```text
- 【新增内容 1】
- 【新增内容 2】
```

### Changed

```text
- 【修改内容 1】
- 【修改内容 2】
```

### Fixed

```text
- 【修复内容 1】
- 【修复内容 2】
```

### Removed

```text
- 【删除内容 1】
- 【删除内容 2】
```

### Docs

```text
- 【文档变更 1】
- 【文档变更 2】
```

### Template

```text
- 【模板变更 1】
- 【模板变更 2】
```

### Skill

```text
- 【Skill 变更 1】
- 【Skill 变更 2】
```

如果某类暂无记录，写：

```text
暂无记录。
```

---

## 5. 未验证变更

用于集中记录尚未验证的变更。

| ID | 日期 | 变更标题 | 未验证原因 | 后续验证方式 | 负责人 |
|---|---|---|---|---|---|
| CHG-001 | 【YYYY-MM-DD】 | 【变更标题】 | 【原因】 | 【验证方式】 | 【用户/Agent/其他】 |

如果没有未验证变更，写：

```text
暂无未验证变更。
```

---

## 6. 高风险变更

用于记录可能影响较大的变更。

| ID | 日期 | 变更标题 | 风险原因 | 回滚方式 | 状态 |
|---|---|---|---|---|---|
| RISK-001 | 【YYYY-MM-DD】 | 【变更标题】 | 【风险原因】 | 【回滚方式】 | 【观察中/已解决/待处理】 |

如果没有高风险变更，写：

```text
暂无高风险变更。
```

---

## 7. 何时更新本文件

以下情况发生时，应更新本文件：

```text
1. 新增文件
2. 修改文件
3. 删除文件
4. 移动或重命名文件
5. 修改目录结构
6. 修改配置文件
7. 修改代码
8. 修改文档
9. 修改模板
10. 修改 Skill 或 Agent 规则
11. 修改测试或验证命令
12. 任务产生可追踪的项目变化
```

以下情况通常不更新本文件：

```text
1. 普通概念解释
2. 单次临时讨论
3. 没有改变任何文件的问答
4. 只是读取文件但没有修改
5. 只是生成临时 Context Package，且不需要长期记录
```

---

## 8. 当前不确定变更

```text
1. 【不确定变更 1】
2. 【不确定变更 2】
3. 【需要用户确认的变更】
```

如果没有，写：

```text
暂无不确定变更。
```
```

---

# 7. Agent 更新 CHANGELOG.md 的规则

Agent 在任务结束后，应根据 `TASK_CLOSING_CHECKLIST.md` 判断是否更新本文件。

更新条件：

```text
1. 本次任务创建了文件
2. 本次任务修改了文件
3. 本次任务删除了文件
4. 本次任务移动或重命名了文件
5. 本次任务改变了目录结构
6. 本次任务改变了规则、模板、Skill、代码、文档或配置
```

不要因为只是读取了文件就更新本文件。

---

# 8. Agent 生成 CHANGELOG.md 后的检查清单

生成后，Agent 必须检查：

```text
1. 是否记录了变更日期？
2. 是否记录了变更类型？
3. 是否记录了变更原因？
4. 是否列出涉及文件？
5. 是否说明具体变更内容？
6. 是否说明影响范围？
7. 是否说明验证方式？
8. 是否说明验证结果？
9. 是否说明是否需要更新其他长期文件？
10. 是否没有写入具体项目内容到模板本身？
```

---

# 9. 最终原则

```text
CHANGELOG.md 是项目变化记录文件，不是项目背景文件，也不是任务清单文件。
```

它应该帮助 Agent 回答：

```text
这个项目最近实际改了什么？
为什么改？
影响哪些文件？
验证了吗？
还需要更新哪些长期文件？
```

如果是长期背景，应写入：

```text
context/PROJECT_CONTEXT.md
```

如果是任务清单，应写入：

```text
context/TODO.md
```

如果是技术决策，应写入：

```text
context/DECISION_LOG.md
```
