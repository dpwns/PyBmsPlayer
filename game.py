import os
import pygame
import time
import threading

Frame = 60
Height = 720
Width = 1280
Text_size1 = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

class Bundle:
    @staticmethod
    def Get_folder_directory():
        file_dir = os.getcwd()
        file_dir = file_dir + '\\Bundle'
        return file_dir

    @staticmethod
    def SongList_all():
        file_dir = Bundle.Get_folder_directory()
        song_list = os.listdir(file_dir)
        return song_list

    @staticmethod
    def SongList_all_directory():
        file_dir = Bundle.Get_folder_directory()
        song_list = os.listdir(file_dir)
        for temp_dir in song_list:
            song_list[song_list.index(temp_dir)] = file_dir + '\\' + temp_dir
        return song_list

    @staticmethod
    def SongList_index(index):
        file_dir = Bundle.Get_folder_directory()
        song_list = os.listdir(file_dir)
        return file_dir + '\\' + song_list[index]

    @staticmethod
    def SongList_name(name):
        file_dir = Bundle.Get_folder_directory()
        song_list = os.listdir(file_dir)
        if name in song_list:
            return file_dir + '\\' + song_list[song_list.index(name)]
        return

    @staticmethod
    def Get_script_file(name):
        file_dir = Bundle.SongList_name(name)
        file_list = os.listdir(file_dir)
        file_list = [file for file in file_list if file.endswith(".bms") or file.endswith(".bme") or file.endswith(".bml")]
        return file_list

    @staticmethod
    def Get_sound_file(name):
        file_dir = Bundle.SongList_name(name)
        file_list = os.listdir(file_dir)
        file_list = [file for file in file_list if file.endswith(".ogg") or file.endswith(".wav")]
        return file_list

    @staticmethod
    def Get_script_file_directory(name):
        file_dir = Bundle.SongList_name(name)
        file_list = Bundle.Get_script_file(name)
        for temp_dir in file_list:
            file_list[file_list.index(temp_dir)] = file_dir + '\\' + temp_dir
        return file_list
        
    @staticmethod
    def Get_sound_file_directory(name):
        file_dir = Bundle.SongList_name(name)
        file_list = Bundle.Get_sound_file(name)
        for temp_dir in file_list:
            file_list[file_list.index(temp_dir)] = file_dir + '\\' + temp_dir
        return file_list

class BMS_Parser:
    file_dir = ''
    folder_dir = ''

    def __init__(self, file_directory):
        self.file_dir = file_directory
        self.folder_dir = self.file_dir
        while len(self.folder_dir) > 0:
            if self.folder_dir[-1] == '\\':
                self.folder_dir = self.folder_dir[0:-1]
                break
            else:
                self.folder_dir = self.folder_dir[0:-1]

    def Set_file_directory(self, directory):
        self.file_dir = directory
        self.folder_dir = self.file_dir
        while True:
            if self.folder_dir[-1] == '\\':
                self.folder_dir = self.folder_dir[0:-1]
                break
            else:
                self.folder_dir = self.folder_dir[0:-1]

    def Get_Header(self):
        if (self.file_dir == ''): 
            return
        File = open(self.file_dir, 'r')
        Header_data = [
        ['Player', ''],
        ['Genre', ''],
        ['Title', ''],
        ['Artist', ''],
        ['BPM', ''],
        ['PlayLevel', ''],
        ['Rank', ''],
        ['Volwav', ''],
        ['Stagefile', ''],
        ['Total', ''],
        ['Midifile', ''],
        ['Videofile', ''],
        ['Bmp', '']]
        temp_string = File.readline()
        while temp_string != '' and temp_string.find('MAIN DATA FIELD') == -1:
            temp_string = temp_string.replace('\n', '')
            if (temp_string.startswith('#')):
                if temp_string.find('#PLAYER ') != -1:
                    Header_data[0][1] = temp_string.replace("#PLAYER ", "")
                elif temp_string.find('#GENRE ') != -1:
                    Header_data[1][1] = temp_string.replace("#GENRE ", "")
                elif temp_string.find('#TITLE ') != -1:
                    Header_data[2][1] = temp_string.replace("#TITLE ", "")
                elif temp_string.find('#ARTIST ') != -1:
                    Header_data[3][1] = temp_string.replace("#ARTIST ", "")
                elif temp_string.find('#BPM ') != -1:
                    Header_data[4][1] = temp_string.replace("#BPM ", "")
                elif temp_string.find('#PLAYLEVEL ') != -1:
                    Header_data[5][1] = temp_string.replace("#PLAYLEVEL ", "")
                elif temp_string.find('#RANK ') != -1:
                    Header_data[6][1] = temp_string.replace("#RANK ", "")
                elif temp_string.find('#VOLWAV ') != -1:
                    Header_data[7][1] = temp_string.replace("#VOLWAV ", "")
                elif temp_string.find('#STAGEFILE ') != -1:
                    Header_data[8][1] = temp_string.replace("#STAGEFILE", "")
                elif temp_string.find('#TOTAL ') != -1:
                    Header_data[9][1] = temp_string.replace("#TOTAL ", "")
                elif temp_string.find('#MIDIFILE ') != -1:
                    Header_data[10][1] = temp_string.replace("#MIDIFILE ", "")
                elif temp_string.find('#VIDEOFILE ') != -1:
                    Header_data[11][1] = temp_string.replace("#VIDEOFILE ", "")
                elif temp_string.find('#BMP ') != -1:
                    Header_data[12][1] = temp_string.replace("#BMP ", "")
            temp_string = File.readline()
        File.close()
        return Header_data
    
    def Get_WAV(self):
        if (self.file_dir == ''): 
            return
        File = open(self.file_dir, 'r')
        temp_string = File.readline()
        Wav_data = list()
        while temp_string != '' and temp_string.find('MAIN DATA FIELD') == -1:
            temp_string = temp_string.replace('\n', '')
            if (temp_string.startswith('#')):
                if temp_string.find('#WAV') != -1:
                    temp_string = temp_string.replace("#WAV", "")
                    Wav_data.append([temp_string[0:2], temp_string[3:]])
            temp_string = File.readline()
        File.close()
        return Wav_data

    def Load_WAV(self):
        wav_file = self.Get_WAV()
        load_wav = list()
        wav_dir = self.folder_dir[self.folder_dir.find('Bundle'):] + '\\'
        for wav in wav_file:
            if wav[1].find(".mp3") != -1:
                sound = None
                load_wav.append([str(wav[0]), sound])
                continue
            dir_temp = wav_dir + wav[1]
            if not os.path.isfile(self.folder_dir + '\\' + wav[1]):
                dir_temp = dir_temp.replace(".wav", ".ogg")
            sound = pygame.mixer.Sound(dir_temp)
            load_wav.append([str(wav[0]), sound])
        return load_wav
    
    def Get_BPM(self):
        if (self.file_dir == ''): 
            return
        File = open(self.file_dir, 'r')
        temp_string = File.readline()
        BPM_data = list()
        while temp_string != '' and temp_string.find('MAIN DATA FIELD') == -1:
            temp_string = temp_string.replace('\n', '')
            if (temp_string.startswith('#')):
                if temp_string.find('#BPM') != -1 and temp_string.find('#BPM ') == -1:
                    temp_string = temp_string.replace("#BPM", "")
                    BPM_data.append([temp_string[0:2], temp_string[3:]])
            temp_string = File.readline()
        File.close()
        return BPM_data
    
    def Get_stop(self):
        if (self.file_dir == ''): 
            return
        File = open(self.file_dir, 'r')
        temp_string = File.readline()
        Stop_data = list()
        while temp_string != '' and temp_string.find('MAIN DATA FIELD') == -1:
            temp_string = temp_string.replace('\n', '')
            if (temp_string.startswith('#')):
                if temp_string.find('#STOP') != -1:
                    temp_string = temp_string.replace("#STOP", "")
                    Stop_data.append([temp_string[0:2], temp_string[3:]])
            temp_string = File.readline()
        File.close()
        return Stop_data

    def Get_Node_length(self):
        temp_list = self.Get_note_data_channel('02')
        List = list()
        index = 0
        for temp in temp_list:
            if len(temp) <= 0 or temp == []:
                List.append([index, '1'])
                index = index + 1
                continue
            temp = temp[0]
            List.append([index, temp[1]])
            index = index + 1
        return List

    def Get_Long_note(self):
        return
        
    def Get_Normal_note(self):
        
        return

    def Get_note_data(self):
        if (self.file_dir == ''): 
            return
        track = list()
        File = open(self.file_dir, 'r')
        temp_string = File.readline()
        while temp_string != '':
            temp_string = File.readline()
            if not temp_string.startswith('#'):
                continue
            if temp_string[6] != ':':
                continue
            temp_string = temp_string.replace('\n', '')
            index = int(temp_string[1:4])
            while len(track) <= index:
                track.append([])
            track[index].append([temp_string[4:6], temp_string[7:]])
        File.close()
        return track

    def Get_note_data_channel(self, channel):
        if (self.file_dir == ''): 
            return
        channel = str(channel)
        if len(channel) > 2 or len(channel) == 0:
            return        
        elif len(channel) == 1:
            channel = '0' + channel
        track = list()
        File = open(self.file_dir, 'r')
        temp_string = File.readline()
        while temp_string != '' and temp_string.find('MAIN DATA FIELD') == -1:
            temp_string = File.readline()
            if not temp_string: 
                break
        while temp_string != '':
            temp_string = File.readline()
            if not temp_string: 
                break
            if temp_string.find('#') == -1:
                continue
            if temp_string[6] != ':':
                continue
            temp_string = temp_string.replace('\n', '')
            index = int(temp_string[1:4])
            while len(track) <= index:
                track.append([])
            if temp_string[4:6] == channel:
                track[index].append([temp_string[4:6], temp_string[7:]])
        File.close()
        return track

    def Get_note_data_bar(self, bar_number):
        track = self.Get_note_data()
        bar_number = int(bar_number)
        if bar_number >= len(track) or bar_number < 0:
            return
        return track[int(bar_number)]

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
        if not is_file_select:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_UP] == 1:
                        if select_song_index - 1 >= 0:
                            select_song_index = select_song_index - 1
                        else:
                            select_song_index = max_song_index - 1
                    elif key[pygame.K_DOWN] == 1:
                        if select_song_index + 1 < max_song_index :
                            select_song_index = select_song_index + 1
                        else:
                            select_song_index = 0
                    elif key[pygame.K_KP_ENTER] == 1 or key[pygame.K_RIGHT] == 1:
                        select_song_file_index = 0
                        is_file_select = True
                    elif key[pygame.K_ESCAPE] == 1:
                        return
            if max_song_index == 0:
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
            if max_song_file_index == 0:
                fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', Resolution_calculate(20))
                text = fontObj.render('Empty', True, WHITE)
                screen.blit(text, (0, Resolution_calculate(10)))
                pygame.display.flip()
                continue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_UP] == 1:
                        if select_song_file_index - 1 >= 0:
                            select_song_file_index = select_song_file_index - 1
                        else:
                            select_song_file_index = max_song_file_index - 1
                    elif key[pygame.K_DOWN] == 1:
                        if select_song_file_index + 1 < max_song_file_index :
                            select_song_file_index = select_song_file_index + 1
                        else:
                            select_song_file_index = 0
                    elif key[pygame.K_ESCAPE] == 1 or key[pygame.K_LEFT] == 1:
                        is_file_select = False
                    elif key[pygame.K_KP_ENTER] == 1 or key[pygame.K_RIGHT] == 1:
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

class Line_Obj:
    y = 0.0
    node = 0
    def __init__(self, y, node):
        self.y = float(y)
        self.node = int(node)

    def Add_y(self, plus):
        self.y = float(self.y + plus)

class Stop_Obj:
    position = 0.0
    time = 0.0
    def __init__(self, position, time):
        self.position = float(position)
        self.time = time

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

class Note_Obj:
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

    def Note_read(self): #Note[channel][Node] || Load Note Data
        Note = list()
        Sound = self.parser.Load_WAV()
        for index1 in range(0, 9):
            Note_data = self.parser.Get_note_data_channel(11 + index1)
            node = 0
            Note.append(list())
            while len(Note_data) > node:
                Note[index1].append(list())
                if Note_data[node] == []:
                    node = node + 1
                    continue
                temp_str = Note_data[node][0]
                count = len(temp_str[1]) // 2

                for index2 in range(0, count):
                    s = str(temp_str[1][index2*2 : index2*2+2])
                    found = False
                    if s == '00':
                        continue
                    for sound_obj in Sound:
                        if sound_obj[0] == s:
                            found = True
                            Note[index1][node].append(Note_data_class(sound_obj[1], float(index2 / count), 11 + index1))
                            break
                    if not found:
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
            if Note_data[node] == []:
                node = node + 1
                continue
            temp_str = Note_data[node][0]
            count = len(temp_str[1]) // 2
            for index1 in range(0, count):
                s = str(temp_str[1][index1*2 : index1*2+2])
                if s == '00':
                    continue
                for index2 in range(0, len(Stop_data)):
                    if s == Stop_data[index2][0]:
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
            if Note_data1[node] == [] and Note_data2[node] == []:
                node = node + 1
                continue
            elif Note_data1[node] != [] and Note_data2[node] == []:
                temp_str1 = Note_data1[node][0]
                count = len(temp_str1[1]) // 2
                for index1 in range(0, count):
                    s = str(temp_str1[1][index1*2 : index1*2+2])
                    if s == '00':
                        continue
                    for index2 in range(0, len(BPM_data)):
                        if s == BPM_data[index2][0]:
                            BPM[node].append(BPM_data_class(float(index1 / count), BPM_data[index2][1]))
                            break
            elif Note_data1[node] == [] and Note_data2[node] != []:
                temp_str1 = Note_data2[node][0]
                count = len(temp_str1[1]) // 2
                for index1 in range(0, count):
                    s = str(temp_str1[1][index1*2 : index1*2+2])
                    if s == '00':
                        continue
                    BPM[node].append(BPM_data_class(float(index1 / count), int('0x' + s, 16)))
            else:
                BPM_temp1 = list()
                temp_str1 = Note_data2[node][0]
                count = len(temp_str1[1]) // 2
                for index1 in range(0, count):
                    s = str(temp_str1[1][index1*2 : index1*2+2])
                    if s == '00':
                        continue
                    BPM_temp1.append(BPM_data_class(float(index1 / count), int('0x' + s, 16)))
                temp_str1 = Note_data1[node][0]
                count = len(temp_str1[1]) // 2
                BPM_temp2 = list()
                for index1 in range(0, count):
                    s = str(temp_str1[1][index1*2 : index1*2+2])
                    if s == '00':
                        continue
                    for index2 in range(0, len(BPM_data)):
                        if s == BPM_data[index2][0]:
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
        for temp in BPM:
            for temp2 in temp:
                print(temp2.bpm, end = ' ')
            print(' ')
        return BPM

    def Play(self):
        self.BPM_read()
        """
        Speed = 1
        End = False
        Node = -1
        clock = pygame.time.Clock()
        is_Stop = False

        header = self.parser.Get_Header()
        Start_BPM = int(header[4][1])

        Line = list()
        BPM = list()
        Note = list()
        Stop = list()

        Stop_data = list()
        BPM_data = list()
        
        time = float(240/Start_BPM)

        Temp = self.parser.Get_note_data_channel('03')
        for bpm_data in Temp:
            if bpm_data == []:
                BPM_data.append([])
                continue
            BPM_data.append([Stop_Obj()])
        self.Note_read()

        node = 0
        Temp = self.parser.Get_stop()
        Temp2 = self.parser.Get_note_data_channel('09')
        for stop in Temp2:
            if stop == []:
                Stop_data.append([])
                continue
            Stop_data.append([Stop_Obj()])

        self.parser.Get_stop()
        Sound = self.parser.Load_WAV()
        Note_Length = self.parser.Get_Node_length()
        Line.append(Line_Obj(0, 0))
        Length = 720 * Speed
        
        for index1 in range(1, 25):
            Line.append(Line_Obj(Line[index1 - 1].y - Length * float(Note_Length[index1 - 1][1]), index1))
        for index1 in range(0, 9):
            Note_list = self.parser.Get_note_data_channel(11 + index1)
            if len(Note_list) <= 25:
                continue
            for index2 in range(0, 25):
                temp = Note_list[index2]
                if temp != []:
                    temp = temp[0]
                    if len(temp[1]) % 2 != 0:
                        continue
                    count = len(temp[1]) // 2
                    for index3 in range(0, count):
                        s = str(temp[1][index3*2:index3*2+2])
                        if s == '00':
                            continue
                        for sound_obj in Sound:
                            if sound_obj[0] == s:
                                Note.append(Note_Obj(sound_obj[1], float(Line[index2].y - Length * float(Note_Length[index2 - 1][1]) * index3 / count), 11 + index1))
                                break
                        Note.append(Note_Obj(None, float(Line[index2].y - Length * float(Note_Length[index2 - 1][1]) * index3 / count), 11 + index1))
        while not End:
            screen.fill(BLACK)
            for index1 in range(1, 8):
                pygame.draw.line(self.screen, (100, 100, 100), [40 * index1, 0], [40 * index1, 600], 1)
            pygame.draw.line(self.screen, WHITE, [0, 600], [320, 600], 2)
            for l in Line:
                value = round(l.y)
                if value >= 0:
                    pygame.draw.line(self.screen, WHITE, [0, value], [320, value], 1)
                if not is_Stop:
                    l.Add_y(float(720 * Speed / time / Frame))
                if value >= 600:
                    Node = l.node
                    Line.remove(l)
            if Line[len(Line) - 1].y >= 0:
                End = True
            for n in Note:
                value = round(n.y)
                if value >= 0:
                    position = 0
                    color = WHITE
                    if int(n.channel) == 11:
                        position = 1
                        color = WHITE
                    elif int(n.channel) == 12:
                        position = 2
                        color = BLUE
                    elif int(n.channel) == 13:
                        position = 3
                        color = WHITE
                    elif int(n.channel) == 14:
                        position = 4
                        color = YELLOW
                    elif int(n.channel) == 15:
                        position = 5
                        color = WHITE
                    elif int(n.channel) == 16:
                        position = 0
                        color = RED
                    elif int(n.channel) == 18:
                        position = 6
                        color = BLUE
                    elif int(n.channel) == 19:
                        position = 7
                        color = WHITE
                    pygame.draw.line(self.screen, color, [position * 40, value], [(position + 1) * 40, value], 4)
                if not is_Stop:
                    n.Add_y(float(720 * Speed / time / Frame))
                if value >= 600:
                    if n.sound != None:
                        n.sound.stop()
                        n.sound.play()
                    Note.remove(n)
                if value >= 720:
                    Note.remove(n)
            pygame.display.flip()
            clock.tick(Frame)"""
        return

pygame.mixer.pre_init(44100, -16, 16, 512)
pygame.mixer.init()
pygame.init()
screen = Screen_init(Width, Height, 'BMS Player')
pygame.mouse.set_visible(True)
clock = pygame.time.Clock()
clock.tick(Frame)
p = BMS_Parser('')
esc = False

while not esc:
    a = Song_select()
    if a == None:
        esc = True
    else:
        p.Set_file_directory(a)
        ttemp = p.Get_note_data()
        s = Song_Play(a, screen)
        s.Play()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                esc = True
            if event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                if key[pygame.K_ESCAPE]:
                    esc = True
    clock.tick(Frame)