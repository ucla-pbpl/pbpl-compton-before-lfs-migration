#!/bin/sh

# run headless blender jobs!
blender --background --python blenderize.py design
blender --background --python blenderize.py gamma-20MeV
blender --background --python blenderize.py gamma-2GeV
