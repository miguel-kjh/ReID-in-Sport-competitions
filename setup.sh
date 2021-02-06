#!/bin/bash
die()
{
	echo "$0:$1" 1>&2
	exit 1
}

if(($# != 1)); then
	die "Bad argument"
fi

if [ $1 == "--d" ];then

  python3 FacesDetection.py --f data/TGC2020v0.3_PRL/ --m retinaface  --heuristic none;
  python3 FacesDetection.py --f data/TGC2020v0.3_PRL/ --m retinaface  --heuristic dimension;

  python3 FacesDetection.py --f data/TGC2020v0.3_PRL/ --m img2pose  --heuristic none;
  python3 FacesDetection.py --f data/TGC2020v0.3_PRL/ --m img2pose  --heuristic dimension;

  chown miguel -R *;
fi

if [ $1 == "--i" ];then

  python3 RunnersIdentifiaction.py --d data/Gallery_faces_retinaface_none --all
  #python3 RunnersIdentifiaction.py --d data/Gallery_faces_retinaface_dimension/ --all

  python3 RunnersIdentifiaction.py --d data/Gallery_faces_img2pose_none --all
  python3 RunnersIdentifiaction.py --d data/Gallery_faces_img2pose_dimension/ --all

fi

exit 0;
