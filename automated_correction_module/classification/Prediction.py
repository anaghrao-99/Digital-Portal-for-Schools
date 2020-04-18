import numpy as np
from Utils import *
from WordSegmentation import wordSegmentation, prepareImg
import matplotlib.pyplot as plt
import numpy as np
import cv2
from Preprocessor import preprocess
from keras.models import model_from_json
import shutil
from keras import backend as K
from keras.utils import plot_model
from Spell import correction_list
import sys

def test_infer(files, file_path, out_file):
	file_out = open(out_file, 'w')

	for img in files:
		if'.png' in img or '.jpg' in img:
			# print(test_img)
			file_out.write(' ')
			test_img = file_path + img
			img = prepareImg(cv2.imread(test_img), 64)
			img2 = img.copy()
			#25
			res = wordSegmentation(img, kernelSize=9, sigma=11, theta=7, minArea=100)
			if not os.path.exists('tmp'):
				os.mkdir('tmp')

			for (j, w) in enumerate(res):
				(wordBox, wordImg) = w
				(x, y, w, h) = wordBox
				cv2.imwrite('tmp/%d.png'%j, wordImg)
				cv2.rectangle(img2,(x,y),(x+w,y+h),(0,255,0),1) # draw bounding box in summary image

			# cv2.imwrite('Resource/summary.png', img2)
			# plt.imshow(img2)
			#start
			# imgFiles = os.listdir('tmp')
			# imgFiles = sorted(imgFiles)
			# 
			# pred_line = []
			# for f in imgFiles:
			# 	pred_line.append(predict_image(w_model_predict, 'tmp/'+f, True))
			# print('-----------PREDICT-------------')
			# print('[Word model]: '+' '.join(pred_line))
			# pred_line = correction_list(pred_line)

			# print('[Word model with spell]: '+' '.join(pred_line))
			#end
			x = predict_image(l_model_predict, test_img, False)
			print('[Line model]: ' + x)

			file_out.write(x)


			plt.show()
			shutil.rmtree('tmp')


if __name__=='__main__':
	#l_model, l_model_predict = line_model()
	#with open('line_model_predict.json', 'w') as f:
	#	f.write(l_model_predict.to_json())

	

	with open('Resource/line_model_predict.json', 'r') as f:
		l_model_predict = model_from_json(f.read())
	# with open('Resource/word_model_predict.json', 'r') as f:
	# 	w_model_predict = model_from_json(f.read())
	#plot_model(l_model_predict, to_file='line_model.png', show_shapes=True, show_layer_names=True)
	# w_model_predict.load_weights('Resource/iam_words--20--1.425.h5')
	l_model_predict.load_weights('Resource/iam_lines--12--17.373.h5')
	file_path = '../out_test/'
	# test_img = 'Users/anagh/Desktop/out_test/1.png'
	# test_img = 'Resource/test_img/5.png'
	files = os.listdir(file_path)
	print(files)
	files.sort()

	file_string = sys.argv[1]
	string = file_string.split('.png')[0]
	string += '.txt'
	out_file = '../' + string
	# out_file = '../recognized.txt'

	test_infer(files, file_path, out_file)

