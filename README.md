**sc** stands for "style check".

The purpose of **sc** is to check source files against rules and notify users
of where source code does not adhere to those rules. The intention of the
project is to be a centralized place to store coding guidelines.

These coding guidelines can then be used by other projects to verify code being
submitted adheres to that project's specified coding guidelines. The
alternative is to manually check submitted code for guideline infractions,
which is prone to human error.

# Installation

Installation should be as simple as:

    python setup.py install

# Usage

To list supported rules for the **C** language:

    sc --list c

To check against a couple rules, an example would be:

    sc --spec lang.c.whitespace.IndentTabsOnly,lang.c.whitespace.NoExtraWhitespace main.c

Optionally, the `--spec` option takes a file argument. This is useful when
many rules are specified. This spec file should contain a list of rules; one
rule per line.

    # Create a rule specification containing all known C rules
    sc --list c > rules.spec
    # Check main.c against the rule specification
    sc --spec rules.spec main.c

# Development

The style rules are organized via different languages, since each language may
have it's own intricacies.

The first rules created were for the C language since I wanted to use this for
my own projects. However, the intention is that it is easy enough for others to
follow the pattern for there own projects in other languages.

The original source code was created using [cpplint.py Google-Styleguide][0] as
a starting reference. I wanted to get a tool up and running for myself quickly,
and [cpplint][0] seemed like a good source.

## Adding new rules

New rules should follow the same pattern as the existing rules; derive a new
class from a `Rule` class (defined in `Rule.py`) and implement `check()`. When
a new rule is created at least one unit test should be created to test its
functionality.

## Adding new languages

It is expected that additional languages will be in demand. The project
structure has been set up to aid in the addition of multiple language support.
Ideally there shouldn't be duplicate code in the project so if rules exist in
other languages, rather than copying the implementation you should create a new
derived `Rule` in the language specific package (perhaps even with the same
name as the existing rule) and call the existing rule's `check()` in the new
rule's `check()` function.

# Testing

Tests are run using [nose][1]. After installing stylecheck running the unit
tests should be as easy as:

    nosetests

[0]: http://google-styleguide.googlecode.com/svn/trunk/cpplint/cpplint.py
[1]: http://nose.readthedocs.org/en/latest/
