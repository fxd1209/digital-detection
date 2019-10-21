#部署脚本
"""
@author  fxd
@Time    2019-10-21
"""
from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '1.0.0'

here = path.abspath(path.dirname(__file__))

# 获取README中的描述
with open('./README.txt', encoding='utf-8') as f:
    long_description = f.read()

# 获得依赖和安装包
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    name='digital_detection',
    version=__version__,
    description="Python Script to discriminate digit",
    long_description=long_description,
    url='https://github.com/fxd1209/digital-detection',
    download_url='https://codeload.github.com/fxd1209/digital-detection/zip/master',
    license='MIT',
    # classifiers=[
    #     'Development Status :: 4 - Beta',
    #     'Intended Audience :: Developers',
    #     'License :: OSI Approved :: MIT License',
    #     'Programming Language :: Python :: 2.7',
    #     'Programming Language :: Python :: 3.3',
    #     'Programming Language :: Python :: 3.4',
    #     'Programming Language :: Python :: 3.5',
    #     'Programming Language :: Python :: 3.6',
    # ],
    keywords='digital detection',
    packages=find_packages(exclude=['docs', 'tests*','images']), #此处加上src，打包后无法找到 src moduel
    include_package_data=True,
    author='fxd',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email='fxd1209@qq.com',
    entry_points={
        'console_scripts': [
            'digitdetection = src.main.main:main'
        ]},

)

# setup(
#     name="DigitalDetection",#应用名
#     version="1.0.0",#版本号
#     packages=["src"],#要打包的项目文件夹
#     include_package_data=True,#自动打包文件夹里面所有数据
#     zip_safe=True,#设定项目包为安全，不用每次都检测其安全性
#
#     #安装依赖的其他包
#     install_requires=[
#         "",
#         ""
#     ],
#
#     # 设置程序的入口为main
#     # 安装后，命令行执行main相当于调用main.py中的main方法
#     entry_points={
#         'console_scripts': [
#             'main = src.main.main:main'
#         ]
#     },
# )