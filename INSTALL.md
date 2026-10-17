# 各工具安装详解

> 返回 [README](README.md#安装)

## 获取 Skill 文件

Skill 就是仓库里的 `skills/minecraft-cc-tweaked/` 文件夹（`SKILL.md` + `references/`）。任选一种方式获取：

```bash
git clone https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill.git
cd CC-Tweaked_LLM_skill
# Skill 文件夹位于 skills/minecraft-cc-tweaked，复制到下文对应目录即可
```

或在 GitHub 页面点 **Code → Download ZIP**，解压后找到 `skills/minecraft-cc-tweaked/`。

### 打包成 zip（用于 Claude.ai、Cherry Studio 等需要上传压缩包的工具）

在仓库根目录执行，得到的压缩包根目录直接是 `SKILL.md` 和 `references/`：

```bash
cd skills/minecraft-cc-tweaked
zip -r ../../CCT_prompt_pack.zip SKILL.md references
```

Windows 可打开 `skills\minecraft-cc-tweaked`，选中 `SKILL.md` 和 `references` 文件夹 → 右键 **压缩为 ZIP 文件**。

```text
CCT_prompt_pack.zip
├── SKILL.md
└── references/
    ├── api-reference.md
    ├── app-engineering.md
    ├── config-and-versions.md
    ├── design-thinking.md
    ├── events-and-concurrency.md
    ├── getting-started.md
    ├── networking.md
    ├── peripherals.md
    ├── security.md
    ├── templates.md
    ├── testing.md
    ├── troubleshooting.md
    └── turtle.md
```

以下各节中 `<skill 文件夹>` 指 `skills/minecraft-cc-tweaked`。安装后确认结构为 `<skills 目录>/minecraft-cc-tweaked/SKILL.md`。

## Claude Code

```bash
cp -r <skill 文件夹> ~/.claude/skills/minecraft-cc-tweaked              # 用户级
cp -r <skill 文件夹> <你的项目>/.claude/skills/minecraft-cc-tweaked      # 项目级
```

也可以通过插件市场安装：

```text
/plugin marketplace add EvergardenRoxy/CC-Tweaked_LLM_skill
/plugin install minecraft-cc-tweaked@cct-llm-skills
```

## Claude.ai / Claude 桌面端

在 **Settings → Capabilities → Skills** 中上传上文打包的 `CCT_prompt_pack.zip`。

## OpenAI Codex（CLI / IDE 插件 / Codex App）

```bash
cp -r <skill 文件夹> ~/.agents/skills/minecraft-cc-tweaked              # 用户级
cp -r <skill 文件夹> <你的项目>/.agents/skills/minecraft-cc-tweaked      # 项目级
```

也可以在 Codex 对话中让内置安装器从仓库下载：

```text
$skill-installer 从 https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill 安装 skills/minecraft-cc-tweaked
```

Codex 通常会自动检测新技能；如果没有出现，重启 Codex。

## Cursor

```bash
cp -r <skill 文件夹> ~/.cursor/skills/minecraft-cc-tweaked              # 用户级
cp -r <skill 文件夹> <你的项目>/.cursor/skills/minecraft-cc-tweaked      # 项目级
```

Cursor 也会读取 `.claude/skills/`、`.agents/skills/`。在 Agent 对话框输入 `/` 可看到并手动调用该技能。

## VS Code + GitHub Copilot

```bash
cp -r <skill 文件夹> ~/.copilot/skills/minecraft-cc-tweaked             # 用户级
cp -r <skill 文件夹> <你的项目>/.github/skills/minecraft-cc-tweaked      # 项目级
```

在 Copilot Chat 输入 `/skills` 打开 **Configure Skills**，确认列表中出现 `minecraft-cc-tweaked`。

## Gemini CLI

```bash
cp -r <skill 文件夹> ~/.gemini/skills/minecraft-cc-tweaked              # 用户级
cp -r <skill 文件夹> <你的项目>/.gemini/skills/minecraft-cc-tweaked      # 项目级
gemini skills list                                                      # 确认已安装
```

也可以直接从仓库安装：

```bash
gemini skills install https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill.git \
  --path skills/minecraft-cc-tweaked          # 默认安装到用户级；加 --scope workspace 装到项目
```

## Cherry Studio

1. 打开 **设置 → 技能**，选择 **从本地 ZIP 安装**，选中 `CCT_prompt_pack.zip`（或选择从文件夹安装 `skills/minecraft-cc-tweaked`），确认全局开关已打开。
2. 进入 **工作**，打开要使用的智能体（Agent）菜单 → **编辑 → 技能**，为该智能体启用；从下一条消息开始生效。

> ⚠️ Cherry Studio 也支持在 **GitHub** 来源中粘贴 `SKILL.md` 链接安装，但这种方式可能只拉取 `SKILL.md` 本身。本 Skill 依赖 `references/` 目录，**推荐用 ZIP 或文件夹方式安装**。

## ChatGPT、DeepSeek 等不支持 Skills 的对话工具

1. 在项目 / 自定义 GPT / 知识库中上传 `SKILL.md` 和 `references/` 下的全部文件；若只能上传少量文件，至少上传 `SKILL.md`、`references/design-thinking.md`、`references/api-reference.md` 和 `references/peripherals.md`。
2. 在系统提示词或项目指令中写入：

   ```text
   回答 Minecraft CC: Tweaked（ComputerCraft）Lua 编程相关问题时，严格遵循附件 SKILL.md 的规则；
   SKILL.md 第 1 节索引指向的细节，到同名附件中查找。不要凭记忆编造 CC 的 API。
   ```

3. 不支持附件的工具，可直接把 `SKILL.md` 正文（去掉开头的 YAML front matter）粘贴为系统提示词。
