
class AnimationFrame:
    def __init__(self,spawn_frame,idle_frame,run_frame,dead_frame,escape_frame):
        self.spawn_frame = spawn_frame
        self.idle_frame = idle_frame
        self.run_frame = run_frame
        self.dead_frame = dead_frame
        self.escape_frame = escape_frame
    def get_spawn_frame(self):
        return self.spawn_frame
    def get_idle_frame(self):
        return self.idle_frame
    def get_run_frame(self):
        return self.run_frame
    def get_dead_frame(self):
        return self.dead_frame
    def get_escape_frame(self):
        return self.escape_frame
    
#TODO