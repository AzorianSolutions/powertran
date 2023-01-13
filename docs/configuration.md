# Powertran Configuration Guide

## Environment Variables

#### PT_DEBUG (bool)

If set to `True`, Powertran will log debug messages to the console. This is useful for debugging issues with Powertran.

#### PT_SALT (str)

The salt used to encrypt the device passwords. This should be a random string of characters.

> **NOTICE !!!**

To make it easy to generate the right type of salt, you can use the following command once the app's environment
has been activated:

> powertran gen_salt

#### PT_MYSQL_HOST (str)

The IP address or hostname of the MySQL server.

#### PT_MYSQL_PORT (int)

The port number of the MySQL server. If not specified, the default port number of `3306` will be used.

#### PT_MYSQL_USER (str)

The username of the MySQL user that has access to the Powercode database. If not specified, the default username
of `root` will be used.

#### PT_MYSQL_PASSWORD (str)

The password of the MySQL user that has access to the Powercode database.

#### PT_MYSQL_DATABASE (str)

The name of the MySQL database that contains the Powercode data.

#### PT_CONFIG (str)

The path to the Powertran configuration file. If not specified, the default path of `conf/config.yml` will be used.

#### PT_KNOWN_HOSTS (str)

The path to the known hosts file. If not specified, the default path of `~/.ssh/known_hosts` will be used.

## YAML Configuration

The application's YAML configuration is fairly straightforward. It contains a simple list of objects that represent each
Adtran device to be synchronized.

### Threading Options

#### pool_size (int)

The number of threads to use when synchronizing devices.

### Device Properties

Each object contains the following properties:

#### name (str)

The name of the device. This is used to identify the device in the application's logs.

#### host (str)

The IP address or hostname of the device.

#### port (int)

The port to use when connecting to the device. If not specified, the default SSH port (22) will be used.

#### username (str)

The username to use when connecting to the device.

#### password (str)

The password to use when connecting to the device.

> **NOTICE !!!**

Device passwords are not stored in plain text and must be encrypted with the app's salt. The easiest way to do this is
to run the following command once the app's environment has been activated:

> powertran add_device [OPTIONS] NAME HOST USERNAME PLAIN-TEXT-PASSWORD ENABLED

#### enabled (bool)

If set to `False`, the device will be ignored by the application. This is useful for temporarily disabling a device.

### Example

The following is an example of a valid YAML configuration:

```
threading:
  pool_size: 10
devices:
  - name: ADTRAN-DEVICE-1
    host: 1.2.3.4
    username: ADMIN
    password: ENCRYPTED-PASSWORD-HERE
    enabled: true
  - name: ADTRAN-DEVICE-2
    host: 4.3.2.1
    port: 1022
    username: ADMIN
    password: ENCRYPTED-PASSWORD-HERE
    enabled: false
```