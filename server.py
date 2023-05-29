from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import sqlite3
import json
import re

def run( server_class = HTTPServer, handler_class = BaseHTTPRequestHandler ):
	addr = ( '', 8000 )
	httpd = server_class ( addr, handler_class )
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		httpd.server_close()
class HttpGetHandler( BaseHTTPRequestHandler ):
	def header( self ):
		self.send_response( 200 )
		self.send_header ("content-type", "text/html; charset=utf-8" )
		self.end_headers()
	def my_file ( self, path):
		file = open ('.' + path, "rb")
		contents = file.read()
		return contents

	def do_GET(self):
		result = ""
		self.header()
		connection = sqlite3.connect("library.db")

		if self.path == "/books":
			result = connection.execute ("SELECT * FROM BOOKS")
			fields = [descr[ 0 ] for descr in result.description ]
			rows = result.fetchall()
			js = [ dict( zip( fields, row ) ) for row in rows ]
			result = json.dumps( js )
		if self.path == "/persons":
			result = connection.execute ("SELECT * FROM PERSONS")
			fields = [descr[ 0 ] for descr in result.description ]
			rows = result.fetchall()
			js = [ dict( zip( fields, row ) ) for row in rows ]
			result = json.dumps( js )

		connection.close()

		if re.search ( r"\.html",self.path, re.I ):
			self.wfile.write( self.my_file( self.path ) )
			return

		self.wfile.write( result.encode() )

run( handler_class = HttpGetHandler )
	
	
