from shapely.geometry.polygon import Polygon
from shapely.affinity import rotate, translate
from pygame import Vector2
import pygame
import numpy as np


class CarDrawer:
    def __init__(self, window_width, window_height, length=55, width=20):
        self.window_width = window_width
        self.window_height = window_height
        self.length = length
        self.width = width
        self.trace = []
        self.init_position = (self.window_width / 2, self.window_height / 2)
        pos_x = self.init_position[0]
        pos_y = self.init_position[1]
        self.r_center = (pos_x, pos_y)

        self.car_model = Polygon([(pos_x - self.length * 2 / 10, pos_y - self.width / 2),
                                  (pos_x - self.length * 2 / 10, pos_y + self.width / 2),
                                  (pos_x + self.length * 8 / 10, pos_y + self.width / 2),
                                  (pos_x + self.length * 8 / 10, pos_y - self.width / 2)])

        self.f_axle =    Polygon([(pos_x + self.length * 6 / 10, pos_y + self.width * 5 / 6),
                                  (pos_x + self.length * 6 / 10, pos_y - self.width * 5 / 6),
                                  (pos_x + self.length * 6 / 10, pos_y + self.width * 5 / 6)])
        self.f_tire_1 =  Polygon([(pos_x + self.length * 4.5 / 10, pos_y + self.width * 5 / 6),
                                  (pos_x + self.length * 4.5 / 10, pos_y + self.width * 7 / 6),
                                  (pos_x + 7.5 / 10 * self.length, pos_y + self.width * 7 / 6),
                                  (pos_x + 7.5 / 10 * self.length, pos_y + self.width * 5 / 6)])
        self.f_tire_2 =  Polygon([(pos_x + self.length * 4.5 / 10, pos_y - self.width * 5 / 6),
                                  (pos_x + self.length * 4.5 / 10, pos_y - self.width * 7 / 6),
                                  (pos_x + 7.5 / 10 * self.length, pos_y - self.width * 7 / 6),
                                  (pos_x + 7.5 / 10 * self.length, pos_y - self.width * 5 / 6)])
        self.r_axle =    Polygon([(pos_x, pos_y + self.width * 5 / 6),
                                  (pos_x, pos_y - self.width * 5 / 6),
                                  (pos_x, pos_y + self.width * 5 / 6)])
        self.r_tire_1 =  Polygon([(pos_x + self.length * 1.5 / 10, pos_y + self.width * 5 / 6),
                                  (pos_x + self.length * 1.5 / 10, pos_y + self.width * 7 / 6),
                                  (pos_x - 1.5 / 10 * self.length, pos_y + self.width * 7 / 6),
                                  (pos_x - 1.5 / 10 * self.length, pos_y + self.width * 5 / 6)])
        self.r_tire_2 =  Polygon([(pos_x + self.length * 1.5 / 10, pos_y - self.width * 5 / 6),
                                  (pos_x + self.length * 1.5 / 10, pos_y - self.width * 7 / 6),
                                  (pos_x - 1.5 / 10 * self.length, pos_y - self.width * 7 / 6),
                                  (pos_x - 1.5 / 10 * self.length, pos_y - self.width * 5 / 6)])

    def draw(self, screen, car, player_car_position):
        car_color = (181, 25, 253)
        angle = - car.angle
        position = (car.position - player_car_position) * 10
        steering = car.steering
        color = car.color


        r_center = (self.window_width / 2 + position.x, self.window_height / 2 + position.y)

        f_axle = translate(self.f_axle, position.x, position.y)
        f_axle = rotate(f_axle, angle, r_center)
        x_axle, y_axle = f_axle.exterior.xy
        pygame.draw.polygon(screen, car_color, [(xx, yy) for xx, yy in zip(x_axle, y_axle)], 2)

        f_tire_1 = translate(self.f_tire_1, position.x, position.y)
        f_tire_1 = rotate(f_tire_1, angle, r_center)
        f_tire_1 = rotate(f_tire_1, - steering, (x_axle[0], y_axle[0]))
        x, y = f_tire_1.exterior.xy
        pygame.draw.polygon(screen, (0, 0, 0), [(xx, yy) for xx, yy in zip(x, y)])

        f_tire_2 = translate(self.f_tire_2, position.x, position.y)
        f_tire_2 = rotate(f_tire_2, angle, r_center)
        f_tire_2 = rotate(f_tire_2, - steering, (x_axle[1], y_axle[1]))
        x, y = f_tire_2.exterior.xy
        pygame.draw.polygon(screen, (0, 0, 0), [(xx, yy) for xx, yy in zip(x, y)])

        r_axle = translate(self.r_axle, position.x, position.y)
        r_axle = rotate(r_axle, angle, r_center)
        x, y = r_axle.exterior.xy
        pygame.draw.polygon(screen, car_color, [(xx, yy) for xx, yy in zip(x, y)], 2)

        r_tire_1 = translate(self.r_tire_1, position.x, position.y)
        r_tire_1 = rotate(r_tire_1, angle, r_center)
        x, y = r_tire_1.exterior.xy
        pygame.draw.polygon(screen, (0, 0, 0), [(xx, yy) for xx, yy in zip(x, y)])

        r_tire_2 = translate(self.r_tire_2, position.x, position.y)
        r_tire_2 = rotate(r_tire_2, angle, r_center)
        x, y = r_tire_2.exterior.xy
        pygame.draw.polygon(screen, (0, 0, 0), [(xx, yy) for xx, yy in zip(x, y)])

        car_model = translate(self.car_model, position.x, position.y)
        car_model = rotate(car_model, angle, r_center)
        x, y = car_model.exterior.xy
        pygame.draw.polygon(screen, color, [(xx, yy) for xx, yy in zip(x, y)])

        rect = pygame.Rect(self.r_center[0], self.r_center[1], 5, 5)
        pygame.draw.rect(screen, (255, 0, 0), rect)


class CarDataDisplay:
    def __init__(self, car, number_of_laps):
        self.car = car
        self.number_of_laps = number_of_laps
        self.current_lap = 1
        self.curr_completion = 100
        self.track_completion = 0

    def display_data(self, screen, position=(0, 0), font='Verdana', size=20):
        font_color = (0, 0, 0)
        font = pygame.font.SysFont(font, size)
        vel_long = font.render('Long velocity: ' + str(round(self.car.velocity.x * 3.6, 2)), False, font_color)
        vel_lat = font.render("Lat velocity: " + str(round(self.car.velocity.y * 3.6, 2)), False, font_color)
        rpm = font.render('Engine RPM: ' + str(round(self.car.wheel_rpm * self.car.diff_ratio * self.car.gears[self.car.gear], 2)),
                          False, font_color)
        gear = font.render('Gear: ' + str(self.car.gear), False, font_color)
        curr_completion = font.render('Current track completion: ' + str(self.curr_completion)[0:3] + '%', False, font_color)
        track_completion = font.render('Lap completion: ' + str(self.track_completion)[0:3] + '%', False, font_color)
        lap = font.render('Lap: ' + str(self.current_lap) + '/' + str(self.number_of_laps), False, font_color)

        screen.blit(vel_long, position)
        screen.blit(vel_lat, (position[0], position[1] + (size * 5 / 4)))
        screen.blit(rpm, (position[0], position[1] + 2 * (size * 5 / 4)))
        screen.blit(gear, (position[0], position[1] + 3 * (size * 5/4)))
        screen.blit(curr_completion, (position[0], position[1] + 4 * (size * 5 / 4)))
        screen.blit(track_completion, (position[0], position[1] + 5 * (size * 5 / 4)))
        screen.blit(lap, (position[0], position[1] + 6 * (size * 5 / 4)))


class TireTracksDrawer:
    def __init__(self, car, window_width, window_height):
        self.car = car
        self.window_width = window_width
        self.window_height = window_height
        self.right_track = []
        self.left_track = []
        self.is_breaking = False
        self.vector = Vector2(0, 20)

    def update(self):
        if self.is_breaking and not self.car.brakes or self.car.velocity.x < 10.5:
            self.right_track = []
            self.left_track = []
            self.is_breaking = False

        if self.car.brakes and self.car.velocity.x > 10.5:
            vector = self.vector.rotate(-self.car.angle)
            self.is_breaking = True
            self.right_track.append(np.array((self.car.position.x * 10, self.car.position.y * 10)) + (vector.x, vector.y))
            self.left_track.append(np.array((self.car.position.x * 10, self.car.position.y * 10)) - (vector.x, vector.y))

    def draw(self, screen, player_car_position):
        left_track_for_drawing = []
        right_track_for_drawing = []
        for left_point, right_point in zip(self.left_track, self.right_track):
            left_track_for_drawing.append(left_point - (player_car_position.x * 10 - self.window_width / 2, player_car_position.y * 10 - self.window_height / 2))
            right_track_for_drawing.append(right_point - (player_car_position.x * 10 - self.window_width / 2, player_car_position.y * 10 - self.window_height / 2))
        if len(left_track_for_drawing) >= 2:
             pygame.draw.lines(screen, (128, 128, 128), False, left_track_for_drawing, 10)
        if len(right_track_for_drawing) >= 2:
            pygame.draw.lines(screen, (128, 128, 128), False, right_track_for_drawing, 10)
