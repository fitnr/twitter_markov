# twitter_markov - Create markov chain ("_ebooks") accounts on Twitter
# Copyright 2014-2015 Neil Freeman contact@fakeisthenewreal.org

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
.PHONY: deploy cov

deploy: README.rst
	rm -rf dist build
	python3 setup.py sdist bdist_wheel
	rm -rf dist build
	python setup.py sdist
	twine upload dist/*
	git push
	git push --tags

README.rst: README.md
	- pandoc $< -o $@
	@touch $@
	python setup.py check --restructuredtext --strict

cov:
	coverage run --include="twitter_markov/*" setup.py test
	coverage html
	open htmlcov/index.html
