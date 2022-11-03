import pygame
from pygame.locals import *
import json

from player import Player
from agent import Agent
from level import Level
from AG import AG

###------Params------###
# Name of file that contains the level
level_file = 'small_2e.json'
# Population size
POP_SIZE = 100
# Max amount of Generations / Amount of steps an agent can make
GEN_LIMIT = 300
IND_SIZE = 1000

# Incremental mode - If false the next params are ignored in execution
incremental = False
# Increment Length (Amount of Gens in each increment) / Incremental Factor (Amount of steps added in each increment)
INC_LEN = 20
INC_FACTOR = 100
###----------End----------###

###------Init PyGame------###
pygame.init()
SCREEN_WIDTH = 810
SCREEN_HEIGHT = 600
flags = DOUBLEBUF
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
font = pygame.font.Font('freesansbold.ttf', 24)
clock = pygame.time.Clock()
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
isRunning = True
AGENT_SPEED = 3
###----------End----------###


def build_agents(population, start_position):
    agents = []
    for ind in population:
        agents.append(Agent(start_position, 10, 10, ind, AGENT_SPEED))
    return agents


def agent_step(agent):
    agent.move(screen, level.collisions(screen, agent.x, agent.y))
    if agent.collision(screen).collidelist(level.enemy_collision(screen)) != -1:  # Collision with enemies
        agent.die()
    if agent.collision(screen).collidelist([level.finish.draw(screen)]) != -1:
        agent.finish()


def update():
    keys = pygame.key.get_pressed()
    level.move_enemies()
    player.move(keys, screen, level.collisions(screen, player.x, player.y))
    # Agent behaviour
    for agent in agents:
        if agent.alive and not agent.finished:
            agent_step(agent)
    # Leader behaviour
    if leader.alive and not leader.finished:
        agent_step(leader)
    # Historic Best behaviour
    if historic_best.alive and not historic_best.finished:
        agent_step(historic_best)
    # Player behaviour
    if player.collision(screen).collidelist(level.enemy_collision(screen)) != -1:
        player.reset()
    if player.collision(screen).collidelist([level.finish.draw(screen)]) != -1:
        player.finish()


def draw():
    screen.fill((183, 175, 250))
    level.draw(screen)
    #player.draw(screen)
    genCounter = font.render("Generation: " + str(generation_counter), True, (255, 255, 255))
    stepCounter = font.render("Step: " + str(steps), True, (255, 255, 255))
    screen.blit(genCounter, (600, 10))
    screen.blit(stepCounter, (50, 10))
    for agent in agents:
        agent.draw(screen)
    if generation_counter != 1:
        historic_best.draw(screen)
        leader.draw(screen)


def reset():
    for agent in agents:
        agent.reset(False)
    level.reset()
    leader.reset(True)
    historic_best.reset(False)


def end_condition():
    if incremental:
        return steps > INC_FACTOR * (((generation_counter - 1) // INC_LEN) + 1)
    else:
        return steps > IND_SIZE

###------Loadout------###
generation_counter = 0
with open(level_file) as f:
    level_data = json.load(f)
level = Level(level_data["layout"], level_data["start"], level_data["finish"], level_data["enemies"])
player = Player(level.start_position(), 10, 10, 2)
if incremental:
    AG = AG(level, POP_SIZE, INC_FACTOR)
else:
    AG = AG(level, POP_SIZE, IND_SIZE)
leader = Agent(level.start_position(), 10, 10, [], AGENT_SPEED)
leader.is_leader = True
historic_best = Agent(level.start_position(), 10, 10, [], AGENT_SPEED, (50, 50, 230))
historic_best_fitness = 10000000.00
###--------End--------###

###------Game Loop------###
while isRunning:
    iteration = True
    generation_counter += 1
    agents = build_agents(AG.population, level.start_position())
    print("Start of generation " + str(generation_counter))
    steps = 0
    pygame.time.delay(100)
    while iteration and isRunning:
         clock.tick(60)
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
               isRunning = False
         update()
         draw()
         steps += 1
         pygame.display.update()
         if end_condition():
            iteration = False
            pygame.time.delay(500)
            best_ind = AG.fitness_evaluation(agents)
            best_ind_fitness = float(str(best_ind.fitness).split(',')[0][1:])
            if historic_best_fitness >= best_ind_fitness:
                historic_best_fitness = best_ind_fitness
                historic_best.moves = best_ind
            leader.moves = best_ind
            AG.evolution_step()
            finished_agents = 0
            dead_agents = 0
            for agent in agents:
                finished_agents += agent.finished
                dead_agents += not agent.alive
            print('Best fitness in this generation: ' + str(best_ind.fitness) + '  ----  Finished: ' + str(finished_agents) + '  ----  Dead: ' + str(dead_agents))
            print('Best fitness overall: ' + str(best_ind_fitness))
            print('End of generation ' + str(generation_counter))
            print()
            if incremental:
                if (generation_counter % INC_LEN == 0) and not generation_counter > (GEN_LIMIT - INC_LEN * (IND_SIZE / INC_FACTOR)):
                    AG.update_toolbox(AG, INC_FACTOR * (((generation_counter-1) // INC_LEN)+2), best_ind)
            reset()
    if generation_counter == GEN_LIMIT:
         isRunning = False
         print('Best ' + str(best_ind))
         print('Fitness: ' + str(best_ind_fitness))

pygame.quit()
###---------End---------###
