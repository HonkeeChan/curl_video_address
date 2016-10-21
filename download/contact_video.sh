#!/bin/bash
ffmpeg -f concat -i list.txt -c copy output.mp4
