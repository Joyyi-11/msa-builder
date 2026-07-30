# Moqi（默契）Builder

**让 AI 不只记得你，而是逐步学会怎样与你协作。**

Moqi（默契）是一套可移植、可验证、可持续更新的人机协作系统。它把个人协作偏好、长期上下文和行动边界组织成 agent 可加载的文件结构，让 AI 在低上下文成本下做出更符合用户目标的选择。

`moqi-builder` 通过对话搭建、更新、诊断和对齐 Moqi 实例。

## 解决什么问题

普通 `AGENTS.md` 很容易把运行规则、个人记忆、偏好、历史说明和专业工作流混在一起。文件越长，agent 越难稳定遵守；跨平台使用时，还会出现多份入口互相复制、逐渐漂移的问题。

Moqi 的做法是拆开职责：

```text
Before: 一个不断变长的入口文件
After: 入口规则 + MSA 协作上下文 + 按需细则 + 对齐控制平面
```

## 架构

```text
entrypoints/       第一层：Agent 入口
MSA/               第二层：Memory.md / Soul.md / Agent.md
references/        第三层：按需执行细则
ALIGNMENT.md       对齐控制平面
```

| 文件 | 回答的问题 |
|:-----|:-----------|
| `Memory.md` | AI 当前必须知道哪些事实，才会采取不同的行动？ |
| `Soul.md` | 用户有哪些经过反复验证的思维和判断模式？ |
| `Agent.md` | 用户希望与 AI 建立怎样的协作关系？ |

入口负责每轮必须执行的规则，MSA 提供协作上下文，references 只在存在明确任务类型时创建，`ALIGNMENT.md` 负责持续减法和系统验证。

## 四种模式

- `build`：从零搭建，或整理已有协作系统。
- `update`：更新事实、模式、关系或运行规则。
- `diagnose`：检查重复、越界、过期和失效路由。
- `align`：完成全局对齐、验证和范围明确的提交。

## 示例产物

一次完整搭建通常会生成：

```text
<moqi-root>/
├── entrypoints/
│   ├── AGENTS.md
│   └── <按平台需要生成的薄适配器>
├── MSA/
│   ├── Memory.md
│   ├── Soul.md
│   └── Agent.md
├── references/
├── ALIGNMENT.md
└── scripts/verify_system.py
```

## 适用边界

适合：

- 长期使用 AI agent，并希望减少重复解释的人。
- 同时使用多个 agent，需要共享规则真实源的人。
- 已经有大量规则、偏好或协作记忆，需要诊断、去重和重构的人。

不适合：

- 一次性 prompt 收藏。
- 单轮任务的临时偏好。
- 完整专业工作流的堆放；这类能力应独立做成 Skill，再由 Moqi 配置触发边界。

## 安装

```bash
npx skills add Joyyi-11/moqi-builder -g
```

安装后可以说：

- “帮我搭建一套 Moqi。”
- “整理一下我现有的 AI 协作系统。”
- “诊断一下我的 AGENTS、Memory、Soul 和 Agent。”
- “更新我的 Moqi。”
- “[对齐]”

## 仓库结构

```text
SKILL.md                  模式路由和核心边界
references/               各模式的方法细则
assets/templates/         实例的最小核心骨架
assets/adapters/          按平台选用的入口适配器
scripts/verify_system.py  跨平台结构校验
agents/openai.yaml        Codex 界面元数据
```

## 作者

连漪（Lianyi）
