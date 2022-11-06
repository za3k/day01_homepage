run-debug:
	flask --debug run
run-demo:
	gunicorn3 -e SCRIPT_NAME=/hackaday/homepage --bind 0.0.0.0:8001 app:app
