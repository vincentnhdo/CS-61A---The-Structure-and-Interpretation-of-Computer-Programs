# A "simple" adventure game.

class Player(object):
    def __init__(self, name, place):
        """Create a player object."""
        self.name = name
        self.place = place

    def look(self):
        self.place.look()

    def go_to(self, location):
        """Go to a location if it's among the exits of player's current place.

        >>> sather_gate = Place('Sather Gate', 'Sather Gate', [], [])
        >>> gbc = Place('GBC', 'Golden Bear Cafe', [], [])
        >>> sather_gate.add_exits([gbc])
        >>> sather_gate.locked = True
        >>> gbc.add_exits([sather_gate])
        >>> me = Player('player', sather_gate)
        >>> me.go_to('GBC')
        You are at GBC
        >>> me.place is gbc
        True
        >>> me.place.name
        'GBC'
        >>> me.go_to('GBC')
        Can't go to GBC from GBC.
        Try looking around to see where to go.
        You are at GBC
        >>> me.go_to('Sather Gate')
        Sather Gate is locked! Go look for a key to unlock it
        You are at GBC
        """
        destination_place = self.place.get_neighbor(location)
        if destination_place.locked:
            print(destination_place.name, 'is locked! Go look for a key to unlock it')
            print('You are at', self.place.name)
        else:
            self.place = destination_place
            print('You are at', self.place.name)


    def talk_to(self, person):
        """Talk to person if person is at player's current place.

        >>> john = Character('John', 'Have to run for lecture!')
        >>> sather_gate = Place('Sather Gate', 'You are at Sather Gate', [john], [])
        >>> me = Player('player', sather_gate)
        >>> me.talk_to(john)
        Person has to be a string.
        >>> me.talk_to('John')
        John says: Have to run for lecture!
        >>> me.talk_to('Albert')
        Albert is not here.
        """
        if type(person) != str:
            print('Person has to be a string.')
        "*** YOUR CODE HERE ***"


    def take(self, thing):
        """Take a thing if thing is at player's current place

        >>> hotdog = Thing('Hotdog', 'A hot looking hotdog')
        >>> gbc = Place('GBC', 'You are at Golden Bear Cafe', [], [hotdog])
        >>> me = Player('Player', gbc)
        >>> me.backpack
        []
        >>> me.take(hotdog)
        Thing should be a string.
        >>> me.take('dog')
        dog is not here.
        >>> me.take('Hotdog')
        Player takes the Hotdog
        >>> me.take('Hotdog')
        Hotdog is not here.
        >>> isinstance(me.backpack[0], Thing)
        True
        >>> len(me.backpack)
        1
        """
        if type(thing) != str:
            print('Thing should be a string.')
        "*** YOUR CODE HERE ***"

    def check_backpack(self):
        """Print each item with its description and return a list of item names.

        >>> cookie = Thing('Cookie', 'A huge cookie')
        >>> donut = Thing('Donut', 'A huge donut')
        >>> cupcake = Thing('Cupcake', 'A huge cupcake')
        >>> gbc = Place('GBC', 'You are at Golden Bear Cafe',
        ...             [], [cookie, donut, cupcake])
        >>> me = Player('Player', gbc)
        >>> me.check_backpack()
        In your backpack:
            there is nothing.
        []
        >>> me.take('Cookie')
        Player takes the Cookie
        >>> me.check_backpack()
        In your backpack:
            Cookie - A huge cookie
        ['Cookie']
        >>> me.take('Donut')
        Player takes the Donut
        >>> food = me.check_backpack()
        In your backpack:
            Cookie - A huge cookie
            Donut - A huge donut
        >>> food
        ['Cookie', 'Donut']
        """
        print('In your backpack:')
        if not self.backpack:
            print('    there is nothing.')
        else:
            for item in self.backpack:
                print('   ', item.name, '-', item.description)
        return [item.name for item in self.backpack]

    def unlock(self, place):
        """If player has a key, unlock a locked neighboring place.

        >>> key = Key('SkeletonKey', 'A Key to unlock all doors.')
        >>> gbc = Place('GBC', 'You are at Golden Bear Cafe', [], [key])
        >>> fsm = Place('FSM', 'Home of the nectar of the gods', [], [])
        >>> gbc.add_exits([fsm])
        >>> fsm.locked = True
        >>> me = Player('Player', gbc)
        >>> me.unlock(fsm)
        Place must be a string
        >>> me.go_to('FSM')
        FSM is locked! Go look for a key to unlock it
        You are at GBC
        >>> me.unlock(fsm)
        Place must be a string
        >>> me.unlock('FSM')
        FSM can't be unlocked without a key!
        >>> me.take('SkeletonKey')
        Player takes the SkeletonKey
        >>> me.unlock('FSM')
        FSM is now unlocked!
        >>> me.unlock('FSM')
        FSM is already unlocked!
        >>> me.go_to('FSM')
        You are at FSM
        """
        if type(place) != str:
            print("Place must be a string")
            return
        key = None
        for item in self.backpack:
            if type(item) == Key:
                key = item
        "*** YOUR CODE HERE ***"


class Character(object):
    def __init__(self, name, message):
        self.name = name
        self.message = message

    def talk(self):
        return self.message


class Thing(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def use(self, place):
        print("You can't use a {0} here".format(self.name))

""" Implement Key here! """

class Treasure(Thing):
    def __init__(self, name, description, value, weight):
        Thing.__init__(self, name, description)
        self.value = value
        self.weight = weight

class Place(object):
    def __init__(self, name, description, characters, things):
        self.name = name
        self.description = description
        self.characters = {character.name: character for character in characters}
        self.things = {thing.name: thing for thing in things}
        self.locked = False
        self.exits = {} # {'name': (exit, 'description')}

    def look(self):
        print('You are currently at ' + self.name + '. You take a look around and see:')
        print('Characters:')
        if not self.characters:
            print('    no one in particular')
        else:
            for character in self.characters:
                print('   ', character)
        print('Things:')
        if not self.things:
            print('    nothing in particular')
        else:
            for thing in self.things.values():
                print('   ', thing.name, '-', thing.description)
        self.check_exits()

    def get_neighbor(self, exit):
        """
        >>> sather_gate = Place('Sather Gate', 'You are at Sather Gate', [], [])
        >>> gbc = Place('GBC', 'You are at Golden Bear Cafe', [], [])
        >>> gbc.add_exits([sather_gate])
        >>> place = gbc.get_neighbor('Sather Gate')
        >>> place is sather_gate
        True
        >>> place = gbc.get_neighbor('FSM')
        Can't go to FSM from GBC.
        Try looking around to see where to go.
        >>> place is gbc
        True
        """
        if type(exit) != str:
            print('Exit has to be a string.')
            return self
        elif exit in self.exits:
            exit_place = self.exits[exit][0]
            return exit_place
        else:
            print("Can't go to {} from {}.".format(exit, self.name))
            print("Try looking around to see where to go.")
            return self

    def take(self, thing):
        return self.things.pop(thing)

    def check_exits(self):
        print('You can exit to:')
        for exit in self.exits:
            print('   ', exit)

    def add_exits(self, places):
        for place in places:
            self.exits[place.name] = (place, place.description)