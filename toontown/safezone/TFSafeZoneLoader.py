# Embedded file name: toontown.safezone.TFSafeZoneLoader
from pandac.PandaModules import *
from SafeZoneLoader import SafeZoneLoader
import TFPlayground
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.effects import Bubbles
from toontown.toon import NPCToons
from toontown.election import ElectionGlobals
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from direct.distributed.DistributedObject import DistributedObject
from toontown.election import DistributedFlippyStand
from toontown.election import ToonfestCog
from otp.nametag.NametagConstants import *
from toontown.pets import Pet
from toontown.pets import PetDNA

class TFSafeZoneLoader(SafeZoneLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = TFPlayground.TFPlayground
        self.musicFile = 'phase_6/audio/bgm/TF_SZ_1.ogg'
        self.activityMusicFile = 'phase_3.5/audio/bgm/TC_SZ_activity.ogg'
        self.dnaFile = 'phase_6/dna/toonfest_sz.xml'
        self.safeZoneStorageDNAFile = 'phase_6/dna/storage_TF.xml'
        self.restockSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_SOS_pies_restock.ogg')
        self.flippyBlatherSequence = Sequence()
        self.fluffy = None
        return

    def load(self):
        SafeZoneLoader.load(self)
        self.flippy = NPCToons.createLocalNPC(2001)
        self.flippy.reparentTo(render)
        self.flippy.setPickable(0)
        self.flippy.setPos(188, -260, 11.187)
        self.flippy.setH(108.411)
        self.flippy.initializeBodyCollisions('toon')
        self.flippy.addActive()
        self.flippy.startBlink()
        self.flippyBlatherSequence = Sequence(Wait(10), Func(self.flippy.setChatAbsolute, 'Welcome Toons, far and wide!', CFSpeech | CFTimeout), Func(self.flippy.play, 'wave'), Func(self.flippy.loop, 'neutral'), Wait(5), Func(self.flippy.setChatAbsolute, "It's been an amazing year at Toontown, and we're glad you could join us!", CFSpeech | CFTimeout), Wait(8), Func(self.flippy.setChatAbsolute, "Oh, don't mind the little guy back there. That's my new pet, Fluffy.", CFSpeech | CFTimeout), Wait(8), Func(self.flippy.setChatAbsolute, "He's a real rascal, but he already has the Cog-fighting down to a science!", CFSpeech | CFTimeout), Wait(8), Func(self.flippy.setChatAbsolute, 'Doctor Surlee says he\'s some sort of creature called a "Doodle". Funny name, right?', CFSpeech | CFTimeout), Wait(8), Func(self.flippy.setChatAbsolute, 'Anyway, what are you waiting for?', CFSpeech | CFTimeout), Wait(8), Func(self.flippy.setChatAbsolute, 'Grab some pies, catch some fish, and go for a spin. ToonFest is in full swing!', CFSpeech | CFTimeout))
        self.flippyBlatherSequence.loop()
        self.fluffy = Pet.Pet()
        self.fluffy.addActive()
        self.flippy.startBlink()
        self.fluffy.setDNA(PetDNA.getRandomPetDNA())
        self.fluffy.setName('Fluffy')
        self.fluffy.setPickable(0)
        self.fluffy.reparentTo(render)
        self.fluffy.setPos(191, -263, 11.382)
        self.fluffy.setH(829)
        self.fluffy.enterNeutralHappy()
        self.fluffy.initializeBodyCollisions('pet')
        try:
            self.towerGeom = self.geom.find('**/toonfest_tower_DNARoot')
            self.base1 = self.towerGeom.find('**/base1')
            self.base2 = self.towerGeom.find('**/base2')
            self.base3 = self.towerGeom.find('**/base3')
        except:
            self.notify.warning('Something messed up loading the tower bases!')

    def unload(self):
        SafeZoneLoader.unload(self)
        self.flippyBlatherSequence.finish()
        if self.flippy:
            self.flippy.stopBlink()
            self.flippy.removeActive()
            self.flippy.cleanup()
            self.flippy.removeNode()
        if self.fluffy:
            self.fluffy.stopBlink()
            self.fluffy.removeActive()
            self.fluffy.enterOff()
            self.fluffy.cleanup()
            self.fluffy.removeNode()

    def enter(self, requestStatus):
        SafeZoneLoader.enter(self, requestStatus)

    def exit(self):
        SafeZoneLoader.exit(self)