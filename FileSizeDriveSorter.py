"""
This program takes a list of folder/file sizes and drive sizes and places them in the correct drives.

"""

import itertools

BYTE_MULTIPLIER = 1000 # Use 1000 for human-readable sizes and 1024 for actual bit sizes
SIZE_MULTIPLIERS = {
    "b": 1,
    "kb": BYTE_MULTIPLIER,
    "mb": BYTE_MULTIPLIER**2,
    "gb": BYTE_MULTIPLIER**3,
    "tb": BYTE_MULTIPLIER**4,
    "pb": BYTE_MULTIPLIER**5,
} # How many bytes each unit stands for

DRIVE_FILL_SPACE = 0.85 # Percentage of the drive that we consider usable
DISPLAY_UNIT = "GB"

def parse_text(text):
    text = text.lower()
    text = text.split(" ")
    size = int(float(text[0]) * SIZE_MULTIPLIERS[text[1]])
    return size

def size_to_text(byte_number, unit):
    return "%s %s" % (str(byte_number / SIZE_MULTIPLIERS[unit.lower()]), unit.upper())

drive_sizes = ["465 GB", "298 GB"]
file_folder_objects = [
    {'name':'foo', 'size':'40 GB'},
    {'name':'bar', 'size':'300 GB'},
    {'name':'reallybigfile', 'size':'90 TB'}
]

drive_sizes = [parse_text(drive_size) for drive_size in drive_sizes]
file_folder_objects = [{"size":parse_text(file_folder_object['size']), "name":file_folder_object['name']} for file_folder_object in file_folder_objects]

drive_spaces_filled = []
end_result = []

for current_drive in range(len(drive_sizes)): # Find the combination of files/folders that utilizes the maximum amount of space on the next drive.
    possible_combinations = itertools.combinations(file_folder_objects, len(file_folder_objects))
    fill_choice = {"used space":0, "files":[]}
    for permutation in possible_combinations:
        current_size = 0
        current_objects = []
        for file_folder_object in permutation:
            if current_size + file_folder_object['size'] < drive_sizes[current_drive] * DRIVE_FILL_SPACE: # We can fit this file, add it
                current_size += file_folder_object['size']
                current_objects.append(file_folder_object)

        if current_size > fill_choice["used space"]:  # We have found a new best permutation
            fill_choice = {"used space": current_size, "files": current_objects}

    for current_object in fill_choice['files']: # Get rid of each object so we don't try to put it on another drive
        file_folder_objects.remove(current_object)
    end_result.append(fill_choice) # Add our result for this drive to the end result

# Print end result
for drive_number in range(len(end_result)):
    print("DRIVE %s | %s / %s | %s%%" % (
        drive_number+1,
        size_to_text(end_result[drive_number]["used space"], DISPLAY_UNIT),
        size_to_text(drive_sizes[drive_number], DISPLAY_UNIT),
        round(end_result[drive_number]["used space"] / drive_sizes[drive_number] * 100, 2)
    ))

    for file in end_result[drive_number]['files']:
        print("    %s | '%s'" % (size_to_text(file['size'], DISPLAY_UNIT), file['name']))
    print()

if len(file_folder_objects) > 0: # There are files left
    print("WARNING: NOT ALL THE FILES COULD FIT ON THESE DRIVES. THESE FILES REMAIN:")

    for file in file_folder_objects:
        print("    %s | '%s'" % (size_to_text(file['size'], DISPLAY_UNIT), file['name']))