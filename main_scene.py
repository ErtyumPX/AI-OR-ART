from game import FadeIn, FadeOut, SquareOut, SquareIn, CirclerIn, CirclerOut, HorizontalSlidingOut, HorizontalSlidingIn
from scene import Scene
from renderer import RenderManager
from ui_elements import TextButton, Text, ProcessElements
from glob import glob
from random import choice, randint
import pygame, defaults


class MainScene(Scene):
    def __init__(self, main_surface):
        super().__init__(main_surface)
        self.surface:pygame.Surface = main_surface
        self.render_manager = RenderManager(main_surface, background_color=(240, 89, 7))

        self.ai_images = list()
        for filename in glob('AI_Image/*.jpg'):
            self.ai_images.append(pygame.image.load(filename))
        self.human_images = list()
        for filename in glob('Human_Image/*.jpg'):
            self.human_images.append(pygame.image.load(filename))

        self.used_image_amount = 0
        self.total_image_amount = len(self.human_images) + len(self.ai_images)

        #self.exit_button = TextButton(main_surface, defaults.SIZE[0]-30, 0, 30, 30, func=self.exit_button_func, text='X', font_size=24)
        self.ai_guess_button = TextButton(main_surface, 60, defaults.SIZE[1]/2, 160, 50, func=self.guess_ai, text='AI  <--', font_size=24)
        self.human_guess_button = TextButton(main_surface, defaults.SIZE[0]-220, defaults.SIZE[1]/2, 160, 50, func=self.guess_human, text='-->  HUMAN', font_size=24)
        self.next_button = TextButton(main_surface, defaults.SIZE[0]/2-60, defaults.SIZE[1]-80, 120, 30, func=self.next_image, text='NEXT', font_size=24, status=2)
        self.UI_ELEMENTS = [self.ai_guess_button, self.human_guess_button,self.next_button]
        
        self.render_manager.add_all(self.UI_ELEMENTS)

        DEFAULT_FONT = 'data/munro.ttf'
        self.font = pygame.font.Font(DEFAULT_FONT, 48)
        self.text_box = self.font.render('CORRECT', True, (0, 0, 0))
        self.text_pos = defaults.SIZE[0]/2, defaults.SIZE[1]/2
        self.is_showing_text = False

        self.font = pygame.font.Font(DEFAULT_FONT, 36)
        
        self.streak_text = self.font.render('Streak: 0', True, (0, 0, 0))
        self.streak_pos = 50, 50
        self.current_streak = 0

        self.prize_text = self.font.render('Prize for 7 streaks!', True, (0, 0, 0))


        self.guess_reveal_text = Text(main_surface, text='Correct', font_size=48, status=2) # status:2 means invisible
        self.guess_reveal_text.center(defaults.SIZE[0]/2, defaults.SIZE[1]/2)
        #self.render_manager.add(self.guess_reveal_text)

        self.is_image_ai:bool = None
        self.current_image:pygame.Surface = None
        self.image_pos:tuple = None
        self.get_random_image() # automatically updates image and relavent necessary variables

        FadeIn(self, 40)

    def guess_ai(self) -> None:
        if self.is_image_ai:
            self.guess(True)
        else:
            self.guess(False)
    
    def guess_human(self) -> None:
        if self.is_image_ai:
            self.guess(False)
        else:
            self.guess(True)
    
    def guess(self, is_correct:bool):
        CirclerOut(self, 30)
        self.ai_guess_button.status = 1
        self.human_guess_button.status = 1
        self.guess_reveal_text.status = 0
        self.next_button.status = 0

        text = 'CORRECT' if is_correct else 'WRONG'
        self.text_box = self.font.render(text, True, (0, 0, 0))
        self.text_pos = defaults.SIZE[0]/2 - self.text_box.get_size()[0]/2, 30
        self.is_showing_text = True


        if is_correct:
            self.current_streak += 1
            self.guess_reveal_text.change_text_to("Correct")
        else:
            self.current_streak = 0
            self.guess_reveal_text.change_text_to("Wrong")
        self.streak_text = self.font.render(f'Streak: {self.current_streak}', True, (0, 0, 0))
        CirclerIn(self, 30)

    def next_image(self):
        self.guess_reveal_text.status = 2
        self.is_showing_text = False
        self.next_button.status = 2
        self.ai_guess_button.status = 0
        self.human_guess_button.status = 0
        self.get_random_image()

    def exit_button_func(self) -> None:
        self.next_scene = None

    def get_random_image(self) -> None:
        self.is_image_ai = choice([True, False])
        if self.is_image_ai:
            self.current_image = choice(self.ai_images)
            self.ai_images.remove(self.current_image)
        else:
            self.current_image = choice(self.human_images)
            self.human_images.remove(self.current_image)

        self.image_pos = defaults.SIZE[0]/2 - self.current_image.get_size()[0]/2, defaults.SIZE[1]/2 - self.current_image.get_size()[1]/2

        self.used_image_amount += 1
        if self.used_image_amount == self.total_image_amount:
            self.ai_images.clear()
            for filename in glob('AI_Image/*.jpg'):
                self.ai_images.append(pygame.image.load(filename))
            self.human_images.clear()
            for filename in glob('Human_Image/*.jpg'):
                self.human_images.append(pygame.image.load(filename))


    def process_input(self, events, pressed_keys, mouse_pos):
        ProcessElements(events, pressed_keys, mouse_pos, elements=self.UI_ELEMENTS)

    def update(self):
        pass
    
    def render(self):
        self.render_manager.render()
        self.surface.blit(self.current_image, self.image_pos)
        self.surface.blit(self.streak_text, self.streak_pos)
        self.surface.blit(self.prize_text, (50, 150))
        if self.is_showing_text:
            self.surface.blit(self.text_box, self.text_pos)
