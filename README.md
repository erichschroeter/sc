**sc** stands for "style check".

The purpose of **sc** is to check source files against rules and notify users
of where source code does not adhere to those rules. The intention of the
project is to be a centralized place to store coding guidelines.

These coding guidelines can then be used by other projects to verify code being
submitted adheres to that project's specified coding guidelines. The
alternative is to manually check submitted code for guideline infractions,
which is prone to human error.

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
class from a `Rule` class and implement `check()`. When a new rule is created
at least one unit test should be created to test its functionality.

## Adding new languages

It is expected a demand for supporting new languages be wanted. The project
structure has been set up to aid in the addition of multiple language support.
Ideally there shouldn't be duplicate code in the project so if rules exist in
other languages, rather than copying the implementation you should create a new
derived `Rule` in the language specific package (perhaps even with the same
name as the existing rule) and call the existing rule's `check()` in the new
rule's `check()` function.

[0]: http://google-styleguide.googlecode.com/svn/trunk/cpplint/cpplint.py
