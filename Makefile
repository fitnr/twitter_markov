readme.rst: README.md
	pandoc $< -o $@ || cp $< $@
