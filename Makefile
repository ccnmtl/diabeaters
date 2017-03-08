APP=diabeaters
JS_FILES=media/js/healthhabit* media/js/dragdropreorder.js
MAX_COMPLEXITY=7

all: jenkins

include *.mk

eslint: $(JS_SENTINAL)
	$(NODE_MODULES)/.bin/eslint $(JS_FILES)

.PHONY: eslint
