import pygame
import random
import time
from settings import *
from ant import Ant
from pheromone import Pheromone
from food import Food
from threat import Threat
from quadtree import *
from game_statistics import *
from export_statistics import PeriodicRecorder


class Setup:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.Font(None, 35)
        pygame.display.set_caption('Ant colony')
        icon = pygame.image.load('../images/ant_ico.png')
        pygame.display.set_icon(icon)
        surf = pygame.transform.scale(pygame.image.load(
            "../images/cursor.png").convert_alpha(), (32, 32)) # 32/2 anlamı
        cursor = pygame.cursors.Cursor((0, 0), surf)
        pygame.mouse.set_cursor(cursor)
        self.clock = pygame.time.Clock()
        self.delta_time = self.clock.tick(FPS)
        self.foods = pygame.sprite.Group()

        #kayıt objesi
        self.recorder = PeriodicRecorder(global_stats_object)
        #oyunun çalışması süresince son kayıt zamanı
        self.last_record_time = 0

        self.last_spawn_time = 0  # Son karınca üretim zamanı
        self.spawn_interval = 2500  # Karınca üretim aralığı (ms)
        self.start_time = pygame.time.get_ticks()

    def draw_nest(self):
        nest = pygame.transform.scale(pygame.image.load(
            "../images/castle.png").convert_alpha(), (32*3, 32*3))
        nest_rect = nest.get_rect(center=(NEST_X, NEST_Y))
        self.screen.blit(nest, nest_rect)
        return nest_rect

    def create_objects(self):
        self.ants = pygame.sprite.Group(
            [Ant(self.delta_time) for _ in range(ANTS)])
        self.leader_ants = pygame.sprite.Group(
            [Ant(self.delta_time) for _ in range(global_stats_object.total_ants)])
        
        rand_locations = [(random.randint(0, WIDTH-100), random.randint(0, HEIGHT-100)) for _ in range(5)]
        # yiyecek konum ve sayısının belirlenmesi
        
        for location in rand_locations:
            temp_foods = pygame.sprite.Group()
            temp_foods = pygame.sprite.Group(
            [Food(random.randint(location[0], location[0]+50),random.randint(location[1], location[1]+50), "food") for i in range(50)])
            self.foods.add(temp_foods)
        
        

        # self.foods = pygame.sprite.Group(
        #     [Food(random.randint(0, WIDTH),
        #           random.randint(0, HEIGHT)) for _ in range(1000)])
        self.pheromones = pygame.sprite.Group() # feromonlar
        self.threats = pygame.sprite.Group() # tehditler

    def create_ant(self):
        ant = Ant(self.delta_time)
        self.ants.add(ant)
        #global_stats_object.produced_ant_count += 1 #mainde zaten bu sayı arttırılıyor
        return ant

    def create_threat(self, pos):
        threat = Threat(*pos)
        self.threats.add(threat)
        return threat

    def threat_spawner(self):
        threat = self.create_threat()
        self.threats.add(threat)


    def show_statistics(self):
        stats = global_stats_object.retun_statistics()

        text = self.font.render(f"Ants: {stats['total_ants']}", True, WHITE)
        self.screen.blit(text, (1450, 25))
        text = self.font.render(f"Total food: {stats['total_food']}", True, WHITE)
        self.screen.blit(text, (1450, 75))
        text = self.font.render(f"Collected food: {stats['collected_food']}", True, WHITE)
        self.screen.blit(text, (1450, 125))
        text = self.font.render(f"Produced ants: {stats['produced_ant_count']}", True, WHITE)
        self.screen.blit(text, (1450, 175))
        text = self.font.render(f"Collected food per second: {stats['collected_food_per_second']}", True, WHITE)
        self.screen.blit(text, (1450, 225))
        text = self.font.render(f"Collected food per ant: {stats['collected_food_per_ant']}", True, WHITE)
        self.screen.blit(text, (1450, 275))

    def ant_spawner(self, current_time): #karınca üretimine saniyede 1 sınırlandırma getirildi
        if global_stats_object.produced_ant_count < 100 and global_stats_object.collected_food > 0 and  current_time - self.last_spawn_time > self.spawn_interval:
            global_stats_object.increase_produced_ant_count()
            global_stats_object.decrease_collected_food()  
            global_stats_object.recalculate_collected_food_per_ant()
            global_stats_object.increase_collected_food_per_second(self.start_time)
            ant = self.create_ant()
            self.ants.add(ant)
            self.last_spawn_time = current_time


    def pheromone_quadtree(self):
        pheromone_boundary = Rectangle(0, 0, WIDTH, HEIGHT)
        self.pheromone_qtree = Quadtree(pheromone_boundary, 1)

    def user_event(self):
        self.add_pheromone = pygame.USEREVENT
        pygame.time.set_timer(self.add_pheromone, 100)

    def type_of_ants(self, ant_type, nest):
        for ant in ant_type:
            ant.update(self.screen, nest, self.foods,
                    self.ant_quad_tree, self.pheromone_qtree)
            ant.draw(self.screen)
            # self.ant_quad_tree.draw(self.screen)
            x, y = ant.ant_coord()
            if ant.dragged_food:
                ant.dragged_food.rect.center = (x, y)

    def main(self):
        self.create_objects()
        self.pheromone_quadtree()
        self.user_event()



        while True:

            self.screen.fill(SAND)
            self.show_statistics()

            current_time = pygame.time.get_ticks()
            self.ant_spawner(current_time)
            
            #recorder
            '''ÇOK ÖNEMLİ NOT: BU AMK YERİNDE FRAME BAŞINA ÇALIŞIYOR BU DEĞİŞMELİ!!!'''
            current_time_f_export = time.time()
            if current_time_f_export - self.last_record_time > 1:
                self.recorder.start_recording(1)
                self.last_record_time = current_time_f_export


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        food = Food(*mouse_pos, "food")
                        self.foods.add(food)
                        global_stats_object.increase_total_food()

                # elif event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_SPACE:
                #         ant = self.create_ant()
                #         self.ants.add(ant)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        food = Food(*mouse_pos, "threat")
                        self.foods.add(food)

                    #     mouse_pos = pygame.mouse.get_pos()
                    #     self.create_threat(mouse_pos)


                if len(self.pheromones) <= 8000: #feromon üretimi sınırlandırıldı
                    if event.type == self.add_pheromone:
                        for leader_ant in self.leader_ants:
                            if leader_ant.choose == 1:
                                type = 'food'
                            elif leader_ant.choose == 0:
                                type = 'trace'
                            elif leader_ant.choose == 2:
                                type = 'threat'
                            # feromon oluşturma mekanizması
                            pheromone = Pheromone(
                                int(leader_ant.x), int(leader_ant.y), lifespan, self.pheromone_qtree,type, priority=1)
                            self.pheromones.add(pheromone)

            for pheromone in self.pheromones:
                pheromone.update(self.pheromone_qtree)
                pheromone.draw(self.screen)
                # pheromone_qtree.draw(screen)

            nest = self.draw_nest()

            for food in self.foods:
                food.draw(self.screen)

            for threat in self.threats:
                threat.draw(self.screen)

            ant_boundary = Rectangle(0, 0, WIDTH, HEIGHT)
            self.ant_quad_tree = Quadtree(ant_boundary, 1)

            self.type_of_ants(self.ants, nest)
            self.type_of_ants(self.leader_ants, nest)

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    setup_instance = Setup()
    setup_instance.main()
