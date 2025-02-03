from utils import image_loader


placeholder = [
    image_loader('Sprite/Temp/placeholder.jpg',flip = False, scale = (30 , 30)),
    image_loader('Sprite/Temp/placeholder2.jpg',flip = False, scale = (30 , 30)),
]


class AnnimationFrame:
    def __init__(self,frame_list = None, interval = 2000):
        self.frame_list = frame_list
        self.current_frame = 0
        self.interval = interval
        self.timer = 0
    def next_frame(self):
        self.timer += 1
        if self.timer < self.interval:
            return  
        if self.current_frame + 1 < len(self.frame_list):
            self.current_frame += 1
        else:
            self.current_frame = 0
        self.timer = 0
    def get_current_frame(self):
        return self.frame_list[self.current_frame]
    def reset_frame(self):
        self.current_frame = 0
        

class PeopleAnimationFrame:
    def __init__(self,spawn_frame = placeholder, idle_frame = None,run_frame = None,dead_frame = None,escape_frame = None):
        self.spawn_frame = AnnimationFrame(spawn_frame)
        self.idle_frame = AnnimationFrame(idle_frame)
        self.run_frame = AnnimationFrame(run_frame)
        self.dead_frame = AnnimationFrame(dead_frame)
        self.escape_frame = AnnimationFrame(escape_frame)
        self.current_frame = self.spawn_frame
    def set_spawn_frame(self):
        self.current_frame = self.spawn_frame
        self.escape_frame.reset_frame()
    def set_idle_frame(self):
        self.current_frame = self.idle_frame
        self.escape_frame.reset_frame()
    def set_run_frame(self):
        self.current_frame = self.run_frame
        self.escape_frame.reset_frame()
    def set_dead_frame(self):
        self.current_frame = self.dead_frame
        self.escape_frame.reset_frame()
    def set_escape_frame(self):
        self.current_frame = self.escape_frame
        self.escape_frame.reset_frame()
    def get_curent_state(self):
        return self.current_frame
        
    

#TODO