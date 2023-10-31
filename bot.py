from game_message import *
from actions import *
from math import atan, sin, cos, asin, atan2, pi, degrees
import random
import numpy as np
from collections import deque
fileout = open('log.txt', 'w')

class Bot:
    def __init__(self):
        self.shooted = []
        self.last_shot_fired_tick = 0
        self.direction = 1
        print("Initializing your super mega duper bot")


    def rotate_coords(self, v: Vector, angle: float):
        new_x = v.x * cos(angle) - v.y * sin(angle)
        new_y = -v.x * sin(angle) + v.y * cos(angle)

        return Vector(new_x, new_y)


    def show_position_at_time(self, cannon_position, rocket_speed, shooting_angle, meteor_position, meteor_velocity, t):
        meteor_pos_x = meteor_position.x + meteor_velocity.x*t
        meteor_pos_y = meteor_position.y + meteor_velocity.y*t

        rocket_pos_x = cannon_position.x + rocket_speed*np.cos(shooting_angle)*t
        rocket_pos_y = cannon_position.y + rocket_speed*np.sin(shooting_angle)*t

        print(f"Time : {t}")
        print(f"Meteor : ({meteor_pos_x}, {meteor_pos_y})")
        print(f"Rocket : ({rocket_pos_x}, {rocket_pos_y})")

    def get_shooting_angle(self, cannon_position: Vector, rocket_speed: float, meteor_position: Vector, meteor_velocity: Vector):
        meteor_pos = Vector(meteor_position.x - cannon_position.x, meteor_position.y - cannon_position.y)

        angle_with_x_axis = np.arctan2(meteor_pos.y, meteor_pos.x)

        meteor_pos = self.rotate_coords(meteor_pos, angle_with_x_axis)
        meteor_vel = self.rotate_coords(meteor_velocity, angle_with_x_axis)

        shooting_angle = np.arcsin(meteor_vel.y/rocket_speed)

        #t = (-meteor_pos.x)/(meteor_vel.x - rocket_speed*np.cos(shooting_angle))

        return shooting_angle+angle_with_x_axis
    def create_queue(self,game_message):
        meteorlist = game_message.meteors
        print(meteorlist)

    def get_shooting_rotation_angle(game_message, next_meteor):
        cannon_position = Vector(game_message.cannon.position.x, -game_message.cannon.position.y)
        rocket_speed = game_message.constants.rockets.speed
        meteor_position = Vector(curently_shot_meteor.position.x, -curently_shot_meteor.position.y)
        meteor_velocity = Vector(curently_shot_meteor.velocity.x, -curently_shot_meteor.velocity.y)

        shooting_angle = -self.get_shooting_angle(cannon_position, rocket_speed, meteor_position, meteor_velocity) 
        rotation_angle = degrees(shooting_angle) - game_message.cannon.orientation

    def get_next_move(self, game_message: GameMessage):
        # va chercher le prochain météor le plus petit sur la liste
        
        meteors = [x for x in game_message.meteors if x.id not in self.shooted]
        next_meteor = 0
        meteors.sort(key=lambda m: m.meteorType, reverse=True) # prend le plus petit meteor sur le jeux
        try:
            curently_shot_meteor = meteors[next_meteor]
        except:
            return []
        
        # trouve l'angle et la rotation du canon pour shoot le meteor choisi
        shooting_angle, rotation_angle = self.get_shooting_rotation_angle(game_message,next_meteor)
        cannon_position = Vector(game_message.cannon.position.x, -game_message.cannon.position.y)
        rocket_speed = game_message.constants.rockets.speed
        meteor_position = Vector(curently_shot_meteor.position.x, -curently_shot_meteor.position.y)
        meteor_velocity = Vector(curently_shot_meteor.velocity.x, -curently_shot_meteor.velocity.y)

        shooting_angle = -self.get_shooting_angle(cannon_position, rocket_speed, meteor_position, meteor_velocity) 
        rotation_angle = degrees(shooting_angle) - game_message.cannon.orientation


        print(f"rotation angle asked = {rotation_angle}", file=fileout)
        print(game_message.tick, file=fileout)
        print(game_message.meteors, file=fileout)
        print(game_message.rockets, file=fileout)
        print(meteor_velocity, file=fileout)
        print("", file=fileout)
        # tire le meteor
        if game_message.tick - self.last_shot_fired_tick > game_message.constants.cannonCooldownTicks:
            self.shooted.append(curently_shot_meteor.id)
            self.last_shot_fired_tick = game_message.tick
            return [
                RotateAction(angle=rotation_angle),
                ShootAction(),
            ]
        else:
            return [
                RotateAction(angle=rotation_angle)
            ]
