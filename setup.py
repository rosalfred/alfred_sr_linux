## ! DO NOT MANUALLY INVOKE THIS setup.py, USE CATKIN INSTEAD

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

# fetch values from package.xml
setup_args = generate_distutils_setup(
    packages = ['alfred_sr_linux'],
    package_dir={'': 'src'},
    requires=['media_msgs', 'std_msgs', 'rospy'])

setup(**setup_args)
