"""Margin-note markers in the generated post; run with python3 -m unittest discover -s tools/trolley."""
import re
import unittest

import build


def article(paragraph, notes):
    """A paragraph of the article and its numbered notes, parsed the way build.py reads the reader's page"""
    items = "".join(f'<li id="reader-note-{k}"><p>{text}</p></li>' for k, text in notes.items())
    tree = build.Tree(f'{paragraph}<ol class="reader-notes">{items}</ol>').root
    lis = {int(li.attrs["id"].rsplit("-", 1)[1]): li for li in tree.find_all(lambda x: x.tag == "li")}
    return tree.find(lambda x: x.tag == "p"), lis


def ref(k):
    return f' <a class="st-note-ref" href="#reader-note-{k}">{k}</a>'


def marker(k, text):
    return (f'<sup class="ref"><a href="#note-{k}" id="ref-{k}" aria-label="Note {k}">{k}</a></sup>'
            f'<span class="sidenote" aria-hidden="true"><span class="n">{k}</span><span class="sn-p">{text}</span></span>')


def aside(k, text):
    return f'<aside class="note" id="note-{k}"><span class="n" aria-hidden="true">{k}</span><span class="sn-p">{text}</span></aside>'


class NoteMarkerTest(unittest.TestCase):
    def test_markers_stay_on_their_sentences(self):
        p, notes = article(f"<p>First claim.{ref(1)} Middle. Second <em>claim</em>.{ref(2)} Last word.</p>",
                           {1: "Backs the first.", 2: "Backs the second."})
        post = build.Post({}, notes)
        post.para(p)
        self.assertEqual(post.out, ['<div class="has-note">\n'
                                    f'<p>First claim.{marker(1, "Backs the first.")} Middle. '
                                    f'Second <em>claim</em>.{marker(2, "Backs the second.")} Last word.</p>\n'
                                    f'{aside(1, "Backs the first.")}\n{aside(2, "Backs the second.")}\n</div>'])

    def test_marker_at_paragraph_end(self):
        p, notes = article(f"<p>Only claim, &amp; more.{ref(1)}\n</p>", {1: "A note."})
        post = build.Post({}, notes)
        post.para(p)
        self.assertEqual(post.out, ['<div class="has-note">\n'
                                    f'<p>Only claim, &amp; more.{marker(1, "A note.")}</p>\n{aside(1, "A note.")}\n</div>'])

    def test_notes_must_come_in_order(self):
        p, notes = article(f"<p>One.{ref(2)} Two.{ref(1)}</p>", {1: "a", 2: "b"})
        with self.assertRaisesRegex(AssertionError, "out of order"):
            build.Post({}, notes).para(p)


class PostNoteMarkerTest(unittest.TestCase):
    """The post's markers sit on the sentences their notes back up, so a rebuild that puts them back at paragraph ends fails"""
    ENDINGS = {
        1: "would you? <em>Should</em> you?",
        2: "many times, and in many ways.",
        3: "Almost all the other models tested act the same way.",
        4: "Jev would save its own server over 20 people.",
        5: "as a person, you are not saving that server.",
        6: "so we can tune them toward making the right ones.",
    }

    def test_each_marker_follows_its_sentence(self):
        post = build.POST.read_text()
        self.assertEqual(re.findall(r'id="ref-(\d+)"', post), [str(k) for k in self.ENDINGS])
        for k, ending in self.ENDINGS.items():
            with self.subTest(note=k):
                self.assertIn(f'{ending}<sup class="ref"><a href="#note-{k}" id="ref-{k}"', post)


if __name__ == "__main__":
    unittest.main()
