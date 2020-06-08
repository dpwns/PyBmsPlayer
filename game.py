import os
import pygame
import time
import random

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

class Note:
    def __init__(self):
        return
    node = 0
    next = None
    position = 0.0
    timing = 0.0
    channel = '00'
    sound = None
    data = '00'
    Absolute_position = 0.0

class BMS_Parser:
    file_dir = ''
    folder_dir = ''
    Data = list() #.bms, .bml 파일 전체
    Main_Data = list() #XXXXX: ~~ 부분만, [Node, Channel, Data] 로 구성
    LongNote_Type = 0 #1 => LNTYPE 1 , 2 => LNTYPE 2 , 3 => LNOBJ
    MaxNode = 0

    def __init__(self, file_directory):
        self.file_dir = file_directory
        self.folder_dir = self.file_dir
        while len(self.folder_dir) > 0:
            if self.folder_dir[-1] == '\\':
                self.folder_dir = self.folder_dir[0:-1]
                break
            else:
                self.folder_dir = self.folder_dir[0:-1]

    def Reset(self):
        self.file_dir = ''
        self.folder_dir = ''
        self.Data = self.Data.clear()
        self.Main_Data = self.Main_Data.clear()
        self.LongNote_Type = 0

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
        if self.Data == None or len(self.Data) <= 0:
            self.Read_Data()

    def Main_Data_Check(self): #Main_Data 리스트 체크
        if self.Main_Data == None or len(self.Main_Data) <= 0:
            self.Parse_Main_Data()

    def Read_Data(self): #파일 전체 읽기 / #으로 시작하는 부분만 저장
        self.Data.clear()
        if self.file_dir == '': 
            return
        File = open(self.file_dir, 'r', encoding='UTF8')
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
    
    def Parse_Main_Data(self): #Main_Data 읽기 , [node, channel, data]
        self.Main_Data.clear()
        self.Data_Check()
        Data_list = list()
        IsIgnore = False
        ignoreElse = False
        randomValue = -1
        for temp_string in self.Data:
            if temp_string.find('#RANDOM ') != -1:
                temp_string = temp_string.replace("#RANDOM ", "")
                randomValue = random.randint(1, int(temp_string))
                continue
            if temp_string.find('#ENDIF') != -1:
                IsIgnore = False
                continue
            if temp_string.find('#IF') != -1:
                temp_string = temp_string.replace("#IF ", "")
                if int(temp_string) != randomValue:
                    IsIgnore = True
                else:
                    ignoreElse = True
                continue
            if temp_string.find('#ELSE') != -1:
                if ignoreElse:
                    IsIgnore = True
                continue
            if IsIgnore:
                continue

            if temp_string[6] != ':':
                continue
            node = temp_string[1:4]
            if int(node) > self.MaxNode:
                self.MaxNode = int(node)
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

    def Parse_Stp(self):
        self.Data_Check()
        Stop_list = list()
        for temp in self.Data:
            if temp.find('#STP') != -1:
                temp = temp.replace("#STP", 0)
                node = temp[0:3]
                position = float(int(temp[4:7]) / 1000)
                data = float(int(temp[8:]) / 1000)
                note_obj = Note()
                note_obj.node = node
                note_obj.channel = '09'
                note_obj.position = position
                note_obj.data = data
                Stop_list.append(note_obj)
        return Stop_list

    def Parse_Start_BPM(self): #시작 BPM 읽기
        self.Data_Check()
        BPM = None
        for temp_string in self.Data:
            if temp_string.find('#BPM ') != -1:
                temp_string = temp_string.replace("#BPM ", "")
                BPM_data = temp_string
                BPM = float(BPM_data)
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

    def Parse_Extended_BPM(self): #확장 BPM 읽기 (08채널, 03채널)
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

    def Parse_Sound(self): # #WAV 읽기
        self.Data_Check()
        Key_Sound = list()
        for temp_string in self.Data:
            if temp_string.find('#WAV') != -1:
                temp_string = temp_string.replace("#WAV", "")
                Key_Sound.append([temp_string[0:2], temp_string[3:]])
        return Key_Sound

    def Load_Key_Sound(self): #mp3, wav, ogg 파일 로드 ['XX', sound오브젝트]
        load_wav = list()
        file_data = self.Parse_Sound()
        wav_dir = self.folder_dir[self.folder_dir.find('Bundle'):] + '\\'
        for wav in file_data:
            sound = None
            dir_temp = wav_dir + wav[1]
            if not os.path.isfile(self.folder_dir + '\\' + wav[1]):
                wav[1] = wav[1].replace(".wav", ".ogg")
                if not os.path.isfile(self.folder_dir + '\\' + wav[1]):
                    dir_temp = wav_dir + wav[1]
                    sound = pygame.mixer.Sound(dir_temp)
            else:
                sound = pygame.mixer.Sound(dir_temp)
            load_wav.append([wav[0], sound])
        return load_wav

    def Parse_LNOBJ_Type(self):
        self.Data_Check()
        for temp_string in self.Data:
            if temp_string.find('#LNOBJ ') != -1:
                return temp_string
            elif temp_string.find('#LNTYPE 2') != -1:
                return temp_string
            elif temp_string.find('#LNTYPE 1') != -1:
                return temp_string
        return ''

    def Parse_Node_Length(self):
        self.Main_Data_Check()
        List = list()
        index = 0
        for temp in self.Main_Data:
            if temp[1] == '02':
                while len(List) < int(temp[0]):
                    List.append([index, float(1)])
                    index = index + 1
                List.append([int(temp[0]), float(temp[2])])
                index = index + 1
        while len(List) <= self.MaxNode:
            List.append([index, float(1)])
            index = index + 1
        return List

    def Get_Note(self):
        self.Main_Data_Check()
        data_list = list()
        Player1_channel = list()
        Player2_channel = list()
        Key_sound = self.Load_Key_Sound()

        LNOBJ_type = self.Parse_LNOBJ_Type()
        LNOBJ_data = ''
        if LNOBJ_type.find('#LNOBJ ') != -1:
            LNOBJ_data = LNOBJ_type[7:]
            LNOBJ_type = 3
        elif LNOBJ_type.find('#LNTYPE 2') != -1:
            LNOBJ_type = 2
        else:
            LNOBJ_type = 1
        channel_divided = list() #[channel, list()]
        Processed_Data = list()
        for temp in self.Main_Data:
            channel_found  = False
            for temp_channel in channel_divided:
                if temp[1] == temp_channel[0]:
                    channel_found = True
            if not channel_found:
                channel_divided.append([temp[1], list()])
            for temp_channel in channel_divided:
                if temp[1] == temp_channel[0]:
                    temp_channel[1].append(temp)
                    break
        for DataList in channel_divided:
            Prev_note = None
            Prev_data = ''
            temp_Processed = list()
            count = 0
            for temp in DataList[1]:
                data = temp[2]
                note_obj = None
                max_index = int(len(data) / 2)
                index = 0
                while len(data) > 0:
                    if data[0:2] == '00':
                        Prev_data = '00'
                        index = index + 1
                        data = data[2:]
                        continue

                    note_obj = Note()
                    note_obj.data = data[0:2]
                    
                    for sound_temp in Key_sound:
                        if sound_temp[0] == note_obj.data:
                            note_obj.sound = sound_temp[1]
                            break
                    if Prev_note != None:
                        if LNOBJ_type == 3 and note_obj.data == LNOBJ_data:
                            Prev_note.next = note_obj
                    if DataList[0][0] == '5' or DataList[0][0] == '6':
                        if LNOBJ_type == 2:
                            if Prev_note != None:
                                if Prev_note.data == note_obj.data and Prev_data == note_obj.data:
                                    Prev_note.next = note_obj
                            temp_note = Note()
                            temp_note.node = temp[0]
                            temp_note.channel = temp[1]
                            temp_note.position = float(index / max_index)
                            note_obj.next = temp_note
                        elif LNOBJ_type == 1:
                            if Prev_note != None:
                                if Prev_note.next == None and count % 2 == 1:
                                    Prev_note.next = note_obj
                                    temp_note = Note()
                                    temp_note.node = temp[0]
                                    temp_note.channel = temp[1]
                                    temp_note.position = float(index / max_index)
                                    note_obj.next = temp_note
                    note_obj.position = float(index / max_index)
                    note_obj.node = temp[0]
                    note_obj.channel = temp[1]
                    if note_obj.channel[0] == '5' or note_obj.channel[0] == '6':
                        note_obj.channel = str(int(note_obj.channel) - 40)
                    index = index + 1
                    if Prev_note != None:
                        if not (LNOBJ_type == 3 and Prev_note.next == note_obj):
                            temp_Processed.append(note_obj)
                    else:
                        temp_Processed.append(note_obj)
                    count = count + 1
                    data = data[2:]
                    Prev_note = note_obj
                    Prev_data = note_obj.data
            
            for temp_note in temp_Processed:
                if temp_note.next == None:
                    continue
                while temp_note.next.next != None:
                    temp_Processed.remove(temp_note.next)
                    temp_note.next = temp_note.next.next
            data_list.append([DataList[0], sorted(temp_Processed, key=lambda note: float(note.node) + float(note.position))])

        return data_list

    def Get_Node_Length(self): #[[Node, 길이], [Node, 누적길이]]
        List = list()
        List.append(self.Parse_Node_Length())
        List.append(list())
        sum = 0.0
        for temp in List[0]:
            sum = sum + temp[1]
            List[1].append([temp[0], sum])
        return List

    def Get_Stop(self):
        Data = self.Parse_Stop()
        BPM_list = self.Get_BPM()
        StartBPM = float(self.Parse_Start_BPM())
        BPM = StartBPM
        stop_list = list()
        for temp in Data:
            max_index = int(len(temp[1]))
            data = temp[1]
            index = 0
            for ttemp in data:
                BPM = StartBPM
                note_obj = Note()
                note_obj.channel = '09'
                note_obj.node = temp[0]
                note_obj.position = float(index / max_index)
                for bpm in BPM_list:
                    if float(bpm.position) + float(bpm.node) <= float(note_obj.node) + float(note_obj.position):
                        BPM = float(bpm.data)
                    else:
                        break
                note_obj.data = float(int(ttemp) / 192 * 240 / BPM)
                stop_list.append(note_obj)
                index = index + 1
        temp = self.Parse_Stp()
        for ttemp in temp:
            stop_list.append(ttemp)
        stop_list = sorted(stop_list, key=lambda note: float(note.node) + float(note.position))
        return stop_list

    def Get_BPM(self):
        bpm = self.Parse_Extended_BPM()
        List = list()
        for temp in bpm:
            index = -1
            note_obj = Note()
            for ttemp in temp[1]:
                index = index + 1
                if ttemp == '00' or ttemp == '0':
                    continue
                note_obj = Note()
                note_obj.data = float(ttemp)
                note_obj.node = int(temp[0])
                note_obj.position = float(index / len(temp[1]))
                List.append(note_obj)
        List = sorted(List, key=lambda note: float(note.node + note.position))
        return List

    def Set_Note_Timing(self):
        self.Data_Check()
        self.Main_Data_Check()
        StartBPM = float(self.Parse_Start_BPM())
        BPM = StartBPM
        BPM_list = self.Get_BPM()
        Stop = self.Get_Stop()
        Length = self.Get_Node_Length()
        Note_list = self.Get_Note()
        Prev_length = 0.0
        Prev_timing = None
        for temp in BPM_list:
            length = 0.0
            temp.timing = 0.0
            node = int(temp.node)
            length = float(Length[1][node][1]) - float(Length[0][node][1]) * (1 - float(temp.position))
            temp.Absolute_position = length
            lengthTemp = length
            length = length - Prev_length
            Prev_length = lengthTemp
            if Prev_timing == None:
                temp.timing = float(BPM / 60 * length)
            else:
                temp.timing = float(BPM / 60 * length) + Prev_timing.timing
            Prev_timing = temp
            BPM = float(temp.data)
        for temp in Stop:
            BPM = StartBPM
            temp_BPM = None
            for ttemp in BPM_list:
                if float(ttemp.node) + float(ttemp.position) <= float(temp.node) + float(temp.position):
                    temp_BPM = ttemp
                    BPM = float(ttemp.data)
                else:
                    break
            node = int(temp.node)
            length = float(Length[1][node][1]) - float(Length[0][node][1]) * (1 - float(temp.position))
            temp.Absolute_position = length
            if temp_BPM != None:
                temp.timing = float(BPM / 60 * length)
            else:
                length = length - float(Length[1][temp_BPM.node] - Length[0][temp_BPM.node] * (1 - temp_BPM.position))
                temp.timing = float(BPM / 60 * length) + temp_BPM.timing
        for temp in Note_list:
            for ttemp in temp[1]:
                node = int(ttemp.node)
                length = float(Length[1][node][1]) - float(Length[0][node][1]) * (1 - float(ttemp.position))
                ttemp.Absolute_position = length
                bpm_note = None
                for temp_bpm in BPM_list:
                    if temp_bpm.Absolute_position > length:
                        break
                    bpm_note = temp_bpm
                if bpm_note == None:
                    ttemp.timing = float(StartBPM / 60 * length)
                else:
                    ttemp.timing = float(float(bpm_note.data) / 60 * (length - bpm_note.Absolute_position)) + bpm_note.timing
        for temp in Stop:
            for ttemp in Stop:
                if temp.Absolute_position < ttemp.Absolute_position:
                    ttemp.timing = ttemp.timing + float(temp.data)
            for ttemp in BPM_list:
                if temp.Absolute_position < ttemp.Absolute_position:
                    ttemp.timing = ttemp.timing + float(temp.data)
            for ttemp in Note_list:
                for tttemp in ttemp[1]:
                    if temp.Absolute_position < tttemp.Absolute_position:
                        tttemp.timing = tttemp.timing + float(temp.data)
        asdf = list()
        asdf.append(BPM_list)
        asdf.append(Stop)
        asdf.append(Note_list)
        return asdf

class BMS_Player:
    position = -1
    BPM = 0.0
    Frame = 100
    speed = 3
    Difficult = 1.0
    maxIndex = 0

    Prev_Time = None

    Start_time = None

    Note_data = None
    Stop_data = None
    BPM_data = None
    BGM_data = None
    Length_data = None

    Parser = BMS_Parser('')

    channel_index = 0

    counter = 0
    FrameTemp = 0

    Stop = 0.0

    def Main(self):
        return

    def Song_select(self):
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

    def Move(self):
        screen.fill(BLACK)
        t = time.time()
        for temp in self.BPM_data:
            if float(temp.Absolute_position) <= self.position:
                self.BPM = float(temp.data)
                self.BPM_data.remove(temp)
            else:
                break
        for temp in self.Stop_data:
            if temp.Absolute_position <= self.position:
                self.Stop = float(temp.data)
                self.Stop_data.remove(temp)
            else:
                break
        fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', 20)
        tempSum = (time.time() - self.Prev_Time)
        if tempSum > 0:
            self.FrameTemp = self.FrameTemp + 1 / tempSum
            self.counter = (self.counter + 1) % 200
        if self.counter == 0:
            self.Frame = self.FrameTemp / 200
            self.FrameTemp = 0
        text = fontObj.render("Frame : " + str(self.Frame), True, WHITE)
        screen.blit(text, (500, 0))

        if self.Stop > 0:
            self.Stop = self.Stop + self.Prev_Time - t
            self.Prev_Time = t
        elif t - self.Prev_Time >= 0:
            self.position = self.position + float(self.BPM / 240) * (t - self.Prev_Time)
            self.Prev_Time = t
    
    def Draw_Note(self, screen):
        End = False
        clock = pygame.time.Clock()
        for index1 in range(1, 8):
            pygame.draw.line(screen, WHITE, [40 * index1 , 0], [40 * index1, 600], 1)
        pygame.draw.line(screen, WHITE, [0, 600], [280, 600], 2)
        for ttemp in self.Length_data[1]:
            if float(ttemp[1]) - self.position < 0:
                continue
            if float(ttemp[1]) - self.position > 1 / self.speed:
                break
            pygame.draw.line(screen, WHITE, [0, 600 - round((float(ttemp[1]) - self.position) * 600 * self.speed)], [280, 600 - round((float(ttemp[1]) - self.position) * 600 * self.speed)], 1)
        for temp in self.Note_data:
            position = 0.0
            position = float(temp.Absolute_position)
            position2 = position
            if position - self.position < 0 and temp.sound != None:
                temp.sound.play()
            if position - self.position < 0 and temp.next == None:
                self.Note_data.remove(temp)
                continue
            if temp.next != None:
                temp2 = temp.next
                position2 = float(temp2.Absolute_position)
                if position2 - self.position < 0:
                    if temp2 in self.Note_data:
                        self.Note_data.remove(temp2)
                    self.Note_data.remove(temp)
            if position - self.position > float(1 / self.speed):
                break
            x = 0
            color = WHITE
            if temp.channel == '11':#1
                x = 40
            elif temp.channel == '12':
                color = BLUE
                x = 80
            elif temp.channel == '13':#3
                x = 120
            elif temp.channel == '14':
                color = BLUE
                x = 160
            elif temp.channel == '15':#5
                x = 200
            elif temp.channel == '16': #0
                color = RED
                x = 0
            elif temp.channel == '18':
                x = 240
            elif temp.channel == '19':
                x = 280
            else:
                continue
            if position == position2:
                pygame.draw.line(screen, color, [x, 600 - round((position - self.position) * 600 * self.speed)],[x+40, 600 - round((position - self.position) * 600 * self.speed)], 4)
            else:
                if position - self.position < 0:
                    pygame.draw.rect(screen, color, [x, 600 - round((position2 - self.position) * 600 * self.speed), 40, round((position2 - self.position) * 600)])
                else:
                    pygame.draw.rect(screen, color, [x, 600 - round((position2 - self.position) * 600 * self.speed), 40, round((position2 - position) * 600)])
        pygame.display.flip()
        return

    def Process_Input(self):
        return

def Screen_init(width, height, caption):
    Screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return Screen

def Resolution_calculate(value):
    return int(float(value) * (Width / 1280))

pygame.mixer.pre_init(22050, -16, 2, 128)
pygame.mixer.init()
pygame.init()
pygame.mixer.set_num_channels(32)  # default is 8
screen = Screen_init(Width, Height, 'BMS Player')
pygame.mouse.set_visible(True)
clock = pygame.time.Clock()
clock.tick(Frame)
#p = BMS_Parser("C:\\Users\\APSP\\Desktop\\BMS_Player\\Bundle\\Moonrise\\HD.bms")
#p = BMS_Parser(os.getcwd() + "\\Bundle\\004. Applesoda - JoHwa\\johwa_5a.bml")
while True:
    PPP = BMS_Player()
    asdfqwer = PPP.Song_select()
    p = BMS_Parser(asdfqwer)
    q = p.Set_Note_Timing()
    w = list()
    for temp in q[2]:
        for ttemp in temp[1]:
            w.append(ttemp)
    w = sorted(w, key=lambda qwer: float(qwer.Absolute_position))
    PPP.Stop_data = sorted(q[1], key=lambda qwer: float(qwer.Absolute_position))
    PPP.BPM_data = sorted(q[0], key=lambda qwer: float(qwer.Absolute_position))
    PPP.BPM = float(p.Parse_Start_BPM())
    PPP.Length_data = p.Get_Node_Length()
    PPP.Note_data = w
    PPP.Prev_Time = time.time()
    PPP.Start_time = PPP.Prev_Time
    PPP.maxIndex = len(PPP.Length_data)
    counter = 0
    while True:
        PPP.Move()
        counter = counter + 1
        counter = counter % 5
        if counter == 0:
            PPP.Draw_Note(screen)
        if len(PPP.Note_data) == 0 and len(PPP.Length_data) == 0:
            break