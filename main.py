from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.metrics import dp
from datetime import datetime
import os


# -----------------------------
# WINDOW SETTINGS
# -----------------------------
Window.clearcolor = (0.08, 0.08, 0.10, 1)


# -----------------------------
# MAIN APPLICATION
# -----------------------------
class MacMoodApp(App):

    def build(self):

        self.title = "MacMood"

        # Store mood counts
        self.mood_counts = {
            "Happy": 0,
            "Calm": 0,
            "Okay": 0,
            "Sad": 0,
            "Angry": 0
        }

        # Load previous mood history
        self.load_history()

        # Main layout
        main_layout = BoxLayout(
            orientation="vertical",
            padding=dp(25),
            spacing=dp(15)
        )

        # -----------------------------
        # TITLE
        # -----------------------------
        title = Label(
            text="MacMood",
            font_size=dp(32),
            bold=True,
            size_hint_y=None,
            height=dp(60),
            color=(1, 1, 1, 1)
        )

        main_layout.add_widget(title)

        # -----------------------------
        # SUBTITLE
        # -----------------------------
        subtitle = Label(
            text="How are you feeling today?",
            font_size=dp(18),
            size_hint_y=None,
            height=dp(40),
            color=(0.75, 0.75, 0.75, 1)
        )

        main_layout.add_widget(subtitle)

        # -----------------------------
        # MOOD BUTTONS
        # -----------------------------
        mood_grid = GridLayout(
            cols=5,
            spacing=dp(8),
            size_hint_y=None,
            height=dp(65)
        )

        moods = [
            ("Happy", "😊"),
            ("Calm", "😌"),
            ("Okay", "😐"),
            ("Sad", "😢"),
            ("Angry", "😠")
        ]

        for mood, emoji in moods:

            button = Button(
                text=f"{emoji}\n{mood}",
                font_size=dp(15),
                background_normal="",
                background_color=(0.16, 0.16, 0.20, 1),
                color=(1, 1, 1, 1)
            )

            button.bind(
                on_press=lambda instance, selected_mood=mood:
                self.select_mood(selected_mood)
            )

            mood_grid.add_widget(button)

        main_layout.add_widget(mood_grid)

        # -----------------------------
        # JOURNAL LABEL
        # -----------------------------
        journal_label = Label(
            text="Write what's on your mind:",
            font_size=dp(17),
            size_hint_y=None,
            height=dp(35),
            halign="left",
            color=(0.9, 0.9, 0.9, 1)
        )

        main_layout.add_widget(journal_label)

        # -----------------------------
        # JOURNAL INPUT
        # -----------------------------
        self.journal_input = TextInput(
            hint_text="Write your journal entry here...",
            multiline=True,
            background_color=(0.15, 0.15, 0.18, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.3, 0.7, 1, 1),
            padding=dp(12),
            font_size=dp(16)
        )

        main_layout.add_widget(self.journal_input)

        # -----------------------------
        # SAVE BUTTON
        # -----------------------------
        save_button = Button(
            text="Save Mood",
            size_hint_y=None,
            height=dp(55),
            font_size=dp(18),
            bold=True,
            background_normal="",
            background_color=(0.15, 0.55, 0.85, 1),
            color=(1, 1, 1, 1)
        )

        save_button.bind(on_press=self.save_mood)

        main_layout.add_widget(save_button)

        # -----------------------------
        # STATISTICS BUTTON
        # -----------------------------
        stats_button = Button(
            text="View Mood Statistics",
            size_hint_y=None,
            height=dp(50),
            font_size=dp(16),
            background_normal="",
            background_color=(0.20, 0.20, 0.24, 1),
            color=(1, 1, 1, 1)
        )

        stats_button.bind(on_press=self.show_statistics)

        main_layout.add_widget(stats_button)

        # -----------------------------
        # STATUS MESSAGE
        # -----------------------------
        self.status_label = Label(
            text="",
            font_size=dp(14),
            size_hint_y=None,
            height=dp(30),
            color=(0.4, 0.9, 0.6, 1)
        )

        main_layout.add_widget(self.status_label)

        return main_layout

    # --------------------------------
    # SELECT MOOD
    # --------------------------------
    def select_mood(self, mood):

        self.selected_mood = mood

        self.status_label.text = f"Selected mood: {mood}"

    # --------------------------------
    # SAVE MOOD
    # --------------------------------
    def save_mood(self, instance):

        # Check whether mood was selected
        if not hasattr(self, "selected_mood"):

            self.status_label.text = "Please select a mood first."

            return

        mood = self.selected_mood
        journal = self.journal_input.text.strip()

        # Increase mood count
        self.mood_counts[mood] += 1

        # Current date and time
        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Save to file
        try:

            with open(
                "mood_history.txt",
                "a",
                encoding="utf-8"
            ) as file:

                file.write(
                    f"Date: {current_time}\n"
                )

                file.write(
                    f"Mood: {mood}\n"
                )

                file.write(
                    f"Journal: {journal}\n"
                )

                file.write(
                    "-" * 40 + "\n"
                )

            self.status_label.text = "Mood saved successfully!"

            # Clear journal
            self.journal_input.text = ""

        except Exception as error:

            self.status_label.text = f"Error: {error}"

    # --------------------------------
    # LOAD PREVIOUS HISTORY
    # --------------------------------
    def load_history(self):

        if not os.path.exists("mood_history.txt"):
            return

        try:

            with open(
                "mood_history.txt",
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read()

            # Count moods from saved history
            for mood in self.mood_counts:

                self.mood_counts[mood] = content.count(
                    f"Mood: {mood}"
                )

        except Exception:
            pass

    # --------------------------------
    # SHOW STATISTICS
    # --------------------------------
    def show_statistics(self, instance):

        # Statistics layout
        layout = BoxLayout(
            orientation="vertical",
            padding=dp(25),
            spacing=dp(15)
        )

        heading = Label(
            text="YOUR MOOD STATISTICS",
            font_size=dp(18),
            bold=True,
            size_hint_y=None,
            height=dp(45),
            color=(1, 1, 1, 1)
        )

        layout.add_widget(heading)

        # Create statistics text
        statistics_text = (
            f"Happy : {self.mood_counts['Happy']}\n\n"
            f"Calm  : {self.mood_counts['Calm']}\n\n"
            f"Okay  : {self.mood_counts['Okay']}\n\n"
            f"Sad   : {self.mood_counts['Sad']}\n\n"
            f"Angry : {self.mood_counts['Angry']}"
        )

        statistics_label = Label(
            text=statistics_text,
            font_size=dp(17),
            halign="left",
            valign="middle",
            color=(0.9, 0.9, 0.9, 1)
        )

        layout.add_widget(statistics_label)

        # Close button
        close_button = Button(
            text="Close",
            size_hint_y=None,
            height=dp(50),
            font_size=dp(16),
            background_normal="",
            background_color=(0.25, 0.25, 0.28, 1)
        )

        layout.add_widget(close_button)

        # Popup
        popup = Popup(
            title="Mood Statistics",
            content=layout,
            size_hint=(0.7, 0.7),
            auto_dismiss=False
        )

        close_button.bind(
            on_press=popup.dismiss
        )

        popup.open()


# -----------------------------
# RUN APPLICATION
# -----------------------------
if __name__ == "__main__":
    MacMoodApp().run()