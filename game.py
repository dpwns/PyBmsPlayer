import os
import pygame
import time

Frame = 144
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
    Data = list() #.bms, .bml 파일 전체
    Main_Data = list() #XXXXX: ~~ 부분만, [Node, Channel, Data] 로 구성

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

    def Data_Check(self): #Data 리스트 체크
        if not self.Data:
            self.Read_Data()

    def Main_Data_Check(self): #Main_Data 리스트 체크
        if not self.Data:
            self.Parse_Main_Data()

    def Read_Data(self): #파일 전체 읽기 / #으로 시작하는 부분만 저장
        self.Data.clear()
        if self.file_dir == '': 
            return
        File = open(self.file_dir, 'r')
        temp_string = File.readline()
        while temp_string != '':
            temp_string = temp_string.replace('\n', '')
            if temp_string.startswith('#'):
                self.Data.append(temp_string)
            temp_string = File.readline()
        File.close()
        return self.Data
                
    def Parse_Header(self): #헤더부분 파싱
        self.Data_Check()
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
        for temp_string in self.Data:
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
        return Header_data
    
    def Parse_Main_Data(self): #Main_Data 읽기
        self.Main_Data.clear()
        self.Data_Check()
        Data_list = list()
        for temp_string in self.Data:
            if temp_string[6] != ':':
                continue
            node = temp_string[1:4]
            channel = temp_string[4:6]
            data = temp_string[7:]
            Data_list.append([node, channel, data])
        self.Main_Data = Data_list
        return Data_list

    def Parse_Stop_key(self): # #STOP 키값 읽기
        self.Main_Data_Check()
        Stop_data = list()
        for temp_string in self.Data:
            if temp_string.find('#STOP') != -1:
                temp_string = temp_string.replace("#STOP", "")
                Stop_data.append([temp_string[0:2], temp_string[3:]])
        return Stop_data
    
    def Parse_Stop(self): # 09번 채널 (시퀀스 정지 채널) 읽기
        self.Main_Data_Check()
        Stop_Key = self.Parse_Stop_key()
        Stop_list = list()
        Stop_Data = list()
        for temp in self.Main_Data:
            if temp[1] != '09':
                continue
            Stop_list.append(temp)
        for temp in Stop_list:
            data = temp[2]
            node = temp[0]
            templist = list()
            while len(data) > 0:
                data_temp = data[0:2]
                data = data[2:]
                data_temp2 = None
                for temp2 in Stop_Key:
                    if temp2[0] == data_temp:
                        data_temp2 = temp2[1]
                        break
                if data_temp2 == None:
                    data_temp2 = '00'
                templist.append(data_temp2)
            Stop_Data.append([node, templist])
        return Stop_Data

    def Parse_Start_BPM(self): #시작 BPM 읽기
        self.Data_Check()
        BPM = None
        for temp_string in self.Data:
            if temp_string.find('#BPM ') == -1:
                temp_string = temp_string.replace("#BPM ", "")
                BPM_data = temp_string
                break
        if BPM == None:
            BPM = '130'
        return BPM
    
    def Parse_Extended_BPM_key(self): #확장 BPM 읽기 (#BPMxx 실수)
        self.Data_Check()
        exBPM_data = list()
        for temp_string in self.Data:
            if temp_string.find('#BPM ') == -1 and temp_string.find('#BPM') != -1:
                temp_string = temp_string.replace("#BPM", "")
                BPM_Num = temp_string[0:2]
                data = float(temp_string[2:])
                exBPM_data.append([BPM_Num, data])
        return exBPM_data

    def Parse_Extended_BPM(self):
        self.Main_Data_Check()
        Start_BPM = self.Parse_Start_BPM()
        Data_list = list()
        BPM_list = list()
        key = self.Parse_Extended_BPM_key()
        for temp in self.Main_Data:
            if temp[1] != '08' and temp[1] != '03':
                continue
            Data_list.append(temp)
        for temp in Data_list:
            data = temp[2]
            channel = temp[1]
            node = temp[0]
            templist = list()
            while len(data) > 0:
                data_temp = data[0:2]
                data = data[2:]
                data_temp2 = None
                if channel == '08':
                    for temp2 in key:
                        if temp2[0] == data_temp:
                            data_temp2 = temp2[1]
                            break
                    if data_temp2 == None:
                        data_temp2 = '00'
                if channel == '03':
                    templist.append(str(int(data_temp, 16)))
                elif channel == '08':
                    templist.append(data_temp2)
            BPM_list.append([node, templist])
        return BPM_list
    
    def Parse_Node_Length(self): #마디 길이 읽기
        self.Main_Data_Check()
        Length_Data = list()
        for temp in self.Main_Data:
            if temp[1] == '02':
                Length_Data.append([temp[0], temp[2]])
        return Length_Data

    def Parse_Sound(self):
        self.Data_Check()
        Key_Sound = list()
        for temp_string in self.Data:
            if temp_string.find('#WAV') != -1:
                temp_string = temp_string.replace("#WAV", "")
                Key_Sound.append([temp_string[0:2], temp_string[3:]])
        return Key_Sound

    def Load_Key_Sound(self):
        return

    def Load_BGM_Sound(self):
        return

    def Load_BPM(self):
        return

    def Parse_LongNote_LNTYPE1(self):
        return

    def Parse_LongNote_LNTYPE2(self):
        return

    def Parse_LongNote_LNOBJ(self):
        return
"""
    def Get_WAV(self):
        self.Data_Check()
        Wav_data = list()
        for temp_string in self.Data:
            if temp_string.find('#WAV') != -1:
                    temp_string = temp_string.replace("#WAV", "")
                    Wav_data.append([temp_string[0:2], temp_string[3:]])
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
        self.Data_Check()
        BPM_data = list()
        for temp_string in self.Data:
            if temp_string.find('#BPM') != -1 and temp_string.find('#BPM ') == -1:
                temp_string = temp_string.replace("#BPM", "")
                BPM_data.append([temp_string[0:2], temp_string[3:]])
        return BPM_data

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
        self.Note_Data.clear()
        self.Data_Check()
        for temp_string in self.Data:
            if temp_string[6] != ':':
                continue
            index = int(temp_string[1:4])
            while len(self.Note_Data) <= index:
                self.Note_Data.append([])
            self.Note_Data[index].append([temp_string[4:6], temp_string[7:]]) 
        return self.Note_Data

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

"""
class BMS_Loader:
    asd = 0

def Screen_init(width, height, caption):
    Screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return Screen

def Resolution_calculate(value):
    return int(float(value) * (Width / 1280))

class Data_class:
    position = 0.0
    node = -1
    channel = ''
    time = 0.0
    def __init__(self, position, node, channel):
        self.channel = channel;
        self.node = int(node)
        self.position = float(position)

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
        return BPM

pygame.mixer.pre_init(22050, -16, 2, 128)
pygame.mixer.init()
pygame.init()
pygame.mixer.set_num_channels(32)  # default is 8
screen = Screen_init(Width, Height, 'BMS Player')
pygame.mouse.set_visible(True)
clock = pygame.time.Clock()
clock.tick(Frame)
p = BMS_Parser("C:\\Users\\APSP\\Desktop\\BMS_Player\\Bundle\\004. Applesoda - JoHwa\\johwa_5a.bml")
lll = p.Parse_Sound()
for qwer in lll:
    print(qwer)