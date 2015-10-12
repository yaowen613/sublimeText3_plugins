"""
BracketHighlighter.

Copyright (c) 2013 - 2015 Isaac Muse <isaacmuse@gmail.com>
License: MIT
"""
import BracketHighlighter.bh_plugin as bh_plugin
import sublime

DEFAULT_TAGS = ["cfml", "html", "angle"]


class SelectBracket(bh_plugin.BracketPluginCommand):

    """Select Bracket plugin."""

    def run(self, edit, name, select='', tags=None, always_include_brackets=False, alternate=False):
        """
        Select the content between brackets.

        If "always_include_brackets" is enabled,
        include the brackts as well.  If the content is already selected, expand to the
        parent.
        """

        if tags is None:
            tags = DEFAULT_TAGS
        current_left, current_right = self.selection[0].begin(), self.selection[0].end()
        left, right = self.left, self.right
        first, last = left.end, right.begin
        if select == 'left':
            if name in tags and left.size() > 1:
                first, last = left.begin + 1, left.begin + 1
                if first == current_left and last == current_right:
                    if alternate:
                        first, last = right.begin + 1, right.begin + 1
                    else:
                        first, last = left.begin, left.begin
            else:
                first, last = left.end, left.end
                if first == current_left and last == current_right:
                    if alternate:
                        first, last = right.begin, right.begin
                    else:
                        first, last = left.begin, left.begin
        elif select == 'right':
            if left.end != right.end:
                if name in tags and left.size() > 1:
                    first, last = right.begin + 1, right.begin + 1
                    if first == current_left and last == current_right:
                        if alternate:
                            first, last = left.begin + 1, left.begin + 1
                        else:
                            first, last = right.end, right.end
                else:
                    first, last = right.begin, right.begin
                    if first == current_left and last == current_right:
                        if alternate:
                            first, last = left.end, left.end
                        else:
                            first, last = right.end, right.end
            else:
                # There is no second bracket, so just select the first
                if name in tags and left.size() > 1:
                    first, last = left.begin + 1, left.begin + 1
                    if first == current_left and last == current_right:
                        if not alternate:
                            first, last = left.end, left.end
                else:
                    first, last = right.end, right.end
                    if first == current_left and last == current_right:
                        if not alternate:
                            first, last = right.end, right.end
        elif first == current_left and last == current_right or always_include_brackets:
            first, last = left.begin, right.end

        self.selection = [sublime.Region(first, last)]


def plugin():
    """Make plugin available."""

    return SelectBracket
