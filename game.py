from drawing import *
from physics import *
from input_providers import *
from track import *
from shapely.geometry import Point, Polygon, LineString
from random import random
from simulator import Simulator
from threading import Thread
import sys

simulations_finished = False
sim_times = []


def simulate_bots(window_width, window_height, track, paths, autonomous_drivers, dt, number_of_laps):
    global simulations_finished
    global sim_times
    sim = Simulator(window_width, window_height)
    for path, driver in zip(paths, autonomous_drivers):
        sim_times.append(sim.run(dt, path, driver, track, number_of_laps))
    simulations_finished = True


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    def set_location(self, location):
        self.rect.left, self.rect.top = location


class Game:
    def __init__(self, width, height):
        pygame.init()
        pygame.display.set_caption("2D CARGAME")
        pygame.font.init()
        self.window_width = width
        self.window_height = height
        self.screen = pygame.display.set_mode((width, height))
        self.fps = 20
        self.background = Background('BlueCheckerPatternPaper.png', [0, 0])
        self.car_engine_effect = pygame.mixer.Sound('car_engine_sound.ogg')
        self.braking_effect = pygame.mixer.Sound('braking.ogg')

        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

    def run(self):
        exit = False
        while not exit:
            option = self.main_menu()
            if option == "singleplayer":
                self.countdown()
                results = self.run_singleplayer()
                while self.display_results(results):
                    self.countdown()
                    results = self.run_singleplayer()
            elif option == "multiplayer":
                pygame.quit()
                exit = True
            else:
                pygame.quit()
                exit = True

    def display_results(self, results):
        font_size = int(self.window_height / 18)
        font = pygame.font.SysFont('Verdana', font_size, True, True)
        title = font.render('Time results', False, (0, 0, 0))
        title_size = title.get_rect()
        results_font_size = int(self.window_height / 27)
        results_font = pygame.font.SysFont('Verdana', results_font_size, True, True)
        green = (0, 200, 0)
        bright_green = (0, 255, 0)
        red = (200, 0, 0)
        bright_red = (255, 0, 0)
        button_size = (int(self.window_width / 5), int(self.window_height / 15))
        button_font = pygame.font.SysFont('Verdana', results_font_size, True, True)
        play_again_text = button_font.render('PLAY AGAIN', False, (255, 255, 255))
        back_to_menu_text = button_font.render('BACK TO MENU', False, (255, 255, 255))
        play_again_text_size = play_again_text.get_rect()
        back_to_menu_text_size = back_to_menu_text.get_rect()

        for index in range(1, len(results)):
            current_index = index
            while current_index > 0 and results[current_index][1] < results[current_index - 1][1]:
                results[current_index], results[current_index - 1] = results[current_index - 1], results[current_index]
                current_index -= 1

        result_texts = []
        for result in results:
            if result[1] > 99000:
                result_texts.append(results_font.render(result[0] + '   disqualified', False, (255, 0, 0)))
            elif result[0] == 'You     ':
                result_texts.append(results_font.render(result[0] + '   ' + str(result[1])[0:5] + ' sec', False, (0, 185, 0)))
            else:
                result_texts.append(results_font.render(result[0] + '   ' + str(result[1])[0:5] + ' sec', False, (255, 165, 0)))

        while True:
            self.clock.tick(15)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0, 0, 0))
            self.background.set_location([0, 0])
            self.screen.blit(self.background.image, self.background.rect)
            self.background.set_location([1200, 0])
            self.screen.blit(self.background.image, self.background.rect)
            self.screen.blit(title, ((self.window_width - title_size.width) / 2, self.window_height / 5))
            for index, text in enumerate(result_texts):
                self.screen.blit(text, ((self.window_width - title_size.width) / 2, self.window_height / 5 + title_size.height * 1.5 + index * title_size.height))

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if Polygon([((self.window_width - button_size[0]) / 2, self.window_height / 5 + title_size.height * 1.5 + 5.5 * title_size.height),
                        ((self.window_width - button_size[0]) / 2 + button_size[0], self.window_height / 5 + title_size.height * 1.5 + 5.5 * title_size.height),
                        ((self.window_width - button_size[0]) / 2 + button_size[0], self.window_height / 5 + title_size.height * 1.5 + 5.5 * title_size.height + button_size[1]),
                        ((self.window_width - button_size[0]) / 2, self.window_height / 5 + title_size.height * 1.5 + 5.5 * title_size.height + button_size[1])]).contains(Point(mouse)):
                pygame.draw.rect(self.screen, bright_green, ((self.window_width - button_size[0]) / 2, self.window_height / 5 + title_size.height * 1.5 + 5.5 * title_size.height, button_size[0], button_size[1]))
                if click[0]:
                    play_again = True
                    break
            else:
                pygame.draw.rect(self.screen, green, ((self.window_width - button_size[0]) / 2, self.window_height / 5 + title_size.height * 1.5 + 5.5 * title_size.height, button_size[0], button_size[1]))

            if Polygon([((self.window_width - button_size[0]) / 2, self.window_height / 5 + title_size.height * 1.5 + 7 * title_size.height),
                        ((self.window_width - button_size[0]) / 2 + button_size[0], self.window_height / 5 + title_size.height * 1.5 + 7 * title_size.height),
                        ((self.window_width - button_size[0]) / 2 + button_size[0], self.window_height / 5 + title_size.height * 1.5 + 7 * title_size.height + button_size[1]),
                        ((self.window_width - button_size[0]) / 2, self.window_height / 5 + title_size.height * 1.5 + 7 * title_size.height + button_size[1])]).contains(Point(mouse)):
                pygame.draw.rect(self.screen, bright_red, ((self.window_width - button_size[0]) / 2, self.window_height / 5 + title_size.height * 1.5 + 7 * title_size.height, button_size[0], button_size[1]))
                if click[0]:
                    play_again = False
                    break
            else:
                pygame.draw.rect(self.screen, red, ((self.window_width - button_size[0]) / 2, self.window_height / 5 + title_size.height * 1.5 + 7 * title_size.height, button_size[0], button_size[1]))

            self.screen.blit(play_again_text, ((self.window_width - play_again_text_size.width) / 2, self.window_height / 5 + title_size.height * 1.5 + 5.5 * title_size.height + button_size[1] / 2 - play_again_text_size.height / 2))
            self.screen.blit(back_to_menu_text, ((self.window_width - back_to_menu_text_size.width) / 2, self.window_height / 5 + title_size.height * 1.5 + 7 * title_size.height + button_size[1] / 2 - back_to_menu_text_size.height / 2))

            pygame.display.flip()

        return play_again

    def main_menu(self, font_name='Verdana'):
        title_font_size = int(self.window_height / 9)
        button_font_size = int(title_font_size / 3)
        logo = pygame.image.load('logo.png')
        org_size = logo.get_rect()
        logo = pygame.transform.scale(logo, (int(org_size.width / (1366 / self.window_width)), int(org_size.height / (1366 / self.window_width))))
        logo_rect = logo.get_rect()
        logo_rect.left = (self.window_width - logo_rect.width) / 2
        logo_rect.top = logo_rect.height / 2
        font_color = (0, 0, 0)
        title_font = pygame.font.SysFont(font_name, title_font_size, True, True)
        button_font = pygame.font.SysFont(font_name, button_font_size, True, True)
        title = title_font.render('2D CARGAME', False, font_color)
        title_size = title.get_rect()
        green = (0, 200, 0)
        red = (200, 0, 0)
        blue = (0, 0, 200)
        bright_green = (0, 255, 0)
        bright_red = (255, 0, 0)
        bright_blue = (0, 0, 255)
        button_size = (int(self.window_width / 4), int(self.window_height / 15))
        padding = int(self.window_height / 7)
        singleplayer_text = button_font.render('SINGLEPLAYER', False, (255, 255, 255))
        singleplayer_text_size = singleplayer_text.get_rect()
        multiplayer_text = button_font.render('MULTIPLAYER', False, (255, 255, 255))
        multiplayer_text_size = multiplayer_text.get_rect()
        quit_text = button_font.render('QUIT', False, (255, 255, 255))
        quit_text_size = quit_text.get_rect()

        option = None

        while True:
            self.clock.tick(15)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0, 0, 0))
            self.background.set_location([0, 0])
            self.screen.blit(self.background.image, self.background.rect)
            self.background.set_location([1200, 0])
            self.screen.blit(self.background.image, self.background.rect)
            self.screen.blit(logo, logo_rect)
            self.screen.blit(title, (self.window_width / 2 - title_size.width / 2, logo_rect.height + title_size.height))

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if Polygon([((self.window_width - button_size[0]) / 2, logo_rect.height + title_size.height + padding),
                        ((self.window_width - button_size[0]) / 2 + button_size[0], logo_rect.height + title_size.height + padding),
                        ((self.window_width - button_size[0]) / 2 + button_size[0], logo_rect.height + title_size.height + padding + button_size[1]),
                        ((self.window_width - button_size[0]) / 2, logo_rect.height + title_size.height + padding + button_size[1])]).contains(Point(mouse)):
                pygame.draw.rect(self.screen, bright_green, ((self.window_width - button_size[0]) / 2, logo_rect.height + title_size.height + padding, button_size[0], button_size[1]))
                if click[0]:
                    option = "singleplayer"
                    break
            else:
                pygame.draw.rect(self.screen, green, ((self.window_width - button_size[0]) / 2, logo_rect.height + title_size.height + padding, button_size[0], button_size[1]))

            if Polygon([((self.window_width - button_size[0]) / 2, logo_rect.height + title_size.height + 2 * padding),
                        ((self.window_width - button_size[0]) / 2 + button_size[0], logo_rect.height + title_size.height + 2 * padding),
                        ((self.window_width - button_size[0]) / 2 + button_size[0], logo_rect.height + title_size.height + 2 * padding + button_size[1]),
                        ((self.window_width - button_size[0]) / 2, logo_rect.height + title_size.height + 2 * padding + button_size[1])]).contains(Point(mouse)):
                pygame.draw.rect(self.screen, bright_blue, ((self.window_width - button_size[0]) / 2, logo_rect.height + title_size.height + 2 * padding, button_size[0], button_size[1]))
                if click[0]:
                    option = "multiplayer"
                    break
            else:
                pygame.draw.rect(self.screen, blue, ((self.window_width - button_size[0]) / 2, logo_rect.height + title_size.height + 2 * padding, button_size[0], button_size[1]))

            if Polygon([((self.window_width - button_size[0]) / 2, logo_rect.height + title_size.height + 3 * padding),
                        ((self.window_width - button_size[0]) / 2 + button_size[0], logo_rect.height + title_size.height + 3 * padding),
                        ((self.window_width - button_size[0]) / 2 + button_size[0], logo_rect.height + title_size.height + 3 * padding + button_size[1]),
                        ((self.window_width - button_size[0]) / 2, logo_rect.height + title_size.height + 3 * padding + button_size[1])]).contains(Point(mouse)):
                pygame.draw.rect(self.screen, bright_red, ((self.window_width - button_size[0]) / 2, logo_rect.height + title_size.height + 3 * padding, button_size[0], button_size[1]))
                if click[0]:
                    option = "quit"
                    break
            else:
                pygame.draw.rect(self.screen, red, ((self.window_width - button_size[0]) / 2, logo_rect.height + title_size.height + 3 * padding, button_size[0], button_size[1]))

            self.screen.blit(singleplayer_text, ((self.window_width - singleplayer_text_size.width) / 2, logo_rect.height + title_size.height + padding + button_size[1] / 2 - singleplayer_text_size.height / 2))
            self.screen.blit(multiplayer_text, ((self.window_width - multiplayer_text_size.width) / 2, logo_rect.height + title_size.height + 2 * padding + button_size[1] / 2 - multiplayer_text_size.height / 2))
            self.screen.blit(quit_text, ((self.window_width - quit_text_size.width) / 2, logo_rect.height + title_size.height + 3 * padding + button_size[1] / 2 - quit_text_size.height / 2))

            pygame.display.flip()

        return option

    def waiting_screeen(self):
        global simulations_finished
        font_size = int(self.window_height / 9)
        font = pygame.font.SysFont('Verdana', font_size, True, True)
        text = font.render('Preparing results...', False, (0, 0, 0))
        text_size = text.get_rect()

        while not simulations_finished:
            self.clock.tick(15)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0, 0, 0))
            self.background.set_location([0, 0])
            self.screen.blit(self.background.image, self.background.rect)
            self.background.set_location([1200, 0])
            self.screen.blit(self.background.image, self.background.rect)
            self.screen.blit(text, ((self.window_width - text_size.width) / 2, (self.window_height - text_size.height) / 2))

            pygame.display.flip()
        simulations_finished = False

    def countdown(self, font='Verdana', size=100):
        font_color = (0, 0, 0)
        font = pygame.font.SysFont(font, size)
        time = 0
        counter = 3
        pygame.mixer.music.load('countdown.wav')
        pygame.mixer.music.play()
        while counter >= 0:
            dt = self.clock.tick(self.fps) / 1000
            time += dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if time > 1:
                time = 0
                counter -= 1
            self.screen.fill((0, 0, 0))
            if counter < 1:
                count = font.render("START!", False, font_color)
            else:
                count = font.render(str(counter), False, font_color)
            text_size = count.get_rect()
            self.background.set_location([0, 0])
            self.screen.blit(self.background.image, self.background.rect)
            self.background.set_location([1200, 0])
            self.screen.blit(self.background.image, self.background.rect)
            self.screen.blit(count, (self.window_width / 2 - text_size.width / 2, self.window_height / 2 - text_size.height / 2))
            pygame.display.flip()

    def run_singleplayer(self, track='track3.svg', number_of_opponents=4, number_of_laps=3):
        player_car = Car(self.window_width / 20, self.window_height / 20)
        track = Track(self.window_width, self.window_height, track)
        opponent_cars = []
        autonomous_drivers = []
        paths = []
        for _ in range(number_of_opponents):
            opponent_cars.append(Car(self.window_width / 20, self.window_height / 20, color=(random()*255, random()*255, random()*255)))
            autonomous_drivers.append(AutonomousDriver(random() * 2 + 6))
            paths.append(Path(track.inner_edge, track.outer_edge))
            paths[-1].randomly_modify_path()

        track_drawer = TrackDrawer(track)
        player_car.position.x, player_car.position.y = track.path[0][0] / 10 - self.window_width / 20, track.path[0][1] / 10 - self.window_height / 20
        for index, car in enumerate(opponent_cars):
            car.position.x, car.position.y = paths[index].path[0][0] / 10 - self.window_width / 20, paths[index].path[0][1] / 10 - self.window_height / 20
        car_drawer = CarDrawer(self.window_width, self.window_height)
        trace = [(player_car.position.x * 10 + self.window_width / 2, player_car.position.y * 10 + self.window_height / 2) for _ in range(2)]
        car_data_display = CarDataDisplay(player_car, number_of_laps)
        input_provider = JoystickInputProvider()

        if not input_provider.joysticks:
            input_provider = KeyboardInputProvider()

        tire_tracks_drawer = TireTracksDrawer(player_car, self.window_width, self.window_height)
        opp_tire_tracks_drawers = []
        for car in opponent_cars:
            opp_tire_tracks_drawers.append(TireTracksDrawer(car, self.window_width, self.window_height))

        pygame.mixer.music.load('cars.mp3')
        pygame.mixer.music.play(-1)
        engine_sound_stopped = True
        braking_sound_stopped = True

        lap = 0
        lap_timer = 3
        time = 0
        dt = 1 / self.fps
        completion = 0

        while True:
            self.clock.tick(self.fps)
            lap_timer += dt
            time += dt

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # User input
            player_car_input = input_provider.get_input()
            if not player_car_input[0]:
                self.car_engine_effect.stop()
                engine_sound_stopped = True
            if engine_sound_stopped and player_car_input[0]:
                self.car_engine_effect.play(-1)
                engine_sound_stopped = False
            if not player_car_input[1] or player_car.velocity.x < 5.5:
                self.braking_effect.stop()
                braking_sound_stopped = True
            if braking_sound_stopped and player_car_input[1] and player_car.velocity.x >= 5.5:
                self.braking_effect.play(-1)
                braking_sound_stopped = False

            player_car.get_driver_input(player_car_input[0], player_car_input[1], player_car_input[2])
            player_car.update(dt)

            for index, car in enumerate(opponent_cars):
                # Calculating position of a front center of a car
                vector = Vector2(40, 0).rotate(-car.angle)
                vector = np.array((vector.x + self.window_width / 2, vector.y + self.window_height / 2))
                front_center = Point(np.array((car.position.x * 10, car.position.y * 10)) + vector)

                # Calculating line error as a distance from front center to a given line (path)
                if Polygon(paths[index].path).contains(front_center):
                    autonomous_drivers[index].line_error = - LineString(paths[index].path).distance(front_center)
                else:
                    autonomous_drivers[index].line_error = LineString(paths[index].path).distance(front_center)

                # Input from PID controller
                opponent_car_input = autonomous_drivers[index].get_input()
                if car.velocity.x < 50/3.6:
                    car.get_driver_input(opponent_car_input[0], 0, opponent_car_input[2])
                else:
                    car.get_driver_input(opponent_car_input[0], opponent_car_input[1], opponent_car_input[2])
                car.update(dt)

            track.check_stain_hitboxes(player_car)
            for car in opponent_cars:
                track.check_stain_hitboxes(car)

            # Updating trace
            trace.pop(1)
            trace.insert(0, (player_car.position.x * 10 + self.window_width / 2, player_car.position.y * 10 + self.window_height / 2))

            tire_tracks_drawer.update()
            for drawer in opp_tire_tracks_drawers:
                drawer.update()

            if lap_timer < 3:
                track.track_chunks[-1].is_active = False
                track.track_chunks[-2].is_active = False
                track.track_chunks[-3].is_active = False

            chunk_indexes = track.check_car_position(trace)
            if chunk_indexes:
                car_data_display.curr_completion = len(chunk_indexes) / (chunk_indexes[-1] + 1) * 100
                car_data_display.track_completion = len(chunk_indexes) / len(track.track_chunks) * 100

            if len(track.track_chunks) - 1 in chunk_indexes and lap_timer > 3:
                lap += 1
                lap_timer = 0
                for chunk in track.track_chunks:
                    chunk.is_active = False
                completion += car_data_display.curr_completion


            car_data_display.current_lap = lap + 1


            # Drawing
            self.screen.fill((0, 0, 0))
            self.background.set_location([- player_car.position.x * 10, 768 - player_car.position.y * 10])
            self.screen.blit(self.background.image, self.background.rect)
            self.background.set_location([1200 - player_car.position.x * 10, 768 - player_car.position.y * 10])
            self.screen.blit(self.background.image, self.background.rect)
            self.background.set_location([2400 - player_car.position.x * 10, 768 - player_car.position.y * 10])
            self.screen.blit(self.background.image, self.background.rect)
            self.background.set_location([- player_car.position.x * 10, 768 + 1200 - player_car.position.y * 10])
            self.screen.blit(self.background.image, self.background.rect)
            self.background.set_location([1200 - player_car.position.x * 10, 768 + 1200 - player_car.position.y * 10])
            self.screen.blit(self.background.image, self.background.rect)
            self.background.set_location([2400 - player_car.position.x * 10, 768 + 1200 - player_car.position.y * 10])
            self.screen.blit(self.background.image, self.background.rect)
            self.background.set_location([- player_car.position.x * 10, 768 + 2400 - player_car.position.y * 10])
            self.screen.blit(self.background.image, self.background.rect)
            self.background.set_location([1200 - player_car.position.x * 10, 768 + 2400 - player_car.position.y * 10])
            self.screen.blit(self.background.image, self.background.rect)
            self.background.set_location([2400 - player_car.position.x * 10, 768 + 2400 - player_car.position.y * 10])
            self.screen.blit(self.background.image, self.background.rect)
            track_drawer.draw(self.screen, player_car.position * 10, chunk_indexes)
            tire_tracks_drawer.draw(self.screen, player_car.position)
            for drawer in opp_tire_tracks_drawers:
                drawer.draw(self.screen, player_car.position)
            car_data_display.display_data(self.screen)

            for car in opponent_cars:
                car_drawer.draw(self.screen, car, player_car.position)

            car_drawer.draw(self.screen, player_car, player_car.position)

            pygame.display.flip()

            if lap == number_of_laps:
                break

        completion = completion / number_of_laps
        pygame.mixer.music.stop()
        self.car_engine_effect.stop()
        self.braking_effect.stop()
        for index in range(1, len(track.track_chunks)):
            track.track_chunks[index].is_active = False
        times = []
        if completion > 80:
            times.append(('You     ', time))
        else:
            times.append(('You     ', 99999))
        sim_thread = Thread(target=simulate_bots, args=[self.window_width, self.window_height, track, paths, autonomous_drivers, dt, number_of_laps])
        sim_thread.start()
        self.waiting_screeen()
        sim_thread.join()
        global sim_times
        for index, time in enumerate(sim_times):
            times.append(('Player ' + str(index + 1), time))

        sim_times = []

        return times


if __name__ == '__main__':
    game = Game(1366, 768)
    game.run()
