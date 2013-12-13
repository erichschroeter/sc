import string

from stylecheck import Rule

class NoTabsRule(Rule.SingleLineRule):
	u"""Tab found; better to use spaces"""

	def __init__(self):
		Rule.SingleLineRule.__init__(self, category = 'whitespace/tab')

	def check(self, text):
		if text.find('\t') != -1:
			return False
		return True

class IndentNoMixedWhitespace(Rule.SingleLineRule):
	u"""Indentation should not mix whitepsace characters"""

	def __init__(self):
		Rule.SingleLineRule.__init__(self, category = 'whitespace/indent')

	def check(self, text):
		if len(text) < 1:
			return True
		if text[0] not in string.whitespace:
			return True
		whitespace_char = text[0]
		# Strip whitespace to find first non-whitespace char
		stripped = text.strip()
		if len(stripped) < 1:
			return True
		first_non_whitespace = stripped[0]
		for i, c in enumerate(text):
			if c == first_non_whitespace:
				return True
			if c != whitespace_char:
				break
		return False

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

class IndentSpacesOnly(Rule.SingleLineRule):
	u"""Indent with spaces"""

	def __init__(self):
		Rule.SingleLineRule.__init__(self, category = 'whitespace/indent')

	def check(self, text):
		if indent_is_only(text, ' '):
			return True
		return False

class IndentTabsOnly(Rule.SingleLineRule):
	u"""Indent with tabs"""

	def __init__(self):
		Rule.SingleLineRule.__init__(self, category = 'whitespace/indent')

	def check(self, text):
		if indent_is_only(text, '\t'):
			return True
		return False

class NoExtraWhitespace(Rule.SingleLineRule):
	u"""Extra whitespace"""

	def __init__(self):
		Rule.SingleLineRule.__init__(self, category = 'whitespace/extra')

	def check(self, text):
		if text and text[-1].isspace():
			return False
		return True

class FunctionNoWhitespaceBeforeParenthesis(Rule.SingleLineRule):
	u"""Whitespace between function and parenthesis"""

	def __init__(self):
		Rule.SingleLineRule.__init__(self, category = 'whitespace/function')

	def check(self, text):
		parts = text.split('(')
		if parts[0][-1:].isspace():
			return False
		return True

