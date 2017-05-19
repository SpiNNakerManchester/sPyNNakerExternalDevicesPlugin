from setuptools import setup
from collections import defaultdict
import os

__version__ = None
exec(open("spynnaker_external_devices_plugin/_version.py").read())
assert __version__

# Build a list of all project modules, as well as supplementary files
main_package = "spynnaker_external_devices_plugin"
data_extensions = {".aplx", ".xml"}
main_package_dir = os.path.join(os.path.dirname(__file__), main_package)
start = len(main_package_dir)
packages = []
package_data = defaultdict(list)
for dirname, dirnames, filenames in os.walk(main_package_dir):
    if '__init__.py' in filenames:
        package = "{}{}".format(
            main_package, dirname[start:].replace(os.sep, '.'))
        packages.append(package)
    for filename in filenames:
        _, ext = os.path.splitext(filename)
        if ext in data_extensions:
            package = "{}{}".format(
                main_package, dirname[start:].replace(os.sep, '.'))
            package_data[package].append("*{}".format(ext))
            break

url = "https://github.com/SpiNNakerManchester/sPyNNakerExternalDevicesPlugin"

setup(
    name="sPyNNakerExternalDevicesPlugin",
    version=__version__,
    description="Spinnaker External Devices Plugin",
    url=url,
    packages=packages,
    package_data=package_data,
    # Same as pynn_0.8 branch
    # This need changing back to master version+? before/when pushing to master
    install_requires=['sPyNNaker >= 1!4.0.0a5, < 1!5.0.0']
)
