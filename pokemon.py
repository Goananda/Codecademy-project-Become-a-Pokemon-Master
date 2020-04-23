class Pokemon:

  def __init__(self, name, element, level):
    self.name = name
    self.element = element
    self.level = level
    self.base_max_health = 100
    self.base_attack = 100
    self.base_defense = 100
    self.regenerative = False
    self.start()

  def __repr__(self):
    return self.name

  def start(self):
    self.set_stats(self.level)
    self.current_health = self.max_health

  def set_stats(self, level):
    self.max_health = int(self.base_max_health*(1 + level)/2)
    self.attack = int(self.base_attack*(1 + level)/2)
    self.defense = int(self.base_defense*(1 + level)/2)

  def info(self):
    plus_healer = lambda healer_status: ", regenerative" if healer_status == True else ""
    print(f"   {self.name}: {self.element}, level {self.level}\nHealth: {int(self.current_health)} \
(of {int(self.max_health)}){plus_healer(self.regenerative)}\nAttack: {int(self.attack)}\nDefense: {int(self.defense)}")

  def lose_health(self, lose):
    lose = min(lose, self.current_health)
    self.current_health -= lose
    print(f"{self.name} loses {lose} of health and has {self.current_health} of health now")

  def gain_health(self, gain):
    gain = min(gain, self.max_health - self.current_health)
    self.current_health += gain
    print(f"{self.name} gains {gain} of health and has {self.current_health} of health now")

  def regenerate(self):
    if self.regenerative == True and 0 < self.current_health < self.max_health:
      print(f"{self.name} regenerates")
      self.gain_health(int(self.max_health*0.15))

  def fight(self, goal):
    elements_triangle = {'Fire': 0, 'Water': 1, 'Grass': 2}
    attack_type = (elements_triangle[self.element] - elements_triangle[goal.element]) % 3
    attack_type_koef = {0: 1, 1: 3/2, 2: 2/3}
    attack_type_description = {0: "", 1: f" with element bonus: {self.element} against {goal.element}",\
                               2: f" with element penalty: {self.element} against {goal.element}"}
    attack = int(self.attack/(1 + goal.defense/self.attack)*attack_type_koef[attack_type])
    print(f"{self.name} attacks {goal.name}"+attack_type_description[attack_type])
    goal.lose_health(attack)

class AttackPokemon(Pokemon):

  def __init__(self, name, element, level):
    super().__init__(name, element, level)
    self.base_attack = 150
    self.start()

class DefensePokemon(Pokemon):

  def __init__(self, name, element, level):
    super().__init__(name, element, level)
    self.base_max_health = 125
    self.base_defense = 125
    self.start()

class RegenerativePokemon(Pokemon):

  def __init__(self, name, element, level):
    super().__init__(name, element, level)
    self.base_max_health = 150
    self.regenerative = True
    self.start()

class Trainer:

  def __init__(self, name, pokemons, potions=3):
    self.name = name
    self.pokemons = pokemons
    self.active_pokemon = None
    self.potions = potions

  def __repr__(self):
    return self.name

  def info(self):
    print(f"{self.name} has {len(self.pokemons)} Pokemon:")
    for pokemon in self.pokemons:
      pokemon.info()
    self.show_active()
    print(f"Potions: {self.potions}")

  def show_active(self):
    if self.active_pokemon != None:
      print(f"{self.name}'s active Pokemon is {self.pokemons[self.active_pokemon]}")
    else:
      print(f"{self.name} has no active Pokemon")

  def activate(self, number=None):
    if number == None:
      self.active_pokemon = None
      for i in range(len(self.pokemons)):
        if self.pokemons[i].current_health > 0:
          self.active_pokemon = i
          break
    else:
      self.active_pokemon = number
    self.show_active()

  def fight(self, goal):
    print(f"{self.name} attacks {goal.name}")
    self.pokemons[self.active_pokemon].fight(goal.pokemons[goal.active_pokemon])
    if goal.pokemons[goal.active_pokemon].current_health == 0:
      print(f"{goal.pokemons[goal.active_pokemon].name} dies")
      goal.activate()

  def use_potion(self, pokemon):
      print(f"{self.name} uses potion on {pokemon.name}")
      pokemon.gain_health(100)
      self.potions -= 1

def game(all_trainers):
  trainers = choose_trainers(all_trainers)
  battle(trainers[0], trainers[1])

def choose_trainers(all_trainers):
  trainers = [None, None]
  order_names = ["first", "second"]
  for trainer_num in range(2):
    choice = choose_from_list([trainer.name for trainer in all_trainers], "Trainers",\
                              f"Choose {order_names[trainer_num]} Trainer's number: ")
    trainers[trainer_num] = all_trainers.pop(choice)
    print(f"{order_names[trainer_num].title()} trainer is {trainers[trainer_num].name}")
    trainers[trainer_num].activate()
  return trainers

def battle(trainer_1, trainer_2):
  full_commands_list = ("Info", "Change active Pokemon", "Fight", "Use healing potion", "Exit")
  while True:
    commands_list = list(full_commands_list)
    if trainer_1.potions == 0:
      commands_list.pop(full_commands_list.index("Use healing potion"))
    command_index = choose_from_list(commands_list, "Commands", f"{trainer_1.name}'s turn: ")
    if commands_list[command_index] == "Info":
      trainer_1.info()
      print("")
      trainer_2.info()
    elif commands_list[command_index] == "Change active Pokemon":
      print(f"{trainer_1.name} changes active Pokemon")
      trainer_1.activate(choose_alive_pokemon(trainer_1))
    elif commands_list[command_index] == "Fight":
      trainer_1.fight(trainer_2)
      if trainer_2.active_pokemon == None:
        print(f"{trainer_1.name} wins!")
        break
      for pokemon in trainer_2.pokemons:
        pokemon.regenerate()
      trainer_1, trainer_2 = [trainer_2, trainer_1]
    elif commands_list[command_index] == "Use healing potion":
      print(f"{trainer_1.name} uses healing potion")
      trainer_1.use_potion(trainer_1.pokemons[choose_alive_pokemon(trainer_1)])
    elif commands_list[command_index] == "Exit":
      break

def choose_alive_pokemon(trainer):
  alive_pokemons_index = [i for i in range(len(trainer.pokemons)) if trainer.pokemons[i].current_health > 0]
  alive_pokemons_names = [trainer.pokemons[i].name for i in alive_pokemons_index]
  return alive_pokemons_index[choose_from_list(alive_pokemons_names, f"{trainer.name}'s Pokemons", "Choose Pokemon's number: ")]

def choose_from_list(list, title, text):
  print(f"\n{title}:")
  for i in range(len(list)):
    print(f"{i} - {list[i]}")
  while True:
    choice = input(text)
    if choice in [str(i) for i in range(len(list))]:
      print("")
      return int(choice)

dragon = AttackPokemon('Fire Dragon', 'Fire', 3)
kraken = AttackPokemon('Kraken', 'Water', 2)
fairy = AttackPokemon('Fury Fairy', 'Grass', 1)
whirlpool = DefensePokemon('Whirlpool', 'Water', 3)
creepers = DefensePokemon('Creepers', 'Grass', 2)
firefly = DefensePokemon('Firefly', 'Fire', 1)
tree = RegenerativePokemon('Mother Tree', 'Grass', 3)
phoenix = RegenerativePokemon('Phoenix', 'Fire', 2)
blob = RegenerativePokemon('Blob', 'Water', 1)
jaba = Trainer('Jaba Bo', [dragon, creepers, blob])
alchemist = Trainer('Alchemist', [whirlpool, phoenix, fairy])
witch = Trainer('Forest Witch', [tree, kraken, firefly])
all_trainers = [jaba, alchemist, witch]

game(all_trainers)
