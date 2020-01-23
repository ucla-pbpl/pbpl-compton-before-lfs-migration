#!/bin/sh

blender --background --python blenderize.py design
blender --background --python blenderize.py gamma-20MeV
