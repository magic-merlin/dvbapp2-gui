#Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/magicBoot/magicboot.py
import sys
import os
import struct

def getKernelVersionString():
    try:
        return open('/proc/version', 'r').read().split(' ', 4)[2].split('-', 2)[0]
    except:
        return _('unknown')


def magicBootMainEx(source, target, installsettings):
    magichome = '/media/magicboot'
    magicroot = 'media/magicboot'
    rc = os.system('init.sysvinit 2')
    cmd = 'showiframe /usr/lib/enigma2/python/Plugins/Extensions/magicBoot/magicboot.mvi > /dev/null 2>&1'
    rc = os.system(cmd)
    to = '/media/magicboot/magicBootI/' + target
    cmd = 'rm -r %s > /dev/null 2<&1' % to
    rc = os.system(cmd)
    to = '/media/magicboot/magicBootI/' + target
    cmd = 'mkdir %s > /dev/null 2<&1' % to
    rc = os.system(cmd)
    to = '/media/magicboot/magicBootI/' + target
    cmd = 'chmod -R 0777 %s' % to
    rc = os.system(cmd)
    rc = magicBootExtract(source, target)
    cmd = 'mkdir -p %s/magicBootI/%s/media > /dev/null 2>&1' % (magichome, target)
    rc = os.system(cmd)
    cmd = 'rm %s/magicBootI/%s/%s > /dev/null 2>&1' % (magichome, target, magicroot)
    rc = os.system(cmd)
    cmd = 'rmdir %s/magicBootI/%s/%s > /dev/null 2>&1' % (magichome, target, magicroot)
    rc = os.system(cmd)
    cmd = 'mkdir -p %s/magicBootI/%s/%s > /dev/null 2>&1' % (magichome, target, magicroot)
    rc = os.system(cmd)
    cmd = 'cp /etc/network/interfaces %s/magicBootI/%s/etc/network/interfaces > /dev/null 2>&1' % (magichome, target)
    rc = os.system(cmd)
    cmd = 'cp /etc/passwd %s/magicBootI/%s/etc/passwd > /dev/null 2>&1' % (magichome, target)
    rc = os.system(cmd)
    cmd = 'cp /etc/resolv.conf %s/magicBootI/%s/etc/resolv.conf > /dev/null 2>&1' % (magichome, target)
    rc = os.system(cmd)
    cmd = 'cp /etc/wpa_supplicant.conf %s/magicBootI/%s/etc/wpa_supplicant.conf > /dev/null 2>&1' % (magichome, target)
    rc = os.system(cmd)
    if installsettings == 'True':
        cmd = 'mkdir -p %s/magicBootI/%s/etc/enigma2 > /dev/null 2>&1' % (magichome, target)
        rc = os.system(cmd)
        cmd = 'cp -f /etc/enigma2/* %s/magicBootI/%s/etc/enigma2/' % (magichome, target)
        rc = os.system(cmd)
        cmd = 'cp -f /etc/tuxbox/* %s/magicBootI/%s/etc/tuxbox/' % (magichome, target)
        rc = os.system(cmd)
    cmd = 'mkdir -p %s/magicBootI/%s/media > /dev/null 2>&1' % (magichome, target)
    rc = os.system(cmd)
    cmd = 'mkdir -p %s/magicBootI/%s/media/usb > /dev/null 2>&1' % (magichome, target)
    rc = os.system(cmd)
    filename = magichome + '/magicBootI/' + target + '/etc/fstab'
    filename2 = filename + '.tmp'
    out = open(filename2, 'w')
    f = open(filename, 'r')
    for line in f.readlines():
        if line.find('/dev/mtdblock2') != -1:
            line = '#' + line
        elif line.find('/dev/root') != -1:
            line = '#' + line
        out.write(line)

    f.close()
    out.close()
    os.rename(filename2, filename)
    tpmd = magichome + '/magicBootI/' + target + '/etc/init.d/tpmd'
    if os.path.exists(tpmd):
        os.system('rm ' + tpmd)
    filename = magichome + '/magicBootI/' + target + '/usr/lib/enigma2/python/Components/config.py'
    if os.path.exists(filename):
        filename2 = filename + '.tmp'
        out = open(filename2, 'w')
        f = open(filename, 'r')
        for line in f.readlines():
            if line.find('if file("/proc/stb/info/vumodel")') != -1:
                line = '#' + line
            elif line.find('rckeyboard_enable = True') != -1:
                line = '#' + line
            out.write(line)

        f.close()
        out.close()
        os.rename(filename2, filename)
    filename = magichome + '/magicBootI/' + target + '/usr/lib/enigma2/python/Tools/HardwareInfoVu.py'
    if os.path.exists(filename):
        filename2 = filename + '.tmp'
        out = open(filename2, 'w')
        f = open(filename, 'r')
        for line in f.readlines():
            if line.find('print "hardware detection failed"') != -1:
                line = '\t\t    HardwareInfoVu.device_name ="duo"'
            out.write(line)

        f.close()
        out.close()
        os.rename(filename2, filename)
    filename = magichome + '/magicBootI/' + target + '/etc/bhversion'
    if os.path.exists(filename):
        os.system('echo "BlackHole 1.7.1" > ' + filename)
    filename = magichome + '/magicBootI/' + target + '/etc/init.d/volatile-media.sh'
    if os.path.exists(filename):
        cmd = 'rm ' + filename
        os.system(cmd)
        cmd = 'wget -O ' + magichome + '/magicBootI/' + target + '/usr/lib/enigma2/python/RecordTimer.py http://code-ini.com/RecordTimer.py'
        os.system(cmd)
    cmd = 'mkdir ' + magichome + '/magicBootI/' + target + '/media/hdd'
    os.system(cmd)
    cmd = 'mkdir ' + magichome + '/magicBootI/' + target + '/media/usb'
    os.system(cmd)
    cmd = 'mkdir ' + magichome + '/magicBootI/' + target + '/media/usb2'
    os.system(cmd)
    cmd = 'mkdir ' + magichome + '/magicBootI/' + target + '/media/usb3'
    os.system(cmd)
    cmd = 'mkdir ' + magichome + '/magicBootI/' + target + '/media/net'
    os.system(cmd)
    mypath = magichome + '/magicBootI/' + target + '/usr/lib/opkg/info/'
    if not os.path.exists(mypath):
        mypath = magichome + '/magicBootI/' + target + '/var/lib/opkg/info/'
    for fn in os.listdir(mypath):
        if fn.find('kernel-image') != -1 and fn.find('postinst') != -1:
            filename = mypath + fn
            filename2 = filename + '.tmp'
            out = open(filename2, 'w')
            f = open(filename, 'r')
            for line in f.readlines():
                if line.find('/boot') != -1:
                    line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                out.write(line)

            if f.close():
                out.close()
                os.rename(filename2, filename)
                cmd = 'chmod -R 0755 %s' % filename
                rc = os.system(cmd)
        if fn.find('-bootlogo.postinst') != -1:
            filename = mypath + fn
            filename2 = filename + '.tmp'
            out = open(filename2, 'w')
            f = open(filename, 'r')
            for line in f.readlines():
                if line.find('/boot') != -1:
                    line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                out.write(line)

            f.close()
            out.close()
            os.rename(filename2, filename)
            cmd = 'chmod -R 0755 %s' % filename
            rc = os.system(cmd)
        if fn.find('-bootlogo.postrm') != -1:
            filename = mypath + fn
            filename2 = filename + '.tmp'
            out = open(filename2, 'w')
            f = open(filename, 'r')
            for line in f.readlines():
                if line.find('/boot') != -1:
                    line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                out.write(line)

            f.close()
            out.close()
            os.rename(filename2, filename)
            cmd = 'chmod -R 0755 %s' % filename
            rc = os.system(cmd)
        if fn.find('-bootlogo.preinst') != -1:
            filename = mypath + fn
            filename2 = filename + '.tmp'
            out = open(filename2, 'w')
            f = open(filename, 'r')
            for line in f.readlines():
                if line.find('/boot') != -1:
                    line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                out.write(line)

            f.close()
            out.close()
            os.rename(filename2, filename)
            cmd = 'chmod -R 0755 %s' % filename
            rc = os.system(cmd)
        if fn.find('-bootlogo.prerm') != -1:
            filename = mypath + fn
            filename2 = filename + '.tmp'
            out = open(filename2, 'w')
            f = open(filename, 'r')
            for line in f.readlines():
                if line.find('/boot') != -1:
                    line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                out.write(line)

            f.close()
            out.close()
            os.rename(filename2, filename)
            cmd = 'chmod -R 0755 %s' % filename
            rc = os.system(cmd)

    filename = magichome + '/magicBootI/.magicboot'
    out = open('/media/magicboot/magicBootI/.magicboot', 'w')
    out.write(target)
    out.close()
    os.system('touch /tmp/.magicreboot')
    os.system('reboot')


def magicBootExtract(source, target):
    for i in range(0, 20):
        mtdfile = '/dev/mtd' + str(i)
        if os.path.exists(mtdfile) is False:
            break

    mtd = str(i)
    if os.path.exists('/media/magicboot/ubi') is False:
        rc = os.system('mkdir /media/magicboot/ubi')
    sourcefile = '/media/magicboot/magicBootUpload/%s.zip' % source
    sourcefile2 = '/media/magicboot/magicBootUpload/%s.nfi' % source
    if os.path.exists(sourcefile2) is True:
        if sourcefile2.endswith('.nfi'):
            cmd = '/usr/lib/enigma2/python/Plugins/Extensions/magicBoot/bin/nfidump ' + sourcefile2 + ' /media/magicboot/magicBootI/' + target
            rc = os.system(cmd)
            cmd = 'rm ' + sourcefile2
            os.system(cmd)
    else:
        if os.path.exists(sourcefile) is True:
            os.chdir('/media/magicboot/magicBootUpload')
            rc = os.system('unzip ' + sourcefile)
        rc = os.system('rm ' + sourcefile)
        if os.path.exists('/media/magicboot/magicBootUpload/et9x00'):
            os.chdir('et9x00')
        if os.path.exists('/media/magicboot/magicBootUpload/et6x00'):
            os.chdir('et6x00')
        if os.path.exists('/media/magicboot/magicBootUpload/et5x00'):
            os.chdir('et5x00')
        if os.path.exists('/media/magicboot/magicBootUpload/venton-hdx'):
            os.chdir('venton-hdx')
        if os.path.exists('/media/magicboot/magicBootUpload/venton-hde'):
            os.chdir('venton-hde')
        if os.path.exists('/media/magicboot/magicBootUpload/vuplus'):
            os.chdir('vuplus')
            if os.path.exists('/media/magicboot/magicBootUpload/vuplus/duo'):
                os.chdir('duo')
                os.system('mv root_cfe_auto.jffs2 rootfs.bin')
            if os.path.exists('/media/magicboot/magicBootUpload/vuplus/ultimo'):
                os.chdir('ultimo')
                os.system('mv root_cfe_auto.jffs2 rootfs.bin')
            if os.path.exists('/media/magicboot/magicBootUpload/vuplus/uno'):
                os.chdir('uno')
                os.system('mv root_cfe_auto.jffs2 rootfs.bin')
        if getKernelVersionString() == '2.6.37':
            print 'Found Kernel 2.6.37'
            rc = os.system('insmod /usr/lib/enigma2/python/Plugins/Extensions/magicBoot/nandsim_2637 cache_file=/media/magicboot/image_cache first_id_byte=0x20 second_id_byte=0xaa third_id_byte=0x00 fourth_id_byte=0x15;sleep 5')
        elif getKernelVersionString() == '3.2.2':
            print 'Found Kernel 3.2.2'
            rc = os.system('insmod /usr/lib/enigma2/python/Plugins/Extensions/magicBoot/nandsim_322 cache_file=/media/magicboot/image_cache first_id_byte=0x20 second_id_byte=0xaa third_id_byte=0x00 fourth_id_byte=0x15;sleep 5')
        elif getKernelVersionString() == '3.6.0':
            print 'Found Kernel 3.6.0'
            rc = os.system('insmod /usr/lib/enigma2/python/Plugins/Extensions/magicBoot/nandsim_360 cache_file=/media/magicboot/image_cache first_id_byte=0x20 second_id_byte=0xaa third_id_byte=0x00 fourth_id_byte=0x15;sleep 5')
        elif getKernelVersionString() == '3.8.7':
            print 'Found Kernel 3.8.7'
            rc = os.system('insmod /usr/lib/enigma2/python/Plugins/Extensions/magicBoot/nandsim_387 cache_file=/media/magicboot/image_cache first_id_byte=0x20 second_id_byte=0xaa third_id_byte=0x00 fourth_id_byte=0x15;sleep 5')
        cmd = 'flash_eraseall -q /dev/mtd3'
        rc = os.system('sleep 10')
        cmd = 'nandwrite -q -p /dev/mtd3 rootfs.bin'
        rc = os.system(cmd)
        cmd = 'ubiattach /dev/ubi_ctrl -O 2048 -m 3 -d 3'
        rc = os.system(cmd)
        rc = os.system('mount -t ubifs ubi3_0 /media/magicboot/ubi')
        os.chdir('/home/root')
        rc = os.system('rm -r /media/magicboot/magicBootUpload/et9x00')
        rc = os.system('rm -r /media/magicboot/magicBootUpload/et6x00')
        rc = os.system('rm -r /media/magicboot/magicBootUpload/venton-hdx')
        rc = os.system('rm -r /media/magicboot/magicBootUpload/venton-hde')
        rc = os.system('rm -r /media/magicboot/magicBootUpload/vuplus')
        cmd = 'cp -r /media/magicboot/ubi/* /media/magicboot/magicBootI/' + target
        rc = os.system(cmd)
        rc = os.system('sleep 50')
        rc = os.system('sleep 50')
        rc = os.system('umount /media/magicboot/ubi')
        cmd = 'ubidetach -p /dev/mtd3'
        rc = os.system(cmd)
        rc = os.system('rmmod nandsim')
        rc = os.system('rm /media/magicboot/image_cache')
        rc = os.system('init 3')
    return 1
