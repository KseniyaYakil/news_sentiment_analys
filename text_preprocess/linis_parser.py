# coding=utf-8
from __future__ import division
import sys
import csv
import codecs

from text_parser import TextParser

class LinisParser(TextParser):
	def __init__(self, debug=False, log=None, data_dir="data"):
		TextParser.__init__(self, debug, log, data_dir)

	# fname contains texts
	def form_features(self, train_fname, target_fname, res_fname):
		try:
			linis_schema = self.get_schema(as_utf8=True)
			linis_schema.append('target')

			self.__print__('DEB', "storing schema to csv file")
			self.csv_writer_init(res_fname, linis_schema)

			train_f = codecs.open(train_fname, mode='r', encoding='utf-8')
			target_f = open(target_fname, 'r')

			index = 0
			pass_cnt = 0
			limit = -1
			text_features = []
			for text in train_f:
				target = float(target_f.readline().replace(',', '.'))

				index += 1
				if index % 100 == 0:
					self.__print__('INF', "processed {} texts".format(index))

				if index <= pass_cnt:
					continue

				self.__print__('DEB', "process text {}".format(index))
				features = self.text_to_features(text, as_utf8=True)
				if features is None:
					continue

				features['target'] = target

				self.__print__('DEB', "storing features to csv file")
				self.csv_writer_insert_row(features)

				if index == limit:
					break

			train_f.close()
			target_f.close()
			self.csv_writer_close()
			self.__print__('INF', "done")
		except Exception as e:
			self.__print__('ERR', str(e))
			sys.exit(1)

