''' 
Project: SOPHINET-2 (retrained inception-v3)
Description: Prediction class summarized in a trained_graph. 
Training Details:
	* learning_rate: 0.001 (no decay)
	* optimizer: SGD (500 batche size)
	* epochs: 4000 (default)
'''
import os, sys, cv2
import tensorflow as tf 
import numpy as np

class SOPHI_net:
	def __init__(self, image_path = '', n_top_picks = 5, verbosity = False):
		# Variables 
		self.verbosity = verbosity
		self.n_top_picks = n_top_picks
		self.image_path = image_path
		# Image 
		if len(image_path) != 0:
			self.get_file_extension()
			self.img = tf.gfile.FastGFile(self.image_path, 'rb').read()
			self.labels = [ line.rstrip() for line in tf.gfile.GFile("retrained_labels.txt") ]
		else:
			print('No image path provided')
			sys.exit()
		# Really fast QA
		if self.fast_QA() != True:
			print('Conditions not met')
			sys.exit()

	def fast_QA(self):
		# Img
		img__ = cv2.imread(self.image_path)
		img_qa = False if (len(img__.shape) != 3) and (img__.shape[0] < 120 and img__.shape[1] < 120) else True
		# Graphs
		files = [each for each in os.listdir('.')]
		graph_qa = True if ( ('retrained_labels.txt' in files) and ('retrained_graph.pb' in files) ) else False
		# ----
		return True if img_qa and graph_qa else False

	def get_file_extension(self):
		# Only JPEG encoding allowed
		extension = self.image_path.split('.')[-1]
		#print(self.image_path)
		if extension.rstrip() != 'JPEG':
			img_ = cv2.imread(self.image_path)
			self.image_path = 'temp_sample.JPEG'
			cv2.imwrite(self.image_path, img_)

	def preprocess(self, z_norm = False):
		# Not used 
		return ( self.img - np.mean(self.img[:,:,:]) ) / np.std(self.img[:,:,:]) if z_norm else ( self.img  - np.amin(self.img) ) / (np.amax(self.img) - np.amin(self.img))

	def predict(self):
		with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
		    graph_def = tf.GraphDef()
		    graph_def.ParseFromString(f.read())
		    _ = tf.import_graph_def(graph_def, name='')

		with tf.Session() as sess:
			softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
			predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': self.img})
			top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

			return_list = []
			for node_id in top_k[:self.n_top_picks]:
				human_string = self.labels[node_id]
				score = predictions[0][node_id]
				return_list.append( (human_string, score) )
				if self.verbosity:
					print('%s (score = %.5f)' % (human_string, score))
		
		return return_list