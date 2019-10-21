#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File      PyVaild.py
@Time      2019-10-21
@Author    fxd
'''

class PyVaild(object):


    @staticmethod
    def isEmpty(obj):
        """
        判断是否为空,为空对象有 None,0,Flase,"",[],{},()
        :param obj: 判断对象
        :return: bool
        """
        return (bool(obj))


if __name__=="__main__":
    pass
