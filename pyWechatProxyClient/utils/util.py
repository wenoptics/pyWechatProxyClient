import inspect
import logging
import threading

import sys


def force_encoded_string_output(func):

    if sys.version_info.major < 3:

        def _func(*args, **kwargs):
            return func(*args, **kwargs).encode(sys.stdout.encoding or 'utf-8')

        return _func

    else:
        return func


def ensure_list(x, except_false=True):
    """
    若传入的对象不为列表，则转化为列表

    :param x: 输入对象
    :param except_false: None, False 等例外，会直接返回原值
    :return: 列表，或 None, False 等
    :rtype: list
    """

    if isinstance(x, (list, tuple)) or (not x and except_false):
        return x
    return [x]


def start_new_thread(target, args=(), kwargs=None, daemon=True, use_caller_name=False):
    """
    启动一个新的进程，需要时自动为进程命名，并返回这个线程

    :param target: 调用目标
    :param args: 调用位置参数
    :param kwargs: 调用命名参数
    :param daemon: 作为守护进程
    :param use_caller_name: 为 True 则以调用者为名称，否则以目标为名称

    :return: 新的进程
    :rtype: threading.Thread
    """

    if use_caller_name:
        # 使用调用者的名称
        name = inspect.stack()[1][3]
    else:
        name = target.__name__

    logging.getLogger(
        # 使用外层的 logger
        inspect.currentframe().f_back.f_globals.get('__name__')
    ).debug('new thread: {}'.format(name))

    _thread = threading.Thread(
        target=target, args=args, kwargs=kwargs,
        name=name, daemon=daemon
    )
    _thread.start()

    return _thread
