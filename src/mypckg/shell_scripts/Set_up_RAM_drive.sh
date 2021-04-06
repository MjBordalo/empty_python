echo "Creating RAM folder /tmpfolder on Rpi...."
sudo mkdir /tmpfolder
echo "tmpfs /tmpfolder tmpfs nodev,nosuid,size=10M 0 0 " | sudo tee -a /etc/fstab
sudo mount -a
df