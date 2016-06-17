======================================
A lightweight online learning platform
======================================

WARNING: this is pre alpha code, pretty much a work-in-progress during the Open edX Conference 2016 `hackathon <https://openedx.atlassian.net/wiki/display/OPEN/Hackathon+the+13th%3A+Part+III>`_.

The goal is to create an extensible, lightweight platform for running online courses, based on the Open edX XBlock runtime.

Make sure a redis server is running and configure the right port in `dietx/settings.py`::

    redis-server --port 6381

Get running::

    pip install -r requirements.txt
    ./runserver.py
    # Or run in debug mode
    FLASK_DEBUG=1 ./runserver.py
