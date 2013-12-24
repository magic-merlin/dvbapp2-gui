#Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/magicBoot/plugin.py
from Screens.Screen import Screen
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Screens.Console import Console
from Screens.ChoiceBox import ChoiceBox
from enigma import eTimer
from Components.Button import Button
from Components.ActionMap import ActionMap, NumberActionMap
from Components.GUIComponent import *
from Components.MenuList import MenuList
from Components.Input import Input
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.Pixmap import Pixmap, MultiPixmap
from Components.config import *
from Components.ConfigList import ConfigListScreen
from os import listdir
import os
from Tools.Directories import fileExists
from os import system, listdir, chdir, getcwd, rename as os_rename, remove as os_remove
from os.path import dirname, isdir
magicBootInstallation_Skin = '\n\t\t<screen name="magicBootInstallation" position="center,center" size="902,380" title="magicBoot - Installation" >\n\t\t      <widget name="label1" position="10,10" size="840,30" zPosition="1" halign="center" font="Regular;25" backgroundColor="#9f1313" transparent="1"/>\n\t\t      <widget name="label2" position="10,80" size="840,290" zPosition="1" halign="center" font="Regular;20" backgroundColor="#9f1313" transparent="1"/>\n\t\t      <widget name="config" position="10,160" size="840,200" scrollbarMode="showOnDemand"/>\n\t\t      <ePixmap pixmap="skin_default/buttons/red.png" position="10,290" size="140,40" alphatest="on" />\n\t\t      <ePixmap pixmap="skin_default/buttons/green.png" position="300,290" size="140,40" alphatest="on" />\n\t\t      <ePixmap pixmap="skin_default/buttons/blue.png" position="600,290" size="140,40" alphatest="on" />\n\t\t      <widget name="key_red" position="10,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t      <widget name="key_green" position="300,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t      <widget name="key_blue" position="600,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t</screen>'
magicBootImageChoose_Skin = '\n\t\t<screen name="magicBootImageChoose" position="center,center" size="902,380" title="magicBoot - Menu" >\n\t\t      <widget name="label1" position="10,10" size="840,30" zPosition="1" halign="center" font="Regular;25" backgroundColor="#9f1313" transparent="1"/>\n\t\t      <widget name="label2" position="10,80" size="840,290" zPosition="1" halign="center" font="Regular;20" backgroundColor="#9f1313" transparent="1"/>\n\t\t      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/magicBoot/dev_hdd.png" position="30,20" size="80,80" alphatest="on" />\n\t\t      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/magicBoot/dev_usb.png" position="780,20" size="80,80" alphatest="on" />\n\t\t      <widget name="config" position="10,160" size="840,200" scrollbarMode="showOnDemand"/>\n\t\t      <ePixmap pixmap="skin_default/buttons/red.png" position="10,340" size="140,40" alphatest="on" />\n\t\t      <ePixmap pixmap="skin_default/buttons/green.png" position="260,340" size="140,40" alphatest="on" />\n\t\t      <ePixmap pixmap="skin_default/buttons/yellow.png" position="520,340" size="140,40" alphatest="on" />\n\t\t      <ePixmap pixmap="skin_default/buttons/blue.png" position="750,340" size="140,40" alphatest="on" />\n\t\t      <widget name="key_red" position="10,340" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t      <widget name="key_green" position="260,340" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t      <widget name="key_yellow" position="520,340" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t      <widget name="key_blue" position="750,340" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t</screen>'
magicBootImageInstall_Skin = '\n\t\t    <screen name="magicBootImageInstall" position="center,center" size="570,350" title="magicBoot - Image Installation" >\n\t\t\t      <widget name="config" position="10,10" size="550,220" scrollbarMode="showOnDemand" />\n\t\t\t      <ePixmap pixmap="skin_default/buttons/red.png" position="10,290" size="140,40" alphatest="on" />\n\t\t\t      <ePixmap pixmap="skin_default/buttons/green.png" position="300,290" size="140,40" alphatest="on" />\n\t\t\t      <widget name="key_red" position="10,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t\t      <widget name="key_green" position="300,290" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t    </screen>'

class magicBootInstallation(Screen):

    def __init__(self, session):
        self.skin = magicBootInstallation_Skin
        Screen.__init__(self, session)
        self.list = []
        self['config'] = MenuList(self.list)
        self['key_red'] = Label(_('Install'))
        self['key_green'] = Label(_('Cancel'))
        self['key_blue'] = Label(_('Devices Panel'))
        self['label1'] = Label(_('Welcome to magicBoot 2.0 MultiBoot Plugin installation.'))
        self['label2'] = Label(_('Here is the list of mounted devices in Your STB\n\nPlease choose a device where You would like to install magicBoot:'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'red': self.install,
         'green': self.close,
         'back': self.close,
         'blue': self.devpanel})
        self.updateList()

    def updateList(self):
        mycf, myusb, myusb2, myusb3, mysd, myhdd = ('', '', '', '', '', '')
        myoptions = []
        if fileExists('/proc/mounts'):
            fileExists('/proc/mounts')
            f = open('/proc/mounts', 'r')
            for line in f.readlines():
                if line.find('/media/cf') != -1:
                    mycf = '/media/cf/'
                    continue
                if line.find('/media/usb') != -1:
                    myusb = '/media/usb/'
                    continue
                if line.find('/media/usb2') != -1:
                    myusb2 = '/media/usb2/'
                    continue
                if line.find('/media/usb3') != -1:
                    myusb3 = '/media/usb3/'
                    continue
                if line.find('/media/card') != -1:
                    mysd = '/media/card/'
                    continue
                if line.find('/hdd') != -1:
                    myhdd = '/media/hdd/'
                    continue

            f.close()
        else:
            self['label2'].setText(_('Sorry it seems that there are not Linux formatted devices mounted on your STB. To install magicBoot you need a Linux formatted part1 device. Click on the blue button to open magic Devices Panel'))
            fileExists('/proc/mounts')
        if mycf:
            self.list.append(mycf)
        else:
            mycf
        if myusb:
            self.list.append(myusb)
        else:
            myusb
        if myusb2:
            self.list.append(myusb2)
        else:
            myusb2
        if myusb3:
            self.list.append(myusb3)
        else:
            myusb3
        if mysd:
            mysd
            self.list.append(mysd)
        else:
            mysd
        if myhdd:
            myhdd
            self.list.append(myhdd)
        else:
            myhdd
        self['config'].setList(self.list)

    def devpanel(self):
        try:
            from magic.magic_devices_menu import EGDeviceManager
            self.session.open(EGDeviceManager)
        except:
            self.session.open(MessageBox, _('You are not running magic Image. You must mount devices Your self.'), MessageBox.TYPE_INFO)

    def myclose(self):
        self.close()

    def myclose2(self, message):
        self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        self.close()

    def checkReadWriteDir(self, configele):
        import os.path
        import Components.Harddisk
        supported_filesystems = frozenset(('ext4', 'ext3', 'ext2', 'nfs'))
        candidates = []
        mounts = Components.Harddisk.getProcMounts()
        for partition in Components.Harddisk.harddiskmanager.getMountedPartitions(False, mounts):
            if partition.filesystem(mounts) in supported_filesystems:
                candidates.append((partition.description, partition.mountpoint))

        if candidates:
            locations = []
            for validdevice in candidates:
                locations.append(validdevice[1])

            if Components.Harddisk.findMountPoint(os.path.realpath(configele)) + '/' in locations or Components.Harddisk.findMountPoint(os.path.realpath(configele)) in locations:
                if fileExists(configele, 'w'):
                    return True
                else:
                    dir = configele
                    self.session.open(MessageBox, _('The directory %s is not writable.\nMake sure you select a writable directory instead.') % dir, type=MessageBox.TYPE_ERROR)
                    return False
            else:
                dir = configele
                self.session.open(MessageBox, _('The directory %s is not a EXT2, EXT3, EXT4 or NFS partition.\nMake sure you select a valid partition type.') % dir, type=MessageBox.TYPE_ERROR)
                return False
        else:
            dir = configele
            self.session.open(MessageBox, _('The directory %s is not a EXT2, EXT3, EXT4 or NFS partition.\nMake sure you select a valid partition type.') % dir, type=MessageBox.TYPE_ERROR)
            return False

    def install(self):
        check = False
        if fileExists('/proc/mounts'):
            fileExists('/proc/mounts')
            f = open('/proc/mounts', 'r')
            for line in f.readlines():
                if line.find('/media/cf') != -1:
                    check = True
                    continue
                if line.find('/media/usb') != -1:
                    check = True
                    continue
                if line.find('/media/usb2') != -1:
                    check = True
                    continue
                if line.find('/media/usb3') != -1:
                    check = True
                    continue
                if line.find('/media/card') != -1:
                    check = True
                    continue
                if line.find('/hdd') != -1:
                    check = True
                    continue

            f.close()
        else:
            fileExists('/proc/mounts')
        if check == False:
            self.session.open(MessageBox, _('Sorry, there is not any connected devices in your STB.\nPlease connect HDD or USB to install magic Multiboot!'), MessageBox.TYPE_INFO)
        else:
            fileExists('/boot/dummy')
            self.mysel = self['config'].getCurrent()
            if self.checkReadWriteDir(self.mysel):
                message = _('Do You really want to install magicBoot in:\n ') + self.mysel + '?'
                ybox = self.session.openWithCallback(self.install2, MessageBox, message, MessageBox.TYPE_YESNO)
                ybox.setTitle(_('Install Confirmation'))
            else:
                self.close()

    def install2(self, yesno):
        if yesno:
            cmd2 = 'mkdir /media/magicboot;mount ' + self.mysel + ' /media/magicboot'
            system(cmd2)
            cmd = 'mkdir ' + self.mysel + 'magicBootI;mkdir ' + self.mysel + 'magicBootUpload'
            system(cmd)
            system('cp /usr/lib/enigma2/python/Plugins/Extensions/magicBoot/bin/magicinit /sbin/magicinit')
            system('chmod 777 /sbin/magicinit;chmod 777 /sbin/init;ln -sfn /sbin/magicinit /sbin/init')
            out2 = open('/media/magicboot/magicBootI/.magicboot', 'w')
            out2.write('Flash')
            out2.close()
            out = open('/usr/lib/enigma2/python/Plugins/Extensions/magicBoot/.magicboot_location', 'w')
            out.write(self.mysel)
            out.close()
            system('cp /usr/lib/enigma2/python/Plugins/Extensions/magicBoot/.magicboot_location /etc/magic/')
            self.myclose2(_('magicBoot has been installed succesfully!'))
        else:
            self.session.open(MessageBox, _('Installation aborted !'), MessageBox.TYPE_INFO)


class magicBootImageChoose(Screen):

    def __init__(self, session):
        self.skin = magicBootImageChoose_Skin
        Screen.__init__(self, session)
        self.list = []
        self['config'] = MenuList(self.list)
        self['key_red'] = Label(_('Boot Image'))
        self['key_green'] = Label(_('Install Image'))
        self['key_yellow'] = Label(_('Remove Image '))
        self['key_blue'] = Label(_('Close'))
        self['label1'] = Label(_('Welcome to magicBoot 2.0 MultiBoot Plugin.'))
        self['label2'] = Label(_('Here is the list of installed images in Your STB\n\nPlease choose an image to boot.'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'red': self.boot,
         'green': self.install,
         'yellow': self.remove,
         'blue': self.myclose,
         'back': self.close})
        self.updateList()

    def updateList(self):
        f = open('/usr/lib/enigma2/python/Plugins/Extensions/magicBoot/.magicboot_location', 'r')
        mypath = f.readline().strip()
        f.close()
        f2 = open('/media/magicboot/magicBootI/.magicboot', 'r')
        mypath2 = f2.readline().strip()
        f2.close()
        self.list.append('Flash')
        self['label2'].setText(_('magicBoot is running from:  ') + mypath + _('\n magicBoot is running image:  ') + mypath2)
        mypath = mypath + 'magicBootI'
        myimages = listdir(mypath)
        for fil in myimages:
            if os.path.isdir(os.path.join(mypath, fil)):
                self.list.append(fil)

        self['config'].setList(self.list)

    def devpanel(self):
        from magic.magic_devices_menu import EGDeviceManager
        self.session.open(EGDeviceManager)

    def myclose(self):
        self.close()

    def myclose2(self, message):
        self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        self.close()

    def boot(self):
        self.mysel = self['config'].getCurrent()
        if self.mysel:
            out = open('/media/magicboot/magicBootI/.magicboot', 'w')
            out.write(self.mysel)
            out.close()
            system('rm /tmp/.magicreboot')
            message = _('Are you sure you want to Boot Image:\n') + self.mysel + ' now ?'
            ybox = self.session.openWithCallback(self.boot2, MessageBox, message, MessageBox.TYPE_YESNO)
            ybox.setTitle(_('Boot Confirmation'))
        else:
            self.mysel

    def boot2(self, yesno):
        if yesno:
            system('touch /tmp/.magicreboot')
            system('reboot -f')
        else:
            system('touch /tmp/.magicreboot')
            self.session.open(MessageBox, _('Image will be booted on the next STB boot!'), MessageBox.TYPE_INFO)

    def remove(self):
        self.mysel = self['config'].getCurrent()
        if self.mysel:
            f = open('/media/magicboot/magicBootI/.magicboot', 'r')
            mypath = f.readline().strip()
            f.close()
            try:
                if mypath == self.mysel:
                    self.session.open(MessageBox, _('Sorry you cannot delete the image currently booted from.'), MessageBox.TYPE_INFO, 4)
                if self.mysel == 'Flash':
                    self.session.open(MessageBox, _('Sorry you cannot delete Flash image'), MessageBox.TYPE_INFO, 4)
                else:
                    out = open('/media/magicboot/magicBootI/.magicboot', 'w')
                    out.write('Flash')
                    out.close()
                    message = _('Are you sure you want to delete Image:\n ') + self.mysel + ' now ?'
                    ybox = self.session.openWithCallback(self.remove2, MessageBox, message, MessageBox.TYPE_YESNO)
                    ybox.setTitle(_('Delete Confirmation'))
            except:
                print 'no image to remove'

        else:
            self.mysel

    def up(self):
        self.list = []
        self['config'].setList(self.list)
        self.updateList()

    def up2(self):
        try:
            self.list = []
            self['config'].setList(self.list)
            self.updateList()
        except:
            print ' '

    def remove2(self, yesno):
        if yesno:
            cmd = "echo -e '\n\nmagicBoot deleting image..... '"
            cmd1 = 'rm -r /media/magicboot/magicBootI/' + self.mysel
            self.session.openWithCallback(self.up, Console, _('magicBoot: Deleting Image'), [cmd, cmd1])
        else:
            self.session.open(MessageBox, _('Removing canceled!'), MessageBox.TYPE_INFO)

    def install(self):
        images = False
        myimages = listdir('/media/magicboot/magicBootUpload')
        print myimages
        for fil in myimages:
            if fil.endswith('.zip') or fil.endswith('.nfi'):
                images = True
                break
            else:
                images = False

        if images == True:
            self.session.openWithCallback(self.up2, magicBootImageInstall)
        else:
            mess = _('The /media/magicboot/magicBootUpload directory is EMPTY!\n\nPlease upload one of the file:\nXtrend ET Series images\n- ZIP format image e.x\nOpenPLi-2.1-beta-et9x00-20120304_usb.zip\n\nDreambox Series images\n- NFI format image e.x\nPeterPan-Neverlan.v2.2-DM800HDse.nfi\n')
            self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)


class magicBootImageInstall(Screen, ConfigListScreen):

    def __init__(self, session):
        self.skin = magicBootImageInstall_Skin
        Screen.__init__(self, session)
        self.list = []
        ConfigListScreen.__init__(self, self.list, on_change=self.schanged)
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions', 'CiSelectionActions'], {'cancel': self.cancel,
         'red': self.imageInstall,
         'green': self.cancel}, -2)
        self['key_red'] = Label(_('Install'))
        self['key_green'] = Label(_('Cancel'))
        fn = 'NewImage'
        sourcelist = []
        for fn in listdir('/media/magicboot/magicBootUpload'):
            if fn.find('.zip') != -1:
                fn = fn.replace('.zip', '')
                sourcelist.append((fn, fn))
                continue
            if fn.find('.nfi') != -1:
                fn = fn.replace('.nfi', '')
                sourcelist.append((fn, fn))
                continue

        if len(sourcelist) == 0:
            sourcelist = [('None', 'None')]
        self.source = NoSave(ConfigSelection(choices=sourcelist))
        self.target = NoSave(ConfigText(fixed_size=False))
        self.sett = NoSave(ConfigYesNo(default=True))
        self.target.value = ''
        self.curselimage = ''
        res = getConfigListEntry(_('Source Image file'), self.source)
        self.list.append(res)
        res = getConfigListEntry(_('Image Name'), self.target)
        self.list.append(res)
        res = getConfigListEntry(_('Copy Settings to the new Image'), self.sett)
        self.list.append(res)

    def schanged(self):
        if self.curselimage != self.source.value:
            self.target.value = self.source.value
            self.curselimage = self.source.value

    def imageInstall(self):
        pluginpath = '/usr/lib/enigma2/python/Plugins/Extensions/magicBoot'
        myerror = ''
        source = self.source.value.replace(' ', '')
        target = self.target.value.replace(' ', '')
        for fn in listdir('/media/magicboot/magicBootI'):
            if fn == target:
                myerror = _('Sorry, an Image with the name ') + target + _(' is already installed.\n Please try another name.')
                continue

        if source == 'None':
            myerror = _('You have to select one Image to install.\nPlease, upload your zip file in the folder: /media/magicboot/magicBootUpload and select the image to install.')
        if target == '':
            myerror = _('You have to provide a name for the new Image.')
        if target == 'Flash':
            myerror = _('Sorry this name is reserved. Choose another name for the new Image.')
        if len(target) > 35:
            myerror = _('Sorry the name of the new Image is too long.')
        if myerror:
            myerror
            self.session.open(MessageBox, myerror, MessageBox.TYPE_INFO)
        else:
            myerror
            message = "echo -e '\n\n"
            message += _('magicBoot will stop all your STB activity now to install the new image.')
            message += _('Your STB will freeze during the installation process.')
            message += _('Please: DO NOT reboot your STB and turn off the power.\n')
            message += _('The new image will be installed and auto booted in few minutes.')
            message += "'"
            cmd1 = 'python ' + pluginpath + '/ex_init.pyo'
            cmd = '%s %s %s %s' % (cmd1,
             source,
             target.lower().replace('.', '_'),
             str(self.sett.value))
            print cmd
            self.session.open(Console, _('magicBoot: Install new image'), [message, cmd])

    def cancel(self):
        self.close()


from magic.magic_tools import checkkernel

def main(session, **kwargs):
    m = checkkernel()
    if m == 1:
        try:
            f = open('/usr/lib/enigma2/python/Plugins/Extensions/magicBoot/.magicboot_location', 'r')
            mypath = f.readline().strip()
            f.close()
            cmd = 'mount ' + mypath + ' /media/magicboot'
            system(cmd)
            f = open('/proc/mounts', 'r')
            for line in f.readlines():
                if line.find('/media/magicboot') != -1:
                    line = line[0:9]
                    break

            cmd = 'mount ' + line + ' ' + mypath
            system(cmd)
            cmd = 'mount ' + mypath + ' /media/magicboot'
            system(cmd)
        except:
            pass

        if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/magicBoot/.magicboot_location'):
            session.open(magicBootImageChoose)
        else:
            session.open(magicBootInstallation)
    else:
        session.open(MessageBox, _('Sorry: Wrong image in flash found. You have to install in flash magic Image'), MessageBox.TYPE_INFO, 3)


def menu(menuid, **kwargs):
    if menuid == 'magic':
        return [(_('magic MultiBoot'),
          main,
          'magic_boot',
          45)]
    return []


from Plugins.Plugin import PluginDescriptor

def Plugins(**kwargs):
    return [PluginDescriptor(name='magicBoot', description=_('E2 Light Multiboot'), icon='plugin_icon.png', where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main)]