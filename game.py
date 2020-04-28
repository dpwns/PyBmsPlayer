import os
import pygame
import sys

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
        ['Total', '']]
        temp_string = File.readline()
        while temp_string != '' and temp_string.find('MAIN DATA FIELD') == -1:
            if not temp_string: 
                break
            temp_string = temp_string.replace('\n', '')
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
        if (self.file_dir == ''): 
            return
        File = open(self.file_dir, 'r')
        temp_string = File.readline()
        Wav_data = list()
        while temp_string != '' and temp_string.find('MAIN DATA FIELD') == -1:
            temp_string = temp_string.replace('\n', '')
            if not temp_string: 
                break
            if temp_string.find('#WAV') != -1:
                temp_string = temp_string.replace("#WAV", "")
                Wav_data.append([temp_string[0:2], temp_string[3:]])
            temp_string = File.readline()
        File.close()
        return Wav_data
    
    def Get_note_data(self):
        if (self.file_dir == ''): 
            return
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
            temp_string = temp_string.replace('\n', '')
            track.append([temp_string[1:4], temp_string[4:6], temp_string[7:]])
            print(temp_string[1:4])
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
            temp_string = temp_string.replace('\n', '')
            if temp_string[4:6] == channel:
                track.append([temp_string[1:4], temp_string[4:6], temp_string[7:]])
        File.close()
        return track

    def Get_note_data_bar(self, bar_number):
        if (self.file_dir == ''): 
            return
        bar_number = str(bar_number)
        if len(bar_number) == 0:
            bar_number = '000'
        elif len(bar_number) == 1:
            bar_number = '00' + bar_number
        elif len(bar_number) == 2:
            bar_number = '0' + bar_number
        print(bar_number)
        track = list()
        File = open(self.file_dir, 'r')
        temp_string = File.readline()
        bar_number = str(bar_number)
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
            if bar_number == temp_string[1:4]:
                temp_string = temp_string.replace('\n', '')
                track.append([temp_string[1:4], temp_string[4:6], temp_string[7:]])
        File.close()
        return track

def Screen_init(width, height, caption):
    Screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return Screen

def Song_select():
    clock = pygame.time.Clock()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
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
        clock.tick(60)
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
            if max_song_index == 0:
                fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', 20)
                text = fontObj.render('Empty', True, WHITE)
                screen.blit(text, (0, 10))
                pygame.display.flip()
                continue
            
            if select_song_index - 3 >= 0:
                fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', 20)
                text = fontObj.render(song_list[select_song_index - 3], True, WHITE)
                screen.blit(text, (0, 10))
            if select_song_index - 2 >= 0:
                fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', 20)
                text = fontObj.render(song_list[select_song_index - 2], True, WHITE)
                screen.blit(text, (0, 40))
            if select_song_index - 1 >= 0:
                fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', 20)
                text = fontObj.render(song_list[select_song_index - 1], True, WHITE)
                screen.blit(text, (0, 70))

            fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', 30)
            text = fontObj.render(song_list[select_song_index], True, WHITE)
            screen.blit(text, (10, 120))

            if select_song_index + 1 < max_song_index:
                fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', 20)
                text = fontObj.render(song_list[select_song_index + 1], True, WHITE)
                screen.blit(text, (0, 170))
            if select_song_index + 2 < max_song_index:
                fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', 20)
                text = fontObj.render(song_list[select_song_index + 2], True, WHITE)
                screen.blit(text, (0, 200))
            if select_song_index + 3 < max_song_index:
                fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', 20)
                text = fontObj.render(song_list[select_song_index + 3], True, WHITE)
                screen.blit(text, (0, 230))
        else:
            song_file_list = Bundle.Get_script_file(song_list[select_song_index])
            max_song_file_index = len(song_file_list)
            if max_song_file_index == 0:
                fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', 20)
                text = fontObj.render('Empty', True, WHITE)
                screen.blit(text, (0, 10))
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
            if select_song_file_index - 3 >= 0:
                fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', 20)
                text = fontObj.render(song_file_list[select_song_file_index - 3], True, WHITE)
                screen.blit(text, (0, 10))
            if select_song_file_index - 2 >= 0:
                fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', 20)
                text = fontObj.render(song_file_list[select_song_file_index - 2], True, WHITE)
                screen.blit(text, (0, 40))
            if select_song_file_index - 1 >= 0:
                fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', 20)
                text = fontObj.render(song_file_list[select_song_file_index - 1], True, WHITE)
                screen.blit(text, (0, 70))

            fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', 30)
            text = fontObj.render(song_file_list[select_song_file_index], True, WHITE)
            screen.blit(text, (10, 120))

            if select_song_file_index + 1 < max_song_file_index:
                fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', 20)
                text = fontObj.render(song_file_list[select_song_file_index + 1], True, WHITE)
                screen.blit(text, (0, 170))
            if select_song_file_index + 2 < max_song_file_index:
                fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', 20)
                text = fontObj.render(song_file_list[select_song_file_index + 2], True, WHITE)
                screen.blit(text, (0, 200))
            if select_song_file_index + 3 < max_song_file_index:
                fontObj = pygame.font.Font('font/NanumGothicCoding.ttf', 20)
                text = fontObj.render(song_file_list[select_song_file_index + 3], True, WHITE)
                screen.blit(text, (0, 230))
        pygame.display.flip()
    return

pygame.init()
screen = Screen_init(1280, 720, 'PPAP')
pygame.mouse.set_visible(True)

Song_select()