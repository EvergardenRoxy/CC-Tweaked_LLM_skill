# Advanced Peripherals（高级外设）模组的外设

> 返回 [SKILL.md](../SKILL.md) 第 1 节。**本文件是 Advanced Peripherals 模组的内容，不是 CC: Tweaked 本体。** CC: Tweaked 自己没有聊天框、玩家探测器；用户没装这个模组时不要用。

方法名和参数**随模组版本变化**；下面是实测记录，用之前按 `peripherals.md`“模组外设的通用排查方法”在用户的游戏里核对。

**实测环境**：Minecraft 1.20.1 Forge、CC: Tweaked 1.120.2、Advanced Peripherals 0.7.48r。来源：cct-run 的联合测试 3（两次）和联合测试 4。

## 聊天框 `chatBox`

| 内容 | 实测结果 |
|---|---|
| 事件 `chat` | 参数依次为：玩家名、消息、UUID、是否隐藏（`isHidden`）、`messageUtf8`。用 `local ev = { os.pullEvent() }` 接住时，它们是 `ev[2]` 到 `ev[6]` |
| 中文消息 | 第 2 个参数（消息）里的中文变成 `?`；要用第 5 个参数 `messageUtf8`（UTF-8 字节）。实测读 `ev[6]`，玩家发的中文指令能正确识别 |
| `sendMessageToPlayer(消息, 玩家名 [, 前缀, 括号, 括号颜色, 范围, utf8Support])` | 成功返回 `true`；冷却中返回 `nil, "chatMessage is on cooldown"`。第 4 个参数“括号”是字符串，传布尔值会报 `bad argument #4` |
| **发中文** | `sendMessageToPlayer` 发的中文在聊天栏是**乱码**：只传两个参数、或者把第 7 个参数 `utf8Support` 设为 `true`，实测都是乱码。**能用的写法**：`sendFormattedMessageToPlayer(JSON 文本, 玩家名)`，JSON 里的中文写成 `\uXXXX` 转义（下面的例子），实测聊天栏显示正常 |
| `getOperationCooldown("chatMessage")` | 必须传参数，不传会报 `bad argument #1`。连续发送会进入冷却，回复要放进队列，失败后稍等再发 |
| 接了两次 | 聊天框直接贴着电脑、又经有线调制解调器接入时，`chat` 事件每次到达两次。去重，或只接一种方式 |

> 更正：本 Skill 1.2.0 曾写“发中文把 `utf8Support` 设为 `true`”，联合测试 4 实测无效，以本表为准。

```lua
-- Reply to one player in Chinese through the Advanced Peripherals chat box.
-- textutils.serialiseJSON with unicode_strings writes UTF-8 text as \uXXXX
-- escapes, which the chat box turns back into the right characters.
local chat = peripheral.find("chatBox") or error("No chat box found", 0)

local outbox = {}                       -- replies waiting for the cooldown

local function tell(player, text)
    outbox[#outbox + 1] = { player = player, text = text }
end

local function sender()
    while true do
        local m = outbox[1]
        if m then
            local json = textutils.serialiseJSON({ text = m.text }, { unicode_strings = true })
            if chat.sendFormattedMessageToPlayer(json, m.player) then
                table.remove(outbox, 1)
            else
                sleep(0.5)              -- on cooldown: try again shortly
            end
        else
            sleep(0.2)
        end
    end
end

local function listener()
    while true do
        local ev = { os.pullEvent("chat") }
        local player, text = ev[2], ev[6] or ev[3]   -- ev[6] is messageUtf8
        if text == "!ping" then tell(player, "pong") end
    end
end

parallel.waitForAny(sender, listener)
```

- 联合测试 4 里能用的是手写的 `\uXXXX` 转义；`textutils.serialiseJSON(…, { unicode_strings = true })`（CC: Tweaked 1.120.2 有这个选项）生成的是同样的转义，在模拟器里核对过输出。
- 发送放在单独的协程里（上例的 `sender`）：发送方法会等待，放在收指令的循环里会丢事件（`events-and-concurrency.md`）。

## 玩家探测器 `playerDetector`

| 方法 | 实测结果 |
|---|---|
| `isPlayerInRange(范围, 玩家名)` | 注意参数顺序：范围在前。常用来限制“只有主人在附近时按钮才能用” |
| `getOnlinePlayers()` | 在线玩家名列表 |

## 测试时

- 聊天指令要请玩家在聊天栏里真的输入；用 `cct_live_event` 注入的 `chat` 事件只能证明程序能处理你构造的参数。
- 中文回复是否正常只能看游戏里的聊天栏：trace 里程序传出去的中文显示成 `å·…` 这样的字节序列时，游戏里就是乱码（见 `chinese-text.md`）。
