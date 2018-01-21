.PHONY: download clean merge

download:
	python download.py

merge: clean
	mkdir temp
	find pdfs -name *.pdf -print0 | sort -z | xargs -0 cp --target-directory=temp/
	cd temp && pdftk *.pdf cat output ../merged.pdf

clean:
	rm -rf *.pdf
	rm -rf temp
