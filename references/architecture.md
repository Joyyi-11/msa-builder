# Moqi 3.0 架构

## 设计目标

让 AI 以尽可能低的上下文成本获得足够信息，做出更符合用户目标、判断方式和行动边界的选择。

## 三层架构

### 第一层：Agent 入口层（entrypoints）

承载每轮都必须执行的沟通规则、行动边界、安全红线、通用执行原则和任务路由。

- `AGENTS.md` 是跨 agent 共享运行规则的唯一真实源。
- 每个 Agent 通过一份薄适配器接入：`entrypoints/<AGENT>.md` 只加载 `AGENTS.md` 并记录本平台差异，不复制共享规则。
- 入口层按需延展：新增 Agent 只新增一份薄适配器，不改动 `AGENTS.md`、MSA 或校验器；Codex、Claude Code、WorkBuddy、Qoder 等都只是案例，不是硬编码名单。
- 项目级规则可以细化全局入口，但不能降低安全边界。

薄适配器的接入流程见 `references/adapter.md`。

Agent 入口层回答“不同 AI Agent 如何进入并加载规则”；MSA 中的 `Agent.md` 回答“用户希望与 AI 建立怎样的协作关系”，两者职责不同。

### 第二层：MSA

- `Memory.md`：当前且会改变协作行动的事实、优先级和资料真实源。
- `Soul.md`：有多个真实场景支撑、更新缓慢的思维模式和判断框架。
- `Agent.md`：协作关系、主动程度、纠错方式和分歧处理。

MSA 不是个人档案。完整履历、项目清单和动态数据应放在外部真实源，`Memory.md` 只在这些资料确有协作价值时保存指针。

### 第三层：references

只在用户确有某类重复任务，而且对应细则不需要每轮加载时创建。每个 reference 必须满足：

1. 有清晰的任务触发条件。
2. 在 `AGENTS.md` 中有唯一加载路由。
3. 不复制入口、MSA 或其他 reference 的完整规则。

完整且可独立复用的专业工作流不应塞入 Moqi；为它配置触发边界，交由相应工具或 Skill 承担。

## ALIGNMENT 控制平面

`ALIGNMENT.md` 负责信息分流、去重、过期清理、Gotchas 生命周期、结构验证和提交边界。它作用于全部三层，因此不属于 MSA，也不是普通领域 reference。

## 单一真实源

- 入口可以摘要安全原则，reference 只展开领域操作步骤。
- README 解释架构，但不定义新的运行规则。
- Git 保存历史，常驻文件只保留当前仍有效的状态。
- Gotcha 是严重问题的临时高优先级提醒，达到退出条件后删除。

## 推荐目录

```text
<moqi-root>/
├── entrypoints/
│   ├── AGENTS.md
│   └── <按平台需要生成的适配器>
├── MSA/
│   ├── Memory.md
│   ├── Soul.md
│   └── Agent.md
├── references/          # 有明确按需规则时才创建
├── ALIGNMENT.md
└── scripts/
```
