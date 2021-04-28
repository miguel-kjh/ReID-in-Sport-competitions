#!/bin/bash
die()
{
	echo "$0:$1" 1>&2
	exit 1
}

if(($# != 1)); then
	die "Bad argument"
fi

metrics=(euclidean cosine)
models=(retinaface retinafaceliif50 retinafaceliif100 retinafaceliif300
  img2pose img2poseliif50 img2poseliif100 img2poseliif300)
heuristics=(none dimension)
embeddings=(vgg_face facenet openface deepface)

if [ $1 == "--d" ];then

  python3 FacesDetection.py --f data/TGC2020v0.3_PRL/ --m retinaface  --heuristic none;
  python3 FacesDetection.py --f data/TGC2020v0.3_PRL/ --m retinaface  --heuristic dimension;

  python3 FacesDetection.py --f data/TGC2020v0.3_PRL/ --m img2pose  --heuristic none;
  python3 FacesDetection.py --f data/TGC2020v0.3_PRL/ --m img2pose  --heuristic dimension;

  chown miguel -R *;
fi

if [ $1 == "--if" ];then

  #python3 RunnersIdentifiaction.py --d data/Probe_faces_retinaface_none --all
  for model in "${models[@]}"
  do
    for heuristic in "${heuristics[@]}"
    do
      echo "########## $model  - $heuristic ############"
      echo "------- Normal ------"
      python3 RunnersIdentifiaction.py --d data/Probe_faces_${model}_${heuristic} --all;
      echo "------- CT ------"
      python3 RunnersIdentifiaction.py --d data/Probe_faces_${model}_${heuristic} --all --temp;
      echo "------- CT + filling ------"
      python3 RunnersIdentifiaction.py --d data/Probe_faces_${model}_${heuristic} --all --temp --filling;
      echo "------- CT + Regression ------"
      python3 RunnersIdentifiaction.py --d data/Probe_faces_${model}_${heuristic} --all --temp --regr;
    done
  done

fi

if [ $1 == "--ib" ];then

   echo "#### Normal ####"
   echo "--- Cosine ---"
   python3 RunnersIdentifiaction.py --aligenReId --met cosine
   echo "--- Euclidean ---"
   python3 RunnersIdentifiaction.py --aligenReId --met euclidean

   echo "#### PCA ####"
   echo "--- Cosine ---"
   python3 RunnersIdentifiaction.py --aligenReId --met cosine --pca
   echo "--- Euclidean ---"
   python3 RunnersIdentifiaction.py --aligenReId --met euclidean --pca

   echo "#### CT ####"
   echo "--- Cosine ---"
   python3 RunnersIdentifiaction.py --aligenReId --met cosine --temp
   echo "--- Euclidean ---"
   python3 RunnersIdentifiaction.py --aligenReId --met euclidean --temp

   echo "#### CT + Regression ####"
   echo "--- Cosine ---"
   python3 RunnersIdentifiaction.py --aligenReId --met cosine --temp --regr
   echo "--- Euclidean ---"
   python3 RunnersIdentifiaction.py --aligenReId --met euclidean --temp --regr

   echo "#### CT + filling ####"
   echo "--- Cosine ---"
   python3 RunnersIdentifiaction.py --aligenReId --met cosine --temp --filling
   echo "--- Euclidean ---"
   python3 RunnersIdentifiaction.py --aligenReId --met euclidean --temp --filling

fi

if [ $1 == "--ifb" ];then
  for model in "${models[@]}"
  do
    for heuristic in "${heuristics[@]}"
    do
      echo "########## $model  - $heuristic ############"
      for metric in "${metrics[@]}"
      do
        echo "-------- $metric -------- "
        for embedding in "${embeddings[@]}"
        do
          echo "++++++ $embedding +++++"
          python3 RunnersIdentifiaction.py --combine --met $metric --heu $heuristic --model $model --emb $embedding --temp --regr
          #echo "pca"
          #python3 RunnersIdentifiaction.py --combine --met $metric --heu $heuristic --model $model --emb $embedding --pca --temp
        done
      done
    done
  done

fi

if [ $1 == "--r" ];then

  python3 CropFacesImages.py --j data/TGC2020v0.3_json_img2pose_dimension/
  python3 CropFacesImages.py --j data/TGC2020v0.3_json_img2pose_none/
  python3 CropFacesImages.py --j data/TGC2020v0.3_json_retinaface_dimension/
  python3 CropFacesImages.py --j data/TGC2020v0.3_json_retinaface_none/

fi

exit 0;
