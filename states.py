from aiogram.fsm.state import State, StatesGroup


class CreateNotepad(StatesGroup):
    input_notepad_title = State()

class CreateLecture(StatesGroup):
    input_lucture_title_and_number = State()
    sending_images = State()
    add_image_to_lecture = State()


