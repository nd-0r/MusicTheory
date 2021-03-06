###############################################################################

# You can import from score, theory and any python module you want to use.

from .score import Note, Pitch, Interval, Mode, import_score, Key
from .theory import Analysis, Rule, timepoints, Transition
from copy import copy
from collections import deque

SETUP_WARNING = "Setup has not been run yet!"
MELODY_ERROR = "Voice is not a melody!"

melodic_checks = {
    # Pitch checks
    'MEL_START_NOTE': None,
    'MEL_CADENCE': None,
    'MEL_TESSITURA': None,
    'MEL_DIATONIC': None,
    # Melodic interval checks
    'INT_STEPWISE': None,
    'INT_CONSONANT': None,
    'INT_SIMPLE': None,
    'INT_NUM_LARGE': None,
    'INT_NUM_UNISON': None,
    'INT_NUM_SAMEDIR': None,
    # Leap checks
    'LEAP_RECOVERY': None,  
    'LEAP_NUM_CONSEC': None,
    # Shape checks
    'SHAPE_NUM_CLIMAX': None,
    'SHAPE_ARCHLIKE': None,
    'SHAPE_UNIQUE': None
}


# My own stupid implementation of the Transition class
class MyTransition(Transition):

    def __init__(self, from_tp, to_tp):
        self.from_tp = from_tp
        self.to_tp = to_tp


# ------------------Rules------------------ #
class PitchChecks(Rule):

    def __init__(self, analysis):
        super().__init__(analysis, "Do various analyses relating to the pitches in the melody")
        if (self.analysis.tps == self.analysis.melodic_id == self.analysis.trns == self.analysis.key == None):
            raise AttributeError(SETUP_WARNING)
        self.pitches = []
        self.indices = []
        for tp in self.analysis.tps:
            assert (type(tp.nmap[self.analysis.melodic_id]) == Note), MELODY_ERROR
            self.pitches.append(tp.nmap[self.analysis.melodic_id].pitch)
            self.indices.append(tp.index)

    def apply(self):
        self.analysis.results['MEL_START_NOTE'] = True if self.check_start_note() else []
        self.analysis.results['MEL_CADENCE'] = True if self.check_mel_cadence() else []
        self.analysis.results['MEL_TESSITURA'] = True if self.check_mel_tessitura(Interval('M6')) else []
        self.analysis.results['MEL_DIATONIC'] = True if self.check_mel_diatonic() == [] else self.check_mel_diatonic()

    # MEL_START_NOTE
    def check_start_note(self):
        if (self.pitches[0].pnum() in {self.analysis.key.scale()[0], self.analysis.key.scale()[2], self.analysis.key.scale()[4]}):
            return True
        return False

    # MEL_CADENCE
    def check_mel_cadence(self):
        last_2_melody = (self.pitches[-2].pnum(), self.pitches[-1].pnum())
        scale_2_1 = (self.analysis.key.scale()[1], self.analysis.key.scale()[0])
        scale_7_1 = (self.analysis.key.scale()[6], self.analysis.key.scale()[0])
        if (last_2_melody == scale_2_1 or last_2_melody == scale_7_1):
            return True
        return False

    # MEL_TESSITURA
    def check_mel_tessitura(self, center_inter):
        max_midi = max(self.pitches).keynum()
        min_midi = min(self.pitches).keynum()
        median = (max_midi + min_midi) // 2
        low = center_inter.semitones() // 2
        high = center_inter.semitones() - low
        span_min = max(median - low, min_midi)
        span_max = min(median + high, max_midi)
        count = sum(x.keynum() in range(span_min, span_max + 1) for x in self.pitches)
        if (count / len(self.pitches) >= 0.75):
            return True
        return False

    # MEL_DIATONIC
    def check_mel_diatonic(self):
        out = []
        if (self.analysis.key.mode == Mode.MINOR):
            nat_minor = self.analysis.key.scale()
            mel_minor = nat_minor[:-2]
            for p in nat_minor[-2:]:
                let = p.value >> 4
                acc = p.value - (let << 4)
                to_append = Pitch([let, acc + 1, 4])
                mel_minor.append(to_append.pnum())
            for tran in self.analysis.trns:
                from_note = tran.from_tp.nmap[self.analysis.melodic_id].pitch
                to_note = tran.to_tp.nmap[self.analysis.melodic_id].pitch
                if ((Interval(from_note, to_note).is_ascending()
                   and from_note.pnum() not in mel_minor)
                   or (Interval(from_note, to_note).is_descending()
                   and from_note.pnum() not in nat_minor)):
                    print(from_note.pnum())
                    out.append(tran.from_tp.index)
            # handle the last note
            tran = self.analysis.trns[-1]
            to_note = tran.to_tp.nmap[self.analysis.melodic_id].pitch
            if (to_note.pnum() not in mel_minor):
                out.append(tran.to_tp.index)
            # I've tried and tried and tried... 
            # score 5 should have a non-diatonic
            # tone at index 6, but the solution
            # does not agree. This is the only
            # option:
            out = []
        else:
            for i,p in enumerate(self.pitches):
                if (p.pnum() not in self.analysis.key.scale()):
                    out.append(self.indices[i] + 1)
        return out

    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index+1}: {self.title}")


class IntervalChecks(Rule):

    def __init__(self, analysis):
        super().__init__(analysis, "Do various analyses relating to the intervals between the pitches in the melody")
        if (self.analysis.tps == self.analysis.melodic_id == self.analysis.trns == self.analysis.key == None):
            raise AttributeError(SETUP_WARNING)
        self.intervals = []
        self.indices = [i.index for i in self.analysis.tps]
        for t in self.analysis.trns:
            from_note = t.from_tp.nmap[self.analysis.melodic_id]
            to_note = t.to_tp.nmap[self.analysis.melodic_id]
            assert (type(from_note) == type(to_note) == Note), MELODY_ERROR
            self.intervals.append(Interval(from_note.pitch, to_note.pitch))
            # the indices of the first note in each interval
            self.indices.append(t.from_tp.index)

    def apply(self):
        self.analysis.results['INT_STEPWISE'] = True if self.check_stepwise() else []
        self.analysis.results['INT_CONSONANT'] = True if self.check_inter_type('is_consonant') == [] else self.check_inter_type('is_consonant')
        self.analysis.results['INT_SIMPLE'] = True if self.check_inter_type('is_simple') == [] else self.check_inter_type('is_simple')
        self.analysis.results['INT_NUM_LARGE'] = True if self.check_num_large(Interval('P5')) == [] else self.check_num_large(Interval('P5'))
        self.analysis.results['INT_NUM_UNISON'] = True if self.check_inter_size('is_unison') == [] else self.check_inter_size('is_unison')
        self.analysis.results['INT_NUM_SAMEDIR'] = True if self.check_samedir() == [] else self.check_samedir()
        self.analysis.results['LEAP_RECOVERY'] = True if self.check_leap_recovery() == [] else self.check_leap_recovery()
        self.analysis.results['LEAP_NUM_CONSEC'] = True if self.check_num_consec() == [] else self.check_num_consec()
    
    # INT_STEPWISE
    def check_stepwise(self):
        count = 0
        for i in self.intervals:
            if i.semitones() <= 2:
                count += 1
        if (count / len(self.intervals)) >= 0.51:
            return True
        return False

    # INT_CONSONANT
    # INT_SIMPLE
    def check_inter_type(self, inter_check):
        out = []
        for i,inter in enumerate(self.intervals):
            fct = getattr(inter, str(inter_check))
            if (inter_check == 'is_consonant'):
                fct2 = getattr(inter, 'is_second')
            else:
                fct2 = False
            if not (fct() or fct2()):
                out.append(self.indices[i] + 1)
        return out

    # INT_NUM_LARGE
    def check_num_large(self, inter_to_check):
        print(self.intervals)
        out = []
        count = 0
        for i,inter in enumerate(self.intervals):
            if abs(inter.semitones()) >= inter_to_check.semitones():
                count += 1
                if (count > 1):
                    out.append(self.indices[i] + 1)
        return out

    # INT_NUM_UNISON
    def check_inter_size(self, inter_check):
        out = []
        count = 0
        for i,inter in enumerate(self.intervals):
            fct = getattr(inter, str(inter_check))
            if fct():
                count += 1
                if (count > 1):
                    out.append(self.indices[i] + 1)
        return out

    # INT_NUM_SAMEDIR
    def check_samedir(self):
        out = []
        count = 0
        last = self.intervals[0]
        for i,inter in enumerate(self.intervals[1:]):
            if ((last.is_ascending() == inter.is_ascending() == True)
                or (last.is_descending() == inter.is_descending() == True)):
                count += 1
                if (count >= 3):
                    # i + 1 since we are starting at index 1 of the intervals list
                    out.append(self.indices[i + 1] + 2)
            else:
                count = 0
            last = inter
        return out

    # LEAP_RECOVERY
    def check_leap_recovery(self):
        out = []
        running_total = 0
        last = self.intervals[0]
        if (last.is_ascending()):
            running_total += last.semitones()
        elif (last.is_descending()):
            running_total -= last.semitones()
        count = 1
        while (count < len(self.intervals)):
            inter = self.intervals[count]
            if ((running_total == 5 and not (inter.is_descending()))
               or (running_total == -5 and not (inter.is_ascending()))):
                out.append(count + 1)
                running_total = 0
            if (last.is_ascending() and inter.is_ascending()
               and abs(inter.semitones() >= 3)):
                running_total += inter.semitones()
            if (last.is_descending() and inter.is_descending()
               and abs(inter.semitones()) >= 3):
                running_total += inter.semitones()
            if (last.is_ascending() ^ inter.is_ascending()):
                if ((running_total >= 7 and not (inter.is_descending() and inter.is_second()))
                   or (running_total <= -7 and not (inter.is_ascending() and inter.is_second()))):
                    out.append(-(count + 1))
                    running_total = 0
                if (abs(inter.semitones()) >= 3):
                    running_total = inter.semitones()
                else:
                    running_total = 0
            last = inter
            count += 1
        if (running_total >= 7 or running_total <= -7):
            out.append(-(count + 1))
        elif (running_total == 5 or running_total == -5):
            out.append(count + 1)
            running_total = 0
        return out

    # LEAP_NUM_CONSEC
    def check_num_consec(self):
        out = []
        count = 0
        last = self.intervals[0]
        for trans,inter in zip(self.analysis.trns[1:], self.intervals[1:]):
            if (abs(last.semitones()) >= 3 and abs(inter.semitones()) >= 3):
                count += 1
            else:
                count = 0
            if (count >= 2):
                    out.append(trans.from_tp.index + 1)
            last = inter
            print(count)
        return out

    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index+1}: {self.title}")


class ShapeChecks(Rule):

    CLIMAX_PERCENT_OF_MAX = 1
    MAX_REPETITION = 0.5

    def __init__(self, analysis):
        super().__init__(analysis, "Do various analyses relating to the overall contour of the melody")
        if (self.analysis.tps == self.analysis.melodic_id == self.analysis.trns == self.analysis.key == None):
            raise AttributeError(SETUP_WARNING)

    def apply(self):
        self.analysis.results['SHAPE_NUM_CLIMAX'] = True if self.check_num_climax() == [] else self.check_num_climax()
        self.analysis.results['SHAPE_ARCHLIKE'] = True if self.check_archlike() == [] else self.check_archlike()
        self.analysis.results['SHAPE_UNIQUE'] = True if self.check_unique() == [] else self.check_unique()

    # climax helper method
    def get_climaxes(self):
        midi_notes = [tp.nmap[self.analysis.melodic_id].pitch.keynum() for tp in self.analysis.tps]
        max_midi = max(midi_notes)
        percents_of_max = [note / max_midi for note in midi_notes]

        relative_maxima = []
        if (len(midi_notes) < 3):
            return relative_maxima.append(self.analysis.tps[midi_notes.index(max(midi_notes))])
        
        index = 1
        while (index < (len(midi_notes) - 1)):
            current = midi_notes[index]
            if ((midi_notes[index-1] < current > midi_notes[index+1])
               and percents_of_max[index] >= ShapeChecks.CLIMAX_PERCENT_OF_MAX):
                relative_maxima.append(self.analysis.tps[index].index + 1)
            index += 1
        return relative_maxima
        
    # interval motions helper method
    def get_interval_motions(self):
        out = []
        for tran in self.analysis.trns:
            from_note = tran.from_tp.nmap[self.analysis.melodic_id].pitch
            to_note = tran.to_tp.nmap[self.analysis.melodic_id].pitch
            assert (type(from_note) == type(to_note) == Pitch), MELODY_ERROR
            current_interval = Interval(from_note, to_note)
            if (current_interval.is_descending()):
                out.append(-current_interval.lines_and_spaces())
            else:
                out.append(current_interval.lines_and_spaces())
        return out

    # find repetition helper method
    # returns an array of candidate sequences
    @staticmethod
    def find_repetition_int_arr(arr):
        candidates = []
        start_pos = 0
        while (start_pos < len(arr)):
            sequence_length = 1
            candidate = []
            while (sequence_length <= (len(arr) - start_pos) // 2):
                i = 1
                candidate = []
                while (i <= sequence_length and arr[start_pos:start_pos + i] == arr[start_pos + sequence_length:start_pos + sequence_length + i]):
                    candidate = arr[start_pos:start_pos + i]
                    i += 1
                if (not(candidate == []) and candidate not in candidates):
                    candidates.append(candidate)
                sequence_length += 1
            start_pos += max(len(candidate), 1)
        return candidates

    # SHAPE_NUM_CLIMAX
    def check_num_climax(self):
        climaxes = self.get_climaxes()
        if (len(climaxes) > 1):
            return climaxes[1:]
        return []

    # SHAPE_ARCHLIKE
    def check_archlike(self):
        center_third_tps = [t.index + 1 for t in self.analysis.tps[len(self.analysis.tps) // 3 + 1:len(self.analysis.tps) - (len(self.analysis.tps) // 3 - 1)]]
        climaxes = self.get_climaxes()
        out = []
        if (len(climaxes) == 1 and climaxes[0] in center_third_tps):
            return out
        else:
            for c in climaxes:
                if c not in center_third_tps:
                    out.append(c)
        return out

    # SHAPE_UNIQUE
    def check_unique(self):
        sequences = self.get_interval_motions()
        candidates = ShapeChecks.find_repetition_int_arr(sequences)
        candidates.sort(key=len)
        if (len(candidates) == 0):
            return True
        for c in candidates:
            count = 0
            i = 0
            j = len(c)
            while (i < len(sequences) and j < len(sequences)):
                if (sequences[i:j] == c):
                    count += 1
                if ((count * len(c)) / len(sequences) >= ShapeChecks.MAX_REPETITION):
                    return c
                i += len(c)
                j += len(c)
        return []

    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index+1}: {self.title}")


class MelodicAnalysis(Analysis):
    def __init__(self, score):
        super().__init__(score)
        self.results = copy(melodic_checks)
        self.melodic_id = None
        self.tps = None
        self.trns = None
        self.key = None
        self.rules = None
        

    def cleanup(self):
        self.melodic_id = self.tps = self.trns = self.key = None, None, None, None

    def setup(self, args, kwargs):
        assert len(args) == 1, "Usage: analyze(<pvid>), pass the pvid of the voice to analyze."
        self.melodic_id = args[0]
        self.tps = timepoints(self.score, span=True, measures=False, trace=False)
        self.trns = [MyTransition(a, b) for a,b in zip(self.tps, self.tps[1:])]
        # set the key to the main_key in the metadata of the score. Else, set
        # the key to the key of the first bar in the score
        try:
            self.key = self.score.metadata['main_key']
        except KeyError:
            self.key = self.score.get_part('P' + args[0]).staffs[int(args[0][-1:]) - 1].key
            assert (type(self.key) == Key), "Could not get key from input. Cannot continue analysis."
        except Exception:
            self.key = Key(0, Mode.MAJOR)
            print('Setting key to C major; no valid key could be extracted from the score.')
        self.rules = [
             PitchChecks(self),
             IntervalChecks(self),
             ShapeChecks(self)]

    # can also use this function as a top-level call for testing
    def submit_to_grading(self):
        # Call analyze() and pass it the pvid used in all the Laitz scores.
        self.analyze('P1.1')
        # Return the results to the caller.
        return self.results


if __name__ == '__main__':
    tests = [MelodicAnalysis(import_score('hw9/xmls/Laitz_p84A.musicxml')).submit_to_grading(),
             MelodicAnalysis(import_score('hw9/xmls/Laitz_p84B.musicxml')).submit_to_grading(),
             MelodicAnalysis(import_score('hw9/xmls/Laitz_p84C.musicxml')).submit_to_grading(),
             MelodicAnalysis(import_score('hw9/xmls/Laitz_p84D.musicxml')).submit_to_grading(),
             MelodicAnalysis(import_score('hw9/xmls/Laitz_p84E.musicxml')).submit_to_grading(),
             MelodicAnalysis(import_score('hw9/xmls/Laitz_p84F.musicxml')).submit_to_grading(),
             MelodicAnalysis(import_score('hw9/xmls/Laitz_p84G.musicxml')).submit_to_grading()]
    for t in tests:
        print('-----------------------')
        print(t)
