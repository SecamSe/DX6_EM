from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
import socket
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget

class MyApp(App):
    def build(self):
        dropdown = DropDown()
        for i in range(15):
            btn = Button(text='Хоз.орган %d' % i, size_hint_y=None, height=20)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        mainbutton = Button(text='Хоз.орган', size_hint=(None, None), height=20)
        mainbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

        bl = BoxLayout(orientation='vertical', padding = [5,5,5,5])

        blserver = BoxLayout(orientation='horizontal')
        blserver.add_widget(Label(text = 'Сервер:',
                                  size_hint_y=None, size_hint_x=None,
                                  height=30, width=60,
                                  )
                            )
        self.server = TextInput(multiline=False,
                            height=30, width=165,
                            size_hint_y=None, size_hint_x=None,
                            text='127.0.0.1:8097'
                           )
        blserver.add_widget(self.server)

        blserver.add_widget(Label(text='№ Объекта:',
                                  size_hint_y=None, size_hint_x=None,
                                  height=30, width=90,
                                  )
                            )
        self.num_object = TextInput(multiline=False,
                                height=30, width=50,
                                size_hint_y=None, size_hint_x=None,
                                text='9999'
                                   )
        blserver.add_widget(self.num_object)

        blserver.add_widget(Button(text = 'test none',
                                   height = 30, width = 100,
                                   size_hint_y = None, size_hint_x = None,
                                   on_press = self.btn_test_press
                                   )
                            )
        blserver.add_widget(mainbutton)
        bl.add_widget(blserver)

        blarea = BoxLayout(orientation = 'horizontal')
        gl = GridLayout(cols = 1, padding = [0,5,0,0],spacing = 3)
        for i in range(1,9):
            gl.add_widget(Button(text = 'Раздел %d СНЯТ\nнажми для охраны' % i,
                            font_size = 12,
                            height=35, width=200,
                            size_hint_y=None, size_hint_x=None,
                            on_press = self.btn_press,
                            background_color = [0, 0 ,1 ,1]
                                 )
                          )

        blarea.add_widget(gl)
        blzone = BoxLayout(orientation = 'vertical' )
        blarea.add_widget(blzone)
        bl.add_widget(blarea)

        return bl

    def btn_press(self, instance):
        num_area = instance.text[7]
        if instance.background_color == [0, 0, 1, 1]:
            if send(f'0101004E"ADM-CID"002AR00IPL000S[#00{self.num_object.text}|1401 0{num_area} 004]',self):
                instance.text = f'Раздел {num_area} НА ОХРАНЕ\nнажми для снятия'
                instance.background_color = 'green'
        else:
            if send(f'0101004E"ADM-CID"002AR00IPL000S[#00{self.num_object.text}|3401 0{num_area} 004]',self):
                instance.text = f'Раздел {num_area} СНЯТ\nнажми для охраны'
                instance.background_color = 'blue'

    def btn_test_press(self, instance):
        if send(f'SR00IPL000S    00{self.num_object.text}XX    ', self):
            instance.text = 'test OK'
            instance.background_color = 'green'
        else:
            instance.text = 'test fail'
            instance.background_color = 'red'


def send(msg,self):
    server_ip_port = (self.server.text.split(':')[0], int(self.server.text.split(':')[1]))
    print(server_ip_port)

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect(server_ip_port)
        data = client.recv(256)
        client.send(msg.encode('utf-8'))
        data = client.recv(256)
        data = client.recv(256)
        print(f'{msg} - has been sent')
        client.close()
        return True

    except Exception as ex:
        print(f'{ex}')
        return False


def main():
    MyApp().run()


if __name__ == '__main__':
    main()