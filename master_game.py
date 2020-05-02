import os
import pygame

from PyBMS import *
from objects import *

Frame = 144
Height = 720
Width = 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

def Screen_init(width, height, caption):
    Screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return Screen

def Resolution_calculate(value):
    return int(float(value) * (Width / 1280))

def Song_select():
    select_song = ''
    select_song_index = 0
    max_song_index = 0
    select_song_file_index = 0
    max_song_file_index = 0
    song_list = Bundle.SongList_all()
    song_file_list = list()
    max_song_index = len(song_list)
    is_file_select = False
    while True:
        screen.fill(BLACK)
        if is_file_select is False:
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    return
                if event.type is pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_UP] is 1:
                        if select_song_index - 1 >= 0:
                            select_song_index = select_song_index - 1
                        else:
                            select_song_index = max_song_index - 1
                    elif key[pygame.K_DOWN] is 1:
                        if select_song_index + 1 < max_song_index :
                            select_song_index = select_song_index + 1
                        else:
                            select_song_index = 0
                    elif key[pygame.K_KP_ENTER] is 1 or key[pygame.K_RIGHT] is 1:
                        select_song_file_index = 0
                        is_file_select = True
                    elif key[pygame.K_ESCAPE] is 1:
                        return
            if max_song_index is 0:
                fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', Resolution_calculate(20))
                text = fontObj.render('Empty', True, WHITE)
                screen.blit(text, (0, Resolution_calculate(10)))
                pygame.display.flip()
                continue

            List_num = 5
            max_list_num = 5
            while List_num > 0:
                if select_song_index - List_num >= 0:
                    fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', Resolution_calculate(20))
                    text = fontObj.render(song_list[select_song_index - List_num], True, WHITE)
                    screen.blit(text, (0, Resolution_calculate(10 + (max_list_num - List_num) * 30)))
                List_num = List_num - 1

            fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', Resolution_calculate(30))
            text = fontObj.render(song_list[select_song_index], True, WHITE)
            screen.blit(text, (Resolution_calculate(10), Resolution_calculate(10 + max_list_num * 30 + 40)))

            while List_num < max_list_num:
                List_num = List_num + 1
                if select_song_index + List_num < max_song_index:
                    fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', Resolution_calculate(20))
                    text = fontObj.render(song_list[select_song_index + List_num], True, WHITE)
                    screen.blit(text, (0, Resolution_calculate(90 + (max_list_num + List_num) * 30)))
        else:
            song_file_list = Bundle.Get_script_file(song_list[select_song_index])
            max_song_file_index = len(song_file_list)
            if max_song_file_index is 0:
                fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', Resolution_calculate(20))
                text = fontObj.render('Empty', True, WHITE)
                screen.blit(text, (0, Resolution_calculate(10)))
                pygame.display.flip()
                continue
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    return
                if event.type is pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_UP] is 1:
                        if select_song_file_index - 1 >= 0:
                            select_song_file_index = select_song_file_index - 1
                        else:
                            select_song_file_index = max_song_file_index - 1
                    elif key[pygame.K_DOWN] == 1:
                        if select_song_file_index + 1 < max_song_file_index :
                            select_song_file_index = select_song_file_index + 1
                        else:
                            select_song_file_index = 0
                    elif key[pygame.K_ESCAPE] is 1 or key[pygame.K_LEFT] is 1:
                        is_file_select = False
                    elif key[pygame.K_KP_ENTER] is 1 or key[pygame.K_RIGHT] is 1:
                        if max_song_file_index > 0:
                            return Bundle.SongList_name(song_list[select_song_index]) + '\\' + song_file_list[select_song_file_index]

            List_num = 5
            max_list_num = 5
            while List_num > 0:
                if select_song_file_index - List_num >= 0:
                    fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', Resolution_calculate(20))
                    text = fontObj.render(song_file_list[select_song_file_index - List_num], True, WHITE)
                    screen.blit(text, (0, Resolution_calculate(10 + (max_list_num - List_num) * 30)))
                List_num = List_num - 1

            fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', Resolution_calculate(30))
            text = fontObj.render(song_file_list[select_song_file_index], True, WHITE)
            screen.blit(text, (Resolution_calculate(10), Resolution_calculate(10 + max_list_num * 30 + 40)))

            while List_num < max_list_num:
                List_num = List_num + 1
                if select_song_file_index + List_num < max_song_file_index:
                    fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', Resolution_calculate(20))
                    text = fontObj.render(song_file_list[select_song_file_index + List_num], True, WHITE)
                    screen.blit(text, (0, Resolution_calculate(90 + (max_list_num + List_num) * 30)))
        pygame.display.flip()
    return

    def Note_read(self): #Note[channel][Node] || Load Note Data
        Note = list()
        Sound = self.parser.Load_WAV()
        for index1 in range(0, 9):
            Note_data = self.parser.Get_note_data_channel(11 + index1)
            node = 0
            Note.append(list())
            while len(Note_data) > node:
                Note[index1].append(list())
                if Note_data[node] is []:
                    node = node + 1
                    continue
                temp_str = Note_data[node][0]
                count = len(temp_str[1]) // 2

                for index2 in range(0, count):
                    s = str(temp_str[1][index2*2 : index2*2+2])
                    found = False
                    if s is '00':
                        continue
                    for sound_obj in Sound:
                        if sound_obj[0] is s:
                            found = True
                            Note[index1][node].append(Note_data_class(sound_obj[1], float(index2 / count), 11 + index1))
                            break
                    if found is false:
                        Note[index1][node].append(Note_data_class(None, float(index2 / count), 11 + index1))
                node = node + 1
        return Note
    
    def Stop_read(self):
        Stop = list()
        Stop_data = self.parser.Get_stop()
        node = 0
        Note_data = self.parser.Get_note_data_channel('09')
        while len(Note_data) > node:
            Stop.append(list())
            if Note_data[node] is []:
                node = node + 1
                continue
            temp_str = Note_data[node][0]
            count = len(temp_str[1]) // 2
            for index1 in range(0, count):
                s = str(temp_str[1][index1*2 : index1*2+2])
                if s is '00':
                    continue
                for index2 in range(0, len(Stop_data)):
                    if s is Stop_data[index2][0]:
                        Stop[node].append(Stop_data_class(float(index1 / count), Stop_data[index2][1]))
                        break
            node = node + 1
        return Stop

    def BPM_read(self):
        BPM = list()
        node = 0
        BPM_data = self.parser.Get_BPM()
        Note_data1 = self.parser.Get_note_data_channel('08')
        Note_data2 = self.parser.Get_note_data_channel('03')
        while len(Note_data1) > node:
            BPM.append(list())
            if Note_data1[node] is [] and Note_data2[node] is []:
                node = node + 1
                continue
            elif Note_data1[node] != [] and Note_data2[node] is []:
                temp_str1 = Note_data1[node][0]
                count = len(temp_str1[1]) // 2
                for index1 in range(0, count):
                    s = str(temp_str1[1][index1*2 : index1*2+2])
                    if s is '00':
                        continue
                    for index2 in range(0, len(BPM_data)):
                        if s is BPM_data[index2][0]:
                            BPM[node].append(BPM_data_class(float(index1 / count), BPM_data[index2][1]))
                            break
            elif Note_data1[node] is [] and Note_data2[node] != []:
                temp_str1 = Note_data2[node][0]
                count = len(temp_str1[1]) // 2
                for index1 in range(0, count):
                    s = str(temp_str1[1][index1*2 : index1*2+2])
                    if s is '00':
                        continue
                    BPM[node].append(BPM_data_class(float(index1 / count), int('0x' + s, 16)))
            else:
                BPM_temp1 = list()
                temp_str1 = Note_data2[node][0]
                count = len(temp_str1[1]) // 2
                for index1 in range(0, count):
                    s = str(temp_str1[1][index1*2 : index1*2+2])
                    if s is '00':
                        continue
                    BPM_temp1.append(BPM_data_class(float(index1 / count), int('0x' + s, 16)))
                temp_str1 = Note_data1[node][0]
                count = len(temp_str1[1]) // 2
                BPM_temp2 = list()
                for index1 in range(0, count):
                    s = str(temp_str1[1][index1*2 : index1*2+2])
                    if s is '00':
                        continue
                    for index2 in range(0, len(BPM_data)):
                        if s is BPM_data[index2][0]:
                            BPM_temp2.append(BPM_data_class(float(index1 / count), BPM_data[index2][1]))
                            break
                while len(BPM_temp1) > 0 or len(BPM_temp2) > 0:
                    if len(BPM_temp1) > 0 and len(BPM_temp2) > 0:
                        if BPM_temp1[0].position > BPM_temp2[0].position:
                            temp = BPM_temp2[0]
                            BPM[node].append(temp)
                            BPM_temp2.remove(temp)
                        else:
                            temp = BPM_temp1[0]
                            BPM[node].append(temp)
                            BPM_temp1.remove(temp)
                    elif len(BPM_temp1) <= 0:
                        while len(BPM_temp2) > 0:
                            temp = BPM_temp2[0]
                            BPM[node].append(temp)
                            BPM_temp2.remove(temp)
                    else:
                        while len(BPM_temp1) > 0:
                            temp = BPM_temp1[0]
                            BPM[node].append(temp)
                            BPM_temp1.remove(temp)
            node = node + 1
        return BPM

    def Play(self):
        self.BPM_read()
        Speed = 1
        End = False
        Node = -1
        clock = pygame.time.Clock()
        is_stop = False
        header = self.parser.Get_Header()
        BPM = float(header[4][1])
        time = float(240/BPM)
        Node_count = 0

        Line_Obj = list()
        BPM_Obj = list()
        Note_Obj = list()
        Stop_Obj = list()

        Stop_data = self.Stop_read()
        BPM_data = self.BPM_read()
        Note_data = self.Note_read()
        Note_Length_data = self.parser.Get_Node_length()

        Node_count = len(Note_data[0])

        Length = 720 * Speed

        sound_channel = 0
        Max_sound_channel = 32

        Line_Obj.append(Line_Obj_class(0, 0, Note_Length_data[0][1]))
        for index1 in range(0, 9):
            for temp1 in Note_data[index1][0]:
                Note_Obj.append(Note_Obj_class(temp1.sound, float(temp1.position) * float(Length) * float(Line_Obj[0].length), temp1.channel))
        for temp1 in BPM_data[0]:
            BPM_Obj.append(BPM_Obj_class(float(temp1.position) * float(Length) * float(Line_Obj[0].length), temp1.bpm))
        for temp1 in Stop_data[0]:
            Stop_Obj.append(Stop_Obj_class(float(temp1.position) * float(Length) * float(Line_Obj[0].length), temp1.duration))

        while not End:
            screen.fill(BLACK)

            for index1 in range(1, 8):
                pygame.draw.line(self.screen, (100, 100, 100), [40 * index1, 0], [40 * index1, 600], 1)
            pygame.draw.line(self.screen, WHITE, [0, 600], [280, 600], 2)

            for temp1 in Line_Obj:
                if temp1.y < 0:
                    break
                value = round(temp1.y)
                pygame.draw.line(self.screen, WHITE, [0, value], [280, value], 1)

            if len(Line_Obj) > 0:
                if Line_Obj[-1].y >= 0:
                    if not Line_Obj[-1].node >= Node_count - 1:
                        #Add Line
                        Line_Obj.append(Line_Obj_class(Line_Obj[-1].y - Length * float(Line_Obj[-1].length), Line_Obj[-1].node + 1, Note_Length_data[Line_Obj[-1].node][1]))
                        #Add Note
                        for index1 in range(0, 9):
                            for temp1 in Note_data[index1][Line_Obj[-1].node]:
                                Note_Obj.append(Note_Obj_class(temp1.sound, Line_Obj[-1].y - float(temp1.position) * Length * float(Line_Obj[-1].length), temp1.channel))

                        #Add BPM
                        for temp1 in BPM_data[Line_Obj[-1].node]:
                            BPM_Obj.append(BPM_Obj_class(Line_Obj[-1].y - float(temp1.position) * Length * float(Line_Obj[-1].length), temp1.bpm))

                        #Add Stop
                        for temp1 in Stop_data[Line_Obj[-1].node]:
                            Stop_Obj.append(Stop_Obj_class(Line_Obj[-1].y - float(temp1.position) * Length * float(Line_Obj[-1].length), temp1.duration))
                    else:
                        End = True

            for temp1 in Note_Obj:
                value = round(temp1.y)
                if value >= 0:
                    position = 0
                    color = WHITE
                    if int(temp1.channel) is 11:
                        position = 1
                        color = WHITE
                    elif int(temp1.channel) is 12:
                        position = 2
                        color = BLUE
                    elif int(temp1.channel) is 13:
                        position = 3
                        color = WHITE
                    elif int(temp1.channel) is 14:
                        position = 4
                        color = YELLOW
                    elif int(temp1.channel) is 15:
                        position = 5
                        color = WHITE
                    elif int(temp1.channel) is 16:
                        position = 0
                        color = RED
                    elif int(temp1.channel) is 18:
                        position = 6
                        color = BLUE
                    elif int(temp1.channel) is 19:
                        position = 7
                        color = WHITE
                    pygame.draw.line(self.screen, color, [position * 40, value], [(position + 1) * 40, value], 4)

            for temp1 in Line_Obj:
                temp1.Add_y(float(Length / time / Frame))
                if temp1.y >= 600:
                    Node = temp1.node
                    Line_Obj.remove(temp1)

            for temp1 in Note_Obj:
                temp1.Add_y(float(Length / time / Frame))
                if temp1.y >= 600:
                    if temp1.sound is not None:
                        pygame.mixer.Channel(sound_channel).play(temp1.sound)
                        sound_channel = sound_channel + 1
                        if sound_channel >= Max_sound_channel:
                            sound_channel = 0
                    Note_Obj.remove(temp1)

            for temp1 in Stop_Obj:
                temp1.Add_y(float(Length / time / Frame))
                if temp1.y >= 600:
                    print("STOP!!!")
                    count = round(float(temp1.duration) / Frame)
                    print(count)
                    for index1 in range(0, count):
                        screen.fill(BLACK)
                        for index2 in range(1, 8):
                            pygame.draw.line(self.screen, (100, 100, 100), [40 * index2, 0], [40 * index2, 600], 1)
                        pygame.draw.line(self.screen, WHITE, [0, 600], [280, 600], 2)
                        for temp2 in Line_Obj:
                            if temp2.y < 0:
                                break
                            value = round(temp2.y)
                            pygame.draw.line(self.screen, WHITE, [0, value], [280, value], 1)
                        for temp2 in Note_Obj:
                            value = round(temp2.y)
                            if value >= 0:
                                position = 0
                                color = WHITE
                                if int(temp2.channel) is 11:
                                    position = 1
                                    color = WHITE
                                elif int(temp2.channel) is 12:
                                    position = 2
                                    color = BLUE
                                elif int(temp2.channel) is 13:
                                    position = 3
                                    color = WHITE
                                elif int(temp2.channel) is 14:
                                    position = 4
                                    color = YELLOW
                                elif int(temp2.channel) is 15:
                                    position = 5
                                    color = WHITE
                                elif int(temp2.channel) is 16:
                                    position = 0
                                    color = RED
                                elif int(temp2.channel) is 18:
                                    position = 6
                                    color = BLUE
                                elif int(temp2.channel) is 19:
                                    position = 7
                                    color = WHITE
                                pygame.draw.line(self.screen, color, [position * 40, value], [(position + 1) * 40, value], 4)
                        pygame.display.flip()
                        clock.tick(Frame)
                    Stop_Obj.remove(temp1)

            for temp1 in BPM_Obj:
                temp1.Add_y(float(Length / time / Frame))
                if temp1.y >= 600:
                    BPM = float(temp1.bpm)
                    time = float(240/BPM)
                    BPM_Obj.remove(temp1)

            pygame.display.flip()
            clock.tick(Frame)
        return

pygame.mixer.pre_init(22050, -16, 2, 128)
pygame.mixer.init()
pygame.init()
pygame.mixer.set_num_channels(32)  # default is 8
screen = Screen_init(Width, Height, 'BMS Player')
pygame.mouse.set_visible(True)
clock = pygame.time.Clock()
clock.tick(Frame)
p = BMS_Parser('')
esc = False

while esc is False:
    a = Song_select()
    if a is None:
        esc = True
    else:
        p.Set_file_directory(a)
        ttemp = p.Get_note_data()
        s = Song_Play(a, screen)
        s.Play()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                esc = True
            if event.type is pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                if key[pygame.K_ESCAPE]:
                    esc = True
    clock.tick(Frame)