import os, re
from pyfiglet import Figlet

class TreeNode:
    def __init__(self, music_data):
        self.music_data = music_data
        self.left = None
        self.right = None

class MusicBST:
    def __init__(self):
        self.root = None

    def insert(self, music_data):
        self.root = self._insert(self.root, music_data)

    def _insert(self, node, music_data):
        if node is None:
            return TreeNode(music_data)

        if music_data < node.music_data:
            node.left = self._insert(node.left, music_data)
        elif music_data > node.music_data:
            node.right = self._insert(node.right, music_data)

        return node

    def search(self, substring):
        result = []
        self._search(self.root, substring, result)
        return result

    def _search(self, node, substring, result):
        if node:
            self._search(node.left, substring, result)
            if re.search(re.escape(substring), node.music_data, re.IGNORECASE):
                result.append(node.music_data)
            self._search(node.right, substring, result)

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

def search_music(substring, my_list = []):
    substring = substring.lower()
    music_bst = MusicBST()
    for music in my_list:
        music_bst.insert(music)
    return music_bst.search(substring)