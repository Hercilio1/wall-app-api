#!/bin/bash

# add crontab entry to renew the letsencrypt certificate
# this cron job will run every day 11.00 P.M
echo "renewing crontab"
docker-compose run --rm certbot renew --webroot --webroot-path /var/www/certbot/
