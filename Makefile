readme.rst: readme.md
	pandoc $< -o $@
