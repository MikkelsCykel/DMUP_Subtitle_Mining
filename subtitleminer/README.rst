Subtitle Miner implementation
=============================


Installation
------------

.. code::

	python setup.py install


Terminal tool
-------------


.. code:: Terminal

	$ srtsentiment 'Pulp Fiction' '200'

	Provides a sentiment plot in three dimentions.

Module usage
------------

.. code:: Python

	>>> from subtitleminer import StampedSrt
	>>> from subtitleminer import SubtitleInIntervals
	>>> from subtitleminer import ValenceArouselDominance as vad
	>>> from subtitleminer import ImdbMiner
	>>> from subtitleminer import SubtitleDownloader
	>>> from subtitleminer.auxillary import DB, Log, System

	>>> search_movie = 'Pulp Fiction'

	>>> path = ImdbMiner().get_subtitle_name_from_title(title=search_movie)

	>>> a_formattet_srt = StampedSrt(path=path, remove_symbols=True)

	>>> devided_srt = SubtitleInIntervals(stamped_srt=a_formattet_srt, interval_sec=240, remove_stop_words=True)

	>>> computed_vad = vad().compute_vad_intervals(text_intervals=devided_srt, lmtzr_fall_back=True)

	>>> mean_vad_data = vad().mean_data(vad=computed_vad)
	>>> figure(1)
	>>> plot(range(0,len(a)), a, 'b')
	>>> plot([0,len(a)],[5.06,5.06], 'b--')
	>>> plot(range(0,len(b)), b, 'r')
	>>> plot([0,len(b)],[4.21,4.21], 'r--')
	>>> plot(range(0,len(c)), c, 'g')
	>>> plot([0,len(c)],[5.18,5.18], 'g--')
	>>> ylim([0,10])
	>>> legend(['Valence,','V.Mean', 'Arousal','A.Mean', 'Dominance','D.mean'])
	>>> show()




Creating an IMDB local database
==============================

.. code:: Python

	>>> from subtitleminer import ImdbMiner
	# fetch 10000 film from IMDB. Best films from 1974-2014
	>>> movies = ImdbMiner().fetch_imdb_releases(range=100) # fetches 100*range up to 10000.
	
	>>> for i in xrange(0, movies):
    		>>> imdbInfo = miner.fetch_imdb_info(id=info[i])
    		>>> miner.insert_imdb_info_into_db(info=imdbInfo)
	
