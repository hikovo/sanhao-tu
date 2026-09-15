# 动画说明

三好兔使用 Codex v1 的 8 列 × 9 行图集。每格为 `192 × 208 px`，完整图集为 `1536 × 1872 px`。

## 行映射

| Row | 动作 | Codex 状态 | 帧数 |
| ---: | --- | --- | ---: |
| 0 | `blink` / 眨眼 | `idle` | 6 |
| 1 | `swing-right` / 右秋千 | `running-right` | 8 |
| 2 | `swing-left` / 左秋千 | `running-left` | 8 |
| 3 | `hop` / 轻跳 | `waving` | 4 |
| 4 | `wink` / 眨眼回应 | `jumping` | 5 |
| 5 | `dizzy` / 晕眩 | `failed` | 8 |
| 6 | `wait` / 等待 | `waiting` | 6 |
| 7 | `typing` / 打字 | `running` | 6 |
| 8 | `smile` / 微笑 | `review` | 6 |

## 动作小记

- `blink` 是一次干净利落的眨眼。
- `swing-right` 和 `swing-left` 让三好兔坐着秋千轻轻摆动。
- `hop` 是很小的一次起跳。
- `wink` 从 `<` 形闭眼开始，随着身体轻晃慢慢收窄，再展开。
- `dizzy` 的圈圈眼会转起来，身体也会轻轻摇摆。
- `wait` 只让眼睛悄悄向左右看。
- `typing` 使用一块偏棕的浅黄色小键盘，双爪轮流敲击。
- `smile` 从小圆点嘴变成短短的微笑，再回到原来的样子。

GIF 位于 `assets/previews/`，用来查看动作。Codex 安装时读取 `spritesheet.webp`。
