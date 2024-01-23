import os, sys, pygame, time, threading
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
    "/page": "Mengatur halaman",
}

pygame.mixer.init()
def play_music():
    while not queue.is_empty():
        if not pygame.mixer.music.get_busy() and not pygame.mixer.music.get_pos() > 0:
            pygame.mixer.music.load(f"music/{queue.dequeue()}")
            pygame.mixer.music.play()

per_page = 5
current_page = 1
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
        case '/queue':
            all_list = music_list(queue.get())
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

        case '/exit':
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()
   
        case '/help':
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