#!/usr/bin/env python3

import rclpy # Python Client Library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from geometry_msgs.msg import Twist
import numpy as np
from cv_bridge import CvBridge # ROS2 package to convert between ROS and OpenCV Images
import cv2 # Python OpenCV library

def default_view():
    img = np.zeros((300,600,3), np.uint8)
    cv2.line(img,(200,0),(200,600),(240,32,160),4)
    cv2.line(img,(400,0),(400,600),(240,32,160),4)
    cv2.line(img,(0,100),(600,100),(240,32,160),4)
    cv2.line(img,(0,200),(600,200),(240,32,160),4)
    cv2.putText(img, 'X<0 R_S<0', (40,50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 60, 40), 1, cv2.LINE_AA)
    cv2.putText(img, 'X=0 R_S<0', (230,50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 60, 40), 1, cv2.LINE_AA)
    cv2.putText(img, 'X>0 R_S<0', (450,50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 60, 40), 1, cv2.LINE_AA)

    cv2.putText(img, 'X<0 R_S=0', (40,150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 60, 40), 1, cv2.LINE_AA)
    cv2.putText(img, 'X=0 R_S=0', (230,150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 60, 40), 1, cv2.LINE_AA)
    cv2.putText(img, 'X>0 R_S=0', (450,150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 60, 40), 1, cv2.LINE_AA)
    
    cv2.putText(img, 'X<0 R_S>0', (40,250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 60, 40), 1, cv2.LINE_AA)
    cv2.putText(img, 'X=0 R_S>0', (230,250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 60, 40), 1, cv2.LINE_AA)
    cv2.putText(img, 'X>0 R_S>0', (450,250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 60, 40), 1, cv2.LINE_AA)
    
    return img

default_img = default_view()
X_speed=0.0
Rotate_speed=0.0
class Publisher(Node):
    def __init__(self):
        super().__init__('pub')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 1)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def draw_circle(self, event, x, y, flags, param):
        global default_img, X_speed, Rotate_speed

        if event == cv2.EVENT_LBUTTONDOWN: 
            default_img = default_view()
            cv2.circle(default_img, (x, y), 10, (53,28,100), -1) 
            if x < 200:
                X_speed = -1.0
            if x > 400:
                X_speed = 1.0
            if x >= 200 and x <= 400:
                X_speed = 0.0
            if y < 100:
                Rotate_speed = -1.0
            if y > 200:
                Rotate_speed = 1.0
            if y >= 100 and y <= 200:
                Rotate_speed = 0.0

    def timer_callback(self):
        global default_img, X_speed

        pure_fun = Twist()
        pure_fun.linear.x = X_speed
        pure_fun.linear.y = 0.0
        pure_fun.linear.z = 0.0
        
        pure_fun.angular.x = 0.0  
        pure_fun.angular.y = 0.0  
        pure_fun.angular.z = Rotate_speed   
        self.publisher_.publish(pure_fun)

        print(X_speed)

        # cv2.namedWindow("Projekt_Turtlesim")
        # cv2.setMouseCallback('Projekt_Turtlesim', self.draw_circle)
        cv2.imshow('Projekt_Turtlesim', default_img)
        cv2.setMouseCallback('Projekt_Turtlesim', self.draw_circle)

        self.get_logger().info(f'ACTUAL SPEED: {X_speed}')
        self.get_logger().info(f'Rotate SPEED: {Rotate_speed}')
        self.i += 1

        cv2.waitKey(1)       


def main(args=None):
    rclpy.init(args=args)

    pub = Publisher()
    rclpy.spin(pub)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

