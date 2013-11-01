**sc** stands for "style check".

The purpose of **sc** is to check source files against rules and notify users
of where source code does not adhere to those rules. The intention of the
project is to be a centralized place to store coding guidelines.

These coding guidelines can then be used by other projects to verify code being
submitted adheres to that project's specified coding guidelines. The
alternative is to manually check submitted code for guideline infractions,
which is prone to human error.

### Organization

The style rules are organized via different languages, since each language may
have it's own intricacies.

The first rules created were for the C language since I wanted to use this for
my own projects. However, the intention is that it is easy enough for others to
follow the pattern for there own projects in other languages.

The original source code was created using [cpplint.py Google-Styleguide][0] as
a starting reference. I wanted to get a tool up and running for myself quickly,
and [cpplint][0] seemed like a good source.

[0]: http://google-styleguide.googlecode.com/svn/trunk/cpplint/cpplint.py
