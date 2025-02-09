from UI import AmmoCounter

class Gun:
    def __init__(self, screen, ammo_capacity):
        self.ammo_capacity = ammo_capacity
        self.current_ammo = ammo_capacity
        self.screen = screen
        self.ammo_counter = AmmoCounter(self.screen, 900, 650, 340, 50, max_ammo=10)

    def get_current_ammo(self):
        return self.current_ammo

    def reload(self):
        self.current_ammo = self.ammo_capacity

    def fire(self):
        if self.current_ammo > 0:
            self.current_ammo -= 1
            return True
        return False

    def draw_ammo(self):
        self.ammo_counter.draw(self.current_ammo)
