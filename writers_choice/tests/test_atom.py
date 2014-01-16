import pyramid.testing

from writers_choice.views.public import atom_feed

from . import AbstractViewTests

class AtomTests(AbstractViewTests):
    def test_feed(self):
        # We'll assume the XML schema is correct and just pick some sample
        # values to test
        request = pyramid.testing.DummyRequest()
        response = atom_feed(request)

        for line in (
                '<title type="text">Site name</title>',
                '<id>http://example.com/feed.atom</id>',
                '<link href="http://example.com/" />',
                '<link href="http://example.com/feed.atom" rel="self" />',
                '<name>Site name</name>',
                '<title type="text">Testsida två</title>',
                '<published>2012-01-03T12:00:00Z</published>',
                '<link href="http://example.com/2012/1/3/testsida-tva" />',
                '<content type="html">&lt;p&gt;Med kod:&lt;/p&gt;',
                '<title type="text">Testsida mittemellan</title>',
                '<id>http://example.com/2012/1/2/testsida-mittemellan</id>'
        ):
            self.assertIn(line, response.text)
