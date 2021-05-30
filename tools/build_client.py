#!/usr/bin/python2.7 -OO
# Yes, the above flags matter: We have to do this on 2.7 and we have to optimize.

from modulefinder import ModuleFinder
import os
import sys
import subprocess
import imp
import marshal
import tempfile
import shutil
import atexit
import argparse
import zipfile

# These are to get the dependency walker to find and binarize them, as they would not be found by it normally
EXTRA_MODULES = (
  'encodings.ascii',
  'encodings.latin_1',
  'encodings.hex_codec',
  '_strptime',

  # Animated props and things loaded through DNA...
  'toontown.hood.MailboxZeroAnimatedProp',
  'toontown.hood.PetShopFishAnimatedProp',
  'toontown.hood.TrashcanOneAnimatedProp',
  'toontown.hood.SleepingHydrantAnimatedProp',
  'toontown.hood.HQPeriscopeAnimatedProp',
  'toontown.hood.HydrantTwoAnimatedProp',
  'toontown.hood.HydrantZeroAnimatedProp',
  'toontown.hood.AnimatedProp',
  'toontown.hood.HQTelescopeAnimatedProp',
  'toontown.hood.MailboxTwoAnimatedProp',
  'toontown.hood.GenericAnimatedProp',
  'toontown.hood.GenericAnimatedBuilding',
  'toontown.hood.FishAnimatedProp',
  'toontown.hood.HydrantOneAnimatedProp',
  'toontown.hood.TrashcanZeroAnimatedProp',
  'toontown.hood.TrashcanTwoAnimatedProp',
  'toontown.hood.InteractiveAnimatedProp',
  'toontown.hood.MailboxOneAnimatedProp',
  'toontown.hood.ZeroAnimatedProp',
  'toontown.hood.HydrantInteractiveProp',
  'toontown.hood.MailboxInteractiveProp',
  'toontown.hood.TrashcanInteractiveProp',
)

root = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

def determineVersion(cwd):
    git = subprocess.Popen(['git', 'rev-parse', 'HEAD'],
                           stdout=subprocess.PIPE,
                           cwd=cwd).stdout.read()
    git = git.strip()[:7]
    return 'ttr-alpha-g%s' % (git,)

class ClientBuilder(object):
    MAINMODULE = 'toontown.toonbase.MiraiStart'

    def __init__(self, directory, version=None, language='english'):
        self.directory = directory
        self.version = version or determineVersion(self.directory)
        self.language = language.lower()

        self.dcfiles = [os.path.join(directory, 'config/otp.dc'),
                        os.path.join(directory, 'config/toon.dc')]
        self.modules = {}
        self.path_overrides = {}

        self.config_file = os.path.join(self.directory, 'config/public_client.prc')

        self.mf = ModuleFinder(sys.path+[self.directory])
        from panda3d.direct import DCFile
        self.dcf = DCFile()

    def should_exclude(self, modname):
        # The NonRepeatableRandomSource modules are imported by the dc file explicitly,
        # so we have to allow them.
        if 'NonRepeatableRandomSource' in modname:
            return False

        if modname.endswith('AI'):
            return True
        if modname.endswith('UD'):
            return True
        if modname.endswith('.ServiceStart'):
            return True

    def find_excludes(self):
        for path, dirs, files in os.walk(self.directory):
            for filename in files:
                filepath = os.path.join(path, filename)
                filepath = os.path.relpath(filepath, self.directory)
                if not filepath.endswith('.py'): continue
                filepath = filepath[:-3]
                modname = filepath.replace(os.path.sep, '.')
                if modname.endswith('.__init__'): modname = modname[:-9]
                if self.should_exclude(modname):
                    self.mf.excludes.append(modname)

    def find_dcfiles(self):
        for path, dirs, files in os.walk(self.directory):
            for filename in files:
                filepath = os.path.join(path, filename)
                if filename.endswith('.dc'):
                    self.dcfiles.append(filepath)

    def create_miraidata(self):
        # Create a temporary _miraidata.py and throw it on the path somewhere...

        # First, we need the minified DC file contents:
        from panda3d.core import StringStream
        dcStream = StringStream()
        self.dcf.write(dcStream, True)
        dcData = dcStream.getData()

        # Next we need config files...
        configData = []
        with open(self.config_file) as f:
            fd = f.read()
            fd = fd.replace('SERVER_VERSION_HERE', self.version)
            fd = fd.replace('LANGUAGE_HERE', self.language)
            configData.append(fd)

        md = 'CONFIG = %r\nDC = %r\n' % (configData, dcData)

        # Now we use tempfile to dump md:
        td = tempfile.mkdtemp()
        with open(os.path.join(td, '_miraidata.py'), 'w') as f:
            f.write(md)

        self.mf.path.append(td)

        atexit.register(shutil.rmtree, td)

    def include_dcimports(self):
        for m in xrange(self.dcf.getNumImportModules()):
            modparts = self.dcf.getImportModule(m).split('/')
            mods = [modparts[0]]
            if 'OV' in modparts[1:]:
                mods.append(modparts[0]+'OV')
            for mod in mods:
                self.mf.import_hook(mod)
                for s in xrange(self.dcf.getNumImportSymbols(m)):
                    symparts = self.dcf.getImportSymbol(m,s).split('/')
                    syms = [symparts[0]]
                    if 'OV' in symparts[1:]:
                        syms.append(symparts[0]+'OV')
                    for sym in syms:
                        try:
                            self.mf.import_hook('%s.%s' % (mod,sym))
                        except ImportError:
                            pass

    def build_modules(self):
        for modname, mod in self.mf.modules.items():
            if modname in self.path_overrides:
                modfile = self.path_overrides[modname]
            else:
                modfile = mod.__file__
            if not (modfile and modfile.endswith('.py')): continue
            is_package = modfile.endswith('__init__.py')
            with open(modfile, 'r') as f:
                code = compile(f.read(), modname, 'exec')
            self.modules[modname] = (is_package, code)

    def load_modules(self):
        #self.find_dcfiles()
        self.find_excludes()

        from panda3d.core import Filename
        for dc in self.dcfiles:
            self.dcf.read(Filename.fromOsSpecific(dc))

        self.create_miraidata()

        self.mf.import_hook(self.MAINMODULE)
        for module in EXTRA_MODULES:
            self.mf.import_hook(module)
        if self.language.lower() != "english":
            self.mf.import_hook('otp.otpbase.OTPLocalizer_%s' % self.language.capitalize())
            self.mf.import_hook('otp.otpbase.OTPLocalizer_%sProperty' % self.language.capitalize())
            self.mf.import_hook('toontown.toonbase.TTLocalizer_%s' % self.language.capitalize())
            self.mf.import_hook('toontown.toonbase.TTLocalizer_%s' % self.language.capitalize())
        self.modules['__main__'] = (False, compile('import %s' % self.MAINMODULE,
                                                   '__main__', 'exec'))

        self.include_dcimports()

        self.build_modules()


    def write_zip(self, outfile):
        zip = zipfile.ZipFile(outfile, 'w')
        for modname, (is_package, code) in self.modules.items():
            mcode = imp.get_magic() + '\x00'*4 + marshal.dumps(code)
            name = modname.replace('.','/')
            if is_package:
                name += '/__init__'
            name += '.pyo'
            zip.writestr(name, mcode)
        zip.close()

    def write_list(self, outfile):
        with open(outfile,'w') as out:
            for modname in sorted(self.modules.keys()):
                is_package, code = self.modules[modname]
                out.write('%s%s\n' % (modname, ' [PKG]' if is_package else ''))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mirai-path', help='The path to the Mirai repository root.')
    parser.add_argument('--format', default='mirai', choices=['mirai', 'zip', 'list'],
                        help='The output format to produce. Choices are:\n'
                        'mirai -- a Mirai package\n'
                        'zip -- a zip file of pyos\n'
                        'list -- a plaintext list of included modules')
    parser.add_argument('--version', help='Override the version string packed into the built blob.')
    parser.add_argument('--language', default='english', help='The language to make the blob with.')
    parser.add_argument('output', help='The filename of the built file to output.')

    args = parser.parse_args()
    if args.mirai_path:
        sys.path.append(args.mirai_path)
        p3d_path = os.path.join(args.mirai_path, 'panda3d-1.8.1')
        sys.path.insert(0, p3d_path)

    cb = ClientBuilder(root, args.version, args.language)

    if args.mirai_path:
        cb.mf.import_hook('direct').__path__ = [os.path.join(p3d_path, 'direct/src')]
        cb.path_overrides['pandac.extension_native_helpers'] = \
            os.path.join(p3d_path, 'direct/src/extensions_native/extension_native_helpers.py')

    cb.load_modules()

    if args.format == 'zip':
        cb.write_zip(args.output)
    elif args.format == 'list':
        cb.write_list(args.output)
    elif args.format == 'mirai':
        try:
            from mirai.packager import MiraiPackager
        except ImportError:
            sys.stderr.write('Could not import Mirai! Check your --mirai-path\n')
            sys.exit(1)

        mp = MiraiPackager(args.output)
        mp.write_modules(cb.modules)
        mp.close()
