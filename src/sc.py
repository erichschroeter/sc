#! /usr/bin/env python
"""
usage: sc [FILE] ...

options:
  -v, --version
  -h, --help
  --spec
"""
import os
import sys
import codecs
import string

from docopt import docopt

rules = {}
categories = {}

def rule(method):
	global rules
	assert method.__doc__, "All rules need properly formmatted docstrings (even %r!!)" % method
	if hasattr(method, 'im_func'): # bound method, if we ever have one
		method = method.im_func
	rules[method.func_name] = method
	return method

def category(name):
	def decorator(method):
		global categories
		assert method not in categories, "This method already has a category."
		categories[method] = name
		return method
	return decorator

@rule
@category('whitespace/tab')
def no_tabs(filename, linenum, line):
	u"""Tab found; better to use spaces"""
	if line.find('\t') != -1:
		error(filename, linenum, no_tabs)

@rule
@category('whitespace/indent')
def indent_no_mixed_whitespace(filename, linenum, line):
	u"""Indentation should not mix whitepsace characters"""
	if len(line) < 1:
		return
	if line[0:1] not in string.whitespace:
		return
	whitespace_char = line[0:1]
	# Strip whitespace to find first non-whitespace char
	stripped = line.strip(string.whitespace)
	if len(stripped) < 1:
		return
	first_non_whitespace = stripped[0:1]
	for i, c in enumerate(line):
		if c == first_non_whitespace:
			break
		if c != whitespace_char:
			error(filename, linenum, indent_no_mixed_whitespace)
			break

def indent_is_only(line, whitespace):
	"""Returns whether the line is indented with the specified whitespace.

	Checks from the beginning of line for any whitespace and if the char is
	whitespace but not the specified whitespace False is returned.
	Otherwise True is returned.
	"""
	if line.count < 1:
		return True
	first_non_whitespace = 0
	for i, c in enumerate(line):
		if c not in string.whitespace:
			first_non_whitespace = i
			break
		# make sure indent is space
		if c != whitespace:
			return False
	return True

@rule
@category('whitespace/indent')
def indent_space_only(filename, linenum, line):
	u"""Indent with spaces"""
	if not indent_is_only(line, ' '):
		error(filename, linenum, indent_space_only)

@rule
@category('whitespace/indent')
def indent_tab_only(filename, linenum, line):
	u"""Indent with tabs"""
	if not indent_is_only(line, '\t'):
		error(filename, linenum, indent_tab_only)

def error(filename, linenum, rule):
	assert len(rule.__doc__) > 0
	if rule in categories:
		txt = u"%s:%d:  %s  [%s]" % (filename, linenum, rule.__doc__, categories[rule])
	else:
		txt = u"%s:%d:  %s" % (filename, linenum, rule.__doc__)
	console_print(txt, sys.stderr)

def console_print(st=u"", f=sys.stdout, linebreak=True):
	f.write(st)
	if linebreak: f.write(os.linesep)

def CheckLine(filename, linenum, line, ruleset):
	for rule in ruleset:
		ruleset[rule](filename, linenum, line)

def ProcessFileData(filename, lines):
	# Create example rule set
	rules = {}
	#rules[no_tabs.func_name] = no_tabs
	rules[indent_tab_only.func_name] = indent_tab_only
	#rules[indent_space_only.func_name] = indent_space_only
	rules[indent_no_mixed_whitespace.func_name] = indent_no_mixed_whitespace

	linenum = 1
	for line in lines:
		CheckLine(filename, linenum, line, rules)
		linenum += 1

def ProcessFile(filename):
	# Note, if no dot is found, this will give the entire filename as the ext.
	file_extension = filename[filename.rfind('.') + 1:]

	valid_extensions = ['py', 'c', 'h']
	if filename != '-' and file_extension not in valid_extensions:
		sys.stderr.write('Ignoring %s; not a valid file name '
			'(.c, .h)\n' % filename)
	else:
		try:
			# Support the UNIX convention of using "-" for stdin.  Note that
			# we are not opening the file with universal newline support
			# (which codecs doesn't support anyway), so the resulting lines do
			# contain trailing '\r' characters if we are reading a file that
			# has CRLF endings.
			# If after the split a trailing '\r' is present, it is removed
			# below. If it is not expected to be present (i.e. os.linesep !=
			# '\r\n' as in Windows), a warning is issued below if this file
			# is processed.
			
			if filename == '-':
			  lines = codecs.StreamReaderWriter(sys.stdin,
			                                    codecs.getreader('utf8'),
			                                    codecs.getwriter('utf8'),
			                                    'replace').read().split('\n')
			else:
			  lines = codecs.open(filename, 'r', 'utf8', 'replace').read().split('\n')
			
			carriage_return_found = False
			# Remove trailing '\r'.
			for linenum in range(len(lines)):
			  if lines[linenum].endswith('\r'):
			    lines[linenum] = lines[linenum].rstrip('\r')
			    carriage_return_found = True
		
		except IOError:
			sys.stderr.write(
			    "Skipping input '%s': Can't open for reading\n" % filename)
			return
		ProcessFileData(filename, lines)

def main(argv):
	for filename in argv['FILE']:
		ProcessFile(filename)

if __name__ == '__main__':
	args = docopt(__doc__, version='0.1.0rc')
	main(args)

