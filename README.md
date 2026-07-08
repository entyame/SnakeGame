# 🐍 贪吃蛇 Snake Game

一个使用原生 **HTML / CSS / JavaScript** 实现的经典贪吃蛇网页游戏，无需安装任何依赖，打开浏览器即可游玩。

## 运行方式

直接用浏览器打开 `index.html` 文件即可运行。

或者使用任意 HTTP 服务器：

```bash
# Python 3
python -m http.server 8080

# Node.js (npx)
npx serve .
```

然后访问 `http://localhost:8080`。

## 操作说明

| 按键 | 功能 |
|------|------|
| `↑` `↓` `←` `→` | 控制蛇的移动方向 |
| `W` `A` `S` `D` | 方向键替代方案 |
| `Space` | 游戏结束后重新开始 |

## 游戏规则

- 🍎 吃到红色食物得 10 分
- 🧱 撞墙游戏结束
- 🐍 撞到自己游戏结束
- ⚡ 分数越高，蛇移动越快
- 🏆 最高分自动保存到浏览器本地存储（localStorage）

## 技术栈

- HTML5 Canvas
- CSS3
- 原生 JavaScript（无框架、无依赖）
