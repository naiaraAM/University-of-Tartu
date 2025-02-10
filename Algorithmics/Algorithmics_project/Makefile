front-build:
	docker build -t algo-front -f front.Dockerfile  .

front-run: 
	docker run -it  -p 3000:3000  algo-front  

back-build:
	docker build -t algo-back -f back.Dockerfile .

back-run: 
	docker run -it  -p 8001:8001  algo-back  

all: front-build back-build
	docker compose up
