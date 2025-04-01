from sys import exit
import pygame
import sqlite3
import pygame.locals
import random
from Database_func import character_finder, get_rounds, set_rounds, set_point, get_points




clock = pygame.time.Clock()
from pygame.locals import *
#ygame.mixer.init()  # Ensure the mixer is initialized
pygame.init()

pygame.display.set_caption('Chef Up')
screen = pygame.display.set_mode((1280,720))
icon_image = pygame.image.load('Graphics\Sprites\Icon image2.png').convert()
pygame.display.set_icon(icon_image)

conn = sqlite3.connect('Account databse.db')
c = conn.cursor()


click = False

#fonts
Large_Momentz_F = pygame.font.Font('Graphics/Fonts/Momentz.ttf',75)
Normal_Momentz_F = pygame.font.Font('Graphics\Fonts\CooperBits.ttf',32)

Norm_CooperBits_F = pygame.font.Font('Graphics\Fonts\CooperBits.ttf',32)

Norm_uphavtt_F = pygame.font.Font('Graphics\Fonts\A Goblin Appears!.otf',32)

defult = pygame.font.Font(None,32)

#text background is a translucent grey
text_background = pygame.Surface((350,720), pygame.SRCALPHA)
text_background.fill((15,15,15,100))


#text class (text_input, Anti-aliasing, text colour, font type, position)
class text():
    def __init__(self, text,  AA, text_colour, font, pos):
        self.text = font.render(text, AA, text_colour)
        self.text_rect = self.text.get_rect(bottomleft = pos)

    def draw_text(self):
        screen.blit(self.text, self.text_rect)

#title
title = text('Chef Up', False, '#FCCD2A', Large_Momentz_F, (15,195))
version_title = text('Alpha', True, 'black', defult, (250,215)) ; version = text('Version 0.9.0', True, 'black', defult, (1140,720))





#music
songs = (
    'Sounds\Solo_Leveling_OST_FULL_DARK_ARIA_LV2.mp3',
    'Sounds\Tek_it_instrumental.mp3',
    
    #menu music
    'Sounds\PinkPantheress_Feel_complete_Instrumental.mp3',
    'Sounds\Terraria_Infernum_Mod__Sky_After_Rain.mp3',

    #game music
    'Sounds/Kendrick_Lamar_Duckworth_Instrumental.mp3',
    'Sounds\Kendrick_Lamar_i_Instrumental.mp3',
    'Sounds\Kendrick_Lamar_The_Heart_Part_5_Instrumental.mp3',

    )

menu_music = pygame.mixer.Sound(songs[3])

game_music = pygame.mixer.Sound(songs[2])

#button class (text input, font type, text colour, base colour for button, hover colour for button, width, height, position)
class button():
    def __init__(self, text, font, text_colour, base_colour, hover_colour, width, height, pos):
        #core attributes

        self.pressed = False

        #rectangle dimensions
        self.top_rect = pygame.Rect(pos, (width,height))
        self.top_colour = base_colour
        self.reserved_base_colour = base_colour
        self.hover_colour = hover_colour

        # text
        self.reserved_text_colour = text_colour
        self.text_colour = text_colour
        self.text_surf = font.render(text, False, self.text_colour)
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw_button(self):
        pygame.draw.rect(screen, self.top_colour, self.top_rect)
        screen.blit(self.text_surf, self.text_rect)
        self.click()
    
    def click(self):
        mx,my = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mx,my):
            self.top_colour = self.hover_colour
            if pygame.mouse.get_pressed()[0] == True:
                self.pressed = True
                return True
            else:
                if self.pressed == True:
                    self.pressed = False
        else:
            self.top_colour = self.reserved_base_colour

#to start game
start_button = button('Start', Normal_Momentz_F, 'white', '#a19e92', '#868479', 100,30, (10,260))

#to go to shop
shop_button = button('Shop' ,Normal_Momentz_F, 'white', '#a19e92', '#868479', 100,30, (10,360))

#to exit game
exit_button = button('Exit', Normal_Momentz_F, '#fe1431', '#a19e92', '#868479', 100,30, (7,675))



### kitchen appliances ###
class kitchen_appliances(pygame.sprite.Sprite):
    pass
### player's account database ###     

class player_sp(pygame.sprite.Sprite):
        def __init__(self, skin_tone, new_inventory, page):
            super().__init__()

            if skin_tone == 'tone 1': #light
                front = pygame.image.load('Graphics\Sprites\player\playerW_F.png').convert_alpha() #front

                front_left_quarter = pygame.image.load('Graphics\Sprites\player\playerW_QL.png').convert_alpha() #front left

                left = pygame.image.load('Graphics\Sprites\player\playerW_L.png').convert_alpha() #left

                back_left_quarter = pygame.image.load('Graphics\Sprites\player\playerW_QL2.png').convert_alpha() #back left

                back = pygame.image.load('Graphics\Sprites\player\playerW_B.png').convert_alpha() #back

                front_right_quarter = pygame.image.load('Graphics\Sprites\player\playerW_QR.png').convert_alpha() #front right

                right = pygame.image.load('Graphics\Sprites\player\playerW_R.png').convert_alpha() #right

                back_right_quarter = pygame.image.load('Graphics\Sprites\player\playerW_QR2.png').convert_alpha() #back right

                self.frame = [front, front_left_quarter, left, back_left_quarter, back, front_right_quarter, right, back_right_quarter ]
            elif skin_tone == 'tone 2': #tanned
                front = pygame.image.load('Graphics\Sprites\player\playerW_F.png').convert_alpha()

                self.frame = [front]
            elif skin_tone == 'tone 3': #brown
                front = pygame.image.load('Graphics\Sprites\player\playerW_F.png').convert_alpha()

                self.frame = [front]
            elif skin_tone == 'tone 4': #black
                front = pygame.image.load('Graphics\Sprites\player\playerW_F.png').convert_alpha()

                self.frame = [front]
            else:
                front = pygame.image.load('Graphics\Sprites\player\playerW_F.png').convert_alpha()

                self.frame = [front]
            if page == 'game':
                pos = (463,445)
            elif page == 'shop':
                pos = (100,100)
            
            self.player_index = 0
            self.image = self.frame[self.player_index]
            self.rect = self.image.get_rect(center = pos)
            self.inventory = new_inventory
            self.points = 0

        #player's animation
        def player_input(self):
            keys = pygame.key.get_pressed()

            # facing top right
            if keys[pygame.K_w] and keys[pygame.K_d] and self.rect.x < 865 and self.rect.y >= 185:
                self.rect.x += 8 ; self.rect.y -= 8
                self.image = self.frame[7]
            
            # facing top left
            elif keys[pygame.K_w] and keys[pygame.K_a] and self.rect.x >= 0 and self.rect.y >= 185:
                self.rect.x -=8 ; self.rect.y -=8
                self.image = self.frame[3]

            # facing bottom right
            elif keys[pygame.K_s] and keys[pygame.K_d] and self.rect.x < 865 and self.rect.y < 655:
                self.rect.x +=8 ; self.rect.y +=8
                self.image = self.frame[5]

            # facing bottom left
            elif keys[pygame.K_s] and keys[pygame.K_a] and self.rect.x >= 0 and self.rect.y < 655:
                self.rect.x -=8 ; self.rect.y +=8
                self.image = self.frame[1]
            else:

                # facing right
                if keys[pygame.K_d] and self.rect.x < 865:
                    self.rect.x += 8
                    self.image = self.frame[6]

                # facing left
                if keys[pygame.K_a] and self.rect.x >= 0:
                    self.rect.x -= 8
                    self.image = self.frame[2]

                # facing up
                if keys[pygame.K_w] and self.rect.y >= 185:
                    self.rect.y -= 8
                    self.image = self.frame[4]

                # facing down
                if keys[pygame.K_s] and self.rect.y < 655:
                    self.rect.y += 8
                    self.image = self.frame[0]

            if self.rect.x <= 100 and self.rect.x >= 60 and self.rect.y <= 500 and self.rect.y >= 440:
                print(True)

        def reset(self):
            self.rect.x = 463 ; self.rect.y = 445
            self.image = self.frame[0]


        def get_points(self):
            return self.points
        
        def update_points(self, amount):
            self.points += amount


        def set_inventory(self, new_inventory):
            self.inventory = new_inventory


        def get_inventory(self):
            return self.inventory


        def get_rect(self):
            return self.rect


        def update(self,command):
            if command == 'move':
                self.player_input()
            elif command == 'reset':
                self.reset()

player1 = pygame.sprite.GroupSingle()
player1.add(player_sp('tone 1', None, 'game'))

player2 = pygame.sprite.GroupSingle()
player2.add(player_sp('tone 1', None, 'game'))

player3 = pygame.sprite.GroupSingle()
player3.add(player_sp('tone 1', None, 'game'))

player4 = pygame.sprite.GroupSingle()
player4.add(player_sp('tone 1', None, 'game'))

player5 = pygame.sprite.GroupSingle()
player5.add(player_sp('tone 1', None, 'game'))

player6 = pygame.sprite.GroupSingle()
player6.add(player_sp('tone 1', None, 'game'))

characters = [player1, player2, player3, player4, player5, player6]

### food ###
#ingredients
tomato = pygame.image.load('Graphics\Sprites\Food\Tomato.png').convert_alpha() #pixel size: 60x55
cheese = pygame.image.load('Graphics\Sprites\Food\cheese.png').convert_alpha() #pixel size: 80x55
mushroom = pygame.image.load('Graphics\Sprites\Food\mushroom.png').convert_alpha() #pixel size: 85x95
sausage = pygame.image.load('Graphics\Sprites\Food\sausage.png').convert_alpha() #pixel size: 150x55
dough = pygame.image.load('Graphics\Sprites\Food\dough.png').convert_alpha() #pixel size: 110x65
food_list = [tomato, cheese, mushroom, sausage, dough]

tomato2 = pygame.image.load('Graphics\Sprites\Food2\Tomato.png').convert_alpha() #pixel size: 60x55
cheese2 = pygame.image.load('Graphics\Sprites\Food2\Cheese.png').convert_alpha() #pixel size: 80x55
mushroom2 = pygame.image.load('Graphics\Sprites\Food2\Mushroom.png').convert_alpha() #pixel size: 85x95
sausage2 = pygame.image.load('Graphics\Sprites\Food2\Sausage.png').convert_alpha() #pixel size: 150x55
dough2 = pygame.image.load('Graphics\Sprites\Food2\Dough.png').convert_alpha() #pixel size: 110x65
invisible_slot = pygame.image.load('Graphics\Sprites\Food2\invisible2.png').convert_alpha()

#food
sausage_pizza = pygame.image.load('Graphics\Sprites\Food2\sausage_pizza.png').convert_alpha()
sausage_pizza_ingre = ('dough','tomato','cheese','sausage')
sausage_pizza = (pygame.transform.scale(sausage_pizza, ((sausage_pizza.get_width() * 0.9) , (sausage_pizza.get_height() * 0.9))),'sausage pizza', sausage_pizza_ingre)

cheese_pizza = pygame.image.load('Graphics\Sprites\Food2\cheese_pizza.png').convert_alpha()
cheese_pizza_ingre = ('dough','tomato','cheese')
cheese_pizza = (pygame.transform.scale(cheese_pizza, ((cheese_pizza.get_width() * 0.9) , (cheese_pizza.get_height() * 0.9))),'cheese pizza', cheese_pizza_ingre)

mushroom_pizza = pygame.image.load('Graphics\Sprites\Food2\mushroom_pizza.png').convert_alpha()
mushroom_pizza_ingre = ('dough','tomato','cheese', 'mushroom')
mushroom_pizza = (pygame.transform.scale(mushroom_pizza, ((mushroom_pizza.get_width() * 0.9) , (mushroom_pizza.get_height() * 0.9))),'mushroom pizza', mushroom_pizza_ingre)

food_objectives = (cheese_pizza, sausage_pizza, mushroom_pizza)

### menu food animation ###
class menu_food(pygame.sprite.Sprite):
    def __init__(self, type, x,y):
        super().__init__()

        self.image = type
        self.rect = self.image.get_rect(center = (x,y))

        self.x_pos = x
        self.y_pos = y

    #goes diagonally to the buttom right with x and y decremented by 1
    def update(self):
        self.rect.x += 1 ; self.rect.y += 1

        #if it reaches its destination then it will restart
        if self.rect.x == 1310 or self.rect.y == 750:
            self.rect.x = self.x_pos ; self.rect.y = self.y_pos
food = pygame.sprite.Group()


### food ###
class food_button():
    def __init__(self, n_image, name, n_pos):
        #core attributess

        self.pressed = False

        #rectangle dimensions
        self.image = n_image #image of the ingredients
        self.rect = self.image.get_rect(center=n_pos)
        self.food_name = name


    #loads the images of the food
    def draw_button(self):
        screen.blit(self.image, self.rect)
        self.click()
    
    #checks if the cursor is over and clicks a certain food 
    def click(self):
        mx,my = pygame.mouse.get_pos()
        if self.rect.collidepoint(mx,my):
            if pygame.mouse.get_pressed()[0] == True:
                self.pressed = True
                return True
            else:
                if self.pressed == True:
                    self.pressed = False
    
    def show_food(self):
        return self.image
    
    def get_food_name(self):
        return self.food_name
    

cheese_but = food_button(cheese2,'cheese', (1010,250))

dough_but = food_button(
    pygame.transform.scale(dough2, ( (dough2.get_width() * 0.8) , (dough2.get_height() * 0.8) ) ),
     'dough', 
     (1108,250)
     )

mushroom_but = food_button(mushroom2, 'mushroom', (1208,250))

sausage_but = food_button(
    pygame.transform.scale(sausage2, ((sausage2.get_width() * 0.6) , (sausage2.get_height() * 0.6))), 
    'sausage', 
    (1008,350)
    )

tomato_but = food_button(tomato2, 'tomato',(1110,350))

### customers ###
class customer_class(pygame.sprite.Sprite):
    def __init__(self, n_x, n_y, end_colour, food_required):
        super().__init__()

        #white skin tone
        white_front = pygame.image.load('Graphics\Sprites\player\playerW_F.png').convert_alpha()
        white_back = pygame.image.load('Graphics\Sprites\player\playerW_B.png').convert_alpha()
        white_frame = (white_front, white_back)

        #tanned skin tone
        tanned_front = pygame.image.load('Graphics\Sprites\player\Tanned\Model_Tan_F.png').convert_alpha()
        tanned_back = pygame.image.load('Graphics\Sprites\player\Tanned\Model_Tan_B.png').convert_alpha()
        tanned_frame = (tanned_front, tanned_back)

        #brown skin tone
        brown_front = pygame.image.load('Graphics\Sprites\player\Brown\Model_Brown_F.png').convert_alpha()
        brown_back = pygame.image.load('Graphics\Sprites\player\Brown\Model_Brown_B.png').convert_alpha()
        brown_frame = (brown_front, brown_back)

        #black skin tone
        black_front = pygame.image.load('Graphics\Sprites\player\Black\Model_Black_F.png').convert_alpha()
        black_back = pygame.image.load('Graphics\Sprites\player\Black\Model_Black_B.png').convert_alpha()
        black_frame = (black_front, black_back)

        

        #list of skin tones to be chosen at random between index 0 and 3
        self.customer_skin_tone = [white_frame, tanned_frame, brown_frame, black_frame]
        self.skin_tone = self.customer_skin_tone[random.randrange(0,4)]

        self.image = self.skin_tone[0]
        self.rect = self.image.get_rect(center  = (n_x,n_y))

        self.points = 10

        #where the customer should end at and show their order
        if end_colour == 'red':
            self.end_point = 125

            self.objective_pos = (341,5)
            self.ingredients_objective_x_pos = 320
        
        elif end_colour == 'green':
            self.end_point = 125

            self.objective_pos = (236,5)
            self.ingredients_objective_x_pos = 215

        elif end_colour == 'blue':
            self.end_point = 125

            self.objective_pos = (131,5)
            self.ingredients_objective_x_pos = 110

        elif end_colour == 'yellow':
            self.end_point = 125

            self.objective_pos = (26,5)
            self.ingredients_objective_x_pos = 5

        self.food_objective = pygame.transform.scale(food_required[0], ((food_required[0].get_width() * 0.4) , (food_required[0].get_height() * 0.4))) #makes the image smaller
        self.food_objective_rect = self.food_objective.get_rect(center= (n_x,85))
        self.food_objective_name = food_required[1]

        self.served = False
        self.x = n_x
        self.y = n_y

    def get_points(self):
        return self.points
    
    def get_food_objective(self):
        return self.food_objective_name[1]

    def check_food(self, food_input):
        if food_input == self.food_objective_name:
            self.served = True
        return self.served


    def customer_movement(self):  
        if self.rect.y < self.end_point and not self.served:
            self.rect.y +=3
        elif self.rect.y > self.end_point or self.rect.y == self.end_point :
            screen.blit(self.food_objective, self.food_objective_rect)

        #allows the customer to walk backwards and changes the direction to walk backwards
        if self.served:
            self.image = self.skin_tone[1] 
            self.rect.y -=3

            if self.rect.y < -100:
                #randomly chooses an index between 0 and 3 for a new or same skin tone
                self.skin_tone = self.customer_skin_tone[random.randrange(0,4)]
                self.image = self.skin_tone[0] #sets customer's direction to the front
                self.served = False

        
    #re-scales the image into a smaller image
    def image_scaler(self, new_image):
        image = pygame.image.load(new_image).convert_alpha()
        scaled_image = pygame.transform.scale(image, ((image.get_width() * 0.35) , (image.get_height() * 0.35)))
        return scaled_image

    def food_ingredients_objective(self):

        #all ingredients
        dough = self.image_scaler('Graphics\Sprites\Food2\Dough.png')
        tomato = self.image_scaler('Graphics\Sprites\Food2\Tomato.png')
        cheese = self.image_scaler('Graphics\Sprites\Food2\Cheese.png')
        sausage = self.image_scaler('Graphics\Sprites\Food2\Sausage.png')
        mushroom = self.image_scaler('Graphics\Sprites\Food2\Mushroom.png')

        if self.rect.y > self.end_point:
            if self.food_objective_name == 'sausage pizza':
                #outputs the ingredients required for sausage pizza in a drop down list

                screen.blit(self.food_objective, self.objective_pos)
                screen.blit(dough, (self.ingredients_objective_x_pos, 50))
                screen.blit(tomato, (self.ingredients_objective_x_pos, 74))
                screen.blit(cheese, (self.ingredients_objective_x_pos, 98))
                screen.blit(sausage, (self.ingredients_objective_x_pos, 122))

            elif self.food_objective_name == 'cheese pizza':
                screen.blit(self.food_objective, self.objective_pos)
                screen.blit(dough, (self.ingredients_objective_x_pos, 50))
                screen.blit(tomato, (self.ingredients_objective_x_pos, 74))
                screen.blit(cheese, (self.ingredients_objective_x_pos, 98))

            elif self.food_objective_name == 'mushroom pizza':
                screen.blit(self.food_objective, self.objective_pos)
                screen.blit(dough, (self.ingredients_objective_x_pos, 50))
                screen.blit(tomato, (self.ingredients_objective_x_pos, 74))
                screen.blit(cheese, (self.ingredients_objective_x_pos, 98))
                screen.blit(mushroom, (self.ingredients_objective_x_pos, 122))
    
    #changes the food objective 
    def randomise(self, image, name):
        self.food_objective = pygame.transform.scale(image, ((image.get_width() * 0.4) , (image.get_height() * 0.4))) #makes the image smaller
        self.food_objective_rect = self.food_objective.get_rect(center= (self.x,85))
        self.food_objective_name = name

    def reset(self):
        self.rect = self.image.get_rect(center  = (self.x, self.y))

    def update(self):
        self.customer_movement()
        self.food_ingredients_objective()
    
customer_add = pygame.sprite.Group()
random_customer1_index = random.randrange(0,3)
random_customer2_index = random.randrange(0,3)
random_customer3_index = random.randrange(0,3)
random_customer4_index = random.randrange(0,3)


customer1 = customer_class(832,-105, 'red', food_objectives[random_customer1_index])
customer2 = customer_class(720,-1200, 'green', food_objectives[random_customer2_index])
customer3 = customer_class(608,-2100, 'blue', food_objectives[random_customer3_index])
customer4 = customer_class(496,-4200, 'yellow', food_objectives[random_customer4_index])

####----(Main menu)----####
def main_menu(username):

    character_type = int(character_finder(username))
    round = int(get_rounds(username))

    menu_music.set_volume(.1)
    menu_music.play(-1)
    
    ### player's account ###
    username_surf = defult.render(f'Username: {username}', True, 'black')
    username_rect = username_surf.get_rect(topright = (1270,50))

    #score points
    points = get_points(username)
    main_menu_points_display = Normal_Momentz_F.render(f"High score: {points}", True, 'black')
    main_menu_points_rect = main_menu_points_display.get_rect(topright = (1270,10))

    ### menu foods ###
    food.add(menu_food(cheese, -170,585))
    food.add(menu_food(dough, -180,300))
    food.add(menu_food(mushroom, -230, -120))
    food.add(menu_food(sausage, -120,-500))
    food.add(menu_food(sausage, -80,-740))
    food.add(menu_food(cheese, -40,-220))
    food.add(menu_food(dough, -390,-650))
    food.add(menu_food(mushroom, -350,-400))
    food.add(menu_food(sausage, -650,-380))
    food.add(menu_food(tomato, -488,-140))
    food.add(menu_food(cheese, -700,-53))
    food.add(menu_food(dough, -520,130))
    food.add(menu_food(mushroom, -700,230))
    food.add(menu_food(sausage, -390,410))
    food.add(menu_food(tomato, 150,-584))
    food.add(menu_food(cheese, 180,-370))
    food.add(menu_food(dough, 310,-105))
    food.add(menu_food(mushroom, 520,-260))
    food.add(menu_food(sausage, 430,-480))
    food.add(menu_food(tomato, 580,-660))
    food.add(menu_food(cheese, 770,-440))
    food.add(menu_food(dough, 1050,-275))
    food.add(menu_food(mushroom, 820,-120))
    

    while True:
        screen.fill(('#FFFBE6'))
        
        mx,my = pygame.mouse.get_pos()
        click = False


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            #mute or unmute music
            if event.type == KEYDOWN:
                if event.key == K_MINUS:
                    menu_music.fadeout(0)
                if event.key == K_EQUALS:
                    menu_music.play(-1)

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        food.draw(screen)
        food.update()

        screen.blit(text_background,(0,0)) #text background is a translucent grey

        title.draw_text() #title
        version_title.draw_text() ; version.draw_text()

        #username
        screen.blit(username_surf, username_rect)

        #display high score for user
        screen.blit(main_menu_points_display, main_menu_points_rect)

        #button to start game
        start_button.draw_button()
        if start_button.click() == True:
            menu_music.fadeout(0)
            game(character_type, username)

            #sets new high score
            points = get_points(username)
            main_menu_points_display = Normal_Momentz_F.render(f"High score: {points}", True, 'black')
            main_menu_points_rect = main_menu_points_display.get_rect(topright = (1270,10))

        #button go to shop menu
        shop_button.draw_button()
        if shop_button.click() == True:
            menu_music.fadeout(0)
            shop_menu()

        #button to exit game
        exit_button.draw_button()
        if exit_button.click() == True:
            menu_music.fadeout(0)
            exit_menu(1)


        
        pygame.display.update()
        clock.tick(30)

#exit menu
def exit_menu(type):

    yes_but = button('Yes', Normal_Momentz_F, '#38b000', '#E4E0E1', '#868479',80,40,(460,435))
    no_but = button('No', Normal_Momentz_F, '#fe1431', '#E4E0E1', '#868479',80,40,(740,435))
    
    #for main menu
    if type == 1:
        exit_screen = pygame.Surface((450,240))
        exit_screen.fill('#E4E0E1')
    
        #message to verfiy exiting 
        message1 = text('Are you sure', True, 'black', Norm_CooperBits_F, (520,300))
        message2 = text('You want to quit?', True, 'black', Norm_CooperBits_F, (480,340))
            
        running = True
        while running:
            mx,my = pygame.mouse.get_pos()
            click = False
            
            screen.blit(exit_screen,exit_screen.get_rect(center = screen.get_rect().center))
    
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
    
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
    
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                        menu_music.play(-1)
    
            #message
            message1.draw_text() ; message2.draw_text()
    
            #yes to exit game
            yes_but.draw_button()
            if yes_but.click() == True:
                pygame.quit()
                exit()   
    
            #no to not exit game
            no_but.draw_button()
            if no_but.click() == True:
                menu_music.play(-1)
                running = False
    
    
            pygame.display.update()
            clock.tick(60)

    #for second menu in-game
    elif type == 2:
        exit_screen = pygame.Surface((450,240))
        exit_screen.fill('blue')
        running = True

        #message to verfiy exiting 
        message1 = text('Are you sure', True, 'black', Norm_CooperBits_F, (520,300))
        message2 = text('You want to quit?', True, 'black', Norm_CooperBits_F, (480,340))

        while running:
            mx,my = pygame.mouse.get_pos()
            click = False
            
            screen.blit(exit_screen,exit_screen.get_rect(center = screen.get_rect().center))
    
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
    
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
    
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                
                #message
                message1.draw_text() ; message2.draw_text()

                no_but.draw_button()
                if no_but.click() == True:
                    running = False

                yes_but.draw_button()
                if yes_but.click() == True:
                    running = False
                    game_music.fadeout(0)
                    return False
                    

                




                pygame.display.update()
                clock.tick(60)
        








####----(Shop starts here)----####

hello = Normal_Momentz_F.render('Working progress :)',True,('black'))
hr = hello.get_rect(bottomleft = (15,300))

def shop_menu():

    running = True
    while running:

        screen.fill((0,255,0))

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            if event.type == KEYDOWN:
                if event.key == K_MINUS:
                    menu_music.fadeout(0)
                if event.key == K_EQUALS:
                    menu_music.play(-1)

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        screen.blit(hello,hr)


        pygame.display.update()
        clock.tick(60)










####----(Main game starts here)----####
def game(character_type, username):

    game_music.set_volume(0.09)
    game_music.play(1)

    running = True
    

    #map
    kitchen_map = pygame.Surface((932,500))
    kitchen_map.fill('#E4E0E1')

    customer_floor = pygame.image.load('Graphics\Sprites\environment\Pixel floor.png').convert_alpha()

    ### HUD ###
    display = pygame.Surface((393,720))
    display.fill('#674636')
    border_display = pygame.Surface((10,720))
    border_display.fill('#543A14')

    points = 0
    points_display = Normal_Momentz_F.render(f"Points: {points}", False, 'white')
    points_display_rect = points_display.get_rect(topleft = (950, 110))

    #ingredients list
    ingredients_display = pygame.Surface((420,160))
    ingredients_display.fill('#674636')
    ingredients_border_display = pygame.Surface((430,170))
    ingredients_border_display.fill('#543A14')

    border1 = pygame.Surface((1,160))
    border1.fill('black')

    #pause
    menu_button = pygame.image.load('Graphics\Sprites\pause image.png').convert_alpha()
    menu_button_rect = menu_button.get_rect(topright = (1270,10))

    #global timer
    time_remaining = 300
    timer = pygame.USEREVENT +1

    timer_display = Norm_uphavtt_F.render(f"{time_remaining}", True, 'white')
    pygame.time.set_timer(timer, 1000)
    timer_display_rect = timer_display.get_rect(topleft = (950,50))

    #round
    round = get_rounds(username)
    round_display = Normal_Momentz_F.render(f"Round {round}", True, '#FCCD2A')
    round_display_rect = round_display.get_rect(topleft = (950,10))



    ## kitchen / fridge inventory
    kitchen_inventory = pygame.image.load('Graphics\others\kitchen inventory.png').convert_alpha()
    kitchen_inventory_rect = kitchen_inventory.get_rect(center = (1110,350))

    #kitchen inventory area / fridge for player to walk to
    kitchen_inventory_area = pygame.Surface((100,80), pygame.SRCALPHA)
    kitchen_inventory_area_rect = kitchen_inventory_area.get_rect(bottomleft = (0,720))
    kitchen_inventory_area.fill((255,0,0, 100))

    #kitchen appliances
    #oven model
    oven_text = text('Oven', False, '#FCCD2A', defult, (0,300))
    oven = pygame.Surface((100,80))
    oven_rect = oven.get_rect(bottomleft = (0,300))
    oven.fill(('red'))

    #oven inventory
    oven_inventory = pygame.image.load('Graphics\others\kitchen appliances inventory.png').convert_alpha()
    oven_inventory_rect = oven_inventory.get_rect(center = (1110,350))



    #oven slots
    slot1 = invisible_slot
    slot1_name = ''
    slot1_rect = slot1.get_rect(center = (1010,300))

    slot2 = invisible_slot
    slot2_name = ''
    slot2_rect = slot2.get_rect(center = (1110,300))

    slot3 = invisible_slot
    slot3_name = ''
    slot3_rect = slot3.get_rect(center = (1010,400))

    slot4 = invisible_slot
    slot4_name = ''
    slot4_rect = slot4.get_rect(center = (1110,400))

    #cooks and combines the ingredients into a final meal
    cook_but_image = pygame.Surface((100,100)) 
    cook_but_image.fill('green')
    cook_but = button('Cook', defult, 'white', 'green', 'green', 100,100, (1160,350))

    #resets and removes all of the currect items in the oven slots
    reset_but_image = pygame.Surface((100,100)) 
    reset_but_image.fill('red')
    reset_but = button('Reset', defult, 'white', 'red', 'red', 100,100, (1160,250))




    ## player's inventory
    player_inventory = pygame.Surface((100,100))
    player_inventory_rect = player_inventory.get_rect(center = (1110,600))
    player_inventory.fill('grey')

    current_inventory = invisible_slot
    current_inventory_rect = current_inventory.get_rect(center = (1110,600))
    current_inventory_name = ''
    #name of the current item occupying the slot



    #customers
    customer_add.add(customer1, customer2, customer3, customer4)



    #customer spawners
    spawn1 = pygame.Surface((10,10))
    spawn1_rect = spawn1.get_rect(center=(832,200))
    spawn1.fill('red')

    spawn2 = pygame.Surface((10,10))
    spawn2_rect = spawn2.get_rect(center=(720,200))
    spawn2.fill('green')

    spawn3 = pygame.Surface((10,10))
    spawn3_rect = spawn3.get_rect(center=(608,200))
    spawn3.fill('blue')

    spawn4 = pygame.Surface((10,10))
    spawn4_rect = spawn4.get_rect(center=(496,200))
    spawn4.fill('yellow')

    #player's food serving area
    serve1 = pygame.Surface((50,25), pygame.SRCALPHA)
    serve1_rect = serve1.get_rect(center=(832,270))
    serve1.fill((255,0,0, 100))

    serve2 = pygame.Surface((50,25), pygame.SRCALPHA)
    serve2_rect = serve1.get_rect(center=(720,270))
    serve2.fill((255,0,0, 100))

    serve3 = pygame.Surface((50,25), pygame.SRCALPHA)
    serve3_rect = serve1.get_rect(center=(608,270))
    serve3.fill((255,0,0, 100))

    serve4 = pygame.Surface((50,25), pygame.SRCALPHA)
    serve4_rect = serve1.get_rect(center=(496,270))
    serve4.fill((255,0,0, 100))




    while running:
        mx,my = pygame.mouse.get_pos()
        click = False
        served = False

        #map layout
        screen.blit(screen, (0,0))
        screen.fill((0,0,0))
        screen.blit(kitchen_map,(0,220))
        screen.blit(customer_floor,(0,-186))
        screen.blit(display,(942,0))
        screen.blit(border_display,(932,0))

        screen.blit(ingredients_border_display, (0,0))
        screen.blit(ingredients_display, (0,0))
        screen.blit(border1, (105,0))
        screen.blit(border1, (210,0))
        screen.blit(border1, (315,0))

        #pause button
        screen.blit(menu_button,menu_button_rect)
        #points
        screen.blit(points_display,points_display_rect)
        #round
        screen.blit(round_display, round_display_rect)

        #customer's spawn
        screen.blit(spawn1, spawn1_rect)
        screen.blit(spawn2, spawn2_rect)
        screen.blit(spawn3, spawn3_rect)
        screen.blit(spawn4, spawn4_rect)

        #player's serving area
        screen.blit(serve1,serve1_rect)
        screen.blit(serve2,serve2_rect)
        screen.blit(serve3,serve3_rect)
        screen.blit(serve4,serve4_rect)

        #kitchen inventory area / fridge
        screen.blit(kitchen_inventory_area,kitchen_inventory_area_rect)
        #kichen appliances
        screen.blit(oven,oven_rect)
        oven_text.draw_text()

        #player's inventory
        screen.blit(player_inventory, player_inventory_rect)
        screen.blit(current_inventory, current_inventory_rect)


        #key inputs
        keys = pygame.key.get_pressed()
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            if event.type == KEYDOWN:
                if event.key == K_MINUS:
                    game_music.fadeout(0)
                if event.key == K_EQUALS:
                    game_music.play(-1)

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game_music.fadeout(0)
                    running = False
                    customer1.reset()
                    customer2.reset()
                    customer3.reset()
                    customer4.reset()
                    menu_music.play(-1)

            if event.type == timer:
                time_remaining -= 1
            
        #checks if timer is not 0
        if time_remaining >= 0:

            display_seconds = time_remaining % 60
            display_minutes = int(time_remaining / 60) % 60
        #displays timer in minutes and seconds
        timer_display = Norm_uphavtt_F.render(f"{display_minutes:02}:{display_seconds:02}", True, 'white')
        screen.blit(timer_display, timer_display_rect)
        
        #when timer ends
        if display_minutes == 0 and display_seconds == 0:
            round += 1
            set_rounds(username, round) #sets round to database
            set_point(username, points) #processes the points earned at the end 
            #ends game
            running = False

            player.update('reset')
            game_music.fadeout(0)
            menu_music.play(-1)
            customer1.reset()
            customer2.reset()
            customer3.reset()
            customer4.reset()

        

        
        ### customer 
        customer_add.draw(screen)
        customer_add.update()

        ### player's movement (boundary: (1280,720))
        player = characters[character_type]
        player.draw(screen)
        player.update('move')

        #player's collisions with counter desk
        if player.sprite.rect.colliderect(serve1_rect):
            served = customer1.check_food(current_inventory_name)
            
            if served:
                #changes food objectives if served correctly 
                random_food_index = random.randrange(0,3)
                customer1.randomise(food_objectives[random_food_index][0], food_objectives[random_food_index][1])

        if player.sprite.rect.colliderect(serve2_rect):
            served = customer2.check_food(current_inventory_name)
            if served:
                random_food_index = random.randrange(0,3)
                customer2.randomise(food_objectives[random_food_index][0], food_objectives[random_food_index][1])

        if player.sprite.rect.colliderect(serve3_rect):
            served = customer3.check_food(current_inventory_name)
            if served:
                random_food_index = random.randrange(0,3)
                customer3.randomise(food_objectives[random_food_index][0], food_objectives[random_food_index][1])

        if player.sprite.rect.colliderect(serve4_rect):
            served = customer4.check_food(current_inventory_name)
            if served:
                random_food_index = random.randrange(0,3)
                customer4.randomise(food_objectives[random_food_index][0], food_objectives[random_food_index][1])

        if served and current_inventory_name != '':
            served = False
            #rewards the user with points
            points = points + customer1.get_points()
            points_display = Normal_Momentz_F.render(f"Points: {points}", False, 'white')

            current_inventory = pygame.image.load('Graphics\Sprites\Food2\invisible2.png').convert_alpha()
            current_inventory_name = ''
        
        #access kitchen / fridge inventory
        if player.sprite.rect.colliderect(kitchen_inventory_area_rect):
            screen.blit(kitchen_inventory, kitchen_inventory_rect) #inventory pops up

            #fills the empty inventory box with the food sprite image when clicked 
            cheese_but.draw_button()
            if cheese_but.click():
                current_inventory = cheese_but.show_food()
                current_inventory_name = cheese_but.get_food_name()
                current_inventory_rect = current_inventory.get_rect(center = (1110,600))    

            dough_but.draw_button()
            if dough_but.click():
                current_inventory = dough_but.show_food()
                current_inventory_name = dough_but.get_food_name()
                current_inventory_rect = current_inventory.get_rect(center = (1110,600))    

            mushroom_but.draw_button()
            if mushroom_but.click():
                current_inventory = mushroom_but.show_food()
                current_inventory_name = mushroom_but.get_food_name()
                current_inventory_rect = current_inventory.get_rect(center = (1110,600))    

            sausage_but.draw_button()
            if sausage_but.click():
                current_inventory = sausage_but.show_food()
                current_inventory_name = sausage_but.get_food_name()
                current_inventory_rect = current_inventory.get_rect(center = (1110,600))    

            tomato_but.draw_button()
            if tomato_but.click():
                current_inventory = tomato_but.show_food()
                current_inventory_name = tomato_but.get_food_name()
                current_inventory_rect = current_inventory.get_rect(center = (1110,600))    
            
        #displays oven's inventory when character is colliding the oven area
        if player.sprite.rect.colliderect(oven_rect):
            screen.blit(oven_inventory, oven_inventory_rect)

            #4 oven slots to be displayed in a 2x2 grid
            screen.blit(slot1,slot1_rect)
            screen.blit(slot2,slot2_rect)
            screen.blit(slot3,slot3_rect)
            screen.blit(slot4,slot4_rect)

            cook_but.draw_button()
            reset_but.draw_button()

            if slot1_rect.collidepoint(mx,my):
                if click:
                    slot1 = current_inventory
                    slot1_name = current_inventory_name
                    slot1_rect = slot1.get_rect(center = (1010,300))
                    current_inventory = invisible_slot
                    current_inventory_name = ''

            if slot2_rect.collidepoint(mx,my):
                if click:
                    slot2 = current_inventory
                    slot2_name = current_inventory_name
                    slot2_rect = slot2.get_rect(center = (1110,300))
                    current_inventory = invisible_slot
                    current_inventory_name = ''

            if slot3_rect.collidepoint(mx,my):
                if click:
                    slot3 = current_inventory
                    slot3_name = current_inventory_name
                    slot3_rect = slot3.get_rect(center = (1010,400))
                    current_inventory = invisible_slot
                    current_inventory_name = ''

            if slot4_rect.collidepoint(mx,my):
                if click:
                    slot4 = current_inventory
                    slot4_name = current_inventory_name
                    slot4_rect = slot4.get_rect(center = (1110,400))
                    current_inventory = invisible_slot
                    current_inventory_name = ''

            if cook_but.click():
                #checks if the ingredients for certain food
                if slot1_name == '' or slot2_name == '' or slot3_name == '' or slot4_name == '':
                    if all(ingredients in cheese_pizza_ingre for ingredients in (slot1_name, slot2_name, slot3_name)):
                        current_inventory = pygame.transform.scale(cheese_pizza[0], ((cheese_pizza[0].get_width() *0.6) , (cheese_pizza[0].get_height() * 0.6)))
                        current_inventory_rect = current_inventory.get_rect(center = (1110,600))                   
                        current_inventory_name = 'cheese pizza'
                    else:
                        pass
                else:

                    if all(ingredients in sausage_pizza_ingre for ingredients in (slot1_name, slot2_name, slot3_name, slot4_name)):
                        current_inventory = pygame.transform.scale(sausage_pizza[0], ((sausage_pizza[0].get_width() *0.6) , (sausage_pizza[0].get_height() * 0.6)))
                        current_inventory_rect = current_inventory.get_rect(center = (1110,600))                   
                        current_inventory_name = 'sausage pizza'

                    elif all(ingredients in mushroom_pizza_ingre for ingredients in (slot1_name, slot2_name, slot3_name, slot4_name)):
                        current_inventory = pygame.transform.scale(mushroom_pizza[0], ((mushroom_pizza[0].get_width() *0.6) , (mushroom_pizza[0].get_height() * 0.6)))
                        current_inventory_rect = current_inventory.get_rect(center = (1110,600))                   
                        current_inventory_name = 'mushroom pizza'

                    else:
                        pass
                slot1 = slot2 = slot3 = slot4 = invisible_slot
                slot1_name = slot2_name = slot3_name = slot4_name = ''

            if reset_but.click():
                slot1 = slot2 = slot3 = slot4 = invisible_slot
                slot1_name = slot2_name = slot3_name = slot4_name = ''



        if menu_button_rect.collidepoint(mx,my):
            if click:
                game_music.fadeout(0)
                exit_menu(2)
                if exit_menu(2) == False:
                    running = False
                    player.update('reset')
                    customer1.reset()
                    customer2.reset()
                    customer3.reset()
                    customer4.reset()
                    menu_music.play(-1)
                else:
                    pass
                    game_music.play(-1)
        
        print(f"FPS: {clock.get_fps()}")

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main_menu('patience')