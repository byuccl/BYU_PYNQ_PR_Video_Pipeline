#   Copyright (c) 2016, Xilinx, Inc.
#   All rights reserved.
# 
#   Redistribution and use in source and binary forms, with or without 
#   modification, are permitted provided that the following conditions are met:
#
#   1.  Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer.
#
#   2.  Redistributions in binary form must reproduce the above copyright 
#       notice, this list of conditions and the following disclaimer in the 
#       documentation and/or other materials provided with the distribution.
#
#   3.  Neither the name of the copyright holder nor the names of its 
#       contributors may be used to endorse or promote products derived from 
#       this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
#   THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
#   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
#   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#   OR BUSINESS INTERRUPTION). HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
#   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
#   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
#   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

__author__ = "Andrew Elbert Wilson"
__copyright__ = "GPL"
__email__ = "Andrew.E.Wilson@byu.edu"

from setuptools import setup, find_packages
import shutil
import subprocess
import sys
import os
from datetime import datetime

GIT_DIR = os.path.dirname(os.path.realpath(__file__))



# Install packages
def install_packages():
    subprocess.check_call(['apt-get', '--yes', '--force-yes', 'install']),
    subprocess.check_call(['pip3.6', 'install'])
    print("Installing packages done ...")


# Notebook delivery
def fill_notebooks():
    src_nb = GIT_DIR + '/Video_notebooks'
    dst_nb_dir = '/home/xilinx/jupyter_notebooks/PR_Video_Demo'
    if os.path.exists(dst_nb_dir):
        shutil.rmtree(dst_nb_dir)
    shutil.copytree(src_nb, dst_nb_dir)

    print("Filling notebooks done ...")


if len(sys.argv) > 1 and sys.argv[1] == 'install':
    install_packages()
    fill_notebooks()


def package_files(directory):
    paths = []
    for (path, directories, file_names) in os.walk(directory):
        for file_name in file_names:
            paths.append(os.path.join('..', path, file_name))
    return paths


extra_files = package_files('video')


setup(name='BYU_PYNQ_PR_Video_Pipeline',
      version='2.1',
      description='BYU PYNQ PR Video Pipeline package',
      author='BYU CCL',
      author_email='Andrew.E.Wilson@byu.edu',
      url='https://github.com/byuccl/BYU_PYNQ_PR_Video_Pipeline.git',
      packages=find_packages(),
      download_url='https://github.com/byuccl/BYU_PYNQ_PR_Video_Pipeline.git',
      package_data={
          '': extra_files,
      }
      )

