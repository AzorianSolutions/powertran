# Powertran Deployment Guide

## Initial Deployment

Deploying Powertran is a fairly simple process. Execute the following commands from a Debian Linux environment that
supports Python 3.10 or higher.

```
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
