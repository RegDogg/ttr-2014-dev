from SZHoodAI import SZHoodAI
from toontown.hood.HoodAI import *
from toontown.toonbase import ToontownGlobals
# TODO: Tables
#from toontown.safezone.DistributedPicnicBasketAI import DistributedPicnicBasketAI
#from toontown.safezone.DistributedPicnicTableAI import DistributedPicnicTableAI

class TFHoodAI(SZHoodAI):
    HOOD = ToontownGlobals.Toonfest
    
    def createZone(self):
        # TODO: Treasure Spawn Points if any
        # SZHoodAI.createTreasurePlanner(self)

        self.spawnObjects()
