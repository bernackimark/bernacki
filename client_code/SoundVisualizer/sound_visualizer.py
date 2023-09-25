import anvil.facebook.auth
import anvil.server
# import pygame
# pygame.mixer.init()

SOUNDS_FOLDER = '/Users/Bernacki_Laptop/PycharmProjects/Bernacki_UI/assets/sound_visualizer/'


class Shape:
    """Shape is separate from Piece, because Shape is a concept of the UI
    tkinter, HTML Canvas, Anvil Canvas may all be different.  I'm not 100% sure that's actually correct, and if not,
    a single class could be easier?"""
    def __init__(self, name: str, height: int, width: int, fill: str = 'black', line_width: int = 1):
        self.name = name
        self.height = height
        self.width = width
        self.main_fill = fill
        self.alt_fill = 'white'
        self.fill = self.main_fill
        self.line_width = line_width

    def __repr__(self):
        return f'{self.name} {self.height} {self.width} {self.fill} {self.line_width}'

    def set_main_fill(self):
        self.fill = self.main_fill

    def set_alt_fill(self):
        self.fill = self.alt_fill

    def switch_fill(self):
        self.fill = self.alt_fill if self.fill == self.main_fill else self.main_fill


shapes = ['rect', 'circle']


class Piece:
    opposite_direction = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}

    def __init__(self, piece_id: int, height: int, width: int, x: int, y: int, shape: str, *,
                 fill, line_width, sound: str, direction: str):
        self.piece_id = piece_id
        self.x = x
        self.y = y
        self.shape: Shape = Shape(shape, height, width, fill, line_width)
        self.sound = sound
        self.direction = direction
        self.speed = self.piece_id + 1
        self.had_collision_last_frame = False

    # is this better off in a separate class for when the audio engine changes?
    # should it just pass an audio file and delegate the playing of the sound to the Audio Engine
    def play_sound(self):
        print(f'{self.piece_id} makes sound {self.sound}')
        # file = pygame.mixer.Sound(self.sound)
        # pygame.mixer.Channel(self.piece_id).play(file)

    def move_to(self, new_x: int, new_y: int):
        self.x, self.y = new_x, new_y

    # this doesn't support any non-cardinal movement
    def move(self, distance: int = 1):
        if self.direction == 'left':
            self.x -= distance * self.speed
        elif self.direction == 'right':
            self.x += distance * self.speed
        elif self.direction == 'up':
            self.y -= distance * self.speed
        elif self.direction == 'down':
            self.y += distance * self.speed
        if self.has_collided:
            self.handle_collision()
        else:
            self.had_collision_last_frame = False
            self.shape.set_main_fill()

    def change_direction(self):
        self.direction = Piece.opposite_direction[self.direction]

    # thinking of projectJDM scenes, a collision doesn't always change direction, it could just play a sound.
    # so then are the collision steps part of another object for Wall/Boundary/Marker?
    # has_collided can stay in the Piece class, i think.
    def handle_collision(self):
        self.had_collision_last_frame = True
        self.shape.set_alt_fill()
        self.change_direction()
        self.play_sound()
        # self.shape.switch_fill()  # can't switch back because it's in the same frame. would have to be another trx

    @property
    def has_collided(self) -> bool:
        if self.x <= 0 and self.direction == 'left':
            print(f'{self.piece_id} collided with left wall at ({self.x}, {self.y})')
            return True
        if self.y <= 0 and self.direction == 'up':
            print(f'{self.piece_id} collided with top wall at ({self.x}, {self.y})')
            return True
        if self.x + self.shape.width >= sv.window_width and self.direction == 'right':
            print(f'{self.piece_id} collided with right wall at ({self.x}, {self.y})')
            return True
        if self.y + self.shape.height >= sv.window_height and self.direction == 'down':
            print(f'{self.piece_id} collided with top wall at ({self.x}, {self.y})')
            return True
        return False


scenes = [
    {'id': 1, 'name': 'Simple Up & Down', 'initial_direction': 'down', 'piece_cnt': 7, 'x_offset': 50, 'y_offset': 0},
    {'id': 2, 'name': 'Simple Side to Side', 'initial_direction': 'right', 'piece_cnt': 7, 'x_offset': 0, 'y_offset': 30}
]


def get_dict_from_list_of_dicts(lod: list[dict], id: int):
    return [entry for entry in lod for k, v in entry.items() if k == 'id' and v == id][0]


def get_value_from_id_from_list_of_dicts(lod: list[dict], id: int, key: str):
    return [entry[key] for entry in lod for k, v in entry.items() if k == 'id' and v == id][0]


chords = {
    'major': [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23],
    'minor': [0, 2, 3, 5, 7, 8, 10, 12, 14, 15, 17, 19, 20, 22],
    'major_7': [0, 4, 7, 11, 12, 16, 19, 23],
    'major_9': [0, 4, 7, 12, 14, 16, 19],
    'major_13': [0, 4, 5, 10, 16, 17, 19],
    'minor_9': [0, 3, 7, 10, 12, 14, 15, 19],
    'minor_maj9': [0, 3, 7, 12, 14, 15, 19]
}

speeds = {'slow': 0.75, 'medium': 1, 'fast': 1.25}


def get_sounds(instrument: str, chord: str, note_cnt: int) -> list[str]:
    degree_priority = (1, 5, 3, 7, 6, 4, 2, 8)
    notes = sorted([chords.get(chord)[n-1] for idx, n in enumerate(degree_priority) if idx < note_cnt], reverse=True)
    return [f'{SOUNDS_FOLDER}{instrument}/key{n}.mp3' for n in notes]


color_schemes = {
        'primary': ['red', 'blue', 'green'],
        'rainbow': ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'],
        'maroon_tones': ['#891616', '#8c2121', '#8e2e2e', '#8e3b3b', '#8c4a4a', '#8a5b5b', '#866d6d', '#808080'],
        'gold_tones': ['#c19c53', '#b99859', '#b0945f', '#a79165', '#9d8c6b', '#948872', '#8a8479', '#808080']
    }


class SoundVisualizer:
    def __init__(self, speed: str, color_scheme: str, chord: str, instrument: str, scene_id: int):
        self.state = 'playing'
        self.window_height = 430
        self.window_width = 430
        self.piece_height = 10
        self.piece_width = 30
        self.piece_shape = 'rect'
        self.speed = speeds[speed]
        self.scene_dict: dict = get_dict_from_list_of_dicts(scenes, scene_id)
        self.initial_direction = self.scene_dict['initial_direction']
        self.piece_cnt = 7

        self.starting_positions: list[tuple[int, int]] = self.get_starting_positions()

        # can i automatically set the starting positions based on piece_cnt, initial_direction and window size?

        self.colors: list[str] = color_schemes[color_scheme]
        self.sounds: list[str] = get_sounds(instrument, chord, self.piece_cnt)

        self.pieces: list[Piece] = []

        for i in range(self.piece_cnt):
            self.pieces.append(Piece(i, self.piece_height, self.piece_width,
                                     self.starting_positions[i][0], self.starting_positions[i][1], self.piece_shape,
                                     fill=self.colors[i], line_width=1, sound=self.sounds[i],
                                     direction=self.initial_direction))

    def play(self):
        self.state = 'playing'
        [p.move() for p in self.pieces]

    def pause(self):
        self.state = 'paused'

    @property
    def piece_positions(self):
        return [(p.x, p.y) for p in self.pieces]

    def get_starting_positions(self) -> list[tuple[int, int]]:
        pass
        if self.initial_direction in ['up', 'down']:
            return [(int(self.window_width / self.piece_cnt * i), 0) for i in range(self.piece_cnt)]
        elif self.initial_direction in ['left', 'right']:
            return [(0, int(self.window_height / self.piece_cnt * i)) for i in range(self.piece_cnt)]


# sv = SoundVisualizer('medium', 'maroon_tones', 'minor_9', 'piano', 1)

sv: SoundVisualizer

# print(sv.piece_positions)
# for i in range(10):
#     sv.play()
#     print(sv.piece_positions)
