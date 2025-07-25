from .warehouse import Warehouse
from .robot import Robot
from .pathfinding import astar_with_blocks


class WarehouseSimulator:
    def __init__(self):
        self.reset("green")

    def reset(self, color):
        self.color = color
        self.robot = Robot()
        self.warehouse = Warehouse()
        self.path = []
        self.step_i = 0
        self.state = "searching"

    def step(self):
        if self.state == "done":
            return (self.robot.x, self.robot.y), "done"

        if self.state == "searching":
            if not self.path:
                targets = self.warehouse.get_items_by_color(self.color)
                blocked = [p for c, lst in self.warehouse.items.items(
                ) if c != self.color for p in lst]
                for pos in targets:
                    path = astar_with_blocks(
                        self.warehouse.grid, (self.robot.y, self.robot.x), pos, blocked)
                    if path:
                        self.path = path
                        self.step_i = 0
                        break

            if self.step_i < len(self.path):
                y, x = self.path[self.step_i]
                self.robot.move_to(x, y)
                self.step_i += 1

                if (self.robot.y, self.robot.x) in self.warehouse.get_items_by_color(self.color):
                    self.warehouse.remove_item_by_position(
                        (self.robot.y, self.robot.x))
                    self.state = "done"

        return (self.robot.x, self.robot.y), self.state
