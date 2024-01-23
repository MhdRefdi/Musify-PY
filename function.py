import os
from pyfiglet import Figlet

def logo():
    os.system('clear')
    figlet = Figlet(font='larry3d')
    print(figlet.renderText('Musify CLI'))
    
def music_list(excpt=[]):
    folder_path = 'music'
    music_files = []

    for filename in os.listdir(folder_path):
        if filename.endswith(('.mp3', '.wav', '.flac', '.m4a')):
            if filename not in excpt:
                music_files.append(filename)
    
    return music_files

def paginate_list(song_list, page_size, current_page):
    start_index = (current_page - 1) * page_size
    end_index = start_index + page_size
    return song_list[start_index:end_index]

def change_file_extension(file_path, new_extension=".txt"):
    try:
        file_name, file_extension = os.path.splitext(file_path)

        new_file_path = file_name + new_extension

        return new_file_path

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")