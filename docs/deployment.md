# Powertran Deployment Guide

## Initial Deployment

Deploying Powertran is a fairly simple process. Execute the following commands from a Debian Linux environment that
supports Python 3.10 or higher.

```
cd /opt

git clone https://github.com/AzorianSolutions/powertran.git

cd powertran

source bin/setup-environment.sh

powertran
```

**That's it!**

Now of course, before you actually use the application, you'll need to configure it. See
the [Configuration](configuration.md) guide for more information.

## Starting Powertran Synchronization

Once the environment is set up, you can start Powertran from a CRON job for example, by executing the following
commands from the application's root directory:

```
source venv/bin/active

powertran sync
```

> **NOTICE !!!!**

If you want to perform a test run to verify information before applying configuration changes to the devices,
provide the `-d` or `--dry-run` flag to the `powertran sync` command as follows:

> powertran sync -d

## CRON Setup

There are many ways to set up an environment to run this application under CRON. This is just one basic example that
you can work off of. This approach assumes you installed Powertran to `/opt/powertran`.

Start by running the following command:

```
sudo tee /root/powertran-sync.sh &> /dev/null <<EOF
#!/usr/bin/env bash
cd /opt/powertran
source venv/bin/activate
powertran sync > /root/powertran.log 2>&1
EOF

sudo tee /root/powertran.yml &> /dev/null <<EOF
threading:
  pool_size: 10
devices:
EOF
```

Now you need to edit the following command block so that the environment variables are set correctly
for your environment.

```
read -r -d '' PT_CRON <<'EOF'
PT_SALT="YOUR-APP-GENERATED-SALT-HERE"
PT_CONFIG=/root/powertran.yml
PT_MYSQL_HOST=YOUR-POWERCODE-DATABASE-HOST-HERE
PT_MYSQL_USER=YOUR-POWERCODE-DATABASE-USER-HERE
PT_MYSQL_PASSWORD=MYSQL-PASSWORD-HERE
PT_MYSQL_DATABASE=POWERCODE-DATABASE-NAME
*/30 * * * * /usr/bin/env bash /root/powertran-sync.sh
EOF

(crontab -l && echo "$PT_CRON") | crontab -
```

> **NOTICE!!!**

You need to set an appropriate salt for the `PT_SALT` environment variable.
You can generate a salt by running the `powertran gen_salt` command once the environment has been activated
using the steps at the beginning of this guide.

Once you have edited the above command block, run it from a terminal. This will set up the CRON job to run
every 30 minutes. You may need to tweak this to be permissive of the time it takes to complete an entire cycle
in your environment.
