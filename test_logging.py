#encoding: utf8
import logging

logger = logging.getLogger("test_logging")
logger.setLevel(logging.DEBUG)      
# 创建一个handler，用于写入日志文件
fh = logging.FileHandler("test_logging.log")
fh.setLevel(logging.DEBUG)       
# 再创建一个handler，用于输出到控制台                                   
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)     
# 定义handler的输出格式
# format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(mess
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)

if __name__ == '__main__':
    logger.debug("hello debug")
    logger.info("hello info")