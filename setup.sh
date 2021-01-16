rm -fr data/data_base_faces;
index=0
for folder in data/TGC2020v0.3_PRL/*; do
 sudo python3 FacesDetection.py $folder none;
 index=$((index+1));
 if [ $index -eq 4 ] ; then
  break;
 fi
done

exit 0;
