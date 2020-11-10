from .data import *
from random import random, shuffle, choice, seed
import time
import csv

"""
Figure out a better way to do replicating menace mangetic
Golden minions
scallywag
selfless hero priority
plant deathrattle
drakonid + bolvar divine shields
"""

class Board:
    MAXsize = 7
    def __init__(self, p1, p2):
        # sides of the board
        self.p1 = []
        for val in p1:
            if type(val) is type(1):
                m = summon(val)
            else:
                m = summon(val[0])
                m.attack = val[1]
                m.health = val[2]
                for attr in val[3:]:
                    m.setAttr(attr)
            self.p1.append(m)

        self.p2 = []
        for val in p2:
            if type(val) is type(1):
                m = summon(val)
            else:
                m = summon(val[0])
                m.attack = val[1]
                m.health = val[2]
                for attr in val[3:]:
                    m.setAttr(attr)
            self.p2.append(m)


        if self.p1:
            self.setupPtrs(self.p1)
        if self.p2:
            self.setupPtrs(self.p2)

        # special minions on each side
        self.p1special = {}
        self.p2special = {}
        self.setupSpecials(self.p1, self.p1special)
        self.setupSpecials(self.p2, self.p2special)

        # apply auras to minions
        self.applyAuras(self.p1, self.p1special)
        self.applyAuras(self.p2, self.p2special)

        # mech graveyard
        self.g1 = []
        self.g2 = []

    def setupPtrs(self, side):
        prev = None
        for m in side:
            m.prev = prev
            if prev:
                prev.next = m
            prev = m
        side[-1].next = side[0]
        side[0].prev = side[-1]

    # specials track minions with triggers and auras
    # so that we only search for them when we know they are on the board
    def setupSpecials(self, side, special):
        for m in side:
            if m.id in speciallist:
                special.setdefault(m.id, 0)
                special[m.id] += 1

    # apply auras to minions
    def applyAuras(self, side, special):
        warleaders = special.get(WARLEADER)
        southseas = special.get(SOUTHSEACAPTAIN)
        siegebreakers = special.get(SIEGEBREAKER)
        malganises = special.get(MALGANIS)

        otherside = self.getOtherSide(side)
        murkeye = special.get(MURKEYE) or self.getSpecial(otherside).get(MURKEYE)

        if warleaders:
            for m in side:
                if m.isMurloc():
                    m.attack += 2*(warleaders-(m.id==WARLEADER))
        if southseas:
            for m in side:
                if m.isPirate():
                    m.attack += 1*(southseas-(m.id==SOUTHSEACAPTAIN))
                    m.health += 1*(southseas-(m.id==SOUTHSEACAPTAIN))
        if siegebreakers:
            for m in side:
                if m.isDemon():
                    m.attack += 1*(siegebreakers-(m.id==SIEGEBREAKER))
        if malganises:
            for m in side:
                if m.isDemon():
                    m.attack += 2*(malganises-(m.id==MALGANIS))
                    m.health += 2*(malganises-(m.id==MALGANIS))
        if murkeye:
            murlocs = sum(1 for m in side if m.isMurloc()) + sum(1 for m in otherside if m.isMurloc())
            for m in side:
                if m.id == MURKEYE:
                    m.attack += murlocs - 1

    def applyAura(self, m, side):
        special = self.getSpecial(side)
        otherside = self.getOtherSide(side)
        id = m.id


        # if warleader: buff all allies +2 attack
        # if murkeye: give it +X attack
        # give all murkeyes except this one +1 attack
        if m.isMurloc():
            warleaders = special.get(WARLEADER)
            if warleaders:
                m.attack += 2*(warleaders-(m.id==WARLEADER))
            if id == WARLEADER:
                for minion in side:
                    if minion.isMurloc() and minion is not m:
                        m.attack += 2
            if special.get(MURKEYE) or self.getSpecial(self.getOtherSide(side)).get(MURKEYE):
                if id == MURKEYE:
                    murlocs = sum(1 for n in side if n.isMurloc()) + sum(1 for n in otherside if n.isMurloc())
                    m.attack += murlocs - 1
                for minion in side:
                    if minion.id == MURKEYE and minion is not m:
                        minion.attack += 1
                for minion in otherside:
                    if minion.id == MURKEYE and minion is not m:
                        minion.attack += 1

        elif m.isPirate():
            southseas = special.get(SOUTHSEACAPTAIN)
            if southseas:
                m.attack += 1*(southseas-(m.id==SOUTHSEACAPTAIN))
                m.health += 1*(southseas-(m.id==SOUTHSEACAPTAIN))
            if id == SOUTHSEACAPTAIN:
                for minion in side:
                    if minion.isPirate() and minion is not m:
                        minion.attack += 1
                        minion.health += 1

        elif m.isDemon():
            siegebreakers = special.get(SIEGEBREAKER)
            if siegebreakers:
                m.attack += 1*(siegebreakers-(m.id==SIEGEBREAKER))
            malganises = special.get(MALGANIS)
            if malganises:
                m.attack += 2*(malganises-(m.id==MALGANIS))
                m.health += 2*(malganises-(m.id==MALGANIS))
            if id == SIEGEBREAKER:
                for minion in side:
                    if minion.isDemon() and minion is not m:
                        minion.attack += 1
            elif id == MALGANIS:
                for minion in side:
                    if minion.isDemon() and minion is not m:
                        minion.attack += 2
                        minion.health += 2

    # remove aura when an aura minion dies
    def removeAura(self, m, side):
        # https://youtu.be/Nnb9vudJKig?t=970
        id = m.id
        if id == WARLEADER:
            for minion in side:
                if minion.isMurloc():
                    minion.attack -= 2
        elif id == SOUTHSEACAPTAIN:
            for minion in side:
                if minion.isPirate():
                    minion.attack -= 1
                    # if minion.health > base health of minion.id:
                    #     minion.health -= 1
        elif id == SIEGEBREAKER:
            for minion in side:
                if minion.isDemon():
                    minion.attack -= 1
        elif id == MALGANIS:
            for minion in side:
                if minion.isDemon():
                    minion.attack -= 2
                    # if minion.health - 1 > base health of minion.id:
                    #     minion.health -= 2

        otherside = self.getOtherSide(side)
        if (self.getSpecial(side).get(MURKEYE) or self.getSpecial(otherside).get(MURKEYE)) and m.isMurloc():
            for minion in side:
                if minion.id == MURKEYE:
                    minion.attack -= 1
            for minion in otherside:
                if minion.id == MURKEYE:
                    minion.attack -= 1


        # Murloc Warleader, Southsea Captain, Siegebreaker, Mal'Ganis (passive aura)
        # Old Murk-Eye (passive aura, applied to self)

    # immediately ends if the board is empty
    # choose starting player (most minions, o.w. random)
    # red whelps trigger
    # starting player attacks, check deaths, next player attacks, check deaths, repeat
    # return win, loss, tie (p1 perspective) when board is empty on one or both sides
    def battle(self):
        if not self.p1 or not self.p2:
            return 1 if self.p1 else -1 if self.p2 else 0

        player = None
        if len(self.p1) > len(self.p2):
            player = 1
        elif len(self.p2) > len(self.p1):
            player = 2
        else:
            player = 1 if random() < .5 else 2


        ## START OF COMBAT ##
        turn = 0
        died1 = False
        died2 = False
        side1dragons = sum([1 for m in self.p1 if m.isDragon()])
        side2dragons = sum([1 for m in self.p2 if m.isDragon()])
        for i in range(max(len(self.p1), len(self.p2))):
            if len(self.p1) > i:
                self.m1 = self.p1[i]
                if self.m1.id == REDWHELP and self.m1.alive:
                    index, enemy = choice([(ind, m) for ind, m in enumerate(self.p2) if m.alive])
                    self.handleMinionDamage(enemy, self.p2, self.m1, side1dragons)
                    if self.singleCheckForDeath(enemy):
                        self.singleDeathrattle(self.p2, index)

            if len(self.p2) > i:
                self.m2 = self.p2[i]
                if self.m2.id == REDWHELP and self.m2.alive:
                    index, enemy = choice([(ind, m) for ind, m in enumerate(self.p1) if m.alive])
                    self.handleMinionDamage(enemy, self.p1, self.m2, side2dragons)
                    if self.singleCheckForDeath(enemy):
                        self.singleDeathrattle(self.p1, index)

        def sideFight(side):
            m = self.getAttacker(side)
            if turn > 0:
                m = m.next
            while not m.alive:
                m = m.next
            tmp = m
            while tmp.attack == 0:
                tmp = tmp.next
                if tmp is m:
                    tmp = None
                    break
            if tmp:
                m = tmp
                self.strike(m, side)

        self.m1 = self.p1[0]
        self.m2 = self.p2[0]
        while self.p1 and self.p2:
            # ensure that minions on both sides can attack
            if not [m for m in self.p1 if m.attack > 0] and \
               not [m for m in self.p2 if m.attack > 0]:
                break
            if debugfight:
                print()
                print(" > " if (player + turn)%2 == 0 else "   ", end = "")
                [print(m, end=" ") for m in self.p2]
                print()
                print(" > " if (player + turn)%2 == 1 else "   ", end = "")
                [print(m, end=" ") for m in self.p1]
                print()
            if (player + turn)%2 == 1:
                if turn > 1:
                    self.m1 = self.m1.next
                sideFight(self.p1)
            else:
                if turn > 1:
                    self.m2 = self.m2.next
                sideFight(self.p2)
            turn += 1
            if debugfight:
                print('\n')

        if self.p1 and not self.p2:   # win
            return 1
        elif self.p2 and not self.p1: # loss
            return -1
        else:                         # tie
            return 0


    # minion goes on the offensive and attacks an enemy
    # windfury attacks -- zapp/pirate
    # choose target -- zapp special
    # whenever triggers -- pirates
    # damage dealth to enemy
    # cleave -- hydra/foereaper
    # after/overkill triggers -- macaw/cannon/herald/etc.
    # resolve deathrattles
    # enemy minion retaliates on the defensive
    def strike(self, m1, side, n=1): # nth attack
        otherside = self.getOtherSide(side)
        if not [m for m in otherside if m.alive]:
            return

        special1 = self.getSpecial(side)
        special2 = self.getSpecial(otherside)

        ## WINDFURY ##
        if m1.hasAttr(WINDFURY) or m1.hasAttr(MEGAWINDFURY):
            if n < 2 and not m1.hasAttr(MEGAWINDFURY):
                self.strike(m1, side, n+1)
            elif n < 4:
                self.strike(m1, side, n+1)
            if not m1.alive or not [m for m in otherside if m.alive]:
                return

        ## CHOOSE TARGET ##
        if m1.id == ZAPP:
            m2 = min(otherside, key=lambda m: (m.attack, random()))
        else:
            taunts = [m for m in otherside if m.hasAttr(TAUNT) and m.alive]
            if taunts:
                m2 = choice(taunts)
            else:
                m2 = choice([m for m in otherside if m.alive])

        ## WHENEVER ATTACK ##
        if m1.id == GLYPHGUARDIAN:
            m1.attack *= 2

        if m1.isPirate():
            ripsnarls = special1.setdefault(RIPSNARLCAPTAIN, 0) - (m1.id == RIPSNARLCAPTAIN)
            if ripsnarls:
                m1.attack += 2 * ripsnarls
                m1.health += 2 * ripsnarls

            elizas = special1.setdefault(ELIZA, 0)
            if elizas:
                for m in side:
                    m.attack += 1 * elizas
                    m.health += 1 * elizas

        ## DEAL DAMAGE ##
        self.handleMinionDamage(m2, otherside, m1, m1.attack)

        ## ADJACENT DAMAGE ##
        if m1.id == HYDRA or m1.id == FOEREAPER:
            if m2.prev is not otherside[-1]:
                self.handleMinionDamage(m2.prev, otherside, m1, m1.attack)
            if m2.next is not otherside[0]:
                self.handleMinionDamage(m2.next, otherside, m1, m1.attack)

        ## RETALIATE DAMAGE ##
        self.handleMinionDamage(m1, side, m2, m2.attack)

        ## AFTER ATTACK (1) ##
        if m1.id == MACAW:
            deathrattles = [(i, m) for i, m in enumerate(side) if m.hasDeathrattle()]
            if deathrattles:
                i, m = choice([(i, m) for i, m in enumerate(side) if m.hasDeathrattle()])
                self.resolveDeathrattle(side, i, m)

        ## CHECK DEATH ##
        died1 = self.checkForDeath(side)
        died2 = self.checkForDeath(otherside)

        ## AFTER ATTACK (2) ##
        ## OVERKILL ##
        if m2.health < 0:
            if m1.id == HERALDOFFLAME:
                continueOverkill = True
                m = otherside[0]
                while not m.alive:
                    m = m.next
                    if m is otherside[0]:
                        continueOverkill = False
                        break
                while continueOverkill:
                    continueOverkill = False
                    self.handleMinionDamage(m, otherside, m1, 3)
                    while m.health < 0:
                        continueOverkill = True
                        m = m.next
                        if m is otherside[0]:
                            continueOverkill = False
                            break

                ## CHECK DEATH ##
                died1 |= self.checkForDeath(side)
                died2 |= self.checkForDeath(otherside)

            elif m1.id == BEASTOVERKILL:
                addMinion(IDtoBASEMINION[OVERKILLRUNT].copy(), m1, side.index(m1), side)
            elif m1.id == WINDFURYOVERKILL:
                for minion in side:
                    if minion.isPirate() and minion is not m1:
                        minion.attack += 2
                        minion.health += 2
            elif m1.id == WILDFIRE:
                m2adj = []
                if m2.prev is not otherside[-1]:
                    m2adj.append(m2.prev)
                if m2.next is not otherside[0]:
                    m2adj.append(m2.next)
                if m2adj:
                    self.handleMinionDamage(choice(m2adj), otherside, m1, -m2.health)
                    ## CHECK DEATH ##
                    died1 |= self.checkForDeath(side)
                    died2 |= self.checkForDeath(otherside)



        # https://www.twitch.tv/videos/661763628 1:18:40 (cannon, scallywag, deathrattles)
        # bronze warden has health buffed from -1 to 0
        # monstrous macaw has health buffed from 0 to 1 and lives
        # scallywag attack, cannons trigger, rat/spawn/scalllywag "die" and deleted,
        #   scallywag deathrattle -> attack, cannons trigger, spawn deathrattle,
        #   rats deathrattle, bronze warden "dies" and respawns
        # if m1.prev and m1.prev.id == ARCANECANNON and m1.prev.alive and side[-1] is not m1.prev:
        #     damage = 2
        #     enemies = [m for m in otherside if m.alive]
        #     if enemies:
        #         enemy = choice(enemies)
        #         self.handleMinionDamage(enemy, otherside, m1.prev, damage)
        #         died2 |= self.singleCheckForDeath(enemy)

        # if m1.next and m1.next.id == ARCANECANNON and m1.next.alive and side[0] is not m1.next:
        #     damage = 2
        #     enemies = [m for m in otherside if m.alive]
        #     if enemies:
        #         enemy = choice(enemies)
        #         self.handleMinionDamage(enemy, otherside, m1.next, damage)
        #         died2 |= self.singleCheckForDeath(enemy)

        ## RESOLVE DEATHRATTLE ##
        while died1 or died2:
            while died1:
                self.loopDeathrattle(side)
                died1 = self.checkForDeath(side)
                died2 |= self.checkForDeath(otherside)
            while died2:
                self.loopDeathrattle(otherside)
                died2 = self.checkForDeath(otherside)
                died1 = self.checkForDeath(side)

        ## WHENEVER SURVIVE ##
        if m2.id == OGRE and m2.alive:
            self.strike(m2, otherside)

    def strikeSkyPirate(self, m1, side): # nth attack
        otherside = self.getOtherSide(side)
        if not [m for m in otherside if m.alive]:
            return

        special1 = self.getSpecial(side)
        special2 = self.getSpecial(otherside)

        taunts = [m for m in otherside if m.hasAttr(TAUNT) and m.alive]
        if taunts:
            m2 = choice(taunts)
        else:
            m2 = choice([m for m in otherside if m.alive])

        if m1.isPirate():
            ripsnarls = special1.setdefault(RIPSNARLCAPTAIN, 0) - (m1.id == RIPSNARLCAPTAIN)
            if ripsnarls:
                m1.attack += 2 * ripsnarls
                m1.health += 2 * ripsnarls

            elizas = special1.setdefault(ELIZA, 0)
            if elizas:
                for m in side:
                    m.attack += 1 * elizas
                    m.health += 1 * elizas

        ## DEAL DAMAGE ##
        self.handleMinionDamage(m2, otherside, m1, m1.attack)

        ## RETALIATE DAMAGE ##
        self.handleMinionDamage(m1, side, m2, m2.attack)

        ## CHECK DEATH ##
        died1 = self.checkForDeath(side)
        died2 = self.checkForDeath(otherside)

        # if m1.prev and m1.prev.id == ARCANECANNON and m1.prev.alive and side[-1] is not m1.prev:
        #     damage = 2
        #     enemies = [m for m in otherside if m.alive]
        #     if enemies:
        #         enemy = choice(enemies)
        #         self.handleMinionDamage(enemy, otherside, m1.prev, damage)
        #         died2 |= self.singleCheckForDeath(enemy)

        # if m1.next and m1.next.id == ARCANECANNON and m1.next.alive and side[0] is not m1.next:
        #     damage = 2
        #     enemies = [m for m in otherside if m.alive]
        #     if enemies:
        #         enemy = choice(enemies)
        #         self.handleMinionDamage(enemy, otherside, m1.next, damage)
        #         died2 |= self.singleCheckForDeath(enemy)

        ## WHENEVER SURVIVE ##
        if m2.id == OGRE and m2.alive:
            self.strike(m2, otherside)

        return died1 or died2


    def handleMinionDamage(self, m, side, source, damage):
        if damage == 0:
            return
        m.lasthitby = source
        if m.hasAttr(DIVINE):
            m.removeAttr(DIVINE)
        else:
            m.health -= damage
            if len(side) < Board.MAXsize:
                if m.id == IMPGANGBOSS:
                    addMinion(IDtoBASEMINION[IMP].copy(), m, side.index(m), side)
                elif m.id == SECURITYROVER:
                    addMinion(IDtoBASEMINION[GUARDBOT].copy(), m, side.index(m), side)
                elif m.id == IMPMAMA:
                    newdemon = IDtoBASEMINION[choice(demon_minions)].copy()
                    newdemon.setAttr(TAUNT)
                    addMinion(newdemon, m, side.index(m), side)
            if source.hasAttr(POISON):
                m.die()

    def singleCheckForDeath(self, m):
        if not m.alive or m.health <= 0:
            m.die()
            return True
        return False

    def checkForDeath(self, side):
        died = False
        for m in side:
            if not m.alive or m.health <= 0:
                m.die()
                died = True
        return died

    def loopDeathrattle(self, side):
        i = 0
        while i < len(side):
            m = side[i]
            if not m.alive:
                self.singleDeathrattle(side, i)
            else:
                i += 1

    def singleDeathrattle(self, side, i):
        m = side[i]
        if m.alive:
            return

        special = self.getSpecial(side)

        del side[i]

        ## HANDLE POINTERS ##
        m.prev.next = m.next
        m.next.prev = m.prev

        ## DEATH TRIGGERS ##
        if m.id in speciallist:
            special[m.id] -= 1
        if special.get(HYENA) and m.isBeast():
            for minion in side:
                if minion.id == HYENA and minion.alive:
                    minion.attack += 2
                    minion.health += 1
        if special.get(JUNKBOT) and m.isMech():
            for minion in side:
                if minion.id == JUNKBOT and m.alive:
                    minion.attack += 2
                    minion.health += 2
        if special.get(JUGGLER) and m.isDemon():
            otherside = self.getOtherSide(side)
            for minion in side:
                if minion.id == JUGGLER and minion.alive:
                    enemiesalive = [n for n in otherside if n.alive]
                    if enemiesalive:
                        n2 = choice(enemiesalive)
                        self.handleMinionDamage(n2, otherside, minion, 3)


        otherside = self.getOtherSide(side)
        otherspecial = self.getSpecial(otherside)
        if otherspecial.get(WAXRIDER) and m.lasthitby and m.lasthitby.isDragon():
            for minion in otherside:
                if minion.id == WAXRIDER:
                    minion.attack += 2
                    minion.health += 2

        ## REMOVE AURAS ##
        self.removeAura(m, side)

        ## GRAVEYARD LOGISTICS ##
        if m.isMech():
            graveyard = self.getGraveyard(side)
            if len(graveyard) < 4:
                graveyard.append(m.id)

        ## DEATHRATTLES ##
        if m.hasDeathrattle():
            self.resolveDeathrattle(side, i, m)

        ## REBORN ##
        if m.hasAttr(REBORN):
            mnew = IDtoBASEMINION[m.id].copy()
            mnew.removeAttr(REBORN)
            mnew.health = 1
            addMinion(mnew, m, i, side)

    # minion deathrattles handled
    def resolveDeathrattle(self, side, i, m):
        def addM(mnew):
            return addMinion(mnew, m, i, side)

        def deathrattleBaron():
            nonlocal m
            if id == FIENDISH:
                alive = [n for n in side if n.alive]
                if alive:
                    minion = choice(alive)
                    minion.attack += m.attack
            elif id == SCALLYWAG:
                addM(IDtoBASEMINION[SKYPIRATE].copy())
            elif id == SELFLESSHERO:
                alive = [n for n in side if n.alive]
                if alive:
                    minion = choice(alive)
                    minion.setAttr(DIVINE)
            elif id == KINDLYGRANDMOTHER:
                addM(IDtoBASEMINION[BIGBADWOLF].copy())
            elif id == UNSTABLEGHOUL:
                damage = 1
                for minion in self.p1:
                    self.handleMinionDamage(minion, self.p1, m, 1)
                for minion in self.p2:
                    self.handleMinionDamage(minion, self.p2, m, 1)
            elif id == HARVESTGOLEM:
                addM(IDtoBASEMINION[DMGGOLEM].copy())
            elif id == IMPRISONER:
                addM(IDtoBASEMINION[IMP].copy())
            elif id == KABOOM:
                damage = 4
                alive = [n for n in otherside if n.alive]
                if alive:
                    minion = choice(alive)
                    self.handleMinionDamage(minion, otherside, m, damage)
            elif id == RATPACK:
                for _ in range(m.attack):
                    if not addM(IDtoBASEMINION[RAT].copy()):
                        break
            elif id == SPAWN:
                for minion in side:
                    if minion.alive:
                        minion.attack += 1
                        minion.health += 1
            elif id == INFESTEDWOLF:
                for _ in range(2):
                    if not addM(IDtoBASEMINION[SPIDER].copy()):
                        break
            elif id == PILOTEDSHREDDER:
                addM(IDtoBASEMINION[choice(twocost_minions)].copy())
            elif id == REPLICATINGMENACE:
                for _ in range(3):
                    if not addM(IDtoBASEMINION[MICROBOT].copy()):
                        break
            elif id == EGG:
                addM(IDtoBASEMINION[ROBOSAUR].copy())
            elif id == GHASTCOILER:
                for _ in range(2):
                    if not addM(IDtoBASEMINION[choice(deathrattle_minions)].copy()):
                        break
            elif id == BAGURGLE:
                for minion in side:
                    if minion.isMurloc() and minion.alive and minion.id != BAGURGLE:
                        minion.attack += 2
                        minion.health += 2
            elif id == NADINA:
                for minion in side:
                    if minion.isDragon() and minion.alive:
                        minion.setAttr(DIVINE)
            elif id == HIGHMANE:
                for _ in range(2):
                    if not addM(IDtoBASEMINION[HIGHMANEHYENA].copy()):
                        break
            elif id == THEBEAST:
                addMinion(IDtoBASEMINION[FINKLEEINHORN].copy(), None, None, otherside)
            elif id == BOAT:
                for _ in range(3):
                    if not addM(IDtoBASEMINION[choice(pirate_minions)].copy()):
                        break
            elif id == GOLDRINN:
                for minion in side:
                    if minion.isBeast() and minion.alive:
                        minion.attack += 5
                        minion.health += 5
            elif id == SNEEDS:
                addM(IDtoBASEMINION[choice(legendary_minions)].copy())
            elif id == KANGORS:
                for mid in self.getGraveyard(side)[:2]:
                    if not addM(IDtoBASEMINION[mid].copy()):
                        break
            elif id == VOIDLORD:
                for _ in range(3):
                    if not addM(IDtoBASEMINION[VOIDWALKER].copy()):
                        break
            elif id == DJINNI:
                addM(IDtoBASEMINION[choice(elemental_minions)].copy())
            else:
                pass

            if m.hasAttr(REPLICATING1):
                for _ in range(3):
                    if not addM(IDtoBASEMINION[MICROBOT].copy()):
                        break
            if m.hasAttr(REPLICATING2):
                for _ in range(6):
                    if not addM(IDtoBASEMINION[MICROBOT].copy()):
                        break
            if m.hasAttr(REPLICATING3):
                for _ in range(9):
                    if not addM(IDtoBASEMINION[MICROBOT].copy()):
                        break

        id = m.id
        otherside = self.getOtherSide(side)

        special = self.getSpecial(side)
        baron = special.get(BARON)
        if not baron:
            deathrattleBaron()
        else:
            for _ in range(2):
                deathrattleBaron()


    def getSide(self, player):
        return self.p1 if player == 1 else self.p2

    def getOtherSide(self, side):
        return self.p2 if side is self.p1 else self.p1

    def getSpecial(self, side):
        return self.p1special if side is self.p1 else self.p2special

    def getAttacker(self, side):
        return self.m1 if side is self.p1 else self.m2

    def getGraveyard(self, side):
        return self.g1 if side is self.p1 else self.g2

def addMinion(mnew, m, i, side): # new, old minions
    def addMinionKh(mnew):
        if len(side) >= Board.MAXsize:
            return False

        nonlocal m

        if not side: # finkle or board is empty
            side.insert(0, mnew)
            mnew.prev = mnew
            mnew.next = mnew
            if m:
                m.next = mnew
                m.prev = mnew
            else:
                board.getAttacker(side).next = mnew
        else:
            if mnew.id == FINKLEEINHORN:
                m = side[-1]
                side.insert(len(side), mnew)
            else:
                m = m
                side.insert(i+m.alive, mnew)

            mnew.next = m.next
            if m.alive:
                mnew.prev = m
            else:
                mnew.prev = m.prev

            mnew.prev.next = mnew
            mnew.next.prev = mnew

            m.next = mnew # commenting this fixes scallywag+arcanecannong+khadgar/baron but messes up battle

        if mnew.isBeast():
            packleaders = special.setdefault(PACKLEADER, 0)
            if packleaders:
                mnew.attack += 2*packleaders
            mamas = special.setdefault(MAMABEAR, 0)
            if mamas:
                mnew.attack += 4*mamas
                mnew.health += 4*mamas

        elif mnew.isMech():
            if special.get(DEFLECTOBOT):
                for minion in side:
                    if minion.id == DEFLECTOBOT:
                        minion.attack += 1
                        minion.setAttr(DIVINE)

        elif mnew.isMurloc():
            if special.get(TIDECALLER):
                for minion in side:
                    if minion.id == TIDECALLER:
                        minion.attack += 1

        if mnew.id in speciallist:
            special.setdefault(mnew.id, 0)
            special[mnew.id] += 1

        board.applyAura(mnew, side)
        if mnew.id == SKYPIRATE:
            board.strike(mnew, side)

        #     if board.strikeSkyPirate(mnew, side):
        #         otherside = board.getOtherSide(side)
        #         died1 = died2 = True
        #         while died1 or died2:
        #             while died1:
        #                 board.loopDeathrattle(side)
        #                 died1 = board.checkForDeath(side)
        #                 died2 |= board.checkForDeath(otherside)
        #             while died2:
        #                 board.loopDeathrattle(otherside)
        #                 died2 = board.checkForDeath(otherside)
        #                 died1 = board.checkForDeath(side)
        return True

    special = board.getSpecial(side)
    for ind in range(pow(2, special.setdefault(KHADGAR, 0))):
        if ind == 0:
            if not addMinionKh(mnew):
                return False
        else:
            if not addMinionKh(mnew.copy()):
                return False
    return True

def summon(id):
    return IDtoBASEMINION[id].copy()

def winRatios(trials):
    wins = trials.count(1) / len(trials)
    ties = trials.count(0) / len(trials)
    losses = trials.count(-1) / len(trials)
    return wins, ties, losses

def run(p1, p2):
    start = time.time()
    seed(10)
    trials = []
    for _ in range(numTrials):
        Minion.mid = 0
        # p1 = [(SCALLYWAG, 4, 2), HOGGARR, (SALTYLOOTER, 9, 8), ELIZA, (BRONZEWARDEN, 9, 6), LIGHTFANG, (RATPACK, 9, 7)]#, BARON]

        # p3 = [MACAW, SPORE, EGG, EGG, EGG, EGG, DJINNI]
        # p4 = [EGG, DJINNI, EGG, MACAW, EGG, EGG, SPORE]

        global board
        board = Board(p1, p2)

        result = board.battle()
        trials.append(result)

    if debugfight:
        print("   ", end="")
        [print(m, end=" ") for m in board.p2]
        print()
        print("   ", end="")
        [print(m, end=" ") for m in board.p1]
        print()
        print("You win!" if result == 1 else "Opponent wins" if result == -1 else "Tie")
        print()

    win, tie, lose = winRatios(trials)
    print("Win {0:.1%}\t".format(win), "Tie {0:.1%}\t".format(tie), "Loss {0:.1%}\t".format(lose), f"out of {numTrials} games")
    end = time.time()
    print(f"This took {end - start} seconds")
    return {
        "win"  : win,
        "tie"  : tie,
        "lose" : lose
    }

def simulate(data):
    s1, s2 = data
    p1 = [(s[0], s[1], s[2]) for s in s1]
    p2 = [(s[0], s[1], s[2]) for s in s2]
    return run(p1, p2)

def getUnits():
    with open('HS/bgminions.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return {row['id']:row for row in reader}

board = None