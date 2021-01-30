python3 FacesDetection.py --f data/TGC2020v0.3_PRL/ --m retinaface  --heuristic none;
python3 FacesDetection.py --f data/TGC2020v0.3_PRL/ --m retinaface  --heuristic dimension;

python3 FacesDetection.py --f data/TGC2020v0.3_PRL/ --m img2pose  --heuristic none;
python3 FacesDetection.py --f data/TGC2020v0.3_PRL/ --m img2pose  --heuristic dimension;

chown miguel -R *;
exit 0;
