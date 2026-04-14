import arcade
import game_core
import threading
import time
import os
import pygame


class Agent(threading.Thread):

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

        self.game = []
        self.move_grid = []
        self.kill_grid = []
        self.isGameClear = False
        self.isGameOver = False
        self.current_stage = 0
        self.time_limit = 0
        self.total_score = 0
        self.total_time = 0
        self.total_life = 0
        self.tanuki_r = 0
        self.tanuki_c = 0
        self.screen = None
        self.win = None
        self.backscreen = None
        self.arr = None
        self.grid_visible = False

    #############################################################
    #      YOUR SUPER COOL ARTIFICIAL INTELLIGENCE HERE!!!      #
    #############################################################
    def ai_function(self):
        # To send a key stroke to the game, use self.game.on_key_press() method
        return

    def run(self):
        print("Starting " + self.name)

        # roughly every 50 milliseconds, retrieve game state (average human response time for visual stimuli = 25 ms)
        go = True
        while go:
            # RETRIEVE CURRENT GAME STATE
            self.move_grid, self.kill_grid, \
                self.isGameClear, self.isGameOver, go, self.current_stage, self.time_limit, \
                self.total_score, self.total_time, self.total_life, self.tanuki_r, self.tanuki_c \
                = self.game.get_game_state()

            self.ai_function()

            # We must allow enough CPU time for the main game application
            # Polling interval can be reduced if you don't display the grid information
            time.sleep(0.05)

        print("Exiting " + self.name)


def pygame_update(dt, ag):
    screen_size = [400, 240]

    # Sync window visibility with game flag (only call show/hide on transitions)
    if ag.game.show_grid_display != ag.grid_visible:
        ag.grid_visible = ag.game.show_grid_display
        if ag.grid_visible:
            ag.win.show()
            ag.game.activate()  # return keyboard focus to arcade window
        else:
            ag.win.hide()

    # Render grid information when window is visible
    if ag.grid_visible and ag.move_grid and ag.kill_grid:
        for row in range(12):
            for col in range(20):
                c = ag.move_grid[row][col] * 255 / 12
                ag.arr[col, row] = (c, c, c)
            for col in range(20, 40):
                if ag.kill_grid[row][col-20]:
                    ag.arr[col, row] = (255, 0, 0)
                else:
                    ag.arr[col, row] = (255, 255, 255)

        pygame.transform.scale(ag.backscreen, screen_size, ag.screen)
        pygame.display.flip()


def main():
    ag = Agent(1, "My Agent", 1)

    ag.game = game_core.GameMain()
    ag.game.set_location(50, 50)

    # Uncomment below for recording
    # ag.game.isRecording = True
    # ag.game.replay('replay.rpy')  # You can specify replay file name or it will be generated using timestamp

    # Uncomment below to replay recorded play
    # ag.game.isReplaying = True
    # ag.game.replay('replay.rpy')

    ag.game.reset()

    # Initialize pygame and create window on the main thread (required on macOS)
    screen_size = [400, 240]
    backscreen_size = [40, 12]
    pygame.init()
    ag.screen = pygame.display.set_mode(screen_size, pygame.HIDDEN)
    ag.win = pygame.Window.from_display_module()
    # place immediately right of arcade window (consider 150% magnification)
    ag.win.position = (50 + game_core.SCREEN_W*2, 50)
    ag.backscreen = pygame.Surface(backscreen_size)
    ag.arr = pygame.PixelArray(ag.backscreen)

    # Schedule pygame rendering on the main thread (required on macOS)
    arcade.schedule(lambda dt: pygame_update(dt, ag), 0.05)

    ag.daemon = True
    ag.start()
    arcade.run()
    ag.join(timeout=0.2)


if __name__ == "__main__":
    main()
