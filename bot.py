from game_message import *
from actions import *
from math import atan, sin, cos, asin, atan2, pi, degrees
import random

fileout = open('log.txt', 'w')

class Bot:
    def __init__(self):
        self.shooted = []
        self.direction = 1
        print("Initializing your super mega duper bot")


    def rotate_coords(self, v: Vector, angle: float):
        new_x = v.x * cos(angle) - v.y * sin(angle)
        new_y = -v.x * sin(angle) + v.y * cos(angle)

        return Vector(new_x, new_y)

    def get_shooting_angle(self, cannon_position: Vector, rocket_speed: float, meteor_position: Vector, meteor_velocity: Vector):
        meteor_pos = Vector(meteor_position.x - cannon_position.x, meteor_position.y - cannon_position.y)

        angle_with_x_axis = atan2(meteor_pos.y, meteor_pos.x)

        meteor_pos = self.rotate_coords(meteor_pos, angle_with_x_axis)
        meteor_vel = self.rotate_coords(meteor_velocity, angle_with_x_axis)

        shooting_angle = asin(meteor_vel.y/rocket_speed)


        return shooting_angle+angle_with_x_axis

    def get_next_move(self, game_message: GameMessage):
        meteors = game_message.meteors

        # change origin to be on the cannon
        next_meteor = 0
        #for i in range(len(meteors)):
        #    if meteors[i].id not in self.shooted and game_message.cannon.cooldown == 0:
        #        next_meteor = i
        #        self.shooted.append(meteors[i].id)
        #        break
        #else:
        #    return []

        cannon_position = Vector(game_message.cannon.position.x, -game_message.cannon.position.y)
        rocket_speed = game_message.constants.rockets.speed
        meteor_position = Vector(meteors[next_meteor].position.x, -meteors[next_meteor].position.y)
        meteor_velocity = Vector(meteors[next_meteor].velocity.x, -meteors[next_meteor].velocity.y)

        shooting_angle = self.get_shooting_angle(cannon_position, rocket_speed, meteor_position, meteor_velocity) 
        rotation_angle = degrees(shooting_angle)-game_message.cannon.orientation

        print(game_message.tick, file=fileout)
        print(game_message.meteors, file=fileout)
        print(game_message.rockets, file=fileout)
        print("", file=fileout)

        return [
            RotateAction(angle=rotation_angle),
            ShootAction(),
        ]
