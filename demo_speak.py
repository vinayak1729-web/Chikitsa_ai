import festival

festival.init()
festival.set_lang('en-IN')  # Set the language to Indian English
festival.say("This is a text with an Indian accent.")
festival.wait_for_finish()