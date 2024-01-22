import os, sys, pygame, time, threading
from tabulate import tabulate
from function import music_list, logo, paginate_list
from pprint import pprint

sys.path.append(os.path.realpath("."))
import inquirer

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

queue = Queue()

music_commands = {
    "/queue": "Menambahkan lagu ke antrian",
    "/play": "Memainkan lagu dari antrian",
    "/skip": "Melompati lagu di antrian",
    "/stop": "Menghapus semua lagu di antrian dan menghentikan lagu",
    "/pause": "Menghentikan lagu",
    "/unpause": "Melanjutkan lagu",
    "/help": "Menampilkan list semua perintah yang ada",
    "/nextpage": "Membuka halaman berikutnya",
    "/prevpage": "Membuka halaman sebelumnya",
    "/exit": "Keluar program",
}

pygame.mixer.init()
def play_music():
    while not queue.is_empty():
        if not pygame.mixer.music.get_busy() and not pygame.mixer.music.get_pos() > 0:
            pygame.mixer.music.load(f"music/{queue.dequeue()}")
            pygame.mixer.music.play()

per_page = 3
current_page = 1
global_run = True
while global_run:
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
    
    if answers["command"] == "/queue":
        all_list = music_list(queue.get())
        all_list.append(">>> Menu Utama <<<")
        answers = inquirer.prompt([
            inquirer.List(
                "queue",
                message="Pilih lagu yang ingin ditambahkan ke antrian",
                choices= all_list,
            )
        ])
        
        if answers["queue"] != ">>> Menu Utama <<<":
            queue.enqueue(answers["queue"])
    elif answers["command"] == "/play":
        threading.Thread(target=play_music).start()
    elif answers["command"] == "/pause":
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
    elif answers["command"] == "/unpause":
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
    elif answers["command"] == "/skip":
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        threading.Thread(target=play_music).start()
    elif answers["command"] == "/stop":
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            queue.items = []
    elif answers["command"] == "/nextpage":
        if current_page == ((len(queue.get()) // per_page) + 1):
            current_page = 1
        else:
            current_page += 1
    elif answers["command"] == "/prevpage":
        if current_page == 1:
            current_page = ((len(queue.get()) // per_page) + 1)
        else:
            current_page -= 1
    elif answers["command"] == "/exit":
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()
    elif answers["command"] == "/help":
        logo()
        
        for key, value in music_commands.items():
            print(key, ":", value)
        
        answers = inquirer.prompt([
            inquirer.Confirm("stop", message="Apakah anda ingin melanjukan program?", default=True)
        ])
        if not answers["stop"]:
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()