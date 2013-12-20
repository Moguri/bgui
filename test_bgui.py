#!/usr/bin/env python
import unittest
import gc

import bgui

class TestMemoryLeaks(unittest.TestCase):
    def setUp(self):
        self.system = bgui.System()

    def test_memory_leak_widget(self):
        w = bgui.Widget(self.system)
        self.system = None

        gc.collect()
        self.assertListEqual(gc.garbage, [])

    def test_memory_leak_frame(self):
        w = bgui.Frame(self.system)
        self.system = None

        gc.collect()
        self.assertListEqual(gc.garbage, [])
    
    @unittest.skip("Fonts are causing a segfault")
    def test_memory_leak_frame_button(self):
        w = bgui.FrameButton(self.system)
        self.system = None

        gc.collect()
        self.assertListEqual(gc.garbage, [])

    @unittest.skip("Texture loading not working for testing (requires OpenGL)")
    def test_memory_leak_image(self):
        w = bgui.Image(self.system, "examples/simple/img.jpg")
        self.system = None

        gc.collect()
        self.assertListEqual(gc.garbage, [])

    def test_memory_leak_image_button(self):
        w = bgui.ImageButton(self.system)
        self.system = None

        gc.collect()
        self.assertListEqual(gc.garbage, [])

    @unittest.skip("Fonts are causing a segfault")
    def test_memory_leak_label(self):
        w = bgui.Label(self.system)
        self.system = None

        gc.collect()
        self.assertListEqual(gc.garbage, [])

    @unittest.skip("Fonts are causing a segfault")
    def test_memory_leak_list_box(self):
        w = bgui.ListBox(self.system, items=[1, 2, 3])
        self.system = None

        gc.collect()
        self.assertListEqual(gc.garbage, [])

    def test_memory_leak_progress_bar(self):
        w = bgui.ProgressBar(self.system)
        self.system = None

        gc.collect()
        self.assertListEqual(gc.garbage, [])

    @unittest.skip("Fonts are causing a segfault")
    def test_memory_leak_text_block(self):
        w = bgui.TextBlock(self.system, text="Testing string")
        self.system = None

        gc.collect()
        self.assertListEqual(gc.garbage, [])

    @unittest.skip("Fonts are causing a segfault")
    def test_memory_leak_text_input(self):
        w = bgui.TextInput(self.system, text="Testing string")
        self.system = None

        gc.collect()
        self.assertListEqual(gc.garbage, [])

    @unittest.skip("Texture loading not working for testing (requires OpenGL)")
    def test_memory_leak_video(self):
        # TODO find an actual video to load
        w = bgui.Video(self.system, "examples/simple/img.jpg")
        self.system = None

        gc.collect()
        self.assertListEqual(gc.garbage, [])

if __name__ == '__main__':
    unittest.main(verbosity=2)
