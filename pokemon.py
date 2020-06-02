class Pokemon:

  def __init__(self, name, element, level):
    self.name = name
    self.element = element
    self.level = level
    self.base_max_health = 100
    self.base_attack = 100
    self.base_defense = 100
    self.regenerative = False

  def __repr__(self):
    return self.name

  def set_stats(self):
    self.max_health = int(self.base_max_health*(1+self.level)/2)
    self.current_health = self.max_health
    self.attack = int(self.base_attack*(1+self.level)/2)
    self.defense = int(self.base_defense*(1+self.level)/2)

  def info(self):
    plus_status = lambda reg_status: ", regenerative" if reg_status == True else ""
    print(f"\t{self}: {self.element}, level {self.level}")
    print(f"Health: {self.current_health} (of {self.max_health}){plus_status(self.regenerative)}")
    print(f"Attack: {self.attack}")
    print(f"Defense: {self.defense}")

  def lose_health(self, lose):
    lose = min(lose, self.current_health)
    self.current_health -= lose
    print(f"{self} loses {lose} of health and has {self.current_health} of health now")

  def gain_health(self, gain):
    gain = min(gain, self.max_health - self.current_health)
    self.current_health += gain
    print(f"{self} gains {gain} of health and has {self.current_health} of health now")

  def regenerate(self):
    if self.current_health < self.max_health:
      print(f"{self} regenerates")
      self.gain_health(int(self.max_health*0.1))

  def fight(self, goal):
    fight_stats = self.fight_stats(goal)
    print(f"{self} attacks {goal} {fight_stats[1]}")
    goal.lose_health(fight_stats[0])

  def fight_stats(self, goal):
    elements_triangle = {'Fire': 0, 'Water': 1, 'Grass': 2}
    attack_type = (elements_triangle[self.element]-elements_triangle[goal.element])%3
    attack_type_koef = {0: 1, 1: 3/2, 2: 2/3}
    attack = int(self.attack/(1+goal.defense/self.attack)*attack_type_koef[attack_type])
    attack_type_description = {0: "",
                               1: f"with element bonus: {self.element} against {goal.element}",
                               2: f"with element penalty: {self.element} against {goal.element}"}
    return (attack, attack_type_description[attack_type])

class AttackPokemon(Pokemon):

  def __init__(self, name, element, level):
    super().__init__(name, element, level)
    self.base_attack = int(self.base_attack*1.2)

class DefensePokemon(Pokemon):

  def __init__(self, name, element, level):
    super().__init__(name, element, level)
    self.base_defense = int(self.base_defense*1.1)
    self.base_max_health = int(self.base_max_health*1.1)

class RegenerativePokemon(Pokemon):

  def __init__(self, name, element, level):
    super().__init__(name, element, level)
    self.regenerative = True

class Trainer:

  def __init__(self, name, pokemons, potions=3):
    self.name = name
    self.pokemons = pokemons
    self.active = pokemons[0]
    self.potions = potions

  def __repr__(self):
    return self.name

  def info(self):
    print(f"\n{self} has {len(self.pokemons)} Pokemon")
    self.show_active()
    print(f"Potions: {self.potions}")
    for pokemon in self.pokemons:
      pokemon.info()

  def show_active(self):
    print(f"{self}'s active Pokemon is {self.active}")

  def fight(self, goal):
    print(f"{self} attacks {goal}")
    self.active.fight(goal.active)
    if goal.active.current_health == 0:
      goal.pokemons.remove(goal.active)
      print(f"{goal.active.name} dies")
      if len(goal.pokemons) > 0:
        goal.active = goal.pokemons[0]
        goal.show_active()

  def use_potion(self, pokemon):
      self.potions -= 1
      print(f"{self} uses potion on {pokemon}")
      pokemon.gain_health(100)

def game(all_trainers):
  game_mode = choose_menu(["Player vs Player", "Player vs Computer"], "Game mode:")
  game_mode_titles = {"Player vs Player": ["First Player", "Second Player"],
                      "Player vs Computer": ["Player", "Computer"]}
  trainer_1, trainer_2 = choose_trainers(all_trainers, game_mode_titles[game_mode])
  computer_turn = False
  full_commands_list = ["Info", "Change active Pokemon", "Fight", "Use healing potion", "Exit"]

  while True:
    if computer_turn:
      command = computer_turn_commands.pop()
    else:
      commands_list = list(full_commands_list)
      if trainer_1.potions == 0:
        commands_list.remove("Use healing potion")
      command = choose_menu(commands_list, f"{trainer_1}'s Turn: ")

    # Info
    if command == "Info":
      trainer_1.info()
      trainer_2.info()

    # Change active Pokemon
    elif command == "Change active Pokemon":
      if computer_turn:
        trainer_1.active = computer_turn_commands.pop()
      else:
        trainer_1.active = choose_menu(trainer_1.pokemons, f"{trainer_1} changes active Pokemon:")
      trainer_1.show_active()

    # Fight
    elif command == "Fight":
      trainer_1.fight(trainer_2)
      if len(trainer_2.pokemons) == 0:
        print(f"{trainer_1} wins!")
        break
      for pokemon in trainer_2.pokemons:
        if pokemon.regenerative:
          pokemon.regenerate()
      trainer_1, trainer_2 = [trainer_2, trainer_1]
      if game_mode == "Player vs Computer":
        computer_turn = not computer_turn
        if computer_turn:
          print(f"\n{trainer_1}'s Turn: ")
          computer_turn_commands = get_computer_turn_commands(trainer_1, trainer_2)

    # Use healing potion
    elif command == "Use healing potion":
      if computer_turn:
        trainer_1.use_potion(computer_turn_commands.pop())
      else:
        trainer_1.use_potion(choose_menu(trainer_1.pokemons, f"{trainer_1} uses healing potion:"))

    # Exit
    elif command == "Exit":
      break

def get_computer_turn_commands(computer, player):
  computer_turn_commands = ["Fight"]
  best_attack = 0
  for pokemon in computer.pokemons:
    attack = pokemon.fight_stats(player.active)[0]
    if attack > best_attack:
      best_pokemon = pokemon
      best_attack = attack
  if (best_pokemon.max_health - best_pokemon.current_health >= 100) and (computer.potions > 0):
    computer_turn_commands += [best_pokemon, "Use healing potion"]
  if best_pokemon != computer.active:
    computer_turn_commands += [best_pokemon, "Change active Pokemon"]
  return computer_turn_commands

def choose_trainers(all_trainers, titles):
  trainers = [None, None]
  for trainer_num in range(2):
    choice = choose_menu(all_trainers, f"Choose {titles[trainer_num]} Trainer:")
    for pokemon in choice.pokemons:
      pokemon.set_stats()
    print(f"{titles[trainer_num]} Trainer: {choice}")
    trainers[trainer_num] = choice
    all_trainers.remove(choice)
  return trainers

def choose_menu(lst, title):
    print(f"\n{title}")
    for item in enumerate(lst):
        print(f"{item[0]} - {item[1]}")
    while True:
        choice = input("Number of your choice: ")
        if choice in map(str, range(len(lst))):
            return lst[int(choice)]

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
