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
    self.max_health = int(self.base_max_health*(2+self.level)/3)
    self.current_health = self.max_health
    self.attack = int(self.base_attack*(2+self.level)/3)
    self.defense = int(self.base_defense*(2+self.level)/3)

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
      self.gain_health(int(self.max_health*0.2))

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
    self.base_defense = int(self.base_defense*1.2)

class RegenerativePokemon(Pokemon):

  def __init__(self, name, element, level):
    super().__init__(name, element, level)
    self.regenerative = True

class Trainer:

  def __init__(self, name, pokemons, potions=3):
    self.name = name
    self.pokemons = pokemons
    self.active = self.pokemons[0]
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
      print(f"{goal.active} dies")
      if len(goal.pokemons) > 0:
        goal.active = goal.pokemons[0]
        goal.show_active()

  def use_potion(self, pokemon):
      self.potions -= 1
      print(f"{self} uses potion on {pokemon}")
      pokemon.gain_health(100)

class Game:

  full_commands_list = ["Info", "Change active Pokemon", "Fight", "Use healing potion", "Exit"]

  def __init__(self, all_trainers):
    self.all_trainers = all_trainers
    self.trainers = []
    self.modes = []
    self.turn = 1
    self.comp_commands = []
    self.set_turn = True

  def start(self):
    self.choose_trainers()
    while True:

      if self.set_turn:
        self.turn = (self.turn+1)%2
        self.act = self.trainers[self.turn]
        self.pas = self.trainers[(self.turn+1)%2]
        if self.modes[self.turn] == "Computer":
          print(f"\n{self.act}'s Turn:")
          self.get_comp_commands()
        self.set_turn = False

      commands_list = list(self.full_commands_list)
      if self.act.potions == 0:
        commands_list.remove("Use healing potion")
      self.get_command(commands_list, f"{self.act}'s Turn:")

      # Info
      if self.command == "Info":
        for trainer in self.trainers:
          trainer.info()

      # Change active Pokemon
      elif self.command == "Change active Pokemon":
        self.get_command(self.act.pokemons, f"{self.act} changes active Pokemon:")
        self.act.active = self.command
        self.act.show_active()

      # Fight
      elif self.command == "Fight":
        self.act.fight(self.pas)
        if len(self.pas.pokemons) == 0:
          print(f"{self.act} wins!")
          break
        for pokemon in self.pas.pokemons:
          if pokemon.regenerative:
            pokemon.regenerate()
        self.set_turn = True

      # Use healing potion
      elif self.command == "Use healing potion":
        self.get_command(self.act.pokemons, f"{self.act} uses healing potion:")
        self.act.use_potion(self.command)

      # Exit
      elif self.command == "Exit":
        break

  def choose_trainers(self):
    titles = ["First", "Second"]
    for num in range(2):
      mode = choose_menu(["Player", "Computer"], f"{titles[num]} Trainer mode:")
      self.modes.append(mode)
      trainer = choose_menu(self.all_trainers, f"{titles[num]} Trainer:")
      self.trainers.append(trainer)
      for pokemon in trainer.pokemons:
        pokemon.set_stats()
      self.all_trainers.remove(trainer)

  def get_command(self, lst, title):
    if self.modes[self.turn] == "Player":
      self.command = choose_menu(lst, title)
    else:
      self.command = self.comp_commands.pop()

  def get_comp_commands(self):
    self.comp_commands.append("Fight")
    best_attack = 0
    for pokemon in self.act.pokemons:
      attack = pokemon.fight_stats(self.pas.active)[0]
      if attack > best_attack:
        best_pokemon = pokemon
        best_attack = attack
    if (best_pokemon.max_health - best_pokemon.current_health >= 100) and (self.act.potions > 0):
      self.comp_commands += [best_pokemon, "Use healing potion"]
    if best_pokemon != self.act.active:
      self.comp_commands += [best_pokemon, "Change active Pokemon"]

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

game = Game(all_trainers)
game.start()
