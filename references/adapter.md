# Adapter 模式：接入新 Agent

## 目标

把 Moqi 接入任意 AI Agent 工具，而不复制共享规则。每个 Agent 只需一份薄适配器，指向 `entrypoints/AGENTS.md` 并只记录该平台的加载方式与差异。Moqi 不为任何 Agent 硬编码名单——Codex、Claude Code、WorkBuddy、Qoder 等都只是案例。

## 何时需要薄适配器

满足以下任一情况，就为该 Agent 生成一份适配器：

- 该 Agent 会在每次会话自动或常驻加载某个入口文件（如全局 `AGENTS.md` / `CLAUDE.md`、记忆常驻指令、产品内配置）。
- 该 Agent 的加载机制、入口路径或 Skills 路径与既有平台不同。
- 用户确认会把该 Agent 作为长期协作者。

不满足时，不创建适配器；Moqi 仍可仅靠 `AGENTS.md` + MSA 工作。

## 薄适配器的标准结构

适配器只做三件事：

1. 声明跨 agent 共享规则的唯一真实源是 `entrypoints/AGENTS.md`。
2. 要求每次会话先读 `AGENTS.md`，再按其要求读 MSA。
3. 只记录本平台的加载方式与差异；不复制共享规则，规则更新只改 `AGENTS.md`。

最小模板：

```text
# Moqi（默契）：<Agent 名> 适配器

跨 agent 共享规则的唯一真实源是：

`{{MOQI_ROOT}}/entrypoints/AGENTS.md`

每次会话先读取并遵循该文件，再按其中要求读取 MSA。共享规则只修改 `AGENTS.md`，不在本文件复制。

## <Agent 名> 差异

- 加载方式：<symlink / 全局配置 / 记忆常驻指令>。
- <平台独有路径或机制>。
```

## 放置与命名

- 文件放在 `entrypoints/<AGENT>.md`，命名用 Agent 标识（如 `CLAUDE.md`、`CODEX.md`、`WORKBUDDY.md`、`QODER.md`）。
- 可在 `assets/adapters/<AGENT>.md` 提供一份带占位符的示例，供 build 阶段复制填充；`assets/adapters/CLAUDE.md`、`WORKBUDDY.md` 已是案例。
- `AGENTS.md` 是入口，不是适配器，不要改名或复制。

## 各 Agent 如何加载（案例）

以下为已知加载方式的案例；新 Agent 按其自身机制接入，原理相同。

- **Codex**：全局入口 `{{CODEX_ENTRY_PATH}}`（如 `~/.codex/AGENTS.md`）通过 symlink 或已验证副本加载 `entrypoints/AGENTS.md`；Skills 经 junction 指向 `{{AGENTS_SKILLS_PATH}}`。
- **Claude Code**：全局入口 `{{CLAUDE_ENTRY_PATH}}`（如 `~/.claude/CLAUDE.md`）加载薄适配器，再转入主入口；项目规则写项目 `CLAUDE.md`，跨 agent 项目规则写项目 `AGENTS.md`。
- **WorkBuddy**：无全局 symlink；由记忆常驻指令（如 `{{WORKBUDDY_MEMORY_PATH}}`）要求每次会话读取 `entrypoints/WORKBUDDY.md`，再转入主入口；Skills 走产品内机制，不接 `{{AGENTS_SKILLS_PATH}}` 的 junction。
- **Qoder 等其它 Agent**：同理，按其提供的全局入口、记忆或配置机制接入，薄适配器只记录加载方式与本平台差异。

## 校验兼容

`verify_system.py` 不把任意适配器列为必需文件，也不会因新增适配器报错。它只校验：`AGENTS.md` 声明 canonical 标记、路由到 `ALIGNMENT.md`，以及每个 `entrypoints/<X>.md`（X≠AGENTS）都必须路由到 `AGENTS.md`。因此：

- 新增适配器默认即可通过校验，无需修改校验器。
- 若某适配器是体系关键入口、希望校验器保护它不被误删，可把它加入 `REQUIRED_FILES`。

## 接入清单

1. 确认该 Agent 会作为长期协作者，且加载机制明确。
2. 在 `entrypoints/<AGENT>.md` 写薄适配器：指向 `AGENTS.md` + 只记本平台差异。
3. 如需示例资产，放一份带占位符的 `assets/adapters/<AGENT>.md`。
4. 在 `AGENTS.md` 的「条件路由」补一行指向本 adapter 说明（如有维护文档）。
5. 运行 `python scripts/verify_system.py <moqi-root>`，确认无 error。
6. 先验证该 Agent 能正确加载主入口，再投入日常使用。
