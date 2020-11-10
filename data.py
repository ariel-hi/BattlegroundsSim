class BaseMinion:
    def __init__(self, id, name, attack, health, tribe, *args):
        self.id = id
        self.name = name
        self.attack = attack
        self.health = health
        self.tribe = tribe
        self.args = args

    def copy(self):
        return Minion(self.id, self.attack, self.health, *self.args)


class Minion:
    mid = 0
    def __init__(self, id, attack, health, *args):
        self.id = id
        self.mid = Minion.mid
        Minion.mid += 1

        self.lasthitby = None
        self.attributes = set(args)

        bm = IDtoBASEMINION[id]
        self.name = bm.name
        self.tribe = bm.tribe

        self.attack = attack
        self.health = health

        self.prev = None
        self.next = None

        self.alive = True

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, health):
        self.__health = health
        if debughealth:
            if self.lasthitby:
                print(f'{self} : last hit by {self.lasthitby}')
            else:
                print(f'{self} (summoned now)')

    def setAttr(self, attr):
        self.attributes.add(attr)

    def hasAttr(self, attr):
        return attr in self.attributes

    def hasDeathrattle(self):
        return self.hasAttr(DEATHRATTLE) or self.hasAttr(REPLICATING1) or \
               self.hasAttr(REPLICATING2) or self.hasAttr(REPLICATING3)

    def removeAttr(self, attr):
        if not self.hasAttr(attr):
            return False
        if attr == DIVINE:
            m = self
            if m.id == BOLVAR:
                m.attack += 2
            elif m.id == DRAKONID:
                m.attack += 2
                m.health += 2
            m = m.next
            while m is not self:
                if m.id == BOLVAR:
                    m.attack += 2
                elif m.id == DRAKONID:
                    m.attack += 2
                    m.health += 2
                m = m.next
        return self.attributes.remove(attr)

    def die(self):
        self.alive = False
        # if self.prev:
        #     self.prev.next = self.next
        # if self.next:
        #     self.next.prev = self.prev

    def copy(self):
        return Minion(self.id, self.attack, self.health, *self.attributes)

    def __str__(self):
        s = f'{self.name} {self.attack}/{self.health}'
        if self.hasAttr(TAUNT):
            s = '[' + s + ']'
        if self.hasAttr(DIVINE):
            s = '(' + s + ')'
        return f'({self.mid}) ' + s


    def isBeast(self):
        return self.tribe == BEAST or self.tribe == ALL

    def isDemon(self):
        return self.tribe == DEMON or self.tribe == ALL

    def isDemon(self):
        return self.tribe == DEMON or self.tribe == ALL

    def isMurloc(self):
        return self.tribe == MURLOC or self.tribe == ALL

    def isPirate(self):
        return self.tribe == PIRATE or self.tribe == ALL

    def isDragon(self):
        return self.tribe == DRAGON or self.tribe == ALL

    def isMech(self):
        return self.tribe == MECH or self.tribe == ALL

    def isElemental(self):
        return self.tribe == ELEMENTAL or self.tribe == ALL

debughealth = debugfight = False
numTrials = 100

DEATHRATTLE  = 'deathrattle'
DIVINE       = 'divine'
TAUNT        = 'taunt'
POISON       = 'poisonous'
WINDFURY     = 'windfury'
MEGAWINDFURY = 'mega-windfury'
REBORN       = 'reborn'
REPLICATING1 = 'replicating1'
REPLICATING2 = 'replicating2'
REPLICATING3 = 'replicating3'

BEAST     = "beast"
DEMON     = "demon"
MURLOC    = "murloc"
PIRATE    = "pirate"
DRAGON    = "dragon"
MECH      = "mech"
ELEMENTAL = "elemental"
ALL       = "all"

ALLEYCAT           = 40426
FIENDISH           = 56112
TIDECALLER         = 475
DIVINETAUNT        = 42467
SELFLESSHERO       = 38740
TOXFIN             = 52277
KHADGAR            = 52502
KINDLYGRANDMOTHER  = 39481
MICROMUMMY         = 53445
TIDEHUNTER         = 976
ROCKPOOLHUNTER     = 41245
HYENA              = 1281
UNSTABLEGHOUL      = 1808
HOMUNCULUS         = 43121
BRANN              = 2949
HYDRA              = 43358
COLDLIGHT          = 453
REDWHELP           = 59968
REROLLELEMENTAL    = 64042
SCALLYWAG          = 61061
ZERUS              = 57742
WRATHWEAVER        = 59670
DRAGONTAUNT        = 60628
MICROMACHINE       = 60055
BUFFELEMENTAL      = 64297
TAVERNPIRATE       = 61055
FREEPIRATE         = 61049
GLYPHGUARDIAN      = 61029
HARVESTGOLEM       = 778
IMPGANGBOSS        = 2288
IRONSENSEI         = 1992
KABOOM             = 49279
METALTOOTHLEAPER   = 2016
WARLEADER          = 1063
RATPACK            = 40428
SOUTHSEACAPTAIN    = 680
SPAWN              = 38797
ANNOYOMODULE       = 48993
BARON              = 1915
CROWDFAVORITE      = 2518
CRYSTALWEAVER      = 40391
ARGUS              = 763
FELFINNAVIGATOR    = 56393
HOUNDMASTER        = 1003
INFESTEDWOLF       = 38734
MURKEYE            = 736
REPLICATINGMENACE  = 48536
IMPRISONER         = 59937
MUG                = 63435
MOLTENROCK         = 64296
MACAW              = 62230
NAZRETHIM          = 59186
PACKLEADER         = 59940
PRIMALFIN          = 60028
SAUROLISK          = 62162
SELLEMENTAL        = 64038
JUGGLER            = 59660
WAXRIDER           = 60559
PIRATECANNONEER    = 61053
BRONZEWARDEN       = 60558
DIVINEELEMENTAL    = 64054
SPORE              = 65031
DEFLECTOBOT        = 61930
RAG                = 63624
PARTYELEMENTAL     = 64056
PILOTEDSHREDDER    = 60048
RIPSNARLCAPTAIN    = 61056
SALTYLOOTER        = 62734
SCREWJANK          = 2023
TAUNTBUFF          = 43022
BOLVAR             = 45392
COBALT             = 42442
FLOATINGWATCHER    = 2068
JUNKBOT	           = 2074
EGG                = 49169
VIRMEN             = 40641
MAEXXNA            = 1791
HIGHMANE           = 1261
SECURITYROVER      = 48100
THEBEAST           = 962
BEASTOVERKILL      = 49973
SIEGEBREAKER       = 54835
STASISELEMENTAL    = 64069
STEWARDDRAGON      = 60621
GOLDGRUBBER        = 61066
HANGRY             = 60552
HERALDOFFLAME      = 60498
JUG                = 63487
SOUTHSEASTRONGARM  = 61048
TAVERNTEMPEST      = 64077
HOGGARR            = 61989
DRAKONID           = 61072
ELIZA              = 61047
GHASTCOILER        = 59687
BAGURGLE           = 60247
LIGHTFANG          = 59707
MAJORDOMO          = 63630
NADINA             = 60629
TWILIGHTEMISSARY   = 60626
WILDFIRE           = 64189
OGRE               = 61060
MUROZOND           = 60637
NATPAGLE           = 61046
NOMI               = 63626
WINDFURYOVERKILL   = 62458
BOAT               = 62232
AMALGADON          = 61444
DEMONHEALTH        = 59714
FOEREAPER          = 2081
MALGANIS           = 1986
VOIDLORD           = 46056
DJINNI             = 64062
GOLDRINN           = 59955
IMPMAMA            = 61028
KALECGOS           = 60630
GARR               = 64081
MAMABEAR           = 60036
RAZORGORE          = 60561
SNEEDS             = 59682
ZAPP               = 60040
KANGORS            = 59935

DROPLET            = 64040

TABBYCAT           = 40425
SKYPIRATE          = 62213
BIGBADWOLF         = 39161
MURLOCSCOUT        = 1078
DMGGOLEM           = 471
IMP                = 2779
RAT                = 41839
SPIDER             = 38735
MICROBOT           = 48842
ROBOSAUR           = 49168
HIGHMANEHYENA      = 1624
GUARDBOT           = 49278
FINKLEEINHORN      = 1006
OVERKILLRUNT       = 50359
VOIDWALKER         = 48

speciallist = {RIPSNARLCAPTAIN, ELIZA, \
               HYENA, JUGGLER, JUNKBOT, WAXRIDER, \
               KHADGAR, PACKLEADER, MAMABEAR, DEFLECTOBOT, TIDECALLER, \
             # DRAKONID, BOLVAR, \
               WARLEADER, SOUTHSEACAPTAIN, MURKEYE, SIEGEBREAKER, MALGANIS, \
               BARON}

attack_triggers = {RIPSNARLCAPTAIN, ELIZA}
death_triggers = {HYENA, JUGGLER, JUNKBOT, WAXRIDER}
summon_triggers = {KHADGAR, PACKLEADER, MAMABEAR, DEFLECTOBOT, TIDECALLER}
divine_tirggers = {DRAKONID, BOLVAR}
passive_auras = {WARLEADER, SOUTHSEACAPTAIN, MURKEYE, SIEGEBREAKER, MALGANIS}
misc = {BARON}



IDtoBASEMINION = {
    ALLEYCAT:BaseMinion(ALLEYCAT, "Alleycat", 1, 1, BEAST),
    FIENDISH:BaseMinion(FIENDISH, "Fiendish Servant", 2, 1, DEMON, DEATHRATTLE),
    TIDECALLER:BaseMinion(TIDECALLER, "Murloc Tidecaller", 1, 2, MURLOC),
    REDWHELP:BaseMinion(REDWHELP, "Red Whelp", 1, 2, DRAGON),
    DIVINETAUNT:BaseMinion(DIVINETAUNT, "Righteous Protector", 1, 1, None, DIVINE, TAUNT),
    SCALLYWAG:BaseMinion(SCALLYWAG, "Scallywag", 2, 1, PIRATE, DEATHRATTLE),
    SELFLESSHERO:BaseMinion(SELFLESSHERO, "Selfless Hero", 2, 1, None, DEATHRATTLE),
    ZERUS:BaseMinion(ZERUS, "Shifter Zerus", 1, 1, None),
    TOXFIN:BaseMinion(TOXFIN, "Toxfin", 1, 2, MURLOC),
    WRATHWEAVER:BaseMinion(WRATHWEAVER, "Wrath Weaver", 1, 1, None),
    DRAGONTAUNT:BaseMinion(DRAGONTAUNT, "Dragonspawn Lieutenant", 2, 3, DRAGON, TAUNT),
    KHADGAR:BaseMinion(KHADGAR, "Khadgar", 2, 2, None),
    KINDLYGRANDMOTHER:BaseMinion(KINDLYGRANDMOTHER, "Kindly Grandmother", 1, 1, BEAST, DEATHRATTLE),
    MICROMACHINE:BaseMinion(MICROMACHINE, "Micro Machine", 1, 2, MECH),
    TIDEHUNTER:BaseMinion(TIDEHUNTER, "Murloc Tidehunter", 2, 1, MURLOC),
    ROCKPOOLHUNTER:BaseMinion(ROCKPOOLHUNTER, "Rockpool Hunter", 2, 3, MURLOC),
    HYENA:BaseMinion(HYENA, "Scavenging Hyena", 2, 2, BEAST),
    UNSTABLEGHOUL:BaseMinion(UNSTABLEGHOUL, "Unstable Ghoul", 1, 3, None, TAUNT, DEATHRATTLE),
    HOMUNCULUS:BaseMinion(HOMUNCULUS, "Vulgar Homunculus", 2, 4, DEMON, TAUNT),
    BRANN:BaseMinion(BRANN, "Brann Bronzebeard", 2, 4, None),
    HYDRA:BaseMinion(HYDRA, "Cave Hydra", 2, 4, BEAST),
    COLDLIGHT:BaseMinion(COLDLIGHT, "Coldlight Seer", 2, 3, MURLOC),
    TAVERNPIRATE:BaseMinion(TAVERNPIRATE, "Deck Swabbie", 2, 2, PIRATE),
    FREEPIRATE:BaseMinion(FREEPIRATE, "Freedealing Gambler", 3, 3, PIRATE),
    GLYPHGUARDIAN:BaseMinion(GLYPHGUARDIAN, "Glyph Guardian", 2, 4, DRAGON),
    HARVESTGOLEM:BaseMinion(HARVESTGOLEM, "Harvest Golem", 2, 3, MECH, DEATHRATTLE),
    IMPGANGBOSS:BaseMinion(IMPGANGBOSS, "Imp Gang Boss", 2, 4, DEMON),
    IMPRISONER:BaseMinion(IMPRISONER, "Imprisoner", 3, 3, DEMON, TAUNT, DEATHRATTLE),
    IRONSENSEI:BaseMinion(IRONSENSEI, "Iron Sensei", 2, 2, MECH),
    KABOOM:BaseMinion(KABOOM, "Kaboom Bot", 2, 2, MECH, DEATHRATTLE),
    METALTOOTHLEAPER:BaseMinion(METALTOOTHLEAPER, "Metaltooth Leaper", 3, 3, MECH),
    MACAW:BaseMinion(MACAW, "Monstrous Macaw", 4, 3, BEAST),
    WARLEADER:BaseMinion(WARLEADER, "Murloc Warleader", 3, 3, MURLOC),
    NAZRETHIM:BaseMinion(NAZRETHIM, "Nathrezim Overseer", 2, 3, DEMON),
    PACKLEADER:BaseMinion(PACKLEADER, "Pack Leader", 2, 3, None),
    PRIMALFIN:BaseMinion(PRIMALFIN, "Primalfin Lookout", 3, 2, MURLOC),
    SAUROLISK:BaseMinion(SAUROLISK, "Rabid Saurolisk", 4, 2, BEAST),
    RATPACK:BaseMinion(RATPACK, "Rat Pack", 2, 2, BEAST, DEATHRATTLE),
    JUGGLER:BaseMinion(JUGGLER, "Soul Juggler", 3, 3, None),
    SOUTHSEACAPTAIN:BaseMinion(SOUTHSEACAPTAIN, "Southsea Captain", 3, 3, PIRATE),
    SPAWN:BaseMinion(SPAWN, "Spawn of N'Zoth", 2, 2, None, DEATHRATTLE),
    WAXRIDER:BaseMinion(WAXRIDER, "Waxrider Togwaggle", 1, 2, None),
    MUG:BaseMinion(MUG, "Menagerie Mug", 2, 2, None),
    ANNOYOMODULE:BaseMinion(ANNOYOMODULE, "Annoy-o-Module", 2, 4, MECH, DIVINE, TAUNT),
    BARON:BaseMinion(BARON, "Baron Rivendare", 1, 7, None),
    PIRATECANNONEER:BaseMinion(PIRATECANNONEER, "Bloodsail Cannoneer", 4, 3, PIRATE),
    BRONZEWARDEN:BaseMinion(BRONZEWARDEN, "Bronze Warden", 2, 1, DRAGON, DIVINE, REBORN),
    CROWDFAVORITE:BaseMinion(CROWDFAVORITE, "Crowd Favorite", 4, 4, None),
    CRYSTALWEAVER:BaseMinion(CRYSTALWEAVER, "Crystalweaver", 5, 4, None),
    ARGUS:BaseMinion(ARGUS, "Defender of Argus", 2, 3, None),
    DEFLECTOBOT:BaseMinion(DEFLECTOBOT, "Deflect-o-Bot", 3, 2, MECH, DIVINE),
    FELFINNAVIGATOR:BaseMinion(FELFINNAVIGATOR, "Felfin Navigator", 4, 4, MURLOC),
    HOUNDMASTER:BaseMinion(HOUNDMASTER, "Houndmaster", 4, 3, None),
    INFESTEDWOLF:BaseMinion(INFESTEDWOLF, "Infested Wolf", 3, 3, BEAST, DEATHRATTLE),
    MURKEYE:BaseMinion(MURKEYE, "Old Murk-Eye", 2, 4, MURLOC),
    PILOTEDSHREDDER:BaseMinion(PILOTEDSHREDDER, "Piloted Shredder", 4, 3, MECH, DEATHRATTLE),
    REPLICATINGMENACE:BaseMinion(REPLICATINGMENACE, "Replicating Menace", 3, 1, MECH, DEATHRATTLE),
    RIPSNARLCAPTAIN:BaseMinion(RIPSNARLCAPTAIN, "Ripsnarl Captain", 3, 4, PIRATE),
    SALTYLOOTER:BaseMinion(SALTYLOOTER, "Salty Looter", 4, 4, PIRATE),
    SCREWJANK:BaseMinion(SCREWJANK, "Screwjank Clunker", 2, 5, MECH),
    STEWARDDRAGON:BaseMinion(STEWARDDRAGON, "Steward of Time", 3, 4, DRAGON),
    TAUNTBUFF:BaseMinion(TAUNTBUFF, "Strongshell Scavenger", 2, 3, None),
    BOLVAR:BaseMinion(BOLVAR, "Bolvar, Fireblood", 1, 7, None, DIVINE),
    COBALT:BaseMinion(COBALT, "Cobalt Scalebane", 5, 5, None, DRAGON),
    FLOATINGWATCHER:BaseMinion(FLOATINGWATCHER, "Floating Watcher", 4, 4, DEMON),
    GOLDGRUBBER:BaseMinion(GOLDGRUBBER, "Goldgrubber", 2, 2, PIRATE),
    HANGRY:BaseMinion(HANGRY, "Hangry Dragon", 4, 4, DRAGON),
    HERALDOFFLAME:BaseMinion(HERALDOFFLAME, "Herald of Flame", 5, 6, DRAGON),
    JUNKBOT:BaseMinion(JUNKBOT, "Junkbot", 1, 5, MECH),
    EGG:BaseMinion(EGG, "Mechano-Egg", 0, 5, MECH, DEATHRATTLE),
    JUG:BaseMinion(JUG, "Menagerie Jug", 3, 3, None),
    SOUTHSEASTRONGARM:BaseMinion(SOUTHSEASTRONGARM, "Southsea Strongarm", 5, 4, PIRATE),
    VIRMEN:BaseMinion(VIRMEN, "Virmen Sensei", 4, 5, None),
    HOGGARR:BaseMinion(HOGGARR, "Cap'n Hoggarr", 6, 6, PIRATE),
    DRAKONID:BaseMinion(DRAKONID, "Drakonid Enforcer", 3, 6, DRAGON),
    ELIZA:BaseMinion(ELIZA, "Dread Admiral Eliza", 6, 7, PIRATE),
    GHASTCOILER:BaseMinion(GHASTCOILER, "Ghastcoiler", 7, 7, None, DEATHRATTLE),
    BAGURGLE:BaseMinion(BAGURGLE, "King Bagurgle", 6, 3, MURLOC, DEATHRATTLE),
    LIGHTFANG:BaseMinion(LIGHTFANG, "Lightfang Enforcer", 2, 2, None),
    MAEXXNA:BaseMinion(MAEXXNA, "Maexxna", 2, 8, BEAST, POISON),
    NADINA:BaseMinion(NADINA, "Nadina the Red", 7, 4, None),
    HIGHMANE:BaseMinion(HIGHMANE, "Savannah Highmane", 6, 5, BEAST, DEATHRATTLE),
    SECURITYROVER:BaseMinion(SECURITYROVER, "Security Rover", 2, 6, MECH),
    THEBEAST:BaseMinion(THEBEAST, "The Beast", 9, 7, BEAST, DEATHRATTLE),
    TWILIGHTEMISSARY:BaseMinion(TWILIGHTEMISSARY, "Twilight Emissary", 4, 4, DRAGON),
    OGRE:BaseMinion(OGRE, "Yo-Ho-Ogre", 2, 8, PIRATE, TAUNT),
    BEASTOVERKILL:BaseMinion(BEASTOVERKILL, "Ironhide Direhorn", 7, 7, BEAST),
    MUROZOND:BaseMinion(MUROZOND, "Murozond", 5, 5, DRAGON),
    NATPAGLE:BaseMinion(NATPAGLE, "Nat Pagle, Extreme Angler", 8, 5, PIRATE),
    WINDFURYOVERKILL:BaseMinion(WINDFURYOVERKILL, "Seabreaker Goliath", 6, 7, PIRATE, WINDFURY),
    SIEGEBREAKER:BaseMinion(SIEGEBREAKER, "Siegebreaker", 5, 8, DEMON, TAUNT),
    BOAT:BaseMinion(BOAT, "The Tide Razor", 6, 4, None, DEATHRATTLE),
    DEMONHEALTH:BaseMinion(DEMONHEALTH, "Annihilan Battlemaster", 3, 1, DEMON),
    FOEREAPER:BaseMinion(FOEREAPER, "Foe Reaper 4000", 6, 9, MECH),
    GOLDRINN:BaseMinion(GOLDRINN, "Goldrinn, the Great Wolf", 5, 5, BEAST, DEATHRATTLE),
    IMPMAMA:BaseMinion(IMPMAMA, "Imp Mama", 6, 10, DEMON),
    KALECGOS:BaseMinion(KALECGOS, "Kalecgos, Arcane Aspect", 4, 12, DRAGON),
    MAMABEAR:BaseMinion(MAMABEAR, "Mama Bear", 4, 4, BEAST),
    RAZORGORE:BaseMinion(RAZORGORE, "Razorgore, the Untamed", 2, 4, DRAGON),
    SNEEDS:BaseMinion(SNEEDS, "Sneed's Old Shredder", 5, 7, MECH, DEATHRATTLE),
    ZAPP:BaseMinion(ZAPP, "Zapp Slywick", 7, 10, None, WINDFURY),
    KANGORS:BaseMinion(KANGORS, "Kangor's Apprentice", 3, 6, None, DEATHRATTLE),
    MALGANIS:BaseMinion(MALGANIS, "Mal'Ganis", 9, 7, DEMON),
    VOIDLORD:BaseMinion(VOIDLORD, "Voidlord", 3, 9, DEMON, DEATHRATTLE),
    AMALGADON:BaseMinion(AMALGADON, "Amalgadon", 6, 6, ALL),
    MICROMUMMY:BaseMinion(MICROMUMMY, "Micro Mummy", 1, 2, MECH, REBORN),
    SELLEMENTAL:BaseMinion(SELLEMENTAL, "Sellemental", 2, 2, ELEMENTAL),
    REROLLELEMENTAL:BaseMinion(REROLLELEMENTAL, "Refreshing Anomaly", 1, 3, ELEMENTAL),
    PARTYELEMENTAL:BaseMinion(PARTYELEMENTAL, "Party Elemental", 3, 2, ELEMENTAL),
    MOLTENROCK:BaseMinion(MOLTENROCK, "Molten Rock", 2, 3, ELEMENTAL, TAUNT),
    STASISELEMENTAL:BaseMinion(STASISELEMENTAL, "Stasis Elemental", 4, 4, ELEMENTAL),
    BUFFELEMENTAL:BaseMinion(BUFFELEMENTAL, "Arcane Assistant", 3, 3, ELEMENTAL),
    DIVINEELEMENTAL:BaseMinion(DIVINEELEMENTAL, "Crackling Cyclone", 4, 1, ELEMENTAL, DIVINE, WINDFURY),
    WILDFIRE:BaseMinion(WILDFIRE, "Wildfire Elemental", 7, 3, ELEMENTAL),
    SPORE:BaseMinion(SPORE, "Deadly Spore", 1, 1, None, POISON),
    MAJORDOMO:BaseMinion(MAJORDOMO, "Majordomo Executus", 6, 3, None),
    NOMI:BaseMinion(NOMI, "Nomi, Kitchen Nightmare", 6, 3, None),
    RAG:BaseMinion(RAG, "Lil' Rag", 6, 6, ELEMENTAL),
    TAVERNTEMPEST:BaseMinion(TAVERNTEMPEST, "Tavern Tempest", 4, 4, ELEMENTAL),
    GARR:BaseMinion(GARR, "Lieutenant Garr", 8, 1, ELEMENTAL, TAUNT),
    DJINNI:BaseMinion(DJINNI, "Gentle Djinni", 4, 5, ELEMENTAL, TAUNT, DEATHRATTLE),

    DROPLET:BaseMinion(DROPLET, "Droplet", 2, 2, ELEMENTAL),

    TABBYCAT:BaseMinion(TABBYCAT, "Tabbycat", 1, 1, BEAST),
    SKYPIRATE:BaseMinion(SKYPIRATE, "Sky Pirate", 1, 1, PIRATE),
    BIGBADWOLF:BaseMinion(BIGBADWOLF, "Big Bad Wolf", 3, 2, BEAST),
    MURLOCSCOUT:BaseMinion(MURLOCSCOUT, "Murloc Scout", 1, 1, MURLOC),
    DMGGOLEM:BaseMinion(DMGGOLEM, "Damaged Golem", 2, 1, MECH),
    IMP:BaseMinion(IMP, "Imp", 1, 1, DEMON),
    RAT:BaseMinion(RAT, "Rat", 1, 1, BEAST),
    SPIDER:BaseMinion(SPIDER, "Spider", 1, 1, BEAST),
    MICROBOT:BaseMinion(MICROBOT, "Microbot", 1, 1, MECH),
    ROBOSAUR:BaseMinion(ROBOSAUR, "Robosaur", 8, 8, MECH),
    HIGHMANEHYENA:BaseMinion(HIGHMANEHYENA, "Hyena", 2, 2, BEAST),
    GUARDBOT:BaseMinion(GUARDBOT, "Guard Bot", 2, 3, MECH, TAUNT),
    FINKLEEINHORN:BaseMinion(FINKLEEINHORN, "Finkle Einhorn", 3, 3, None),
    OVERKILLRUNT:BaseMinion(OVERKILLRUNT, "Ironhide Runt", 5, 5, BEAST),
    VOIDWALKER:BaseMinion(VOIDWALKER, "Voidwalker", 1, 3, DEMON, TAUNT)
}

twocost_minions = [DRAGONTAUNT, KHADGAR, KINDLYGRANDMOTHER, MICROMACHINE,     \
                   TIDEHUNTER, ROCKPOOLHUNTER, HYENA, UNSTABLEGHOUL,          \
                   HOMUNCULUS, MICROMUMMY]

deathrattle_minions = [FIENDISH, SCALLYWAG, SELFLESSHERO,                     \
                       KINDLYGRANDMOTHER, UNSTABLEGHOUL, HARVESTGOLEM,        \
                       IMPRISONER, RATPACK, SPAWN, INFESTEDWOLF,              \
                       PILOTEDSHREDDER, REPLICATINGMENACE, EGG, BAGURGLE,     \
                       HIGHMANE, THEBEAST, BOAT, GOLDRINN, SNEEDS, KANGORS,   \
                       VOIDLORD, DJINNI]

pirate_minions = [SCALLYWAG, TAVERNPIRATE, FREEPIRATE,                        \
                  SOUTHSEACAPTAIN, PIRATECANNONEER, RIPSNARLCAPTAIN,          \
                  SALTYLOOTER, GOLDGRUBBER, SOUTHSEASTRONGARM, ELIZA,         \
                  HOGGARR, OGRE, NATPAGLE, WINDFURYOVERKILL]

demon_minions = [FIENDISH, HOMUNCULUS, IMPGANGBOSS, IMPRISONER, NAZRETHIM,    \
                 FLOATINGWATCHER, SIEGEBREAKER, DEMONHEALTH, MALGANIS, VOIDLORD]

elemental_minions = [SELLEMENTAL, REROLLELEMENTAL, PARTYELEMENTAL,            \
                     MOLTENROCK, STASISELEMENTAL, BUFFELEMENTAL,              \
                     DIVINEELEMENTAL, WILDFIRE, NOMI, RAG, TAVERNTEMPEST, GARR]

legendary_minions = [ZERUS, MURKEYE, THEBEAST, BOLVAR, BAGURGLE, MAEXXNA,     \
                     KHADGAR, BRANN, BARON, FOEREAPER, MALGANIS, GOLDRINN,    \
                     WAXRIDER, MUROZOND, RAZORGORE, KALECGOS, NADINA, NOMI,   \
                     NATPAGLE, HOGGARR, ELIZA, ZAPP, MAJORDOMO, RAG, GARR]

collectible_minions = [ALLEYCAT, FIENDISH, TIDECALLER,                        \
 REDWHELP, DIVINETAUNT, SCALLYWAG, SELFLESSHERO, ZERUS, TOXFIN, WRATHWEAVER,  \
 DRAGONTAUNT, KHADGAR, KINDLYGRANDMOTHER, MICROMACHINE, TIDEHUNTER,           \
 ROCKPOOLHUNTER, HYENA, UNSTABLEGHOUL, HOMUNCULUS, BRANN,                     \
 HYDRA, COLDLIGHT, TAVERNPIRATE, FREEPIRATE, GLYPHGUARDIAN, HARVESTGOLEM,     \
 IMPGANGBOSS, IMPRISONER, IRONSENSEI, KABOOM, METALTOOTHLEAPER, MACAW,        \
 WARLEADER, NAZRETHIM, PACKLEADER, PRIMALFIN, SAUROLISK, RATPACK, JUGGLER,    \
 SOUTHSEACAPTAIN, SPAWN, WAXRIDER, MUG, ANNOYOMODULE, BARON,                  \
 PIRATECANNONEER, BRONZEWARDEN, CROWDFAVORITE, CRYSTALWEAVER, ARGUS,          \
 DEFLECTOBOT, FELFINNAVIGATOR, HOUNDMASTER, INFESTEDWOLF, MURKEYE,            \
 PILOTEDSHREDDER, REPLICATINGMENACE, RIPSNARLCAPTAIN, SALTYLOOTER, SCREWJANK, \
 STEWARDDRAGON, TAUNTBUFF, BOLVAR, COBALT, FLOATINGWATCHER, GOLDGRUBBER,      \
 HANGRY, HERALDOFFLAME, JUNKBOT, EGG, JUG, SOUTHSEASTRONGARM,                 \
 VIRMEN, HOGGARR, DRAKONID, ELIZA, GHASTCOILER, BAGURGLE, LIGHTFANG, MAEXXNA, \
 NADINA, HIGHMANE, SECURITYROVER, THEBEAST, TWILIGHTEMISSARY, OGRE,           \
 BEASTOVERKILL, MUROZOND, NATPAGLE, WINDFURYOVERKILL, SIEGEBREAKER, BOAT,     \
 DEMONHEALTH, FOEREAPER, GOLDRINN, IMPMAMA, KALECGOS, MAMABEAR, RAZORGORE,    \
 SNEEDS, ZAPP, KANGORS, MALGANIS, VOIDLORD, AMALGADON, MICROMUMMY,            \
 SELLEMENTAL, REROLLELEMENTAL, PARTYELEMENTAL, MOLTENROCK, STASISELEMENTAL,   \
 BUFFELEMENTAL, DIVINEELEMENTAL, WILDFIRE, SPORE, MAJORDOMO, NOMI, RAG,       \
 TAVERNTEMPEST, GARR, DJINNI, DROPLET]
