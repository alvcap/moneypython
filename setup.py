from setuptools import setup

setup(name="moneypython",
      version="0.0.1",
      description="Simple currency converter",
      author="alvcap",
      author_email="kape013@gmail.com",
      url='https://github.com/alvcap/moneypython',
      packages=["moneypython"],
      provides=["moneypython"],
      license="GNU General Public License v3",

      install_requires=["requests>=2.13.0"],
      entry_points={'console_scripts':
                    ['moneypython = moneypython.converter:main']
                    },
      classifiers=[
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Topic :: Office/Business :: Financial"
      ]
      )
