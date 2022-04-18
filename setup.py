import setuptools

setuptools.setup(name='livevolpy',
        version='0.0.1',
        description='A wrapper for livevol Datashop API',
        author='Juan Marquez git@numberjuani',
        author_email='juanignaciomarquez@gmail.com',
        packages = setuptools.find_packages(),
        install_requires=[
                        'requests',
                        'urllib3'])