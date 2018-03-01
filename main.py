from random import shuffle

r = 0
c = 0
n = 0
f = 0
b = 0
t = 0


def distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Ride:

    def __init__(self, ride_id, start, finish, time_start, time_finish):
        self.ride_id = ride_id
        self.start = start
        self.finish = finish
        self.time_start = time_start
        self.time_finish = time_finish


class Car:

    def __init__(self, rides):
        self.rides = rides

    def score(self):
        current = Point(0, 0)
        time = 0
        score = 0
        for ride in self.rides:
            arrival = time + distance(ride.start, current)
            finish_time = (ride.time_start if arrival < ride.time_start else arrival) + distance(ride.start, ride.finish)
            if arrival <= ride.time_start:
                score += b
            if finish_time < ride.time_finish:
                score += distance(ride.start, ride.finish)
            current = ride.finish
            time = finish_time
        return score


def partition(lst, n):
    division = len(lst) / float(n)
    return [lst[int(round(division * i)): int(round(division * (i + 1)))] for i in range(n)]


def randomize_cars(rides: list, n_cars):
    shuffle(rides)
    return [Car(rides_p) for rides_p in partition(rides, n_cars)]


class Configuration:

    def __init__(self, cars: list, logFile):
        self.generation = 1
        self.cars = cars
        self.rounds_per_gen = 10
        self.logFile = logFile

    def fitness(self):
        return sum(car.score() for car in self.cars)

    def get_better(self):
        bestfitness = 0
        while self.generation < len(self.cars) - 1:
            for i in range(self.rounds_per_gen):
                self.cars.sort(key=lambda car: car.score(), reverse=True)
                rides_not_optimized = []
                for car in self.cars[self.generation + 1:]:
                    for ride in car.rides:
                        rides_not_optimized.append(ride)
                self.cars[self.generation + 1:] = randomize_cars(rides_not_optimized,
                                                                 len(self.cars) - self.generation - 1)
                fitness = self.fitness()
                if fitness > bestfitness:
                    bestfitness = fitness
                    self.log()
                    print("gen", self.generation, "pop", i, fitness)
            self.generation += 1

    def log(self):
        with open(self.logFile, "w") as out:
            for i, car in enumerate(self.cars):
                out.writelines(
                    str(len(car.rides)) + " " + " ".join(map(lambda ride: str(ride.ride_id), car.rides)) + "\n")


inputf = "e_high_bonus.in"

with open(inputf, "r") as file:
    r, c, f, n, b, t = map(int, file.readline().split(" "))
    rides = []
    print(r, c, f, n, b, t)
    for i in range(n):
        x1, y1, x2, y2, start, fin = map(int, file.readline().split(" "))
        rides.append(Ride(i, Point(x1, y1), Point(x2, y2), start, fin))

    conf = Configuration(randomize_cars(rides, f), inputf + ".out")
    conf.get_better()
