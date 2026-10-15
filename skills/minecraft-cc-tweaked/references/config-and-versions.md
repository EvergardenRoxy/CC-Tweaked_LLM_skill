# 配置、命令、版本差异与资料来源

## 服务器配置

- 文件位置（MC 1.13+、CC:T 1.87.0+）：存档目录下 `serverconfig/computercraft-server.toml`（单人和多人都是）。修改后重启游戏/服务器。
- 更早的版本：`config/computercraft-common.toml`（CC:T ≤ 1.86.2），MC 1.12.2 及以前为 `config/ComputerCraft.cfg`。

常见配置项（**名称和默认值以用户实际文件为准**，不同版本会有增减）：

| 配置项 | 常见默认 | 作用 |
|---|---|---|
| `computer_space_limit` | 1000000 字节 | 每台计算机硬盘大小 |
| `floppy_space_limit` | 125000 字节 | 软盘大小 |
| `maximum_open_files` | 128 | 每台计算机同时打开的文件数 |
| `default_computer_settings` | 空 | 默认 settings（即 `_CC_DEFAULT_SETTINGS`），如 `shell.autocomplete=false` |
| `[http] enabled` / `websocket_enabled` | true | 是否开放 `http` API / WebSocket |
| `[http] max_requests` / `max_websockets` | 16 / 4 | 同时请求数 |
| `[[http.rules]]` | 一条 `host = "$private"`、`action = "deny"`，一条 `host = "*"`、`action = "allow"` | 按域名/通配/CIDR 允许或拒绝；`$private` 表示局域网和本机地址。允许规则里还有 `max_download`（16 MiB）、`max_upload`（4 MiB）、`max_websocket_message`（128 KiB）、`timeout`（30000 ms） |
| `[turtle] need_fuel` | true | 关闭后 `getFuelLevel()` 返回 `"unlimited"` |
| `[turtle] normal_fuel_limit` / `advanced_fuel_limit` | 20000 / 100000 | 燃料上限 |
| `[peripheral] modem_range` / `modem_high_altitude_range` | 64 / 384 | 无线调制解调器范围 |
| 命令方块外设开关 | false | 文档名为 `enable_command_block`；开启后命令方块才作为 `command` 外设出现 |
| `[term_sizes]` | 计算机 51×19、口袋 26×20 等 | 终端尺寸 |

**允许访问本机/局域网（测试用）**：删除 `host = "$private"`、`action = "deny"` 的那条 `[[http.rules]]`，保存并重启。1.95.0 之前是多条列出具体 IP 段的 deny 规则，全部删除。生产服务器不要这样做。

## `/computercraft` 命令

| 子命令 | 权限 | 作用 |
|---|---|---|
| `/computercraft dump [计算机]` | OP（单人世界可直接用） | 列出已加载的计算机：ID、位置、是否运行；可点按钮传送或查看终端 |
| `/computercraft turn-on [计算机...]` / `shutdown [计算机...]` | OP（单人可用） | 开机 / 关机；不带参数作用于全部已加载计算机（卡顿时可用 `shutdown`） |
| `/computercraft tp <计算机>` / `view <计算机>` | OP（单人需开作弊） | 传送到计算机 / 远程打开其终端 |
| `/computercraft track start\|stop\|dump [字段...]` | OP（单人可用） | 性能分析：每台计算机运行耗时、服务器线程任务、HTTP 流量（`server_tasks_count server_tasks`、`http_upload http_download`） |
| `/computercraft queue <计算机> [参数...]` | 所有玩家 | 给**命令计算机**发送 `computer_command` 事件（类似 `/trigger`） |

计算机选择器：`#12`（ID 12）、`@c[id=12]`、`@c[label=名字]`、`@c[family=normal|advanced|command]`、`@c[distance=..100]`、`@c[instance=id]`。安装权限模组时可按 `computercraft.command.<子命令>` 节点授权。

## 数据包扩展

- 往 ROM 加文件：`data/computercraft/lua/rom/...`（文件名必须小写；改动后可能要 `/reload`）。
  - `rom/autorun/*`：开机运行；`rom/modules/main/*`：可 `require`；`rom/programs/*`：新程序；`rom/apis/*`（及 `http`/`turtle`/`pocket`/`command` 子目录）：开机 `os.loadAPI`。
- 可扩展的标签：`computercraft:turtle_can_place`（物品，`turtle.place` 可使用）、`computercraft:turtle_can_use`（方块，可交互，默认蜂箱、炼药锅、堆肥桶）、`computercraft:always_breakable`、`computercraft:turtle_shovel_harvestable`、`turtle_sword_harvestable`、`turtle_hoe_harvestable`。
- 数据包格式随 MC 版本变化（文档分 1.20.1、1.21.1 等版本）。

## 版本差异速查（按功能首次出现的 CC: Tweaked 版本）

| 版本 | 变化 |
|---|---|
| 1.80pr1 | 程序在独立环境运行（全局变量不再泄漏到其他程序）；带 `/` 的程序名按当前目录查找；调色板 API；普通计算机可用全部 16 色（显示为灰度） |
| 1.87.0 | `settings.define`；`setting_changed` 事件；`textutils.unserialiseJSON`；服务器配置移到 `serverconfig/` |
| 1.88.0 | 无标签计算机挖下后也保留 ID；`peripheral.getName`；`getType` 接受 wrap 对象 |
| 1.90.0 | `turtle.getItemDetail` 的 `detailed` 参数；`cc.image.nft` |
| 1.94.0 | 通用外设 `inventory`、`fluid_storage`、`energy_storage`；物品详情增加 nbt 哈希、tags、附魔等；`colors.toBlit` |
| 1.95.0 | `fs.combine` 多参数；`cc.strings`；`[[http.rules]]` 改为 `$private` 单条规则 |
| 1.96.0 | `inventory.getItemLimit`；`cc.expect.range` |
| 1.97.0 | `textutils.serialise` 的 `opts` 参数 |
| 1.99 | 外设可有多个类型、`peripheral.hasType`；`commands.getBlockInfo(s)` 的维度参数；`cc.pretty.pretty_print` |
| 1.100 | `speaker.playAudio`/`stop`、`cc.audio.dfpwm` |
| 1.103.0 | 程序支持 hashbang |
| 1.105.0 | HTTP 自定义超时；`colors.fromBlit` |
| 1.106.0 | `fs.find` 支持 `?`；JSON 选项重载 |
| 1.109.0 | **运行时升级到 Lua 5.2**：移除 `arg` 伪参数（用 `...`）、`getfenv`/`setfenv` 受限、`load` 默认全局环境、不支持 `string.dump`/二进制块、`math.random` 换算法；文件/HTTP/WebSocket 一律原始字节；`fs.open` 支持 `r+`/`w+` |
| 1.111.0 | `io.open` 支持 `r+`/`w+` |
| 1.112.0 | `cc.strings.split` |
| 1.114.0 | 红石继电器 `redstone_relay` |
| 1.116.0 | `turtle.getEquippedLeft/Right` |
| 1.117.0 | 物品/方块详情增加地图颜色、药水效果；`Websocket.getResponseHeaders` |
| 1.118.0 | `rednet.lookup` 超时参数；`commands.getEntities`；实体详情 |
| 1.119.0 | `cc.base64`；`commands.getDimension` |
| 1.120.0 | `parallel.waitForAll` 可 `spawn` 新任务 |
| 1.121.0 | `turtle_storage`（海龟装备存储物品）；HTTP 方法名校验放宽 |

**Minecraft 版本带来的变化**
- MC 1.13：键码改变（必须用 `keys.*` 常量；小键盘回车与回车键码不同）；方块/物品"扁平化"——`turtle.inspect` 不再有 metadata，改为 `state`；`getItemDetail` 不再有 damage 值区分物品（如 16 种羊毛是 16 个 ID）；自定义 ROM 改用数据包；海龟可含水。
- MC 1.7.10 / 1.12 的老 ComputerCraft 教程中的 `os.loadAPI`、`arg`、数字键码、`metadata`、`peripheral.wrap("left").getStackInSlot` 等写法在新版不适用（最后一个是 OpenPeripherals 之类附属模组的方法）。

## Lua 兼容性（Cobalt 运行时）

| 支持 | 不支持 |
|---|---|
| `goto`/标签、`_ENV`、`\z` `\xNN` `\u{XXX}` 转义、`__len` `__pairs` 元方法 | 整数子类型、位运算符、整除 `//` |
| `bit32` 库、`utf8` 库、`string.pack/unpack/packsize`、`table.move`、`table.pack/unpack`、`table.create` | `collectgarbage`、`os.execute`、`os.exit`、`string.dump` |
| `load` 新语法（含 mode、env）、`loadfile` 的 mode、`rawlen`、`select` 负索引、`xpcall` 额外参数 | `math.type`、`math.tointeger`、`math.maxinteger/mininteger`、`math.ult` |
| `coroutine.isyieldable`、`coroutine.running` 第二返回值、跨 C 边界 yield | `%g` 匹配类；ephemeron 表 |
| `math.atan(y, x)`；`math.log(x, base)` | `debug.getuservalue/setuservalue`、尾调用钩子 |
| 5.0 兼容：`string.gfind`、`table.getn`、`math.mod`、`table.foreach(i)` | `table.setn`、`gcinfo` |

## 资料来源与已知出入

- 官方文档：<https://tweaked.cc>（模块、外设、事件、指南、参考页）；源码与问题反馈：<https://github.com/cc-tweaked/CC-Tweaked>。
- 本 Skill 中的 `lua` 代码块均通过 Lua 5.2 编译器语法检查，并对照 tweaked.cc 的成员列表核对了全局 API 名称；**外设方法与运行时行为无法静态验证**，以游戏内实测为准。
- 官方 Item details 页的示例 `local ok, block = turtle.getItemDetail(slot, true)` 有误：`getItemDetail` 只返回一个值（表或 nil），应写 `local item = turtle.getItemDetail(slot, true)`。
- 燃料值（煤 80 等）、终端尺寸、配置项默认值来自模组默认设置，整合包可能修改。
- 海龟动作失败原因字符串、部分报错原文随版本变化，排错时让用户提供实际输出。
- 第三方附属模组（Advanced Peripherals、Plethora 等）提供的外设与方法不在 tweaked.cc 文档内，必须用 `peripheral.getMethods` 实测。
