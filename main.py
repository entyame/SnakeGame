"""
贪吃蛇游戏 — Snake Game
使用 Python 内置 turtle 模块，无需额外安装依赖。
方向键控制移动，吃到食物得分，撞墙或撞到自己则游戏结束。
"""

import turtle
import random
import time


# ============================================================
# 配置
# ============================================================
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GRID_SIZE = 20
INITIAL_SPEED = 0.12  # 初始移动间隔（秒），越小越快


# ============================================================
# 游戏主体
# ============================================================
class SnakeGame:
    def __init__(self):
        # 窗口
        self.win = turtle.Screen()
        self.win.title("🐍 贪吃蛇 Snake Game")
        self.win.bgcolor("#1a1a2e")
        self.win.setup(WINDOW_WIDTH + 40, WINDOW_HEIGHT + 60)
        self.win.tracer(0)  # 关闭自动刷新，手动控制帧率

        # 绘制边框
        self._draw_border()

        # 分数
        self.score = 0
        self.high_score = 0
        self._load_high_score()
        self.score_display = self._create_score_display()

        # 蛇
        self.head = self._create_turtle("square", "#00d2ff")
        self.head.goto(0, 0)
        self.head.direction = "stop"

        self.body = []  # 身体段列表
        self.body_colors = ["#00d2ff", "#00b4d8", "#0096c7", "#0077b6", "#023e8a"]

        # 食物
        self.food = self._create_turtle("circle", "#ff6b6b")
        self.food.shapesize(0.6, 0.6)
        self._move_food()

        # 键盘绑定
        self.win.listen()
        self.win.onkeypress(lambda: self._set_direction("up"), "Up")
        self.win.onkeypress(lambda: self._set_direction("down"), "Down")
        self.win.onkeypress(lambda: self._set_direction("left"), "Left")
        self.win.onkeypress(lambda: self._set_direction("right"), "Right")
        self.win.onkeypress(lambda: self._set_direction("up"), "w")
        self.win.onkeypress(lambda: self._set_direction("down"), "s")
        self.win.onkeypress(lambda: self._set_direction("left"), "a")
        self.win.onkeypress(lambda: self._set_direction("right"), "d")

        # 游戏状态
        self.running = True
        self.speed = INITIAL_SPEED

    # ---- 辅助方法 ----
    def _create_turtle(self, shape, color):
        t = turtle.Turtle()
        t.speed(0)
        t.shape(shape)
        t.color(color)
        t.penup()
        return t

    def _create_score_display(self):
        t = self._create_turtle("square", "white")
        t.hideturtle()
        t.goto(0, WINDOW_HEIGHT // 2 + 15)
        self._update_score_display(t)
        return t

    def _update_score_display(self, t):
        t.clear()
        t.write(
            f"Score: {self.score}    High Score: {self.high_score}",
            align="center",
            font=("Courier New", 16, "bold"),
        )

    def _draw_border(self):
        border = self._create_turtle("square", "#e94560")
        border.goto(0, 0)
        border.shapesize(
            WINDOW_HEIGHT // 2 // 10 + 0.1,
            WINDOW_WIDTH // 2 // 10 + 0.1,
        )
        border.color("#e94560")
        inner = self._create_turtle("square", "#1a1a2e")
        inner.goto(0, 0)
        inner.shapesize(
            (WINDOW_HEIGHT - GRID_SIZE) // 2 // 10,
            (WINDOW_WIDTH - GRID_SIZE) // 2 // 10,
        )

    def _set_direction(self, d):
        opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}
        if self.head.direction != opposites[d]:
            self.head.direction = d

    def _load_high_score(self):
        try:
            with open("high_score.txt", "r") as f:
                self.high_score = int(f.read().strip())
        except (FileNotFoundError, ValueError):
            self.high_score = 0

    def _save_high_score(self):
        with open("high_score.txt", "w") as f:
            f.write(str(self.high_score))

    def _move_food(self):
        max_coord = WINDOW_WIDTH // 2 - GRID_SIZE
        x = random.randint(-max_coord // GRID_SIZE, max_coord // GRID_SIZE) * GRID_SIZE
        y = random.randint(-max_coord // GRID_SIZE, max_coord // GRID_SIZE) * GRID_SIZE
        self.food.goto(x, y)

    def _add_body_segment(self):
        seg = self._create_turtle("square", self.body_colors[len(self.body) % len(self.body_colors)])
        if self.body:
            seg.goto(self.body[-1].position())
        else:
            seg.goto(self.head.position())
        self.body.append(seg)

    # ---- 移动 ----
    def _move(self):
        if self.head.direction == "stop":
            return

        # 记录蛇身位置（从尾到头传递）
        positions = [self.head.position()]
        for seg in self.body:
            positions.append(seg.position())

        # 移动蛇头
        x, y = self.head.position()
        step = GRID_SIZE
        if self.head.direction == "up":
            self.head.sety(y + step)
        elif self.head.direction == "down":
            self.head.sety(y - step)
        elif self.head.direction == "left":
            self.head.setx(x - step)
        elif self.head.direction == "right":
            self.head.setx(x + step)

        # 移动蛇身（每段移到前一段的上一个位置）
        for i, seg in enumerate(self.body):
            seg.goto(positions[i])

    # ---- 碰撞检测 ----
    def _check_collision(self):
        x, y = self.head.position()
        half = WINDOW_WIDTH // 2 - GRID_SIZE // 2

        # 撞墙
        if abs(x) > half or abs(y) > half:
            return True

        # 撞自己
        for seg in self.body:
            if self.head.distance(seg) < GRID_SIZE // 2:
                return True

        return False

    # ---- 主循环 ----
    def _game_loop(self):
        if not self.running:
            return

        self.win.update()
        self._move()

        # 吃到食物
        if self.head.distance(self.food) < GRID_SIZE:
            self._move_food()
            self._add_body_segment()
            self.score += 10
            if self.score > self.high_score:
                self.high_score = self.score
                self._save_high_score()
            self._update_score_display(self.score_display)
            # 加速
            self.speed = max(0.04, self.speed - 0.002)

        # 碰撞检测
        if self._check_collision():
            self._game_over()
            return

        self.win.ontimer(self._game_loop, int(self.speed * 1000))

    def _game_over(self):
        self.running = False
        self.head.direction = "stop"

        # 蛇头变红
        self.head.color("#e94560")
        for seg in self.body:
            seg.color("#e94560")

        # 显示 Game Over
        go = self._create_turtle("square", "white")
        go.hideturtle()
        go.goto(0, 40)
        go.write("GAME OVER", align="center", font=("Courier New", 36, "bold"))
        go.goto(0, -10)
        go.write(f"Final Score: {self.score}", align="center", font=("Courier New", 20, "bold"))
        go.goto(0, -60)
        go.write("Press SPACE to restart  |  Press ESC to quit",
                 align="center", font=("Courier New", 12, "normal"))

        self.win.onkeypress(self._restart, "space")
        self.win.onkeypress(lambda: self.win.bye(), "Escape")

    def _restart(self):
        # 清除蛇身
        for seg in self.body:
            seg.hideturtle()
        self.body.clear()

        # 重置蛇头
        self.head.goto(0, 0)
        self.head.direction = "stop"
        self.head.color("#00d2ff")

        # 重置分数
        self.score = 0
        self.speed = INITIAL_SPEED
        self._update_score_display(self.score_display)

        # 清理所有 GAME OVER 文字
        for t in turtle.turtles():
            if getattr(t, "shape", lambda: "")() == "square" and not t.isvisible():
                continue
        # 直接找到并清除文字 turtle
        for t in list(turtle.turtles()):
            # 保留蛇头、身体、食物、分数、边框
            if t not in [self.head, self.food, self.score_display] and t not in self.body:
                try:
                    if t.shape() == "square" and t.color()[0] == "white":
                        t.clear()
                        t.hideturtle()
                except Exception:
                    pass

        # 重新绑定游戏按键
        self.win.onkeypress(lambda: self._set_direction("up"), "Up")
        self.win.onkeypress(lambda: self._set_direction("down"), "Down")
        self.win.onkeypress(lambda: self._set_direction("left"), "Left")
        self.win.onkeypress(lambda: self._set_direction("right"), "Right")
        self.win.onkeypress(lambda: self._set_direction("up"), "w")
        self.win.onkeypress(lambda: self._set_direction("down"), "s")
        self.win.onkeypress(lambda: self._set_direction("left"), "a")
        self.win.onkeypress(lambda: self._set_direction("right"), "d")

        self._move_food()
        self.running = True
        self._game_loop()

    # ---- 启动 ----
    def run(self):
        self.win.update()
        self.win.ontimer(self._game_loop, 500)
        self.win.mainloop()


# ============================================================
# 入口
# ============================================================
if __name__ == "__main__":
    game = SnakeGame()
    game.run()
