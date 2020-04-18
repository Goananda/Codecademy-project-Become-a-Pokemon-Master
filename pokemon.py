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
(of {int(self.max_health)})"+plus_healer(self.regenerative)+f"\nAttack: {int(self.attack)}\nDefense: {int(self.defense)}")
  
  def lose_health(self, lose):
    if self.current_health < lose:
      lose = self.current_health
    self.current_health -= lose
    print(f"{self.name} loses {lose} of health")
  
  def gain_health(self, gain):
    if self.max_health - self.current_health < gain:
      gain = self.max_health - self.current_health
    self.current_health += gain
    print(f"{self.name} gains {gain} of health")
  
  def regenerate(self):
    if self.regenerative == True and self.current_health > 0 and self.current_health < self.max_health:
      print(f"{self.name} regenerates")
      self.gain_health(int(self.max_health*0.15))
  
  def fight(self, goal):
    elements_triangle = {'Fire': 0, 'Water': 1, 'Grass': 2}
    attack_type = (elements_triangle[self.element] - elements_triangle[goal.element]) % 3
    attack_type_koef = {0: 1, 1: 3/2, 2: 2/3}
    attack_type_description = {0: "", 1: f" with element bonus: {self.element} againts {goal.element}",\
                               2: f" with element penalty: {self.element} againts {goal.element}"}
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
  
  def __init__(self, name, pokemons, poisons=3):
    self.name = name
    self.pokemons = pokemons
    self.active_pokemon = None
    self.poisons = poisons
  
  def __repr__(self):
    return self.name
  
  def info(self):
    print(f"{self.name} has {len(self.pokemons)} Pokemon:")
    for pokemon in self.pokemons:
      pokemon.info()
    self.show_active()
    print(f"Poisons: {self.poisons}")
  
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
  
  def use_poison(self, pokemon):
      print(f"{self.name} uses poison on {pokemon.name}")
      pokemon.gain_health(100)
      self.poisons -= 1

def battle(trainer_1, trainer_2):
  trainer_1.activate()
  trainer_2.activate()
  print("")
  full_commands_list = ("0 - Info", "1 - Change active pokemon", "2 - Fight", "3 - Use healing poison", "4 - Exit")
  full_choices = ('0', '1', '2', '3', '4')
  while True:
    commands_list = list(full_commands_list)
    choices = list(full_choices)
    if trainer_1.poisons == 0:
      commands_list.pop(3)
      choices.pop(3)
    print("Commands:")
    for i in commands_list:
        print(i)
    command = None
    while command == None:
      choice = input(f"{trainer_1.name}'s turn: ")
      if choice in choices:
          command = int(choice)
    # 0 - Info
    if command == 0:
      print("")
      trainer_1.info()
      print("")
      trainer_2.info()
      print("")
    # 1 - Change active pokemon
    elif command == 1:
      print("")
      dict = {}
      num = 0
      for i in range(len(trainer_1.pokemons)):
        if trainer_1.pokemons[i].current_health > 0:
          dict[str(num)] = i
          print(f"{num}: {trainer_1.pokemons[i].name}")
          num +=1
      chosen = False
      while chosen == False:
        choice = input("Choose Pokemon's number: ")
        try:
          if choice in dict:
            trainer_1.activate(dict[choice])
            chosen = True
          else:
            raise Error
        except:
          continue
      print("")
    # 2 - Fight
    elif command == 2:
      print("")
      trainer_1.fight(trainer_2)
      if trainer_2.active_pokemon == None:
        print(f"{trainer_1.name} won!")
        break
      for pokemon in trainer_2.pokemons:
        pokemon.regenerate()
      trainer_1, trainer_2 = [trainer_2, trainer_1]
      print("")
    # 3 - Use healing poison
    elif command == 3:
      print("")
      dict = {}
      num = 0
      for i in range(len(trainer_1.pokemons)):
        if trainer_1.pokemons[i].current_health > 0:
          dict[str(num)] = i
          print(f"{num}: {trainer_1.pokemons[i].name}")
          num +=1
      chosen = False
      while chosen == False:
        choice = input("Choose Pokemon's number: ")
        try:
          if choice in dict:
            trainer_1.use_poison(trainer_1.pokemons[dict[choice]])
            chosen = True
          else:
            raise Error
        except:
          continue
      print("")
    # 4 - Exit
    elif command == 4:
      break

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

def choose_trainers():
  trainers = [None, None]
  order_names = ["first", "second"]
  for trainer_num in range(2):
    print("Trainers:")
    for i in range(len(all_trainers)):
      print(f"{i}: {all_trainers[i].name}")
    while trainers[trainer_num] == None:
      try:
        chosen_num = int(input(f"Choose {order_names[trainer_num]} Trainer's number: "))
        if chosen_num in range(len(all_trainers)):
          trainers[trainer_num] = all_trainers.pop(chosen_num)
        else:
          raise Error
      except:
        continue
    print("")
  return trainers

def game():
  trainers = choose_trainers()
  battle(trainers[0], trainers[1])

game()
