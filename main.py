from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window
from datetime import datetime
import os


class MacMoodApp(App):

    def build(self):
        Window.size = (900, 650)
        Window.clearcolor = (0.05, 0.05, 0.05, 1)

        self.selected_mood = "Happy"

        main_layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=20
        )

        # Title
        title = Label(
            text="MacMood",
            font_size=34,
            bold=True,
            size_hint_y=None,
            height=60
        )
        main_layout.add_widget(title)

        # Question
        question = Label(
            text="How are you feeling today?",
            font_size=22,
            size_hint_y=None,
            height=50
        )
        main_layout.add_widget(question)

        # Mood buttons
        mood_layout = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint_y=None,
            height=70
        )

        moods = ["Happy", "Calm", "Okay", "Sad", "Angry"]

        for mood in moods:
            button = Button(
                text=mood,
                font_size=18
            )
            button.bind(
                on_press=lambda instance, m=mood:
                self.select_mood(m)
            )
            mood_layout.add_widget(button)

        main_layout.add_widget(mood_layout)

        # Journal box
        self.journal = TextInput(
            hint_text="Write what's on your mind...",
            font_size=18,
            multiline=True
        )
        main_layout.add_widget(self.journal)

        # Save button
        save_button = Button(
            text="Save Mood",
            font_size=20,
            size_hint_y=None,
            height=60
        )
        save_button.bind(on_press=self.save_mood)
        main_layout.add_widget(save_button)

        # History button
        history_button = Button(
            text="View Mood History",
            font_size=18,
            size_hint_y=None,
            height=55
        )
        history_button.bind(on_press=self.show_history)
        main_layout.add_widget(history_button)

        # Statistics button
        stats_button = Button(
            text="View Mood Statistics",
            font_size=18,
            size_hint_y=None,
            height=55
        )
        stats_button.bind(on_press=self.show_statistics)
        main_layout.add_widget(stats_button)

        # Status
        self.status = Label(
            text="Mood selected: Happy",
            font_size=16,
            size_hint_y=None,
            height=40
        )
        main_layout.add_widget(self.status)

        return main_layout

    def select_mood(self, mood):
        self.selected_mood = mood
        self.status.text = f"Mood selected: {mood}"

    def save_mood(self, instance):

        journal_text = self.journal.text.strip()

        if not journal_text:
            journal_text = "No journal entry."

        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        entry = (
            f"Date: {current_time}\n"
            f"Mood: {self.selected_mood}\n"
            f"Journal: {journal_text}\n"
            f"{'-' * 50}\n"
        )

        with open(
            "mood_history.txt",
            "a",
            encoding="utf-8"
        ) as file:
            file.write(entry)

        self.status.text = "Mood saved successfully!"

        self.journal.text = ""

    def show_history(self, instance):

        if not os.path.exists("mood_history.txt"):
            history_text = "No mood history found."
        else:
            with open(
                "mood_history.txt",
                "r",
                encoding="utf-8"
            ) as file:
                history_text = file.read()

            if not history_text.strip():
                history_text = "No mood history found."

        content = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        history_box = TextInput(
            text=history_text,
            readonly=True,
            font_size=16,
            multiline=True
        )

        close_button = Button(
            text="Close",
            size_hint_y=None,
            height=50
        )

        content.add_widget(history_box)
        content.add_widget(close_button)

        popup = Popup(
            title="Mood History",
            content=content,
            size_hint=(0.85, 0.85)
        )

        close_button.bind(
            on_press=popup.dismiss
        )

        popup.open()

    def show_statistics(self, instance):

        counts = {
            "Happy": 0,
            "Calm": 0,
            "Okay": 0,
            "Sad": 0,
            "Angry": 0
        }

        if os.path.exists("mood_history.txt"):
            with open(
                "mood_history.txt",
                "r",
                encoding="utf-8"
            ) as file:

                for line in file:
                    if line.startswith("Mood:"):
                        mood = line.replace(
                            "Mood:", ""
                        ).strip()

                        if mood in counts:
                            counts[mood] += 1

        statistics_text = (
            "YOUR MOOD STATISTICS\n\n"
            f"Happy : {counts['Happy']}\n\n"
            f"Calm  : {counts['Calm']}\n\n"
            f"Okay  : {counts['Okay']}\n\n"
            f"Sad   : {counts['Sad']}\n\n"
            f"Angry : {counts['Angry']}"
        )

        content = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        stats_label = Label(
            text=statistics_text,
            font_size=20
        )

        close_button = Button(
            text="Close",
            size_hint_y=None,
            height=50
        )

        content.add_widget(stats_label)
        content.add_widget(close_button)

        popup = Popup(
            title="Mood Statistics",
            content=content,
            size_hint=(0.7, 0.7)
        )

        close_button.bind(
            on_press=popup.dismiss
        )

        popup.open()


if __name__ == "__main__":
    MacMoodApp().run()