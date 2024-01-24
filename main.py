import os, sys, pygame, time, threading, random
from function import music_list, logo, paginate_list, change_file_extension, search_substring
from pprint import pprint

sys.path.append(os.path.realpath("."))
import inquirer

import random

class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        else:
            print("Antrian kosong!")

    def size(self):
        return len(self.items)

    def get(self):
        return self.items.copy()

    def shuffle(self):
        random.shuffle(self.items)

queue = Queue()

music_commands = {
    "/queue": "Menambahkan lagu ke antrian",
    "/play": "Memainkan lagu dari antrian",
    "/skip": "Melompati lagu di antrian",
    "/stop": "Menghapus semua lagu di antrian dan menghentikan lagu",
    "/pause": "Menghentikan lagu",
    "/unpause": "Melanjutkan lagu",
    "/lyrics": "Menampilkan lirik lagu",
    "/shuffle": "Mengacak lagu",
    "/search": "Mencari lagu"
}

pangination_commands = {
    "/page": "Mengatur halaman",
    "/nextpage": "Membuka halaman berikutnya",
    "/prevpage": "Membuka halaman sebelumnya",
}

system_commands = {
    "/help": "Menampilkan list semua perintah yang ada",
    "/exit": "Keluar program",
}

pygame.mixer.init()
def play_music():
    global active_song
    active_song = None
    while not queue.is_empty():
        if not pygame.mixer.music.get_busy() and not pygame.mixer.music.get_pos() > 0:
            music = queue.dequeue()
            pygame.mixer.music.load(f"music/{music}")
            pygame.mixer.music.play()
            active_song = change_file_extension(music)

def select_music(musics = None):
    if musics is None:
        all_list = music_list(queue.get())
    else:
        all_list = musics
    answers = inquirer.prompt([
        inquirer.Checkbox(
            "command",
            message="Pilih lagu yang ingin ditambahkan ke antrian",
            choices=all_list,
        ),
        inquirer.Confirm("stop", message="Apakah anda ingin melanjukan program?", default=True)
    ])
    
    if answers["stop"]:
        for music in answers["command"]:
            queue.enqueue(music)

per_page = 5
current_page = 1
active_song = None
total_page = (len(queue.get()) // per_page) + 1 if len(queue.get()) % per_page != 0 else len(queue.get()) // per_page
while True:
    logo()

    print("Queue Music List:")
    for i, music in enumerate(paginate_list(queue.get(), per_page, current_page)):
        print(f"{i+1}. {music}")
    if len(queue.get()) > 0:
        print(f"\n>>> Page {current_page}/{max(1, ((len(queue.get()) // per_page) + 1))} <<<")

    print("\n/help untuk menampilkan list semua perintah yang ada")
    answers = inquirer.prompt([
        inquirer.Text("command", message="Masukkan perintah"),
    ])

    match answers["command"]:
        case '/search':
            answers = inquirer.prompt([
                inquirer.Text("command", message="Masukkan judul lagu")
            ])
            
            select_music(search_substring(answers["command"], music_list(queue.get())))

        case '/queue':
            select_music()

        case '/play':
            threading.Thread(target=play_music).start()

        case '/pause':
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
    
        case '/unpause':
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.unpause()
  
        case '/skip':
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            threading.Thread(target=play_music).start()

        case '/stop':
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                queue.items = []
        
        case '/nextpage':
            if current_page == ((len(queue.get()) // per_page) + 1):
                current_page = 1
            else:
                current_page += 1
 
        case '/prevpage':
            if current_page == 1:
                current_page = ((len(queue.get()) // per_page) + 1)
            else:
                current_page -= 1

        case '/shuffle':
            if not queue.is_empty():
                queue.shuffle()
            
        case '/page':
            answers = inquirer.prompt([
                inquirer.List(
                    "command",
                    message="Pilih pengaturan halaman",
                    choices=["Paginate", "Per Page"],
                ),
            ])
            
            if answers["command"] == "Paginate":
                pages = [f"Page {i}" for i in range(1, total_page + 1)]
                
                answers = inquirer.prompt([
                    inquirer.List(
                        "command",
                        message="Ganti halaman",
                        choices=pages,
                    ),
                ])
                
                current_page = pages.index(answers["command"]) + 1
            elif answers["command"] == "Per Page":
                per_page = [5, 10, 15, 20]
                answers = inquirer.prompt([
                    inquirer.List(
                        "command",
                        message="Ganti jumlah per halaman",
                        choices=per_page,
                    )
                ])
                
                per_page = int(answers["command"])

        case '/lyrics':
            file_path = f"music/lyrics/{active_song}"
            try:
                os.system("clear")
                with open(file_path, 'r') as file:
                    file_content = file.read()
                    print(file_content)

            except FileNotFoundError:
                input(f"File tidak ditemukan di path: {file_path}")

            except Exception as e:
                input(f"Terjadi kesalahan: {e}")
            
            input("\nPress enter to continue...")
            
        case '/exit':
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()
   
        case '/help':
            logo()
        
            print(" Music Command ".center(30, "="))
            for key, value in music_commands.items():
                print(f"{key}: {value}")
            
            print("\n" + " Pangination Command ".center(30, "="))
            for key, value in pangination_commands.items():
                print(f"{key}: {value}")
            
            print("\n" + " System Command ".center(30, "="))
            for key, value in system_commands.items():
                print(f"{key}: {value}")
            
            answers = inquirer.prompt([
                inquirer.Confirm("stop", message="Apakah anda ingin melanjukan program?", default=True)
            ])
            if not answers["stop"]:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()