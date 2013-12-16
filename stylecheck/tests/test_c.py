import unittest

from .. import sc

class TestCIndentation(unittest.TestCase):
	def setUp(self):
		self.hello_world_tab_indented = (
		"#include <stdio.h>\n"
		"\n"
		"int main(int args, char **argv) {\n"
		"\tprintf(\"Hello World!\");\n"
		"}"
		)
		self.hello_world_space_indented = (
		"#include <stdio.h>\n"
		"\n"
		"int main(int args, char **argv) {\n"
		"    printf(\"Hello World!\");\n"
		"}"
		)
		self.hello_world_mixed_whitespace = (
		"#include <stdio.h>\n"
		"\n"
		"int main(int args, char **argv) {\n"
		"\t    printf(\"Hello World!\");\n"
		"}"
		)
		self.hello_world_extra_whitespace = (
		"#include <stdio.h>\t\n"
		"\n"
		"int main(int args, char **argv) {\n"
		"\tprintf(\"Hello World!\");  \n"
		"}"
		)

	def test_tab_indentation(self):
		from stylecheck.lang.c.whitespace import IndentTabsOnly
		rule = IndentTabsOnly()
		lines = self.hello_world_tab_indented.split('\n')
		for line in lines:
			self.assertTrue(rule.check(line))

	def test_space_indentation(self):
		from stylecheck.lang.c.whitespace import IndentSpacesOnly
		rule = IndentSpacesOnly()
		lines = self.hello_world_space_indented.split('\n')
		for line in lines:
			self.assertTrue(rule.check(line))

	def test_no_tabs(self):
		from stylecheck.lang.c.whitespace import NoTabsRule
		rule = NoTabsRule()
		lines = self.hello_world_space_indented.split('\n')
		for line in lines:
			self.assertTrue(rule.check(line))
		# Only line 3 has a tab
		line = self.hello_world_tab_indented.split('\n')[3]
		self.assertFalse(rule.check(line))

	def test_no_mixed_whitespace(self):
		from stylecheck.lang.c.whitespace import IndentNoMixedWhitespace
		rule = IndentNoMixedWhitespace()
		lines = self.hello_world_mixed_whitespace.split('\n')
		# Only line 3 should have mixed whitespace
		mixed_linenums = [3]
		mixed_lines = [l for i, l in enumerate(lines) if i in mixed_linenums]
		lines = [l for i, l in enumerate(lines) if i not in mixed_linenums]

		for line in lines:
			self.assertTrue(rule.check(line))
		for line in mixed_lines:
			self.assertFalse(rule.check(line))

	def test_no_extra_whitespace(self):
		from stylecheck.lang.c.whitespace import NoExtraWhitespace
		rule = NoExtraWhitespace()
		lines = self.hello_world_extra_whitespace.split('\n')
		# Only these lines should have extra whitespace
		extra_linenums = [0,3]
		extra_lines = [l for i, l in enumerate(lines) if i in extra_linenums]
		lines = [l for i, l in enumerate(lines) if i not in extra_linenums]

		for line in lines:
			self.assertTrue(rule.check(line))
		for line in extra_lines:
			self.assertFalse(rule.check(line))

