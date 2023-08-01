SMALL_IMAGE_SIZE = (60, 60)

SMALL_FRAMES_VARIABLES = [
    'label_small_date',
    'label_small_image',
    'label_small_temp',
    'label_small_weather'
]

FRAME = {
    'Date': None,
    'Image': None,
    'Temp': None,
    'Weather': None
}


SMALL_FRAMES = [
    None,
    None,
    None,
    None,
    None,
    None,
    None
]
for i in range(0, 7):
    SMALL_FRAMES[i] = FRAME