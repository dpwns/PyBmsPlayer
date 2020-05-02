from PyBMS import BMS_Parser

class Line_Obj_class:
    y = 0.0
    node = 0
    length = 0.0
    def __init__(self, y, node, length):
        self.y = float(y)
        self.node = int(node)
        self.length = length

    def Add_y(self, plus):
        self.y = float(self.y + plus)

class Stop_Obj_class:
    y = 0.0
    duration = 0.0
    def __init__(self, y, duration):
        self.y = float(y)
        self.duration = duration

class Note_data_class:
    channel = ''
    sound = None
    position = 0.0
    def __init__(self, sound, position, channel):
        self.position = float(position)
        if self.position > 1:
            self.position = float(1)
        elif self.position < 0:
            self.position = float(0)
        self.sound = sound
        self.channel = channel

class Stop_data_class:
    position = 0.0
    duration = 0.0
    def __init__(self, position, duration):
        self.position = float(position)
        if self.position > 1:
            self.position = float(1)
        elif self.position < 0:
            self.position = float(0)
        self.duration = float(int(duration) / 192)
        if self.duration < 0:
            self.duration = 0

class BPM_data_class:
    position = 0.0
    bpm = 0.0
    def __init__(self, position, bpm):
        self.position = float(position)
        if self.position > 1:
            self.position = float(1)
        elif self.position < 0:
            self.position = float(0)
        self.bpm = float(bpm)

class BPM_Obj_class:
    y = 0.0
    bpm = 0.0
    def __init__(self, y, bpm):
        self.y = float(y)
        self.bpm = float(bpm)

    def Add_y(self, plus):
        self.y = float(self.y + plus)

class Note_Obj_class:
    channel = ''
    sound = None
    y = 0.0
    def __init__(self, sound, y, channel):
        self.y = float(y)
        self.sound = sound
        self.channel = channel
    def Add_y(self, plus):
        self.y = float(self.y + plus)

class Long_Note:
    node = -1
    channel = -1
    start = float(-1)
    end = float(-1)
    sound = None
    def __init__(self, node, channel, start, end, sound):
        self.node = int(node)
        self.channel = int(node)
        self.start = float(start)
        self.end = float(end)
        self.sound = sound
    def is_vaild(self):
        if self.node < 0:
            return False
        if self.channel < 0:
            return False
        if self.start < 0:
            return False
        if self.end <= self.start:
            return True

class Song_Play():
    select_song = ''
    parser = BMS_Parser('')
    screen = None
    def __init__(self, song_file_directory, screen):
        self.select_song = song_file_directory
        self.parser.Set_file_directory(song_file_directory)
        self.screen = screen
