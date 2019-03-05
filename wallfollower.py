#!/usr/bin/env python

import time
import math

import rospy
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan



def wallfollower():
    Running = True;

    sinceLastAlign = 0
    alignToWall()

    tolerance = 10
    tSize = 5
    detectOpening = []

    while Running:
        # Distance from right wall
        newDist = distances[int(90 / angle_increment)]

        # This determines if there is an opening to the right
        if (newDist > median(sorted(detectOpening)) + tolerance) :
            print("Detected opening")
            # Distance will have to be determined through testing
            moveForwardDistance(0.05)
            turnRight(90)
            print("Moving into opening")
            # Distance will have to be determined through testing
            moveForwardDistance(0.05)
            detectOpening = []
        else :
            detectOpening.append(newDist)

        # To keep it from overflowing memory
        if (len(detectOpening > tSize)) :
            detectOpening.pop(0)

        # This aligns regularly
        moveForwardDistance(1)
        alignToWall()



'''
For the beginning, it might be better look to at the back half of the robot to alignToWall, but this
will only work for the beginning.
    -Stephane
'''
def alignToWall():
    minDist = distances[0]
    minDistAngle = 0
    for i in range(int(len(distances) / 4)):
        if distances[i] < minDist:
            minDist = distances[i]
            minDistAngle = angle_increment * i
    if minDistAngle < 90:
        turnLeft(90 - minDistAngle)
    else:
        turnRight(minDistAngle - 90)

def setup():
    rospy.init_node('wallfollower', anonymous=False)
    rospy.Subscriber("/scan", LaserScan, scanHandler)
    vels = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    wallfollower()
    rospy.spin()

# gives list of distances starting from angle 0 to 360, at increment of angle_increment
def scanHandler(scan):
    distances = scan.ranges
    angle_increment = scan.angle_increment

# Moves forward m meters at .20
def moveForwardDistance(distance):
    time = distance / 0.2
    moveForward(0.2)
    #
    rospy.sleep(time)

#SPEED IS IN M/S
def moveForward(speed):
    msg = Twist()
    msg.linear = Vector3(speed, 0, 0)
    msg.angular = Vector3(0, 0, 0)
    vel.publish(msg)

def moveBackward(speed):
    msg = Twist()
    msg.linear = Vector3(-speed, 0, 0)
    msg.angular = Vector3(0, 0, 0)
    vel.publish(msg)

def turnLeft(speed):
    msg = Twist()
    msg.linear = Vector3(0, 0, 0)
    msg.angular = Vector3(0, 0, -speed)
    vel.publish(msg)

def turnRight(speed):
    msg = Twist()
    msg.linear = Vector3(0, 0, 0)
    msg.angular = Vector3(0, 0, speed)
    vel.publish(msg)


if __name__ == '__main__':
    angle_increment = None
    vels = None
    distances = None
    setup()
