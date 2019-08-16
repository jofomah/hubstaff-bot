# HubStaff Bot

A simple time report project for HubStaff bot

### Requirement
- [Docker](https://docs.docker.com/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Setup

- Clone repository: `git clone git@github.com:jofomah/hubstaff-bot.git && cd hubstaff-bot` 
- Run `cp env.example .env` to copy sample .env to .env file
- Run `chmod +x src/app/entrypoint.sh` might require `sudo`
- Run `docker-compose build` might require `sudo`
- Open `.env` and enter values for the variables
- Run `docker-compose up`
- Open browser tab and navigate to `http://localhost:5000`
- Login with `ADMIN_EMAIL` and `ADMIN_PASSWORD` specified in the `.env`

### Enviroment variables

- `FLASK_ENV`: can be `production`, `development` or `testing` 
- `APP_SECRET_KEY`: Flask's secret key
- `HUBSTAFF_APP_TOKEN`: HubStaff App Key, visit [HubStaff Developer Apps](https://app.hubstaff.com/developer/my_apps) to get one.
- `HUBSTAFF_API_ACCOUNT_EMAIL`: HubStaff API account email
- `HUBSTAFF_API_ACCOUNT_PASSWORD`: HubStaff API account password
- `HUBSTAFF_ORGANIZATION_ID`: HubStaff Organization Id whose report will be processed.
- `HUBSTAFF_AUTH_TOKEN`: HubStaff API auth token, after setting the envs above, run `docker-compose run --rm app gen_auth_token` upon successful running, it will output `auth_token`, copy the output string and use it to set `HUBSTAFF_AUTH_TOKEN`


### Command

- `docker-compose run --rm app help` shows available commands

- `docker-compose up`: start all containers and services, use this to call `start_dev`

- `docker-compose run --rm app gen_auth_token`: fetches HubStaff API auth token

- `docker-compose run --rm app test_py` run test
    - 