import os
import pygame
import time

Frame = 60
Height = 720
Width = 1280
Text_size1 = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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
                    Wav_data.append([temp_string[0:1], temp_string[3:]])
            temp_string = File.readline()
        File.close()
        return Wav_data

    def Load_WAV(self):
        wav_file = self.Get_WAV()
        print(wav_file)
        load_wav = list()
        wav_dir = self.folder_dir[self.folder_dir.find('Bundle'):] + '\\'
        print(wav_dir)
        for wav in wav_file:
            dir_temp = wav_dir + wav[1]
            if not os.path.isfile(self.folder_dir + '\\' + wav[1]):
                dir_temp = dir_temp.replace(".wav", ".ogg")
            sound = pygame.mixer.Sound(dir_temp)
            load_wav.append([wav[0], sound])
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
                    BPM_data.append([temp_string[0:3], temp_string[3:]])
            temp_string = File.readline()
        File.close()
        return BPM_data

    def Get_Node_shorten(self):
        temp_list = self.Get_note_data_channel('02')
        List = list()
        index = 0
        for temp in temp_list:
            if len(temp) <= 0 or temp == []:
                List.append([])
                index = index + 1
                continue
            temp = temp[0]
            List.append([index, temp[1]])
        return List

    """
    def LongNote_LNTYPE1(self):
        return

    def LongNote_LNTYPE2(self):
        return

    def LongNote_LNOBJ(self):
        return
    """

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
            if temp_string[4:6] == channel:
                index = int(temp_string[1:4])
                while len(track) <= index:
                    track.append([])
                track[index].append([temp_string[4:6], temp_string[7:]])
        File.close()
        return track

    def Get_note_data_bar(self, bar_number):
        track = self.Get_note_data()
        bar_number = int(bar_number)
        if bar_number >= len(track) or bar_number < 0:
            return
        return track[int(bar_number)]

class Note:
    node = -1
    channel = -1
    interval = float(-1)
    sound = None
    def __init__(self, node, channel, interval, sound):
        self.node = int(node)
        self.channel = int(node)
        self.interval = float(interval)
        self.sound = sound
    
    def is_vaild(self):
        if self.node < 0:
            return False
        if self.channel < 0:
            return False
        if self.interval < 0:
            return False
        return True

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

def Song_play(parser):
    header = parser.Get_Header()
    BPM = int(head[head.index('BPM')][1])
    return

pygame.init()
pygame.mixer.init()
screen = Screen_init(Width, Height, 'BMS Player')
pygame.mouse.set_visible(True)
clock = pygame.time.Clock()
clock.tick(Frame)
p = BMS_Parser('')
a = Song_select()
c = 0
esc = False

if a != None:
    clock = pygame.time.Clock()
    p.Set_file_directory(a)
    ttemp = p.Get_note_data()
    print(p.Get_BPM())
    """
    i = 0
    while i < len(ttemp):
        print(str(i)+' : ')
        print(ttemp[i])
        i = i + 1
    """
    b = p.Get_Header()
    for d in b:
        fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', Resolution_calculate(20))
        text = fontObj.render(str(d), True, WHITE)
        screen.blit(text, (0, Resolution_calculate(c * 20)))
        c = c + 1
    while not esc:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                esc = True
            if event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                if key[pygame.K_ESCAPE]:
                    esc = True