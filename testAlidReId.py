from Services.AlignedReIDServices import AlignedReIDServices

reId = AlignedReIDServices("data/TGC_places")

r = reId.imgToEmbedding()

print(r)