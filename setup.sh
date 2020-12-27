rm -fr data/data_base_faces;
for folder in data/TGC2020v0.3_PRL/*; do
 sudo python3 FacesDetection.py $folder none;
done
