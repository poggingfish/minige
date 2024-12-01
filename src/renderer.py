from pyray import *
import PIL.Image
import json
from io import BytesIO
import base64
import lupa.lua52
import random

scale = 20
try:
    rooms = json.load(open("data/rooms.json", "r"))
except FileNotFoundError:
    print("There is no game in this directory..")
    exit(1)
globals = None
current_room = ""
song_name = ""
current_animation = None

def render_to_texture(texture, imdata, layer_width, locationx, locationy):
    global scale
    h = 0
    v = 0
    begin_texture_mode(texture)
    for i in imdata:
        draw_rectangle(h+(locationx*scale), (v-scale)+locationy*scale, scale, scale, i)
        h += scale
        if h >= layer_width:
            h = 0
            v += scale
    end_texture_mode()

class Animation:
    frames = []
    cf = 0
    tbf = 0
    tbfc = 0

    def __init__(self, gif, tbf):
        self.tbf = tbf
        self.frames = []
        g = PIL.Image.open("data/anim/"+gif+".gif")
        i = 0
        while True:
            try:
                g.seek(i)
            except EOFError:
                break
            frame = g.convert('RGBA')
            frame = frame.rotate(180)
            frame = frame.transpose(PIL.Image.Transpose.FLIP_LEFT_RIGHT)
            t = load_render_texture(meta["width"]*scale, meta["height"]*scale)
            l = list(frame.getdata())
            render_to_texture(t, l, meta["width"]*scale, 0, 1)
            self.frames.append(t)
            i += 1
    def unload(self):
        for i in self.frames:
            unload_render_texture(i)
    def render(self):
        r = False
        if self.tbfc > self.tbf:
            self.tbfc = 0
            self.cf += 1
        if self.cf >= len(self.frames):
            self.cf = 0
            r = True
        frame = self.frames[self.cf]
        draw_texture_rec(frame.texture, (0, 0, frame.texture.width, frame.texture.height), (0, 0), WHITE)
        self.tbfc += 1
        return r
class Room:
    layers = {}
    name = ""

    def __init__(self, name):
        global room_colliders, lua_ctx, globals, current_room, a
        layers = rooms[name]
        self.name = name
        current_room = self.name
        room_colliders = []
        for l in layers:
            if l == "METADATA":
                continue
            layer = layers[l]
            layer_width = layer["size"][0]*scale
            layer_height = layer["size"][1]*scale
            img = PIL.Image.open(BytesIO(base64.b85decode(layer["img_data"])))
            imdata = list(img.getdata())
            render_to_texture(room_texture, imdata, layer_width, layer["location"][0], layer["location"][1])
            room_colliders.append(
                {
                    "name": l,
                    "rec": [
                        layer["location"][0]*scale,
                        layer["location"][1]*scale,
                        layer_width,
                        layer_height
                    ]
                }
            )
        room_colliders.reverse()
        if lua_ctx != None:
            globals = lua_ctx.eval("globals")
        lua_script = get_lua_script(name)
        lua_ctx = lupa.lua52.LuaRuntime()
        f = lua_ctx.eval("""function(glbl)
                            _G.globals = glbl
                        end""")
        f(globals if globals != None else {})
        if lua_script != None:
            lua_ctx.execute(get_lua_script("std"))
            lua_ctx.execute(lua_script)
            f = lua_ctx.eval("Init")
            if f != None:
                e = f()
                for i in e:
                    action = e[i]
                    a.append(Action(action.type, action.value, action.value2, action.value3))
        self.unload()

    def unload(self):
        for i in self.layers:
            unload_render_texture(self.layers[i]["texture"])
    def __enter__(self, *args):
        return self

    def __exit__(self, *args):
        self.unload()

class Action:
    type = ""
    value = ""
    value2 = ""
    value3 = ""

    def __init__(self, type, value, value2, value3):
        self.type = type
        self.value = value
        self.value2 = value2
        self.value3 = value3
meta = rooms[list(rooms.keys())[0]]["METADATA"]
room_texture = None

def get_lua_script(room):
    try:
        return open(f"data/scripts/{room}.lua").read()
    except:
        print(f"NO FILE {room}.lua!")
        return None

def load_room_all(cr):
    global room_colliders
    global lua_ctx

tstb = 0
new_room = None
room_texture = None
room_colliders = []
lua_ctx = None
italic = False
room_before_pause = ""
exit_window = False
music = None
animation_repeat_times = 0
animation_played = 0
def render(sel):
    global tstb, new_room, room_texture, room_colliders, lua_ctx, a, italic, exit_window, room_before_pause, music, song_name, current_animation
    global animation_repeat_times, animation_played
    clear_background(DARKGRAY)
    draw_texture_rec(room_texture.texture, (0, 0, room_texture.texture.width, -room_texture.texture.height), (0, 0), WHITE)
    if current_animation != None:
        if current_animation.render():
            animation_played += 1
            if animation_played >= animation_repeat_times:
                current_animation.unload()
                current_animation = None
                animation_repeat_times = 0
                animation_played = 0
                a.pop(0)
        sel = "Animation Playing"
    draw_text_ex(pixel_font, sel.replace("_", " "), [
        0,
        window_height*0.91
    ], window_height*0.08, 2, YELLOW)
    if len(a) > 0:
        action = a[0]
        if action.type == "TextBox":
            tstb += get_frame_time()
            draw_rectangle(0, int(window_height*0.72), window_width, int(window_height*0.28), (0, 0, 0, 244))
            draw_text_ex(pixel_font, action.value2, [
                0,
                window_height*0.73
            ], window_height*0.065, 1, YELLOW)
            draw_text_ex(pixel_font if not italic else italic_font, 
                         action.value, [
                0,
                window_height*0.80
            ], window_height*0.045, 1, WHITE if not italic else GREEN)
            if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT) and tstb >= 0.35:
                tstb = 0
                a.pop(0)
        elif action.type == "Goto":
            new_room = action.value
            a.pop(0)
        elif action.type == "Italic":
            italic = not italic
            a.pop(0)
        elif action.type == "Quit":
            exit_window = True
            a.pop(0)
        elif action.type == "Save":
            glbl = dict(globals)
            for i in glbl:
                if str(type(glbl[i])) == "<class 'lupa.lua52._LuaTable'>": # Stupid hack...
                    glbl[i] = dict(glbl[i])
            sv = {
                "globals": glbl,
                "room": room_before_pause,
                "song": song_name
            }
            with open("save.json", "w") as save:
                json.dump(sv, save)
            a.pop(0)
        elif action.type == "Back":
            new_room = room_before_pause
            room_before_pause = ""
            a.pop(0)
        elif action.type == "Music":
            if music != None:
                unload_music_stream(music)
                music = None
            music = load_music_stream("data/audio/" + action.value + ".ogg")
            song_name = action.value
            play_music_stream(music)
            a.pop(0)
        elif action.type == "Animation" and animation_repeat_times == 0:
            if current_animation != None:
                current_animation.unload()
                current_animation = None
                animation_repeat_times = 0
                animation_played = 0
            current_animation = Animation(action.value, action.value3)
            animation_repeat_times = action.value2
            
            
    mp = get_mouse_position()
    draw_crosshair(mp)
a = []
def update():
    global a, tstb, new_room, room_texture, room_colliders, lua_ctx, room_before_pause, music
    if music != None:
        update_music_stream(music)
    sel = "Nothing"
    mp = get_mouse_position()
    if new_room != None:
        Room(new_room)
        new_room = None
    if is_key_pressed(KeyboardKey.KEY_ESCAPE) and a == [] and room_before_pause == "":
        room_before_pause = current_room
        Room("pause")
    for i in room_colliders:
        if check_collision_recs(i["rec"], [mp.x, mp.y+scale, 1, 1]):
            sel = i["name"]
            break
    if a == [] and is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
            f = lua_ctx.eval(sel + "Clicked")
            if f != None:
                e = f()
                for i in e:
                    action = e[i]
                    a.append(Action(action.type, action.value, action.value2, action.value3))
    return sel

def try_load_save():
    global globals
    try:
        with open("save.json", "r") as save:
            s = json.load(save)
            globals = s["globals"]
            Room(s["room"])
            if s["song"] != "":
                a.append(Action("Music", s["song"], None, None))

        return True
    except Exception as e:
        return False

def init():
    global new_room, room_texture, room_colliders, lua_ctx
    if try_load_save() != True:
        Room("room")

ca = 5
c = ca
def draw_crosshair(mp):
    global c, ca
    color = [
        c,
        c,
        c,
        255
    ]
    color2 = [
        abs(c - 255),
        abs(c - 255),
        abs(c - 255),
        255
    ]
    draw_line_ex([mp.x-scale, mp.y], [mp.x, mp.y], 4, color)
    draw_line_ex([mp.x, mp.y+scale], [mp.x, mp.y], 4, color)
    draw_line_ex([mp.x, mp.y-scale], [mp.x, mp.y], 4, color2)
    draw_line_ex([mp.x+scale, mp.y], [mp.x, mp.y], 4, color2)
    if c > 255-ca or c <= 0:
        ca = -ca
    c += ca

if __name__ == "__main__":
    set_trace_log_level(TraceLogLevel.LOG_WARNING)
    window_width = meta["width"]*scale
    window_height = meta["height"]*scale+int((meta["height"]*scale)/10) 
    init_window(window_width, window_height, "Mini GE 0.0.1")
    set_target_fps(60)
    init_audio_device()
    set_exit_key(0)
    pixel_font = load_font("data/pixel.ttf")
    italic_font = load_font("data/italics.ttf")
    room_texture = load_render_texture(meta["width"]*scale, meta["height"]*scale)
    init()
    hide_cursor()
    while (not exit_window):
        sel = update()
        begin_drawing()
        render(sel)
        draw_fps(0,0)
        end_drawing()
    unload_render_texture(room_texture)
    unload_font(italic_font)
    unload_font(pixel_font)
    close_window()