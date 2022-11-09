package:
	rm -rf build
	rm -f tweetgen-lambda.zip
	mkdir build
	pip install -r requirements.txt --target build
	cp *.py build
	cd build; zip -r ../tweetgen-lambda.zip .
