import sys 
from predict_image_class import SOPHI_net

nn = SOPHI_net(image_path = sys.argv[1], n_top_picks = 5, verbosity = True)

for each in nn.predict():
	print(each[0], ' ', each[1])
