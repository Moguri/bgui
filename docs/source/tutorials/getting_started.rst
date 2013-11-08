Getting Started
===============

This tutorial is intended to get you up and running with Bgui quickly and easily. This tutorial assumes you already know how to use Python with the BGE. If you do not, take a look `here <http://solarlune-gameup.blogspot.com/search/label/BGE%20Tutorials here>`_.

Getting Bgui
------------

First, you'll need to either grab a "release" version of Bgui from `here <https://github.com/Moguri/bgui/releases>`_, or you can grab the latest development version from `here <https://github.com/Moguri/bgui/archive/master.zip>`_. After you've downloaded Bgui copy the "bgui" folder to where you need to for your project to access it (the current working directory of the project works well). To test if your project can find Bgui simply try an ``import bgui`` in a script and try to run it from the BGE.

Setup a System
--------------

After getting Bgui setup in your project, the next step is to setup a System. In Bgui a System is the top level element in a GUI. It handles mouse and keyboard events and renders the widgets. Bgui's ultimate goal is to be independent of Blender and the BGE. However, there is a ``bgui.bge_utils`` module that contains classes for getting Bgui setup quickly for the BGE::

    import bgui
    import bgui.bge_utils
    import bge


    class SimpleLayout(bgui.bge_utils.Layout):
        """A layout showcasing various Bgui features"""

        def __init__(self, sys, data):
            super().__init__(sys, data)

            # Add widgets here

    def main(cont):
        own = cont.owner
        mouse = bge.logic.mouse

        if 'sys' not in own:
            # Create our system and show the mouse
            own['sys'] = bgui.bge_utils.System('../../themes/default')
            own['sys'].load_layout(SimpleLayout, None)
            mouse.visible = True
        else:
            own['sys'].run()

BGE Logic
---------

To get Bgui working in the BGE we'll need to setup a bit of logic. The good news is it's pretty simple: just add an always sensor (pulse mode on) and a Python module controller. Now, assuming you used the earlier example, just enter ``name_of_py_file.main`` into the module controller. You should now be able to press "P", but you wont see much because we haven't added any widgets yet. So, let's get to that next.

Adding Widgets
--------------

Widgets (also known as controls or components in other GUI libraries) are the actual elements that will be drawn to the screen. This includes things like text and buttons. At the time of this writing, Bgui currently has the following widgets available:

* :class:`.Frame`
* :class:`.FrameButton`
* :class:`.Image`
* :class:`.ImageButton`
* :class:`.Label`
* :class:`.ListBox`
* :class:`.ProgressBar`
* :class:`.TextBlock`
* :class:`.TextInput`
* :class:`.Video`

Let's go ahead and add a :class:`.FrameButton` and a :class:`.Label` to our example. After the ``# Add widgets here`` line add the following::

    # Use a frame to store all of our widgets
    self.frame = bgui.Frame(self, border=0)
    self.frame.colors = [(0, 0, 0, 0) for i in range(4)]

    # A Label widget
    self.lbl = bgui.Label(self.frame, text='I sure wish someone would push that button...',
            pt_size=70, pos=[0, 0.7], options=bgui.BGUI_CENTERX)

    # A FrameButton widget
    self.btn = bgui.FrameButton(self.frame, text='Click Me!', size=[0.3, 0.1], pos=[0, 0.4],
            options=bgui.BGUI_CENTERX)

I won't go much into the constructors for these widgets. You can look up more on the constructors in the :ref:`API docs <api-docs-label>`.

Okay, so now we test the changes. You should have a label and a button, both just asking for the button to be pushed. However, when we push the button, nothing much happens other than pretty button effects. A GUI isn't much use if it can't actually do anything. To add actions to widgets, we use callbacks, which are described in the next section.

Callbacks
---------

Alright, time to get our button to do something. The :class:`.FrameButton` widget has an ``on_click`` callback that we can make use of. Add the following after creating the button::

    self.btn.on_click = self.button_click

And then add the following method to the SimpleLayout class::

    def button_click(self, widget):
        self.lbl.text = 'Yippie! You clicked the button! ^_^'

Now if you test the new changes, you should get a very ecstatic message when clicking the button.

What next?
----------

Okay, so where to go from here, right? Well, unfortunately there isn't much in the way of docs, so I'd recommend taking a look at the examples in the example folder. They show you how to use some widgets.
