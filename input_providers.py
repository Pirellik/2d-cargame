import pandas as pd
import pygame
from pid_controller import PidController


class InputProvider:
    def get_input(self):
        pass


class RecordedInputProvider(InputProvider):
    def __init__(self, csv_path):
        self.input_dataframe = pd.read_csv(csv_path, index_col=0)
        self.index = self.input_dataframe.first_valid_index()

    def get_input(self):
        if self.index <= self.input_dataframe.last_valid_index():
            throttle = self.input_dataframe.Throttle[self.index]
            brakes = self.input_dataframe.Brakes[self.index]
            steering = self.input_dataframe.Steering[self.index]
            gear = self.input_dataframe.Gear[self.index]
            self.index += 1
            return throttle, gear, brakes, steering


class JoystickInputProvider(InputProvider):
    def __init__(self):
        self.gear = 0
        self.gear_timer = 0
        self.clock = pygame.time.Clock()
        self.joysticks = []
        for i in range(pygame.joystick.get_count()):
            self.joysticks.append(pygame.joystick.Joystick(i))
            self.joysticks[-1].init()
            print("Detected pad:", self.joysticks[-1].get_name())

    def get_input(self):
        self.gear_timer += self.clock.tick()
        throttle = - self.joysticks[-1].get_axis(3)
        steering = - self.joysticks[-1].get_axis(4) * 30
        if self.joysticks[-1].get_axis(2) < - 0.5:
            brakes = - self.joysticks[-1].get_axis(2) * 5000
        else:
            brakes = 0

        if - self.joysticks[-1].get_axis(1) > 0.9 and self.gear < 6 and self.gear_timer > 300:
            self.gear += 1
            self.gear_timer = 0

        elif - self.joysticks[-1].get_axis(1) < -0.9 and self.gear > -1 and self.gear_timer > 300:
            self.gear -= 1
            self.gear_timer = 0

        return throttle, self.gear, brakes, steering


class KeyboardInputProvider(InputProvider):
    def __init__(self):
        pass

    def get_input(self):
        steering = 0

        if pygame.key.get_pressed()[pygame.K_UP]:
            throttle = 1
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            throttle = -1
        else:
            throttle = 0

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            brakes = 1
        else:
            brakes = 0

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            steering = 20

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            steering = -20

        return throttle, brakes, steering


class AutonomousDriver(InputProvider):
    def __init__(self, throttle_factor=5.0):
        self.pid_controller = PidController(2.0, 0.007, 16.5)
        self.line_error = 0
        self.throttle_factor = throttle_factor

    def get_input(self):
        steering = self.pid_controller.get_control(self.line_error)
        if abs(steering) > 1:
            throttle = max(1 / abs(steering), 0.5)
        else:
            throttle = 1
        if abs(steering) > 29.5:
            brakes = 1
        else:
            brakes = 0

        return throttle * self.throttle_factor, brakes, steering
