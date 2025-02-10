import pygame
from UI import AmmoCounter

class Gun:
    def __init__(self, screen, ammo_capacity):
        self.ammo_capacity = ammo_capacity
        self.current_ammo = ammo_capacity
        self.screen = screen
        self.ammo_counter = AmmoCounter(self.screen, 900, 650, 340, 50, max_ammo=ammo_capacity)

        self.reset_timer = None
        self.waiting_for_reset = False
        self.base_reload_time = 200  # Mỗi viên đạn cần 200ms để reload

        self.font = pygame.font.Font(None, 36)  # Font cho text reload
        self.reload_bar_width = 100
        self.reload_bar_height = 8
        self.reload_bar_x = 950
        self.reload_bar_y = 650

    def get_current_ammo(self):
        return self.current_ammo

    def reload(self):
        if not self.waiting_for_reset:
            bullets_fired = self.ammo_capacity - self.get_current_ammo()  # Số viên đã bắn
            self.reset_delay = bullets_fired * self.base_reload_time  # Tính thời gian reload
            if self.reset_delay == 0:  # Nếu đạn đã đầy, không cần reload
                return
            
            self.reset_timer = pygame.time.get_ticks()
            self.waiting_for_reset = True

    def _complete_reset(self):
        self.current_ammo = self.ammo_capacity
        self.waiting_for_reset = False
        self.reset_timer = None

    def fire(self):
        if not self.waiting_for_reset and self.current_ammo > 0:
            self.current_ammo -= 1
            if self.current_ammo == 0:
                self.reload()
            return True
        return False

    def draw_ammo(self):
        current_time = pygame.time.get_ticks()
        self.ammo_counter.draw(self.current_ammo)

        if self.waiting_for_reset:
            # Hiển thị dòng chữ "Reloading..." với hiệu ứng nhấp nháy
            alpha = abs(255 * (pygame.time.get_ticks() % 1000 / 1000 - 0.5) * 2)  # Nhấp nháy giữa 0-255
            text_surface = self.font.render("Reloading...", True, (255, 255, 255))
            text_surface.set_alpha(int(alpha))  # Thay đổi độ trong suốt
            self.screen.blit(text_surface, (self.reload_bar_x - 20, self.reload_bar_y - 25))

            # Thanh tiến trình
            elapsed_time = current_time - self.reset_timer
            progress = min(1, elapsed_time / self.reset_delay)
            pygame.draw.rect(self.screen, (100, 100, 100), (self.reload_bar_x, self.reload_bar_y, self.reload_bar_width, self.reload_bar_height))
            pygame.draw.rect(self.screen, (192, 192, 192), (self.reload_bar_x, self.reload_bar_y, self.reload_bar_width * progress, self.reload_bar_height))

            if elapsed_time >= self.reset_delay:
                self._complete_reset()
