Subtitle Miner implementation
=============================


Installation
------------

.. code::

    python setup.py install


Usage
-----


.. code:: Terminal

    $ srtsentiment 'Pulp Fiction' '200'

    Provides a sentiment plot in three dimentions.

.. code:: Python

	>>> from subtitleminer import StampedSrt
	>>> from subtitleminer import SubtitleInIntervals
	>>> from subtitleminer import ValenceArouselDominance
	>>> from subtitleminer import ImdbMiner
	>>> from subtitleminer import SubtitleDownloader
	>>> from subtitleminer.auxillary import DB, Log, System
