.PHONY: up down restart_bot

up:
	sudo docker compose up --build -d

up_and_logs:
	sudo docker compose up --build -d && sudo docker compose logs -f bot

down:
	sudo docker compose down

restart_bot:
	sudo docker compose up --build --force-recreate -t 1 bot -d

logs:
	sudo docker compose logs -f bot
