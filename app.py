import pygame
import sys
import random

# Αρχικοποίηση του Pygame
pygame.init()

# Διαστάσεις του παραθύρου
window_width = 800
window_height = 500

# Δημιουργία του παραθύρου με τον τίτλο "Car-X"
win = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Drunk Driver")

# Φόντο
clock = pygame.time.Clock()
FPS = 60
bg_img = pygame.image.load("Resourses/Game_objects/background.png").convert()  # Φορτώνει την εικόνα του φόντου
bg_img = pygame.transform.scale(bg_img, (window_width, window_height))  # Αλλάζει το μέγεθος της εικόνας για να ταιριάζει στο παράθυρο
bg_x = 0  # Αρχική θέση του φόντου
bg_vel = 5  # Ταχύτητα κίνησης του φόντου


# Μετρητής νομισμάτων
coins_collected = 0
font = pygame.font.SysFont(None, 36)  # Δημιουργία γραμματοσειράς
coins_collected_text = font.render("Coins: " + str(coins_collected), True, (0, 0, 0))  # Δημιουργία κειμένου με μαύρο χρώμα
coins_collected_rect = coins_collected_text.get_rect(topleft=(10, 10))  # Θέση του μετρητή νομισμάτων


# Φόρτωση της μουσικής
pygame.mixer.music.load("Resourses/Audio_sounds/background_music.mp3")
pygame.mixer.music.play(-1)  # Αναπαραγωγή της μουσικής σε επανάληψη

# Φόρτωση των ήχων
jump_sound = pygame.mixer.Sound("Resourses/Audio_sounds/jump_sound.wav")
game_over_sound = pygame.mixer.Sound("Resourses/Audio_sounds/game_over_sound.wav")
coin_collect_sound = pygame.mixer.Sound("Resourses/Audio_sounds/coin_collect_sound.wav")
drink_collect_sound = pygame.mixer.Sound("Resourses/Audio_sounds/drink_collect_sound.mp3")
obstacle_collect_sound = pygame.mixer.Sound("Resourses/Audio_sounds/obstacle_collect_sound.mp3")
escaped_sound = pygame.mixer.Sound("Resourses/Audio_sounds/escaped_sound.mp3")

# Αμάξι
car_img = pygame.image.load("Resourses/Game_objects/car.png")  # Φορτώνει την εικόνα του αμαξιού
car_img = pygame.transform.scale(car_img, (180, 145))  # Αλλάζει το μέγεθος της εικόνας του αμαξιού
car_x = 0  # Αρχική θέση του αμαξιού στην αρχή του παραθύρου αριστερά
car_y = window_height - car_img.get_height() - 5  # Υ-συντεταγμένη του αμαξιού

# Λίστα για τα εμπόδια
obstacles = []

# Χρονομετρητής για τη δημιουργία νέων εμποδίων
obstacle_timer = 0

# Λίστα για τα νομίσματα
coins = []

# Χρονομετρητής για τη δημιουργία νέων νομισμάτων
coin_timer = 0

drinks = []
drink_timer = 0

drunk_timer = 0  # Αρχικοποίηση του μετρητή χρόνου μεθύσιου

class Obstacle:
    def __init__(self, img_path, x, y):
        self.img = pygame.image.load(img_path)  # Φορτώνει την εικόνα του εμποδίου
        self.img = pygame.transform.scale(self.img, (85, 85))  # Αλλάζει το μέγεθος της εικόνας του εμποδίου
        self.x = x  # Θέση x του εμποδίου
        self.y = y  # Θέση y του εμποδίου

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))  # Εμφανίζει το εμπόδιο στο παράθυρο του παιχνιδιού

class Coin:
    def __init__(self, img_path, x, y):
        self.img = pygame.image.load(img_path)  # Φορτώνει την εικόνα του νομίσματος
        self.img = pygame.transform.scale(self.img, (65, 65))  # Αλλάζει το μέγεθος της εικόνας του νομίσματος
        self.x = x  # Θέση x του νομίσματος
        self.y = y  # Θέση y του νομίσματος

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))  # Εμφανίζει το νόμισμα στο παράθυρο του παιχνιδιού

class Drink:
    def __init__(self, img_path, x, y):
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (75, 75))
        self.x = x
        self.y = y

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

# Κύρια λούπα του παιχνιδιού
font = pygame.font.SysFont(None, 36)
coins_collected_text = font.render("Coins: " + str(coins_collected), True, (0, 0, 0))

run = True
drunk = False
jumping = False  # Μεταβλητή που υποδεικνύει αν το αμάξι κάνει άλμα
jump_vel = 6.7  # Αρχική ταχύτητα άλματος
gravity = 0.10  # Βαρύτητα
drunk_timer_max = 4  # Ο αριθμός των frames που το αμάξι θα είναι μεγαλύτερο
coins_collected = 0
energy_drink = []

def game_over_screen():
    # Εμφάνιση μηνύματος "Game Over"
    font = pygame.font.SysFont(None, 70)
    text = font.render("Game Over", True, (255, 0, 0))  # Κόκκινο χρώμα
    text_rect = text.get_rect(center=(window_width // 2, window_height // 2))  # Τοποθέτηση στο κέντρο του παραθύρου
    win.blit(text, text_rect)

    pygame.mixer.music.stop()
    game_over_sound.play()

    # Δημιουργία κουμπιού "Restart"
    restart_button = pygame.Rect(250, 300, 300, 50)  # Αντικείμενο Rect για το κουμπί "Restart"
    pygame.draw.rect(win, (255, 0, 0), restart_button)  # Σχεδίαση του κουμπιού με κόκκινο χρώμα

    # Δημιουργία κειμένου "Restart"
    font = pygame.font.SysFont(None, 40)  # Επιλογή γραμματοσειράς
    text = font.render("Restart", True, (0, 0, 0))  # Δημιουργία κειμένου "Restart" με μαύρα γράμματα
    text_rect = text.get_rect(center=(window_width // 2, 320))  # Ορισμός θέσης του κειμένου στο κέντρο του παραθύρου
    win.blit(text, text_rect)  # Τοποθέτηση του κειμένου στο παράθυρο

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                game_over_sound.stop()
                pygame.mixer.music.play(-1)
                if restart_button.collidepoint(mouse_pos):
                    return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_over_sound.stop()
                    pygame.mixer.music.play(-1)
                    return True

while run:
    for event in pygame.event.get():  # Ελέγχει τα γεγονότα που συμβαίνουν στο παιχνίδι
        if event.type == pygame.QUIT:  # Αν το γεγονός είναι η έξοδος από το παιχνίδι
            run = False  # Τερματίζει τη λούπα
        elif event.type == pygame.KEYDOWN:  # Αν πατηθεί ένα κουμπί του πληκτρολογίου
            if event.key == pygame.K_SPACE:  # Αν το πλήκτρο που πατήθηκε είναι το SPACE
                if not jumping:  # Αν το αμάξι δεν κάνει ήδη άλμα
                    jump_sound.play()  # Αναπαραγωγή ήχου για το άλμα
                    jumping = True  # Το αμάξι θα κάνει άλμα
                    jump_vel = 6.7  # Επαναφέρεται η ταχύτητα άλματος στην αρχική τιμή

    # Κίνηση του φόντου προς τα αριστερά
    bg_x -= bg_vel
    if bg_x <= -bg_img.get_width():
        bg_x = 0

    # Έλεγχος για άλμα
    if jumping:
        car_y -= jump_vel
        jump_vel -= gravity
        if car_y >= window_height - car_img.get_height() - 5:  # Εάν το αμάξι έχει φτάσει στο έδαφος
            jumping = False  # Τερματίζεται το άλμα
            car_y = window_height - car_img.get_height() - 5  # Ορίζεται το αμάξι στο επίπεδο του εδάφους

    # Δημιουργία energy drink
    drink_timer += 1
    if drink_timer % 3000 == 0:
        drink_img_path = "Resourses/Game_objects/energy_drink.png"
        drink_x = window_width
        drink_y = window_height - random.randint(80, 80)
        # Έλεγχος για σύγκρουση με εμπόδια
        if not any(
                obstacle.x < drink_x + 50 < obstacle.x + 85 and obstacle.y < drink_y + 50 < obstacle.y + 85 for obstacle
                in obstacles):
            new_drink = Drink(drink_img_path, drink_x, drink_y)
            drinks.append(new_drink)

    # Δημιουργία νέου νομίσματος
    coin_timer += 1
    if coin_timer % 575 == 0:  # Κάθε 575 frames
        coin_img_path = "Resourses/Game_objects/coin.png"  # Εικόνα νομίσματος
        coin_x = window_width  # Το νόμισμα εμφανίζεται στο δεξί άκρο του παραθύρου
        coin_y = window_height - random.randint(80, 80)  # Τυχαία ύψος του νομίσματος
        # Έλεγχος για σύγκρουση με εμπόδια
        if not any(
                obstacle.x < coin_x + 50 < obstacle.x + 85 and obstacle.y < coin_y + 50 < obstacle.y + 85 for obstacle
                in obstacles):
            new_coin = Coin(coin_img_path, coin_x, coin_y)  # Δημιουργία νέου νομίσματος
            coins.append(new_coin)  # Προσθήκη του νομίσματος στη λίστα
        
    # Κίνηση των νομισμάτων προς τα αριστερά
    for coin in coins:
        coin.x -= 3

    # Κίνηση energy drink προς τα αριστερά
    for drink in drinks:
        drink.x -= 3

    # Έλεγχος σύγκρουσης με drink
    for drink in drinks:
        if car_x + car_img.get_width() >= drink.x and car_x <= drink.x + drink.img.get_width():
            if car_y + car_img.get_height() >= drink.y and car_y <= drink.y + drink.img.get_height():
                drinks.remove(drink)
                drunk = True
                drink_collect_sound.play()
                car_img = pygame.transform.scale(car_img, (230, 200))  # το μέγεθος του αμαξιού
                car_x = 0  # Αρχική θέση του αμαξιού στην αρχή του παραθύρου αριστερά
                car_y = window_height - car_img.get_height() - 5  # Υ-συντεταγμένη του αμαξιού

    # Έλεγχος σύγκρουσης με τα νομίσματα
    for coin in coins:
        if car_x + car_img.get_width() >= coin.x and car_x <= coin.x + coin.img.get_width():
            if car_y + car_img.get_height() >= coin.y and car_y <= coin.y + coin.img.get_height():
                coins.remove(coin)
                coin_collect_sound.play()
                coins_collected += 1  # Αύξηση του μετρητή νομισμάτων
                # Ανανέωση του μετρητή νομισμάτων στην οθόνη
                font = pygame.font.SysFont(None, 36)
                coins_collected_text = font.render("Coins: " + str(coins_collected), True, (0, 0, 0))
                win.blit(coins_collected_text, (window_width - coins_collected_text.get_width() - 10, 10))

                if coins_collected == 1:
                    font = pygame.font.SysFont(None, 70)
                    text = font.render("You escaped !", True, (255, 0, 0))
                    text_rect = text.get_rect(center=(window_width // 2, window_height // 4))
                    win.blit(text, text_rect)

                    pygame.mixer.music.stop()
                    escaped_sound.play()

                    pygame.quit()

    # Αφαίρεση των νομισμάτων που έχουν ξεπεράσει το αριστερό άκρο του παραθύρου
    coins = [coin for coin in coins if coin.x > -coin.img.get_width()]

    # Αφαίρεση energy drink που έχουν ξεπεράσει το αριστερό άκρο του παραθύρου
    drinks = [drink for drink in drinks if drink.x > -drink.img.get_width()]

    # Δημιουργία νέου εμποδίου
    obstacle_timer += 1
    if obstacle_timer % 300 == 0:  # Κάθε 300 frames
        obstacle_img_path = random.choice(
            ["Resourses/Game_objects/obstacle1.png", "Resourses/Game_objects/obstacle2.png", "Resourses/Game_objects/obstacle3.png"])  # Τυχαία επιλογή εικόνας εμποδίου
        obstacle_x = window_width  # Το εμπόδιο εμφανίζεται στο δεξί άκρο του παραθύρου
        obstacle_y = window_height - random.randint(90, 90)  # Τυχαία ύψος του εμποδίου
        new_obstacle = Obstacle(obstacle_img_path, obstacle_x, obstacle_y)  # Δημιουργία νέου εμποδίου  
        obstacles.append(new_obstacle)  # Προσθήκη του εμποδίου στη λίστα

    # Κίνηση των εμποδίων προς τα αριστερά
    for obstacle in obstacles:
        obstacle.x -= 3

    # Έλεγχος σύγκρουσης με τα εμπόδια
    for obstacle in obstacles:
        if car_x + car_img.get_width() >= obstacle.x and car_x <= obstacle.x + obstacle.img.get_width():
            if car_y + car_img.get_height() >= obstacle.y and car_y <= obstacle.y + obstacle.img.get_height():
                if not drunk:
                    game_over_screen()
                    car_x = 0
                    car_y = window_height - car_img.get_height() - 5
                    obstacles = []
                    obstacle_timer = 0
                    coins_collected = 0
                    # Ανανέωση του μετρητή νομισμάτων στην οθόνη
                    font = pygame.font.SysFont(None, 36)
                    coins_collected_text = font.render("Coins: " + str(coins_collected), True, (0, 0, 0))
                    win.blit(coins_collected_text, (window_width - coins_collected_text.get_width() - 10, 10))
                else:
                    obstacles.remove(obstacle)
                    obstacle_collect_sound.play()
                    coins_collected += 1  # Αύξηση του μετρητή νομισμάτων
                    # Ανανέωση του μετρητή νομισμάτων στην οθόνη
                    font = pygame.font.SysFont(None, 36)
                    coins_collected_text = font.render("Coins: " + str(coins_collected), True, (0, 0, 0))
                    win.blit(coins_collected_text, (window_width - coins_collected_text.get_width() - 10, 10))
                    drunk_timer = drunk_timer + 1
                    if drunk_timer == 4:
                        drunk = False
                        drunk_timer = 0
                        car_img = pygame.transform.scale(car_img, (180, 145))
                        car_x = 0  # Αρχική θέση του αμαξιού στην αρχή του παραθύρου αριστερά
                        car_y = window_height - car_img.get_height() - 5  # Υ-συντεταγμένη του αμαξιού

    # Αφαίρεση των εμποδίων που έχουν ξεπεράσει το αριστερό άκρο του παραθύρου
    obstacles = [obstacle for obstacle in obstacles if obstacle.x > -obstacle.img.get_width()]

    # Εμφάνιση του φόντου και του αμαξιού στο παράθυρο
    win.blit(bg_img, (bg_x, 0))
    win.blit(bg_img, (bg_x + bg_img.get_width(), 0))
    win.blit(car_img, (car_x, car_y))
    win.blit(coins_collected_text, (window_width - coins_collected_text.get_width() - 10, 10))

    # Εμφάνιση και κίνηση των εμποδίων
    for obstacle in obstacles:
        obstacle.draw(win)

    # Εμφάνιση και κίνηση των νομισμάτων
    for coin in coins:
        coin.draw(win)

    # Εμφάνιση και κίνηση energy drink
    for drink in drinks:
        drink.draw(win)

    pygame.display.update()  # Ενημέρωση της οθόνης
    clock.tick(FPS)  # Ρύθμιση του FPS για να ελέγχει τον ρυθμό ανανέωσης της οθόνης

# Τερματισμός του Pygame
pygame.quit()

sys.exit()
