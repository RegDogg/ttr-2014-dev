from pandac.PandaModules import *
from toontown.toonbase import ToontownGlobals
import Playground
from toontown.toonbase import TTLocalizer
from direct.fsm import State
from toontown.safezone import PicnicBasket
from direct.task.Task import Task
from toontown.toon import NPCToons

class TFPlayground(Playground.Playground):

    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)
        self.parentFSM = parentFSM
        self.flippy = None

    def load(self):
        Playground.Playground.load(self)

    def unload(self):
        Playground.Playground.unload(self)

    def enter(self, requestStatus):
        Playground.Playground.enter(self, requestStatus)

    def exit(self):
        Playground.Playground.exit(self)
        self.loader.hood.setNoFog()
