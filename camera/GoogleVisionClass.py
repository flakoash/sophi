import io, os, sys 
from google.cloud import vision 

class GoogleVision:
	def __init__(self, image_path):
		self.image_path = image_path
		self.vision_client = vision.Client('sophi')

	def predict(self):
		# Read file 
		with io.open(self.image_path, 'rb') as image_file:
			content = image_file.read()
			image = self.vision_client.image(content=content)

		# Label detection
		labels = image.detect_labels()

		# Store labels
		return_labels = [each.description for each in labels]

		# Return labels 
		return return_labels
