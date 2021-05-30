from pandac.PandaModules import *
import SafeZoneLoader
import TFPlayground

class TFSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = TFPlayground.TFPlayground
        self.musicFile = 'phase_6/audio/bgm/TF_SZ_1.ogg'
        self.activityMusicFile = 'phase_3.5/audio/bgm/TC_SZ_activity.ogg' # Temporary
        self.dnaFile = 'phase_6/dna/toonfest_sz.xml'
        self.safeZoneStorageDNAFile = 'phase_6/dna/storage_TF.xml'
