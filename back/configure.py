import logging

ENLIGHTENING_VALUE = 400

# 创建一个logger
ztz_logger = logging.getLogger('ztz')
ztz_logger.setLevel(logging.DEBUG)
# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('test.log', encoding='utf-8')
fh.setLevel(logging.DEBUG)
# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(message)s')
fh.setFormatter(formatter)
# 给logger添加handler
ztz_logger.addHandler(fh)

if __name__ == "__main__":
    pass
