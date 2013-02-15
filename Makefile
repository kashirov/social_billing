ENV=$(PWD)/env

all: clean env

env:
	virtualenv env
	. $(ENV)/bin/activate; pip install . --use-mirrors

clean:
	rm -rf $(ENV)

test:
	nosetests

