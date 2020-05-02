import os
import pygame

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
            if self.folder_dir[-1] is '\\':
                self.folder_dir = self.folder_dir[0:-1]
                break
            else:
                self.folder_dir = self.folder_dir[0:-1]

    def Set_file_directory(self, directory):
        self.file_dir = directory
        self.folder_dir = self.file_dir
        while True:
            if self.folder_dir[-1] is '\\':
                self.folder_dir = self.folder_dir[0:-1]
                break
            else:
                self.folder_dir = self.folder_dir[0:-1]

    def Get_Header(self):
        if self.file_dir is '': 
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
        while temp_string is not '' and temp_string.find('MAIN DATA FIELD') is not -1:
            temp_string = temp_string.replace('\n', '')
            if temp_string.startswith('#'):
                if temp_string.find('#PLAYER ') is not -1:
                    Header_data[0][1] = temp_string.replace("#PLAYER ", "")
                elif temp_string.find('#GENRE ') is not -1:
                    Header_data[1][1] = temp_string.replace("#GENRE ", "")
                elif temp_string.find('#TITLE ') is not -1:
                    Header_data[2][1] = temp_string.replace("#TITLE ", "")
                elif temp_string.find('#ARTIST ') is not -1:
                    Header_data[3][1] = temp_string.replace("#ARTIST ", "")
                elif temp_string.find('#BPM ') is not -1:
                    Header_data[4][1] = temp_string.replace("#BPM ", "")
                elif temp_string.find('#PLAYLEVEL ') is not -1:
                    Header_data[5][1] = temp_string.replace("#PLAYLEVEL ", "")
                elif temp_string.find('#RANK ') is not -1:
                    Header_data[6][1] = temp_string.replace("#RANK ", "")
                elif temp_string.find('#VOLWAV ') is not -1:
                    Header_data[7][1] = temp_string.replace("#VOLWAV ", "")
                elif temp_string.find('#STAGEFILE ') is not -1:
                    Header_data[8][1] = temp_string.replace("#STAGEFILE", "")
                elif temp_string.find('#TOTAL ') is not -1:
                    Header_data[9][1] = temp_string.replace("#TOTAL ", "")
                elif temp_string.find('#MIDIFILE ') is not -1:
                    Header_data[10][1] = temp_string.replace("#MIDIFILE ", "")
                elif temp_string.find('#VIDEOFILE ') is not -1:
                    Header_data[11][1] = temp_string.replace("#VIDEOFILE ", "")
                elif temp_string.find('#BMP ') is not -1:
                    Header_data[12][1] = temp_string.replace("#BMP ", "")
            temp_string = File.readline()
        File.close()
        return Header_data

    def Get_WAV(self):
        if self.file_dir is '': 
            return
        File = open(self.file_dir, 'r')
        temp_string = File.readline()
        Wav_data = list()
        while temp_string is not '' and temp_string.find('MAIN DATA FIELD') is -1:
            temp_string = temp_string.replace('\n', '')
            if temp_string.startswith('#'):
                if temp_string.find('#WAV') is not -1:
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
        if self.file_dir is '': 
            return
        File = open(self.file_dir, 'r')
        temp_string = File.readline()
        BPM_data = list()
        while temp_string is not '' and temp_string.find('MAIN DATA FIELD') is -1:
            temp_string = temp_string.replace('\n', '')
            if (temp_string.startswith('#')):
                if temp_string.find('#BPM') is not -1 and temp_string.find('#BPM ') is -1:
                    temp_string = temp_string.replace("#BPM", "")
                    BPM_data.append([temp_string[0:2], temp_string[3:]])
            temp_string = File.readline()
        File.close()
        return BPM_data
    
    def Get_stop(self):
        if self.file_dir is '': 
            return
        File = open(self.file_dir, 'r')
        temp_string = File.readline()
        Stop_data = list()
        while temp_string is not '' and temp_string.find('MAIN DATA FIELD') is -1:
            temp_string = temp_string.replace('\n', '')
            if (temp_string.startswith('#')):
                if temp_string.find('#STOP') is not -1:
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
            if len(temp) <= 0 or temp is []:
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
        if self.file_dir is '': 
            return
        track = list()
        File = open(self.file_dir, 'r')
        temp_string = File.readline()
        while temp_string != '':
            temp_string = File.readline()
            if not temp_string.startswith('#'):
                continue
            if temp_string[6] is not ':':
                continue
            temp_string = temp_string.replace('\n', '')
            index = int(temp_string[1:4])
            while len(track) <= index:
                track.append([])
            track[index].append([temp_string[4:6], temp_string[7:]])
        File.close()
        return track

    def Get_note_data_channel(self, channel):
        if self.file_dir is '': 
            return
        channel = str(channel)
        if len(channel) > 2 or len(channel) is 0:
            return        
        elif len(channel) is 1:
            channel = '0' + channel
        track = list()
        File = open(self.file_dir, 'r')
        temp_string = File.readline()
        while temp_string is not '' and temp_string.find('MAIN DATA FIELD') is -1:
            temp_string = File.readline()
            if not temp_string: 
                break
        while temp_string is not '':
            temp_string = File.readline()
            if not temp_string: 
                break
            if temp_string.find('#') is -1:
                continue
            if temp_string[6] is not ':':
                continue
            temp_string = temp_string.replace('\n', '')
            index = int(temp_string[1:4])
            while len(track) <= index:
                track.append([])
            if temp_string[4:6] is channel:
                track[index].append([temp_string[4:6], temp_string[7:]])
        File.close()
        return track

    def Get_note_data_bar(self, bar_number):
        track = self.Get_note_data()
        bar_number = int(bar_number)
        if bar_number >= len(track) or bar_number < 0:
            return
        return track[int(bar_number)]