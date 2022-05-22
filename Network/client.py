from UI.canvas import Canvas
from UI.button import Button
from UI.input_box import InputBox
from UI.text_box import TextBox
from UI.chat_box import ChatBox
from UI.timer import Timer
from NeuralNetwork.model import Model
from file_parser import FileParser

import socket
import pygame
import threading
import time
import os
import numpy as np
import Network.netlib as netlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 8080
PRINT_DEBUG = True



def build_app():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Scribble')

    screen = pygame.display.set_mode((1200, 800))
    screen.fill((122, 122, 122))

    logo = pygame.image.load('images/logo.png')
    screen.blit(logo, ((1200 - 338) // 2, 10))

    canvas = Canvas(screen, 100, 150, 650, 500)
    file_parser = FileParser()
    ai =Model(None, None, None, None)
    ai.load("NeuralNetwork/Models/10_85.pkl")

    img = pygame.image.load("images/eraser.png")
    ui_elements = [
        Button((800, 610, 100, 40), image=img, color=(235, 232, 232), hover_color=(196, 191, 191),
               on_click=canvas.fill),
        InputBox((800, 500, 300, 40)),
        Timer((1000, 610, 100, 40), '00h:01m:05s', color=(125, 125, 125), text_color=(100, 255, 100), border_width=0)
    ]

    clock = pygame.time.Clock()
    clock.tick(60)

    return screen, canvas, clock, ui_elements, file_parser, ai


class Client:

    def __init__(self, ip, port):

        self.IP = SERVER_IP
        self.PORT = SERVER_PORT

        self.run_ai = True
        self.socket = None

        self.name = ""

        self.to_draw = None
        self.score = 0

    @staticmethod
    def error():
        exit()

    def connect(self):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.IP, self.PORT))

        if PRINT_DEBUG:
            print("Connected to Server")

    def send_message(self, code, data):
        """
            Builds a new message using chatlib, wanted code and message.
            Prints debug info, then sends it to the given socket.
            Paramaters: conn (socket object), code (str), data (str)
            Returns: Nothing
        """
        message = netlib.pack_message(code, data)

        if message:
            self.socket.send(message.encode())

    def receive_message(self):
        message = self.socket.recv(1024).decode()
        code, data = netlib.unpack_message(message)
        return code, data

    def send_and_receive(self, code, data):
        self.send_message(code, data)
        return self.receive_message()

    def login(self, username):
        code, data = self.send_and_receive(netlib.CLIENT_PROTOCOL["request_login"], f"{username}")

        if code == netlib.SERVER_PROTOCOL["login_success"]:
            self.name = username
            return True
        else:
            if PRINT_DEBUG:
                print(f"Failed Login {data}! Try Again.\n")
            return False

    def request_object(self, objects):

        objects_list = ",".join(objects)

        code, data = self.send_and_receive(netlib.CLIENT_PROTOCOL['request_object'], f"{len(objects)}#{objects_list}")

        if code == netlib.SERVER_PROTOCOL['send_object']:

            while data == self.to_draw:
                code, data = self.send_and_receive(netlib.CLIENT_PROTOCOL['request_object'],
                                                   f"{len(objects)}#{objects_list}")
                print("CLIENT")

                if code != netlib.SERVER_PROTOCOL['send_object']:
                    self.error()
        return data

    def update_score(self):
        code, data = self.send_and_receive(netlib.CLIENT_PROTOCOL["update_score"], f"{self.name}#{self.score}")

        if code != netlib.SERVER_PROTOCOL["score_received"]:
            self.error()

    def send_chat(self, text):
        code, data = self.send_and_receive(netlib.CLIENT_PROTOCOL["update_chat"], f"{text}")

        if code != netlib.SERVER_PROTOCOL["chat_received"]:
            self.error()

    def update_chat(self, chat_box):
        code, data = self.send_and_receive(netlib.CLIENT_PROTOCOL["request_chat"], "")

        if code != netlib.SERVER_PROTOCOL["send_chat"]:
            self.error()

        if data != "":
            messages = netlib.split_data(data, -1)
            for message in messages[1:]:
                chat_box.append_text(message)




