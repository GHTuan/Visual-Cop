
class Gun():
    def __init__(self, ammo_capacity):
        self.ammo_capacity = ammo_capacity
        self.current_ammo = ammo_capacity
    def get_current_ammo(self):
        return self.current_ammo
    def reload(self):
        self.current_ammo = self.ammo_capacity
    def fire(self):
        if self.current_ammo > 0:
            self.current_ammo = self.current_ammo - 1
            return True
        return False
        