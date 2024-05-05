from kivy.app import App
from kivy.graphics.svg import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
window_width = Window.size[0]
window_height = Window.size[1]
class ScrollableListApp(App):
    def build(self):

        # Create ScrollView
        scroll_view = ScrollView(size=(400, 400), do_scroll_x=False)
        layout = GridLayout(cols=1, padding=(30, 100), spacing=100, size_hint=(None, None))
        layout.width = 800  # Đặt chiều rộng mong muốn
        layout.height = 400  # Đặt chiều cao mong muốn
        layout.bind(minimum_height=layout.setter('height'))
        # Add list items to GridLayout (example)
        for i in range(10):
            # Create a BoxLayout for each item
            item_layout = BoxLayout(orientation='horizontal', spacing=100, padding=10)

            # Create a BoxLayout for the first column
            column1_layout = BoxLayout(orientation='vertical', spacing=40)

            # Phòng số in the first column
            title_label = Label(text=f"Phòng số {i}", font_size='20sp', bold=True, halign='left')
            column1_layout.add_widget(title_label)

            # Content in the first column
            content_label = Label(text=f"Số người: 1/{i}", font_size='16sp', halign='left')
            column1_layout.add_widget(content_label)

            # Add the first column layout to the item layout
            item_layout.add_widget(column1_layout)

            # Button in the second column
            button = Button(text=f"Button {i}", size_hint=(None, None), size=(120, 40))
            item_layout.add_widget(button)

            # Add the item layout to the main layout
            layout.add_widget(item_layout)

        # Add GridLayout to ScrollView
        scroll_view.add_widget(layout)

        # Return ScrollView as main widget
        return scroll_view


# Run the application
if __name__ == '__main__':
    ScrollableListApp().run()
