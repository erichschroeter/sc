#! /usr/bin/env python
"""
usage: sc [options] [<file> ...]

options:
  -v, --version                 Print the version
  -h, --help                    Print this help menu
  --list [lang],...             List all available rules. Optionally filter by language.
  --spec <file> | <rule>,...    Specify the set of rules to check
  --color                       Use color output
"""
import os
import sys
import codecs
import string
import importlib
import inspect

from docopt import docopt

color_red = '\033[31m'
color_green = '\033[32m'
color_yellow = '\033[33m'
color_blue = '\033[34m'
color_purple = '\033[35m'
color_cyan = '\033[36m'
color_white = '\033[37m'
color_reset = '\033[00m'

colorize = False
categories = {}

def error(filename, linenum, rule):
	assert len(rule.__doc__) > 0
	if rule.category != '':
		txt = u"%s:%d:  %s  [%s]" % (filename, linenum, rule.__doc__, rule.category)
	else:
		txt = u"%s:%d:  %s" % (filename, linenum, rule.__doc__)
	console_print(txt, color=color_red)

def console_print(st=u"", f=sys.stdout, linebreak=True, color=None):
	global colorize
	if colorize is True and color is not None:
		f.write(color + st + color_reset)
	else:
		f.write(st)
	if linebreak: f.write(os.linesep)

def CheckLine(filename, linenum, line, rules):
	for rule in rules:
		passed = rule.check(line)
		if not passed:
			error(filename, linenum, rule)

def AggregateRules(filename):
	'''Recursively aggregates rules from the specified filename. If a line in
	filename is another filename, the rules are aggregated from that file.
	'''
	f = open(filename, 'r')
	lines = f.readlines()
	lines = set(lines)
	# Remove all newlines and comments
	lines = [line.strip() for line in lines if line[0] != '#']
	## Check if line is a file to import all rules within the file
	for line in lines:
		filepath = os.path.abspath(os.path.dirname(filename)) + os.sep + line.strip()
		if os.path.isfile(filepath):
			more = AggregateRules(filepath)
			lines = set(list(lines) + list(more))
	# Remove files
	lines = [line for line in lines if not os.path.isfile(os.path.abspath(os.path.dirname(filename)) + os.sep + line)]

	return set(lines)

def ProcessFileData(filename, lines, spec):
	linenum = 1
	for line in lines:
		CheckLine(filename, linenum, line, spec)
		linenum += 1

def ProcessFile(filename, spec):
	# Note, if no dot is found, this will give the entire filename as the ext.
	file_extension = filename[filename.rfind('.') + 1:]

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
	ProcessFileData(filename, lines, spec)

def ResolveRules(rules):
	resolved = []
	for rule in rules:
		m = rule[:rule.rfind('.')]
		r = rule[rule.rfind('.')+1:]
		try:
			# prepend stylecheck package for the user to save on typing
			importlib.import_module('stylecheck.' + m)
			res = getattr(sys.modules['stylecheck.' + m], r)()
			resolved.append(res)
		except AttributeError:
			console_print("Rule does not exist: %s" % rule, f=sys.stderr)
	return resolved

def find_subclasses(module, clazz):
	return [cls for name, cls in inspect.getmembers(module) if inspect.isclass(cls) and issubclass(cls, clazz)]

def main():
	import stylecheck.lang
	global colorize

	argv = docopt(__doc__, version=stylecheck.__version__)

	rules = []
	colorize = argv['--color']

	if argv['--list']:
		import pkgutil
		import Rule

		langs = argv['--list'].split(',')

		for lang in langs:
			package = 'stylecheck.lang.' + lang
			try:
				package = importlib.import_module(package)
			except ImportError:
				continue

			# iterate over all the modules in the language package looking for rules
			for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__,
				prefix=package.__name__ + '.',
				onerror=lambda x: None):
				mod = importlib.import_module(modname)
				if not inspect.ismodule(mod):
					continue
				rules = find_subclasses(mod, Rule.Rule)
				for rule in rules:
					pkg = rule.__module__[rule.__module__.find('.') + 1:]
					print(pkg + '.' + rule.__name__)
		return

	if argv['--spec'] is not None and argv['<file>']:
		spec_args = argv['--spec'].split(',')
		# Check if --spec is a file
		if len(spec_args) == 1 and os.path.isfile(spec_args[0]):
			rules = AggregateRules(spec_args[0])
		else:
			rules = spec_args

		rules = ResolveRules(rules)
		for filename in argv['<file>']:
			ProcessFile(filename, rules)

