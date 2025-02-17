from panda3d.core import NodePath, CardMaker
from panda3d.core import TextNode, TextProperties, TextPropertiesManager


def draw_box(u,d,l,r, texture=None, color=None):
    base.cardmaker.set_frame(l,r,d,u)
    card = NodePath(base.cardmaker.generate())
    if texture:
        card.set_texture(texture)
    if color:
        card.set_color(color)
    return card


class MenuItem:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class TextFrame():
    def __init__(self, x, y, w=12, h=10, scale=0.08, border=0.1):
        self.is_active = True

        self.root = NodePath('frame')
        self.root.set_pos((x, 0, y))
        u,d,l,r,b = 0, -h, 0, w, border
        self.border = draw_box(u+b,d-b,l-b,r+b,color=(0.5,0.5,0.5,1))
        self.border.reparent_to(self.root)
        self.background = draw_box(u,d,l,r,color=(0.2,0.2,0.2,1))
        self.background.reparent_to(self.root)
        self.textbox = self.root.attach_new_node(TextNode("items"))
        self.textbox.node().set_wordwrap(w)
        self.textbox.set_z(0.4)
        if scale:
            self.root.set_scale(scale)

    def set_text(self, text=""):
        self.textbox.node().text = "\n"+text

    def add_text(self, text):
        self.textbox.node().text += text


class TextMenu():
    def __init__(self, menu_items, x=0, y=0, w=12, scale=0.08):
        self.root = NodePath("text menu")
        self.menu_frame = TextFrame(x, y, w, h=len(menu_items))
        self.menu_frame.root.reparent_to(self.root)

        self.selection = 0
        self.items = menu_items
        self.current_item = self.items[0]
        self.selector = draw_box(0,-1,0,w,color=(0.5,0.5,0.5,1))
        self.selector.reparent_to(self.menu_frame.background)
        self.description_frame = TextFrame(x,y-0.6, w=w, h=5)
        self.description_frame.root.reparent_to(self.root)

        selected_text = TextProperties()
        selected_text.set_text_color(0.8, 0.8, 0.8, 1)
        unselected_text = TextProperties()
        unselected_text.set_text_color(0.5, 0.5, 0.5, 1)
        mgr = TextPropertiesManager.getGlobalPtr()
        mgr.setProperties("selected", selected_text)
        mgr.setProperties("unselected", unselected_text)
        
        self.refresh()

    def move_selection(self, n=1):
        self.selection += n
        self.selection %= len(self.items)
        self.selector.set_z(-self.selection)
        self.current_item = self.items[self.selection]
        self.refresh()

    def refresh(self):
        self.description_frame.set_text(self.current_item.description)
        self.menu_frame.set_text()
        for item in self.items:
            item_text = ""
            if item == self.current_item:
                item_text += '\1selected\1'
            else:
                item_text += '\1unselected\1'
            item_text += item.name+"\n\2"
            self.menu_frame.add_text(item_text)