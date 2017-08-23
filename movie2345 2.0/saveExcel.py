#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-21 21:41:33
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import xlwt

class save2017Movie(object):
	"""docstring for 
save2017Movie"""
	def __init__(self, items):
		self.items = items
		self.run(self.items)

	def run(self,items):
		fileName = u'电影.xls'.encode('GBK')
		book = xlwt.Workbook(encoding='utf8')
		sheet = book.add_sheet('2017',cell_overwrite_ok=True)
		sheet.write(0,0,u'电影名字'.encode('utf8'))
		sheet.write(0,1,u'电影评分'.encode('utf8'))
		sheet.write(0,2,u'电影主演'.encode('utf8'))
		i = 1
		while (i<=len(items)):
			item = items[i-1]
			sheet.write(i,0,item.name)
			sheet.write(i,1,item.point)
			sheet.write(i,2,item.staring)
			i+=1
		book.save(fileName)

if __name__ == '__main__':
	pass
	
		