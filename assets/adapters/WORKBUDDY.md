# Moqi（默契）：WorkBuddy 适配器

跨 agent 共享规则的唯一真实源是：

`{{MOQI_ROOT}}/entrypoints/AGENTS.md`

每次会话先读取并遵循该文件，再按其中要求读取 MSA（Memory / Soul / Agent）。共享规则只修改 `AGENTS.md`，不在本文件复制。

## WorkBuddy 差异

- 加载方式：记忆常驻指令（如 `~/.workbuddy/MEMORY.md` 中的常驻条目），而非全局 symlink。WorkBuddy 没有宿主在会话启动时自动注入 `AGENTS.md` 的机制，加载入口在记忆系统。
- Skills 走产品内机制，不接 `{{AGENTS_SKILLS_PATH}}` 的 junction。
- 触发：每次会话开始时，记忆指令要求先读 `entrypoints/AGENTS.md` + MSA 三件套，references 按 `AGENTS.md` 的条件路由加载，`[对齐]` 精确触发时再读 `ALIGNMENT.md`。
- 如需把"WorkBuddy 也读 Moqi"写成仓库内公开事实，可在 `entrypoints/` 放本薄适配器，供校验器登记保护（见 `references/adapter.md` 的校验兼容一节）。
