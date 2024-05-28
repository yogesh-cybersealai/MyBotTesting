#!/bin/bash
gunicorn --worker-class aiohttp.GunicornWebWorker app:APP
