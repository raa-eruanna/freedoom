#!/usr/bin/env python
#
# Copyright (c) 2013 Contributors to the Freedoom project.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#  * Neither the name of the freedoom project nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
# OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# ----------------------------------------------------------------------
#
# Script to gather statistics from MIDI files about instrument usage.
# Generates stats.py which is used as input for the ultramid.ini
# generator script.
#
# This script requires python-midi; see here:
#   https://github.com/vishnubob/python-midi
#

import midi
import sys

def get_instr_stats(filename):
	"""Get a set of instruments used by the specified MIDI file."""
	result = set()
	midfile = midi.read_midifile(filename)

	for track in midfile:
		for event in track:
			if isinstance(event, midi.ProgramChangeEvent) \
			   and event.channel != 9:
				instr = event.data[0]
				result.add(instr)
			# Percussion:
			if isinstance(event, midi.NoteOnEvent) \
			   and event.channel == 9:
				instr = event.data[0] + 128
				result.add(instr)

	return result

total_stats = [0] * 217

for filename in sys.argv[1:]:
	print "Processing %s" % filename
	stats = get_instr_stats(filename)
	print sorted(stats)
	for instrument in stats:
		total_stats[instrument] += 1

with open("stats.py", "w") as f:
	f.write("# Instrument stats, autogenerated by gather_stats.py\n\n")
	f.write("INSTRUMENT_STATS = [\n\t")

	for index, stat in enumerate(total_stats):
		f.write("% 5i," % stat)
		if (index % 10) == 9:
			f.write("\n\t")

	f.write("\n]\n")


