FROM python:3.7.2-alpine3.8

LABEL maintainer='Jideobi Ofomah <osdevseries@gmail.com>'

ENV APP_HOST 0.0.0.0
ENV APP_PORT 5000

##############################################################################
## setup app
## copy app folder, config folders and install dependencies
##############################################################################

COPY ./conf/pip /app/pip

RUN pip install -q --upgrade pip && \
    pip install -q -r /app/pip/requirements.txt -r /app/pip/requirements_dev.txt

WORKDIR /app

COPY ./src/app /app

################################################################################
# expose app web server port 
################################################################################

EXPOSE ${APP_PORT}

################################################################################
# create user, grant permissions to folders etc
################################################################################

RUN addgroup -S hubstaff && adduser -S -G hubstaff hubstaff
RUN chown -R hubstaff: /app
RUN chmod +x /app/entrypoint.sh

################################################################################
# set app entry point script
################################################################################

ENTRYPOINT ["/app/entrypoint.sh"]