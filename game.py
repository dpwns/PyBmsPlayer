import os
import pygame

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 80

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
        while True:
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
        if (self.file_dir == ''): return
        File = open(self.file_dir, 'r')
        Header_data = [
        ['Player', ''],
        ['Genre', ''],
        ['Title', ''],
        ['Artist', ''],
        ['BPM', ''],
        ['PlayLevel', ''],
        ['Rank', ''],
        ['Total', '']]
        temp_string = File.readline()
        while temp_string != '' and temp_string.find('MAIN DATA FIELD') == -1:
            temp_string = temp_string.replace('\n', '')
            if not line: break
            if temp_string.find('#PLAYER') != -1:
                Header_data[0][1] = temp_string.replace("#PLAYER ", "")
            elif temp_string.find('#GENRE') != -1:
                Header_data[1][1] = temp_string.replace("#GENRE ", "")
            elif temp_string.find('#TITLE') != -1:
                Header_data[2][1] = temp_string.replace("#TITLE ", "")
            elif temp_string.find('#ARTIST') != -1:
                Header_data[3][1] = temp_string.replace("#ARTIST ", "")
            elif temp_string.find('#BPM') != -1:
                Header_data[4][1] = temp_string.replace("#BPM ", "")
            elif temp_string.find('#PLAYLEVEL') != -1:
                Header_data[5][1] = temp_string.replace("#PLAYLEVEL ", "")
            elif temp_string.find('#RANK') != -1:
                Header_data[6][1] = temp_string.replace("#RANK ", "")
            elif temp_string.find('#TOTAL') != -1:
                Header_data[7][1] = temp_string.replace("#TOTAL ", "")
            temp_string = File.readline()
        File.close()
        return Header_data
    
    def Get_WAV(self):
        if (self.file_dir == ''): return
        File = open(self.file_dir, 'r')
        temp_string = File.readline()
        Wav_data = list()
        while temp_string != '' and temp_string.find('MAIN DATA FIELD') == -1:
            temp_string = temp_string.replace('\n', '')
            if not temp_string: break
            if temp_string.find('#WAV') != -1:
                temp_string = temp_string.replace("#WAV", "")
                Wav_data.append([temp_string[0:2], temp_string[3:]])
            temp_string = File.readline()
        print(Wav_data)
    
    def Get_note_data(self):
        if (self.file_dir == ''): return
        track = list()
        File = open(self.file_dir, 'r')
        temp_string = File.readline()
        while temp_string != '' and temp_string.find('MAIN DATA FIELD') == -1:
            temp_string = File.readline()
            if not temp_string: break

        while temp_string != '':
            temp_string = File.readline()
            if not temp_string: break
            if temp_string.find('#') == -1:
                continue
            temp_string = temp_string.replace('\n', '')
            track.append([temp_string[1:4], temp_string[4:6], temp_string[7:]])

        return track

    def Get_note_data_bar(self, bar_number):
        if (self.file_dir == ''): return
        track = list()
        File = open(self.file_dir, 'r')
        temp_string = File.readline()
        bar_number = str(bar_number)

        while temp_string != '' and temp_string.find('MAIN DATA FIELD') == -1:
            temp_string = File.readline()
            if not temp_string: break

        while temp_string != '':
            temp_string = File.readline()
            if not temp_string: break
            if temp_string.find('#') == -1:
                continue

            if bar_number == temp_string[1:4]:
                temp_string = temp_string.replace('\n', '')
                track.append([temp_string[1:4], temp_string[4:6], temp_string[7:]])

        return track

temp = Bundle.Get_script_file_directory('004. Applesoda - JoHwa')
print(temp[0])
p = BMS_Parser(temp[0])
p.Get_note_data()
