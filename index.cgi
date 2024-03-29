#!/usr/bin/python

import cgi 
import os
import sys
import string
from Album import Album
from Pic   import Pic


albumLoc   = 'album'
seperator  = '|'
pixVersion = '1.3.1'

class Presenter: 
	def __init__(self, subAlbum, picName, control):
		templateLines = open('template.html')

		currDir = '%s%s%s' % (albumLoc, os.sep, subAlbum)	
		#currDir = '%s%s' % (albumLoc, subAlbum)	
		album = Album(currDir)

		if (control == ''):
			if (picName != ''):
				pic = Pic('%s%s%s' % (currDir, os.sep, picName))
				#pic = Pic('%s%s' % (currDir, picName))
			else:
				pic = Pic('')
		else:
			if (control == 'first'):
				pic = Pic('%s%s%s' % (currDir, os.sep, album.getFirstPic()))
			if (control == 'previous'):
				pic = Pic('%s%s%s' % (currDir, os.sep, album.getPreviousPic(picName)))
			if (control == 'next'):
				pic = Pic('%s%s%s' % (currDir, os.sep, album.getNextPic(picName)))
			if (control == 'last'):
				pic = Pic('%s%s%s' % (currDir, os.sep, album.getLastPic()))


		self.printMetaData(albumLoc, currDir, pic, control)

		line = string.join(templateLines, '')
		line = string.replace(line, '@breadcrumb@', self.formatBreadCrumb(album, pic )) 
		line = string.replace(line, '@title@',      self.formatTitle(     album, pic ))
		line = string.replace(line, '@albums@',     self.formatAlbums(    album      ))
		line = string.replace(line, '@pics@',       self.formatPics(      album, pic ))
		line = string.replace(line, '@meta@',       self.formatMeta(      album      ))
		line = string.replace(line, '@control@',    self.formatControl(   album, pic ))
		line = self.formatContent(line, album, currDir, pic)
		print line,


	def printMetaData(self, albumLoc, currDir, pic, control):
		print '<!--'
		print 'albumLoc : %s' % albumLoc
		print 'subAlbum : %s' % currDir
		print 'pic      : %s' % pic
		print 'control  : %s' % control
		print 'pix ver  : %s' % pixVersion
		print '-->'


	def formatBreadCrumb(self, album, pic):
		outLines = []
		outLines.append(album.getBreadCrumb())
		if (pic.getName() != ''):
			outLines.append(' %s %s' % (seperator, pic))

		return string.join(outLines) 


	def formatTitle(self, album, pic):

		albumSep = ' %s ' % (seperator)
		if (album.getName() == ''):
			albumSep = ''

		picSep = ' %s ' % (seperator)
		if (pic.getName() == ''):
			picSep = ''

		return "%s%s%s%s" % (albumSep, album.getName(), picSep, pic)


	def formatAlbums(self, album):
		albums = album.getAlbums() 

		if len(albums) == 0:
			return ''

		outLines = ['<h2>%s albums</h2>' % (len(albums))]
		for album in albums:
			outLines.append('<a href="?album=%s">%s</a><br>' % (
				album.getLinkPath(), 
				album.getName()))
		return string.join(outLines, '\n')


	def formatPics(self, album, pic):
		if album.getNumPics() == 0:
			return ''

		pics     = album.getPics()
		outLines = ['<h2>%s pictures </h2>' % (len(pics))]

		for currPic in pics:
			selected = ''
			if (currPic.getName() == pic.getName()):
				selected = 'id="selected-pic"'

			outLines.append('<a href="?album=%s&pic=%s"><img %s alt="%s" title="%s" src="%s"/></a>' % ( 
				album.getLinkPath(), 
				currPic.getFileName(),
				selected,
				currPic.getName(), 
				currPic.getName(), 
				currPic.getThumb())) 
		return string.join(outLines, '\n')


	def formatMeta(self, album):
		try:
			metaFileName = '%s%s%s.meta' % (albumLoc, album.getLinkPath(), os.sep)
			metaFile = open(metaFileName)
		except:
			return ''
		return '<a target="_new" href="%s%s%s.meta">m</a> %s ' % (albumLoc, album.getLinkPath(), os.sep, seperator) 


	def formatControl(self, album, pic):
		if (len(album.getPics()) < 4):
			return ''

		control   = '&nbsp; <a href="?album=%s&pic=%s&control=%s">%s</a> &nbsp; '
		albumPath = album.getLinkPath()
		picFile   = pic.getFileName()

		firstLink    = control % (albumPath, picFile, 'first',    '|<')
		previousLink = control % (albumPath, picFile, 'previous', '<<')
		nextLink     = control % (albumPath, picFile, 'next',     '>>')
		lastLink     = control % (albumPath, picFile, 'last',     '>|')

		return '%s %s %s %s' % (firstLink, previousLink, nextLink, lastLink) 


	def formatContent(self, line, album, currDir,  pic):
		albumDescription = string.strip(album.getDescription())

		# TODO: this can be done better
		if pic.getOriginal() != '':
			line = string.replace(line, '@album-description@', '')
			line = string.replace(line, '@web-pic@',           self.formatWebPic(pic))
			line = string.replace(line, '@comment@',           pic.getComment())
			line = string.replace(line, '@page-type@', 'Picture' )
			line = string.replace(line, '@fb-url@',    "index.cgi?album=%s&pic=%s" %(album.getLinkPath(),pic.getFileName()))
			line = string.replace(line, '@pic-url@',   "album/%s/%s" %( album.getLinkPath(), pic.getFileName()))


		elif albumDescription != '': 
			line = string.replace(line, '@album-description@', albumDescription)
			line = string.replace(line, '@web-pic@',           '')
			line = string.replace(line, '@comment@',           '')
			line = string.replace(line, '@page-type@', 'Album')
			line = string.replace(line, '@fb-url@',    'index.cgi?album=%s' %(album.getLinkPath()))

		else:
			if album.getNumPics() > 0:
				firstPic = album.getPics()[0].getFileName()
				pic = Pic('%s%s%s' % (currDir, os.sep, firstPic))
				line = string.replace(line, '@page-type@', 'Album')
				line = string.replace(line, '@fb-url@', 'index.cgi?album=%s' %(album.getLinkPath()))
			else:
				pic = Pic('')

			line = string.replace(line, '@album-description@', '')
			line = string.replace(line, '@web-pic@', self.formatWebPic(pic))
			line = string.replace(line, '@comment@', pic.getComment())
			line = string.replace(line, '@pic-url@',   "album/%s/%s" %( album.getLinkPath(), pic.getFileName()))

		line = string.replace(line, '@page-type@', 'Site')
		line = string.replace(line, '@fb-url@', '' )

		return line


	def formatWebPic(self, pic):
		if pic.getOriginal() == '':
			return ''

		# use this return so that the users can click on the web-sized image and
		# then see the original image.  of course sometimes the originals are huge
		# so using the alternate return will keep your bandwidth usage down.
		# return '<a href="%s"><img align="right" alt="%s" title="%s" src="%s"/></a>' % (
		# 		pic.getOriginal(), 
		# 		'click here to view the original image',
		# 		'click here to view the original image',
		# 		pic.getWeb())

		return '<img align="right" src="%s"/>' % (pic.getWeb())


def getArg(aForm, aKey):
	if aForm.has_key(aKey): 
		print '<!-- %s: %s -->' % (aKey, aForm[aKey].value)
		return aForm[aKey].value 
	return ''


def doAdminFunction(action, album, pic):
	# TODO: 
	# presumablye in the future if there were any other admin functions
	# besides clean there would be some if statements here
	print '<pre>'
	print 'cleaning cache recursively from %s%s' % (albumLoc, album)

	albumToClean = '%s%s' % (albumLoc, album)
	for root, dirs, files in os.walk(albumToClean):
		for file in files:
			if string.find(file, '.web_') == 0 or string.find(file, '.thumb_') == 0:
				pathAndEntry = '%s%s%s' % (root, os.sep, file)
				os.remove(pathAndEntry)
				print 'deleted <i>%s</i>' % (pathAndEntry)
	print '</pre>'


if __name__=='__main__': 

	sys.stderr == sys.stdout 
	print 'Content-type:text/html\n' 

	try:
		iForm       = cgi.FieldStorage() 
		album       = getArg(iForm, 'album')
		pic         = getArg(iForm, 'pic')
		control     = getArg(iForm, 'control')
		adminAction = getArg(iForm, 'admin')
		if (adminAction != ''):
			doAdminFunction(adminAction, album, pic)
		else:
			Presenter(album, pic, control)
	except Exception, exceptionData:
		print '''
			<pre><h1>pix broke, you get to keep both pieces</h1>%s</pre>
		''' % exceptionData

