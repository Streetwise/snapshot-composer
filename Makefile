default: safety atmosphere tidy

clean:
	rm -rf output/*

tidy:
	rm output/temp*

test:
	# Not (yet) a test runner!
	mkdir -p output
	python main.py template/test.yml

safety:
	mkdir -p output
	python main.py template/safety.yml

atmosphere:
	mkdir -p output
	python main.py template/atmosphere.yml
