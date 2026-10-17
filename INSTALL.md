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

## 配合 cct-run 使用

[cct-run](https://github.com/EvergardenRoxy/CC-Tweaked_MCP) 是本 Skill 的配套测试工具。Skill 会先看 AI 当前的工具列表：

- 有 `cct_run` 等工具时，交付前先在模拟器里运行程序；
- 还有 `cct_live_*` 工具时，经你同意后可以接管游戏里的电脑；
- 都没有时，只会在第一次交付时提醒一次可以安装。

规则见 [`references/testing.md`](skills/minecraft-cc-tweaked/references/testing.md)。

### 1. 安装 cct-run（模拟器）

需要 Java 17 或更高版本。解压 cct-run 的发布包（还没有发布包时，按它 README 的“从源码构建”一节构建），然后运行 `bin/cct-run version`（Windows：`bin\cct-run.bat version`），能输出带 `"cc_tweaked"` 的 JSON 就说明装好了。

### 2. 在 AI 客户端里配置 MCP

把 `<解压目录>` 换成实际路径；JSON 里的 `\` 要写成 `\\`。

Claude Code（在 cmd 里运行）：

```bat
claude mcp add --scope user cct-run -- cmd /c <解压目录>\bin\cct-run.bat mcp
```

使用 `mcpServers` JSON 配置的客户端（Claude Desktop、Cherry Studio、DeepSeek Harness 等）：

```json
{
  "mcpServers": {
    "cct-run": {
      "command": "cmd",
      "args": ["/c", "<解压目录>\\bin\\cct-run.bat", "mcp"],
      "env": { "CCT_LIVE_DIR": "<游戏目录>" }
    }
  }
}
```

Codex（`~/.codex/config.toml`）：

```toml
[mcp_servers.cct-run]
command = "cmd"
args = ["/c", "<解压目录>\\bin\\cct-run.bat", "mcp"]
tool_timeout_sec = 300
env = { CCT_LIVE_DIR = "<游戏目录>" }
```

macOS / Linux 把 `cmd /c ...cct-run.bat` 换成 `<解压目录>/bin/cct-run`。只用模拟器时，可以不写 `CCT_LIVE_DIR`。

### 3. （可选）实机测试：cct-live mod

把 cct-live 的 jar 放进游戏的 `mods/`，和 CC: Tweaked 1.120.2 放在一起（只支持 Forge 1.20.1）。`<游戏目录>` 是有 `mods/` 的那个文件夹；启动器开了版本隔离时，是版本文件夹。

- AI 接管电脑时，聊天栏会有提示；你可以随时用 `/cctlive detach <id>` 收回控制。
- 想让 AI 写文件、使用 `cct_live_lua`，需要在 `config/cctlive-common.toml` 里把 `files.allow_write` 改成 `true`（默认关闭）。
- 详见 cct-run 仓库的 `mod/README.md`。

### 4. 确认生效

重新连接 MCP 后，对 AI 说：“列出 cct-run 的工具”。它应该能看到 `cct_run`、`cct_guide` 等工具，装了 mod 的话还有 `cct_live_*`。

