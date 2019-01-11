from track import *
from physics import Car
from pygame.math import Vector2


class Simulator:
    def __init__(self, window_width, window_height, timeout=60):
        self.timeout = timeout
        self.window_width = window_width
        self.window_height = window_height

    def run(self, dt, path, driver, track, number_of_laps=1, required_completion=80):
        car = Car(self.window_width / 20, self.window_height / 20)
        car.position.x, car.position.y = path.path[0][0] / 10 - self.window_width / 20, path.path[0][1] / 10 - self.window_height / 20
        input_provider = driver
        input_provider.pid_controller.reset()

        for index in range(1, len(track.track_chunks)):
            track.track_chunks[index].is_active = False

        time = 0
        trace = [(car.position.x * 10 + self.window_width / 2, car.position.y * 10 + self.window_height / 2) for _ in range(2)]

        lap = 0
        lap_timer = 3
        completion = 0
        current_completion = 100

        while True:
            time += dt
            lap_timer += dt

            if time > self.timeout:
                break

            # User input
            vector = Vector2(40, 0).rotate(-car.angle)
            vector = np.array((vector.x + self.window_width / 2, vector.y + self.window_height / 2))
            front_center = Point(np.array((car.position.x * 10, car.position.y * 10)) + vector)
            if Polygon(path.path).contains(front_center):
                input_provider.line_error = - LineString(path.path).distance(front_center)
            else:
                input_provider.line_error = LineString(path.path).distance(front_center)

            car_input = input_provider.get_input()
            car.get_driver_input(car_input[0], car_input[1], car_input[2])
            car.update(dt)

            track.check_stain_hitboxes(car)

            trace.pop(1)
            trace.insert(0, (car.position.x * 10 + self.window_width / 2, car.position.y * 10 + self.window_height / 2))

            indexes = track.check_car_position(trace)

            if lap_timer < 3:
                track.track_chunks[-1].is_active = False
                track.track_chunks[-2].is_active = False
                track.track_chunks[-3].is_active = False

            if indexes:
                current_completion = len(indexes) / (indexes[-1] + 1) * 100

            if len(track.track_chunks) - 1 in indexes and lap_timer > 3:
                completion += current_completion
                lap += 1
                lap_timer = 0
                for chunk in track.track_chunks:
                    chunk.is_active = False

            if lap == number_of_laps:
                break

        completion = completion / number_of_laps

        if completion >= 80 and time < self.timeout:
            return time
        else:
            return 99999


