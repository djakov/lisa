#! /usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
#
# Copyright (C) 2018, Arm Limited and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys
import itertools
from setuptools import setup, find_namespace_packages


with open('README.rst', 'r') as f:
    long_description = f.read()

with open('LICENSE.txt', 'r') as f:
    license_txt = f.read()

with open("lisa/version.py") as f:
    version_globals = dict()
    exec(f.read(), version_globals)
    lisa_version = version_globals['__version__']

packages = find_namespace_packages(where='lisa', include=['lisa*'])
package_data = {
    package: ['*']
    for package in packages
    if package.startswith('lisa.assets.')
}
package_data['lisa.assets'] = ['*']

extras_require={
    "notebook": [
        "jupyterlab",
        "ipympl", # For %matplotlib widget under jupyter lab
        "sphobjinv", # To open intersphinx inventories
    ],

    "dev": [
        "pytest",
        "build",
        "twine",
    ],

    "wa": [
        "wlauto",
    ],
}

extras_require["doc"] = [
    "sphinx >= 1.8",
    "sphinx_rtd_theme",
    "sphinxcontrib-plantuml",
    "nbsphinx",

    # Add all the other optional dependencies to ensure all modules from lisa
    # can safely be imported
    *itertools.chain.from_iterable(extras_require.values())
]

setup(
    name='lisa-linux',
    license='Apache License 2.0',
    version=lisa_version,
    maintainer='Arm Ltd.',
    packages=packages,
    url='https://github.com/ARM-software/lisa',
    project_urls={
        "Bug Tracker": "https://github.com/ARM-software/lisa/issues",
        "Documentation": "https://lisa-linux-integrated-system-analysis.readthedocs.io/",
        "Source Code": "https://github.com/ARM-software/lisa",
    },
    description='A stick to probe the kernel with',
    long_description=long_description,
    python_requires='>= 3.6',
    install_requires=[
        "psutil >= 4.4.2",
        # Figure.savefig() (without pyplot) does not work in matplotlib <
        # 3.1.0, and that is used for non-interactive plots when building the
        # doc.
        "matplotlib >= 3.1.0",
        # Pandas >= 1.0.0 has support for new nullable dtypes
        # Pandas 1.2.0 has broken barplots:
        # https://github.com/pandas-dev/pandas/issues/38947
        "pandas >= 1.0.0",
        "numpy",
        "scipy",
        # Earlier versions have broken __slots__ deserialization
        "ruamel.yaml >= 0.16.6",
        # For the HTML output of analysis plots
        "docutils",
        # For pandas.to_parquet() dataframe storage
        "pyarrow",

        "ipython",
        "ipywidgets",
        "mplcursors",

        # Depdendencies that are shipped as part of the LISA repo as
        # subtree/submodule
        "devlib",
    ],

    extras_require=extras_require,
    package_data=package_data,
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        # This is not a standard classifier, as there is nothing defined for
        # Apache 2.0 yet:
        # https://pypi.org/classifiers/
        "License :: OSI Approved :: Apache Software License 2.0 (Apache-2.0)",
        # It has not been tested under any other OS
        "Operating System :: POSIX :: Linux",

        "Topic :: System :: Operating System Kernels :: Linux",
        "Topic :: Software Development :: Testing",
        "Intended Audience :: Developers",
    ],
    entry_points={
        'console_scripts': [
            'lisa-conf-cat=lisa.tools.lisa_conf_cat:main',
            'lisa-platinfo-extract=lisa.tools.lisa_platinfo_extract:main',
            'lisa-plot=lisa.tools.lisa_plot:main',
        ],
    },
)

# vim :set tabstop=4 shiftwidth=4 textwidth=80 expandtab
