class Information:
    def __init__(self, start_time, screen, font, text_color, background_color):
        self.start_time = start_time  # Total time in seconds
        self.screen = screen  # Pygame display surface
        self.font = font  # Font for timer text
        self.text_color = text_color  # Color of timer text
        self.background_color = background_color  # Color of timer background

        self.remaining_time = self.start_time  # Remaining time in seconds

    def update(self):
        # Decrement the remaining time
        self.remaining_time -= 1

        # Stop the timer when it reaches zero
        if self.remaining_time <= 0:
            self.remaining_time = 0

    def render(self):
        # Create a text surface with the remaining time
        timer_text = self.font.render(str(self.remaining_time), True, self.text_color, self.background_color)

        # Get the text rectangle
        text_rect = timer_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        # Blit the text onto the screen
        self.screen.blit(timer_text, text_rect)
