#!/bin/bash
set -x
#set -e

export VAGRANT_LOG=ERROR

echo $#
if [[ $# -lt 2 ]];
then
    echo "no image"
    exit 1
fi

VBOX_IMAGE=$1
OUTPUT=$2
#OUTPUT="pxe-server"
BASE_DIR="`pwd`/machines"
BOX_DIR="${BASE_DIR}/${VBOX_IMAGE}"
 
vm_remove()
{
    box=$1
    vagrant box list |grep -w " $box "
    if [[ $? -eq 0 ]];
    then
        vagrant box remove $box
    fi
}
vm_remove $OUTPUT

#VBoxManage createvm --name "${VBOX_IMAGE}" --ostype Ubuntu_64 --basefolder "${BASE_DIR}"
#VBoxManage registervm "${BOX_DIR}/${VBOX_IMAGE}-CREATE.vbox"
     
#mkdir -p tmp
#rm -rf tmp/clone.vdi
#VBoxManage clonehd $IMAGE.vmdk tmp/clone.vdi --format vdi
#VBoxManage modifyhd tmp/clone.vdi --resize 20480
#VBoxManage clonehd tmp/clone.vdi "${BOX_DIR}/${VBOX_IMAGE}.vmdk" --format vmdk
#VBoxManage -q closemedium disk tmp/clone.vdi
#rm -f tmp/clone.vdi
     
#VBoxManage storagectl "${VBOX_IMAGE}" --name LsiLogic --add scsi --controller LsiLogic
#VBoxManage storageattach "${VBOX_IMAGE}" --storagectl LsiLogic --port 0 --device 0 --type hdd --medium "${BOX_DIR}/${VBOX_IMAGE}.vmdk"
# NAT interface with SSH forwarding
#VBoxManage modifyvm "${VBOX_IMAGE}" --natpf2 delete "ssh" 2>&1

VBoxManage modifyvm "${VBOX_IMAGE}" --nic1 nat
VBoxManage modifyvm "${VBOX_IMAGE}" --natpf1 "ssh,tcp,,2222,,22" 

VBoxManage modifyvm "${VBOX_IMAGE}" --nic2 bridged

VBoxManage modifyvm "${VBOX_IMAGE}" --usb on --usbehci on
VBoxManage modifyvm "${VBOX_IMAGE}" --memory 512
     
#exit
#OUTPUT=`echo ${VBOX_IMAGE}|sed -e 's/ /_/g'`
TMP=`mktemp /tmp/$OUTPUT.XXXXXX`.box
vagrant package --base "${VBOX_IMAGE}" --output ${TMP}
vagrant box add ${OUTPUT} ${TMP} 
TMP=~/tmp/test
cd $TMP
#vagrant init $OUTPUT
vagrant up
