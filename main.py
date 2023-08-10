import psychopy.visual
import psychopy.event
import psychopy.sound
import psychopy.core
import random
import csv
from psychopy.gui import Dlg


def get_participant_details():
    """Get and return the details of the participant."""
    dlg = Dlg(title="Experiment Details")
    dlg.addField('Participant Number:')
    dlg.addField('Session Number:')
    dlg.show()
    if dlg.OK:
        return dlg.data
    else:
        exit()

def show_message(message, duration=2.0):
    """Display a message on screen for a given duration."""
    text_stim = psychopy.visual.TextStim(win, text=message, height=0.1)
    text_stim.draw()
    win.flip()
    psychopy.core.wait(duration)
    win.flip()

def present_feedback(text, color, duration=1):
    """Present feedback to the participant."""
    feedback = psychopy.visual.TextStim(win, text=text, color=color, height=0.1)
    feedback.draw()
    win.flip()
    psychopy.core.wait(duration)

def present_visual_stimulus(duration):
    """Present a visual stimulus."""
    gaussian = psychopy.visual.GratingStim(win, tex='sin', mask='gauss', size=2.5, pos=[0, 0], sf=0)
    gaussian.draw()
    win.flip()
    psychopy.core.wait(duration)
    win.flip()

def present_audio_stimulus(duration):
    """Present an auditory stimulus."""
    global sound
    sound = psychopy.sound.Sound(value=1000, sampleRate=44100, secs=duration/1000.0, stereo=True)
    sound.play()
    psychopy.core.wait(duration / 1000.0)

def run_trial(stim_type, duration):
    """Run a single trial."""
    if stim_type == 'visual':
        present_visual_stimulus(duration / 1000.0)
    else:
        present_audio_stimulus(duration / 1000.0)

    # collect responses
    timer = psychopy.core.Clock()
    keys = psychopy.event.waitKeys(maxWait=5.0, keyList=['space'], timeStamped=timer)
    
    if keys:
        response_time = keys[0][1] * 1000  # Convert to ms
        if 0.9 * duration <= response_time <= 1.1 * duration:
            present_feedback(str(duration), 'green')
        else:
            present_feedback(str(duration), 'red')
        return response_time
    else:
        return None

def main():
    """Main function to run the experiment."""
    global win, sound    

    # Configurations
    repetitions = 2
    durations_short = [450]  # durations_short = [450, 500, 550, 600, 650, 700]         
    durations_long = [700]   # durations_long = [700, 750, 800, 850, 900, 950]       

    # Participant details
    participant_number, session_number = get_participant_details()

    # init window and Sound
    win = psychopy.visual.Window(fullscr=True, color='grey')
    sound = psychopy.sound.Sound(value=1000, sampleRate=44100, secs=1.0, stereo=True)
    
    # Warn that the test is starting
    show_message("The test is starting. Please wait...", 3.0)

    conditions = [('visual', 'short'), ('auditory', 'long'), ('visual', 'long'), ('auditory', 'short')]

    responses = []

    for condition in conditions:
        modality, duration_type = condition
        if duration_type == 'short':
            durations = durations_short
        else:
            durations = durations_long

        for _ in range(repetitions):
            for duration in durations:
                response_time = run_trial(modality, duration)
                responses.append({
                    'ParticipantNumber': participant_number,
                    'SessionNumber': session_number,
                    'Modality': modality,
                    'Duration': duration,
                    'ResponseTime': response_time,
                    'Condition': duration_type
                })

    # Warn that the test has ended
    show_message("Thank you! The test has ended.", 3.0)

    # Saving data into a csv file
    filename = f'participant_{participant_number}_session_{session_number}_responses.csv'
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['ParticipantNumber', 'SessionNumber', 'Modality', 'Duration', 'ResponseTime', 'Condition']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for response in responses:
            writer.writerow(response)

    win.close()

if __name__ == '__main__':
    main()
