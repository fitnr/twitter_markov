# twitter_markov - Create markov chain ("_ebooks") accounts on Twitter
# Copyright 2014-2016 Neil Freeman contact@fakeisthenewreal.org

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
.PHONY: all deploy cov test

all: docs.zip README.rst

docs.zip: docs/source/conf.py $(wildcard docs/*.rst docs/*/*.rst twitter_markov/*.py) 
	$(MAKE) -C docs html
	cd docs/_build/html; \
	zip -qr ../../../$@ . -x '*/.DS_Store' .DS_Store

deploy: README.rst | clean
	python3 setup.py sdist bdist_wheel --universal
	twine upload dist/*
	git push
	git push --tags

README.rst: README.md
	- pandoc $< -o $@
	@touch $@
	- python setup.py check --restructuredtext --strict

test: cov
	coverage html

cov:
	- coverage run --include="build/lib/twitter_markov/*,twitter_markov/*" setup.py test
	coverage report

clean:; rm -rf dist build

