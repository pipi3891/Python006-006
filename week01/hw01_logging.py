#!/usr/bin
#coding:utf-8
import logging
from pathlib import Path
import time

pre_logpath = "/Users/stellashi/works/geek_test/"


def log_test(pre_path):
    s_date =time.strftime("%Y-%m-%d",time.localtime())
    log_file = ""
    log_path = pre_path+"python-"+s_date
    p_log = Path(log_path)
    if p_log.is_dir():
        log_file = log_path+"/pathliblog.log"
    else:
        p_log.mkdir()
        log_file = log_path + "/pathliblog.log"
    Path(log_file).touch(mode=0o666, exist_ok=True)

    logging.basicConfig(filename=log_file,filemode='a',
                        format='%(asctime)s-%(name)s-[%(levelname)s]-[%(lineno)d]-%(message)s',
                        datefmt='[%y/%m/%d %H:%M:%S]',
                        level=logging.DEBUG)
    logging.warning('WARN LOG')
    logging.info("INFO LOG")
    logging.debug('DEUBG LOG')
    logging.error('ERROR LOG')
    logging.critical("CRITICAL LOG")

    #print log_file


if __name__ == '__main__':
    log_test(pre_logpath)