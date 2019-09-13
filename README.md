# seed_image_metadata

Build the docker image
```
seed build -d seed_image_size
```

Run the docker image
```
seed run --in tiff-metadata-job-0.0.1-seed:1.0.1 -i TIFF_FILE=./seed_image_size/inputs/CO_Berthoud_Pass_20160906_TM_geo.tif -o ./seed_image_size/outputs -m MOUNT_BIN=/usr/bin -m MOUNT_TMP=/tmp
```

Publish the docker image
```
seed publish -in tiff-metadata-job-0.0.1-seed:1.0.1 -r docker.io -o username -u username -p "password"
```
