class Scene:
    def __init__(self, surface):
        self.surface = surface
        self.next_scene = self

    def process_input(self, events, pressed_keys, mouse_pos):
        pass
    
    def update(self):
        pass
    
    def render(self):
        pass

    def terminate(self):
        self.next_scene = None