.PHONY: download clean merge

download:
	python download.py

merge: clean
	python merge.py

clean:
	rm -rf *.pdf
	rm -rf temp
