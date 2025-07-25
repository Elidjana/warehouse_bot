import pygame
from config import *
from warehouse import Warehouse
from robot import Robot
from pathfinding import astar

# --- Helper: A* with blocked items ---


def astar_with_blocks(grid, start, goal, blocked_positions=None):
    from heapq import heappush, heappop
    if blocked_positions is None:
        blocked_positions = []

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []
    heappush(oheap, (fscore[start], start))

    while oheap:
        current = heappop(oheap)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        close_set.add(current)
        for i, j in neighbors:
            neighbor = (current[0]+i, current[1]+j)
            if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]):
                if grid[neighbor[0]][neighbor[1]] == 1 or neighbor in blocked_positions:
                    continue
            else:
                continue

            tentative_g_score = gscore[current] + 1
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, float('inf')):
                continue

            if tentative_g_score < gscore.get(neighbor, float('inf')) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + \
                    heuristic(neighbor, goal)
                heappush(oheap, (fscore[neighbor], neighbor))
    return []

# --- Button Helper ---


def draw_button(screen, rect, text, font, color, hover_color, mouse_pos):
    pygame.draw.rect(screen, hover_color if rect.collidepoint(
        mouse_pos) else color, rect)
    label = font.render(text, True, (255, 255, 255))
    screen.blit(label, (rect.x + 20, rect.y + 10))


# --- Game States ---
STATE_START = 'start'
STATE_SELECT = 'select'
STATE_GAME = 'game'

# --- Main ---


def main():
    pygame.init()
    screen = pygame.display.set_mode(
        (GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)

    state = STATE_START
    selected_color = None
    warehouse = None
    robot = None
    path = []
    step = 0

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # --- State: START SCREEN ---
            elif state == STATE_START:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = STATE_SELECT

            # --- State: COLOR SELECTION ---
            elif state == STATE_SELECT:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if green_btn.collidepoint(mouse_pos):
                        selected_color = 'green'
                        state = STATE_GAME
                    elif blue_btn.collidepoint(mouse_pos):
                        selected_color = 'blue'
                        state = STATE_GAME
                    elif yellow_btn.collidepoint(mouse_pos):
                        selected_color = 'yellow'
                        state = STATE_GAME

                    if state == STATE_GAME:
                        warehouse = Warehouse()
                        robot = Robot()
                        step = 0
                        target_positions = warehouse.get_items_by_color(
                            selected_color)
                        blocked = [pos for c, lst in warehouse.items.items(
                        ) if c != selected_color for pos in lst]
                        robot_pos = (robot.y, robot.x)
                        _, path = next(((pos, astar_with_blocks(warehouse.grid, robot_pos, pos, blocked))
                                        for pos in target_positions if astar_with_blocks(warehouse.grid, robot_pos, pos, blocked)), (None, []))

        # --- Render states ---
        if state == STATE_START:
            label = font.render("Warehouse Bot Simulation",
                                True, (255, 255, 255))
            screen.blit(label, (100, 150))
            start_btn = pygame.Rect(180, 250, 200, 60)
            draw_button(screen, start_btn, "Start", font,
                        (0, 120, 255), (0, 150, 255), mouse_pos)

        elif state == STATE_SELECT:
            label = font.render("Choose item color to pick:",
                                True, (255, 255, 255))
            screen.blit(label, (100, 80))
            green_btn = pygame.Rect(100, 150, 150, 60)
            blue_btn = pygame.Rect(300, 150, 150, 60)
            yellow_btn = pygame.Rect(200, 250, 150, 60)
            draw_button(screen, green_btn, "Green", font,
                        (0, 200, 0), (0, 255, 0), mouse_pos)
            draw_button(screen, blue_btn, "Blue", font,
                        (0, 100, 255), (0, 150, 255), mouse_pos)
            draw_button(screen, yellow_btn, "Yellow", font,
                        (200, 200, 0), (255, 255, 0), mouse_pos)

        elif state == STATE_GAME:
            warehouse.draw(screen)

            # Draw robot as a circle
            center_x = robot.x * CELL_SIZE + CELL_SIZE // 2
            center_y = robot.y * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(screen, ROBOT_COLOR,
                               (center_x, center_y), CELL_SIZE // 3)

            if not robot.carrying and path:
                next_y, next_x = path[step]
                robot.move_to(next_x, next_y)
                step += 1

                if (robot.y, robot.x) in warehouse.get_items_by_color(selected_color):
                    warehouse.remove_item_by_position((robot.y, robot.x))
                    robot.carrying = True
                    print(
                        f"✅ Picked up '{selected_color}' item at ({robot.y}, {robot.x})")

            elif robot.carrying:
                label = font.render(
                    f"🎉 Task complete. Robot got the {selected_color} item.", True, selected_color)
                screen.blit(label, (50, 10))

        pygame.display.flip()
        clock.tick(FPS)

    # pygame.quit()


if __name__ == "__main__":
    main()
