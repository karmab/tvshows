sample tvshows app showing finales for tvshows

![Screenshot](screenshot.png)

## How to install

For banners of the tvshows to show up, You will need to set *TVDB_KEY* environment variable to your tdvb api key

### Create mysql database and sample data

```
mysql < load.sql
```

### Install app

```
python3 setup.py install
sed -i "s/TVDB_KEY=/TVDB_KEY=$TVDB_KEY/" tvshows.service
cp tvshows.service /usr/lib/systemd/system
restorecon /usr/lib/systemd/system/tvshows.service
systemctl enable --now tvshows
```
