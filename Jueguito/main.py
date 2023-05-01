import pygame 
from sys import exit #llamamos este modulo para evitar que nos de error al cerrar el juego
from random import randint, choice
from pathlib import Path #cwd

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('imagenes/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('imagenes/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0 #se utilizará para elegir entre las formas de caminar
        self.player_jump = pygame.image.load('imagenes/Player/jump.png').convert_alpha()

        
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0   
    
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.1)
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
 
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'fly':
            fly_1 = pygame.image.load('imagenes/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('imagenes/Fly/Fly2.png').convert_alpha()   
            self.frames = [fly_1,fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('imagenes/snail/snail1.png').convert_alpha()#De esta forma removemos los valores alpha
            snail_2 = pygame.image.load('imagenes/snail/snail2.png').convert_alpha()
            self.frames = [snail_1,snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):    
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5 # De esta forma cada obstáculo que aparezca se moverá ligeramente más rapido que el anterior

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf,obstacle_rect)
            else:
                screen.blit(fly_surf,obstacle_rect)
           # screen.blit(snail_surf,obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100] # Esta lista se encarga de copiar los items de la lista siempre y cuando los valores de x sean mayores a -100, en caso de que no los eliminará
        return obstacle_list
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def collisions_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group, False):
        obstacle_group.empty()  
        return False
    else:
        return True

def player_animation():
    global player_surf, player_index
    #Queremos ejecutar la animacion de caminar si el pj esta en el piso
    #Y la de salto si no está en el piso
    if player_rect.bottom < 300: #jump
        player_surf = player_jump
    else:
        player_index += 0.1 # De esta forma evitamos que la transiciónde una imagen a otra no sea tan agresiva
        # por cada frame solo se desplazará 0.1 a la siguiente imagen
        if player_index >= len(player_walk):player_index = 0
        player_surf = player_walk[int(player_index)]

def score_data(high_score, score):
    if (not score_path.exists()):
                score_path.touch()
    else:
        content = score_path.read_text()
        return content
    
    """with open(score_path, 'r') as high:
        if (not score_path.exists()):
                score_path.touch()
        else:
            content = high.read()
            return content"""
   
    with open(score_path,'w') as high:
        if int(high_score) < score:
            high_score = score
            high.write(str(high_score))
        else:
            return high_score
                
 
pygame.init()
screen = pygame.display.set_mode((800,400))#Tupla, Display surface(Superficie de visualización) usamos dos valores
#Anchura y Altura
#Si intento ejecutar el archivo hasta ahora saldrá una ventana que se cerrará automáticamente
#Como no hay más código se cerrará inmediatamente.
pygame.display.set_caption('Pata Caliente') # Al llamar esta función podemos asignar un titulo 
clock = pygame.time.Clock() #Con esta variable creamos un objeto reloj, pero de momento no hace nada
# Debemos llamarlo dentro del loop while
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)#Lo usaremos para crear texto. Primero creamos el texto y luego lo agregamos como imagen
#Tiene dos argumentos el font type, y el font syze
game_active = False
start_time = 0
score = 0
high_score = 0 
current_path = Path.cwd()
score_path = current_path / 'high_score.txt'

#test_surf = pygame.Surface((100,200))#Tupla(w,h) de esta forma agregamos una plataforma
#test_surf.fill('Red')
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)#De esta forma la canción se reproduce para siempre
bg_music.set_volume(0.1)
#Groups
player = pygame.sprite.GroupSingle()
player.add(Player()) #Agrego la instancia de mi clase Player

obstacle_group = pygame.sprite.Group()


sky_surf = pygame.image.load('imagenes/sky.png').convert()
ground_surf = pygame.image.load('imagenes/ground.png').convert()

score_intro = test_font.render('Jueguito maton', False, (64,64,64))#tiene tres argumentos, Texto, ?, Color
score_intro_rect = score_intro.get_rect(center = (400,50))

# Obstacles
# Caracol
snail_frame_1 = pygame.image.load('imagenes/snail/snail1.png').convert_alpha()#De esta forma removemos los valores alpha
snail_frame_2 = pygame.image.load('imagenes/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1,snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]
#Mosca
fly_frame_1 = pygame.image.load('imagenes/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('imagenes/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1,fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

#Player
player_walk_1 = pygame.image.load('imagenes/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('imagenes/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0 #se utilizará para elegir entre las formas de caminar
player_jump = pygame.image.load('imagenes/Player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_walk_1.get_rect(midbottom = (80,300))# En el caso de convertir una surface en rectangulo solo hacerlo de esa manera
#pygame.Rect() # Los rectangulos tienen 4 argumentos left, top, width, height
player_gravity = 0

#Pantalla de entrada
player_stand = pygame.image.load('imagenes/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)# Necesitaremos la anchura y altura, reemplazamos la variable pero nos quedamos con la imagen
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Pata Caliente', False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to run', False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400,320))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2 
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)



while True: #Con el ciclo while evitaremos que la interfaz cierre ya que siempre dará True
    # dentro de este ciclo podremos dibujar todos los elementos 
    # y generar actualizaciones.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() #Invocamos el modulo para evitar que python siga leyendo codigo y arroje error

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:#MOUSEBOTTON UP, MOUSEBOTTONDOWN, MOUSEMOTION(TE DICE LA POSICIÓN)
                if player_rect.collidepoint(event.pos) and player_rect.bottom >=300:
                    player_gravity = -20
                #print(event.pos)#event.pos te dice la posición
            if event.type == pygame.KEYDOWN: #Detecta si la tecla está presionada
                if event.key == pygame.K_SPACE and player_rect.bottom >=300: # Si la tecla espacio está presionado el player adquiere -20 gravedad
                    player_gravity = -20        # Pareciendo así que brinca
        
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000) #Funciona para al reinciar el juego empezar los valores de tiempo en 0
        
        if game_active:
            if event.type == obstacle_timer:
            #Llamamos al randomizer para que los obstaculos aparezcan de forma random entre los 900 y 1100
                obstacle_group.add(Obstacle(choice(['fly', 'snail','snail','snail'])))
                
            """  if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100), 210)))
"""
            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]
            
            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]


    if game_active:   #Partes del juego activo
        screen.blit(sky_surf,(0,0)) #Blit significa transferencia de imagenes en bloque. 
        #Básicamente que pondremos una surface dentro de otra surface
        #Necesitamos dos argumentos el nombre de la surface y la posición.
        #screen.blit(nombre, posicion(tupla))
        screen.blit(ground_surf,(0,300))
        """pygame.draw.rect(screen,'#c0e8ec', score_rect)# De esta forma agregamos un fondo al título
        pygame.draw.rect(screen,'#c0e8ec', score_rect, 4)
        #pygame.draw.rect(screen,'Yellow', score_rect,2)
        #pygame.draw.ellipse(screen,'Brown',pygame.Rect(50,200,100,100))#Left, Top, Width, Height
        screen.blit(score_surf,score_rect)
        #snail_rect -= 4 #De esta forma le damos dinanismo a la posición del caracol
        # Al estar dentro del bucle while infinito cada vez que se repita el ciclo el caracol se moverá
        #if snail_rect < -100: snail_rect = 800"""
        score = display_score()
        
        # Caracol
        """snail_rect.x -= 4
        if snail_rect.right <= 0: snail_rect.left = 800
        screen.blit(snail_surf, snail_rect)"""
        # player_rect.left += 1
        #Si quiero saber la posición exacta de mi rectangulo puedo imprimirla
        #print(player_rect.left) y me dirá exactamente el punto donde está
        
        # Player
        """ player_gravity += 1
         player_rect.y += player_gravity # De esta forma hacemos que el pj se desplace hacia abajo
        if player_rect.bottom >= 300: player_rect.bottom = 300
        player_animation()#Llamamos la función para animar al pj
        screen.blit(player_surf, player_rect)"""#Se intercambia los valores de la tupla por la variable rectangulo
        
        player.draw(screen)
        player.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()
        # Obstacle movement
        #obstacle_rect_list = obstacle_movement(obstacle_rect_list)#Llamamos a la función que será continuamente reemplazada mientras el ciclo no termine.



        # Collision
        game_active = collisions_sprite()
        #if snail_rect.colliderect(player_rect):
           # game_active = False
        #game_active = collisions(player_rect,obstacle_rect_list)   

    
    else: # En este else definiremos el menu, básicamente la interfaz cuando el juego no se ejecuta
        screen.fill((94,129,162))   
        screen.blit(player_stand,player_stand_rect) 
        obstacle_rect_list.clear()#De esta forma removemos los items que se encuentran dentro del juego cuando se reinicie
        player_rect.midbottom = (80,300)
        player_gravity = 0

        score_message = test_font.render(f'Your Score: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400,300))
        screen.blit(game_name,game_name_rect)
        
        #Con el if haremos que en la pantalla de inicio salga el score después de jugar una partida
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)

        score_data(high_score,score)

    pygame.display.update() # esta linea estará actualizando la surface
    clock.tick(60)#Invocamos la variable clock, agregamos un valor int y se encarga de 
    # informar al loop while que no debe correr mas rapido de 60 veces por segundo
    # Muy importante esto, en base al numero de que indique como parametro la velocidad variará