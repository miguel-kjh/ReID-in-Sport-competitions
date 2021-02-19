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

if [ $1 == "--if" ];then

  python3 RunnersIdentifiaction.py --d data/Probe_faces_retinaface_none --all
  python3 RunnersIdentifiaction.py --d data/Probe_faces_retinaface_dimension/ --all

  python3 RunnersIdentifiaction.py --d data/Probe_faces_img2pose_none --all
  python3 RunnersIdentifiaction.py --d data/Probe_faces_img2pose_dimension/ --all

fi

if [ $1 == "--ia" ];then

   python3 RunnersIdentifiaction.py --aligenReId --met cosine
   python3 RunnersIdentifiaction.py --aligenReId --met euclidean

fi

if [ $1 == "--r" ];then

  python3 CropFacesImages.py --j data/TGC2020v0.3_json_img2pose_dimension/
  python3 CropFacesImages.py --j data/TGC2020v0.3_json_img2pose_none/
  python3 CropFacesImages.py --j data/TGC2020v0.3_json_retinaface_dimension/
  python3 CropFacesImages.py --j data/TGC2020v0.3_json_retinaface_none/

fi

exit 0;
