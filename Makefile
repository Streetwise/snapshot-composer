default: safety atmosphere tidy

clean:
	rm -rf output/*

tidy:
	rm output/temp*

safety:
	mkdir -p output
	python main.py template/safety.yml

atmosphere:
	mkdir -p output
	python main.py template/atmosphere.yml
