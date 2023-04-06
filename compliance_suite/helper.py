import argparse
import logging
import logging.config
from logging.handlers import RotatingFileHandler
import socket
import os
import structlog
import zipfile
from zipfile import ZipFile
from supported_drs_versions import SUPPORTED_DRS_VERSIONS

host_ip = socket.gethostbyname("")
host_name = socket.getfqdn()


class Logger:

    def get_logger(severity, logfile, env):
        if not os.path.exists("./logs"):
            os.makedirs("./logs")

        # custom logging config
        # TODO: back up every night instead of every minute
        logging.config.dictConfig({
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {

                    "format": " %(levelname)s  %(lineno)d %(funcName)s  %(filename)s %(message)s",
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter"
                },
                "terse": {
                    "format": "%(message)s"
                }
            },
            "handlers": {
                "stream": {
                    "level": severity,
                    "class": "logging.StreamHandler",
                    "formatter": "terse",
                },
                "file": {
                    "level": "DEBUG",
                    "class": "helper.ZippedTimedRotatingFileHandler",
                    "filename": logfile,
                    "when": "midnight",
                    "backupCount": 4,
                    "utc": True,
                    "formatter": "json",
                    "encoding": "utf8"
                }
            },
            "loggers": {

                # set all library logs to "DEBUG" level
                "": {
                    "handlers": ["stream", "file"],
                    "level": "DEBUG"
                },

                # set request library logs to "CRITICAL" in order to avoid too many internal logs
                "requests": {
                    "handlers": ["file"],
                    "level": logging.CRITICAL
                }
            }
        })

        # configure structlog
        structlog.configure(
            context_class=structlog.threadlocal.wrap_dict(dict),
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.stdlib.render_to_log_kwargs]
        )

        # structlog.getLogger allows dynamic adding of optional fields to the json log
        # Example usage: logger.warning("test log",except_msg="test exception occured")
        log = structlog.getLogger(__name__)
        log = log.bind(hostnm=host_name, hostip=host_ip)
        return log

class ZippedTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    """ My rotating file hander to compress rotated file """

    def __init__(self, **kwargs):
        logging.handlers.TimedRotatingFileHandler.__init__(self, **kwargs)

    def rotate(self, source, dest):
        destination = dest.split(".")[0] + ".log"
        with ZipFile("%s.zip" % dest, "w", zipfile.ZIP_DEFLATED) as newzip:
            newzip.write("%s" % source)
        os.remove(destination)

class Parser:

    @staticmethod
    def parse_args():
        """
		define shell arguments
		server_base_url : the server url of DRS implementation that will be tested for compliance with DRS Spec
		"""
        parser = argparse.ArgumentParser(
            description="script to access DRS objects using GA4GH DRS API")
        parser.add_argument("--server_base_url",
                            required=True,
                            help="DRS server base url",
                            type=str)
        parser.add_argument("--platform_name",
                            required=True,
                            help="name of the platform hosting the DRS server",
                            type=str)
        parser.add_argument("--platform_description",
                            required=True,
                            help="description of the platform hosting the DRS server",
                            type=str)
        parser.add_argument("--log_level",
                            required=False,
                            help="display logs at or above this level",
                            type=str,
                            choices=["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"],
                            default="INFO")
        parser.add_argument("--report_path",
                            required=False,
                            help="path of the output file",
                            type=str,
                            default="./output/drs_compliance_report.json")
        parser.add_argument("--drs_version",
                            required=True,
                            help="DRS version implemented by the DRS server",
                            type=str,
                            choices=SUPPORTED_DRS_VERSIONS)
        parser.add_argument("--serve",
                            required=False,
                            help="If this flag is set, the output report is served as an html webpage",
                            action='store_true')
        parser.add_argument("--serve_port",
                            required=False,
                            type=int,
                            help="The port where the output report html is deployed",
                            default=57568)
        parser.add_argument("--config_file",
                            required=True,
                            type=str,
                            help="The File path of JSON config file. The config file must contain auth information "
                                 "for endpoints and different DRS objects")
        args = parser.parse_args()
        return (args)