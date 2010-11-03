from tests import FlexGetBase


class TestRegexp(FlexGetBase):

    __yaml__ = """
        presets:
          global:
            mock:
              - {title: 'regexp1', 'imdb_score': 5}
              - {title: 'regexp2', 'bool_attr': true}
              - {title: 'regexp3', 'imdb_score': 5}
              - {title: 'regexp4', 'imdb_score': 5}
              - {title: 'regexp5', 'imdb_score': 5}
              - {title: 'regexp6', 'imdb_score': 5}
              - {title: 'regexp7', 'imdb_score': 5}
              - {title: 'regexp8', 'imdb_score': 5}
              - {title: 'regexp9', 'imdb_score': 5}
              - {title: 'regular', otherfield: 'genre1'}
              - {title: 'expression', genre: ['genre1', 'genre2']}
            seen: false

        feeds:
          # test accepting, setting custom path (both ways), test not (secondary regexp)
          test_accept:
            regexp:
              accept:
                - regexp1
                - regexp2: '~'
                - regexp3:
                    path: '~'
                - regexp4:
                    not:
                      - exp4
                - regexp5:
                    not: exp7

          # test rejecting
          test_reject:
            regexp:
              reject:
                - regexp1

          # test rest
          test_rest:
            regexp:
              accept:
                - regexp1
              rest: reject


          # test excluding
          test_excluding:
            regexp:
              accept_excluding:
                - regexp1

          # test from
          test_from:
            regexp:
              accept:
                - localhost:
                    from:
                      - title

          test_multiple_excluding:
            regexp:
              reject_excluding:
                - reg
                - exp
                - 5
              rest: accept

          # test complicated
          test_complicated:
            regexp:
              accept:
                - regular
                - regexp9
              accept_excluding:
                - reg
                - exp5
              rest: reject

          test_match_in_list:
            regexp:
              # Also tests global from option
              from: genre
              accept:
                - genre1
    """

    def test_accept(self):
        self.execute_feed('test_accept')
        assert self.feed.find_entry('accepted', title='regexp1'), 'regexp1 should have been accepted'
        assert self.feed.find_entry('accepted', title='regexp2'), 'regexp2 should have been accepted'
        assert self.feed.find_entry('accepted', title='regexp3'), 'regexp3 should have been accepted'
        assert self.feed.find_entry('entries', title='regexp4') not in self.feed.accepted, 'regexp4 should have been left'
        assert self.feed.find_entry('accepted', title='regexp2', path='~'), 'regexp2 should have been accepter with custom path'
        assert self.feed.find_entry('accepted', title='regexp3', path='~'), 'regexp3 should have been accepter with custom path'
        assert self.feed.find_entry('accepted', title='regexp5'), 'regexp5 should have been accepted'

    def test_reject(self):
        self.execute_feed('test_reject')
        assert self.feed.find_entry('rejected', title='regexp1'), 'regexp1 should have been rejected'

    def test_rest(self):
        self.execute_feed('test_rest')
        assert self.feed.find_entry('accepted', title='regexp1'), 'regexp1 should have been accepted'
        assert self.feed.find_entry('rejected', title='regexp3'), 'regexp3 should have been rejected'

    def test_excluding(self):
        self.execute_feed('test_excluding')
        assert not self.feed.find_entry('accepted', title='regexp1'), 'regexp1 should not have been accepted'
        assert self.feed.find_entry('accepted', title='regexp2'), 'regexp2 should have been accepted'
        assert self.feed.find_entry('accepted', title='regexp3'), 'regexp3 should have been accepted'

    def test_from(self):
        self.execute_feed('test_from')
        assert not self.feed.accepted, 'should not have accepted anything'

    def test_multiple_excluding(self):
        self.execute_feed('test_multiple_excluding')
        assert self.feed.find_entry('rejected', title='regexp2'), '\'regexp2\' should have been rejected'
        assert self.feed.find_entry('rejected', title='regexp7'), '\'regexp7\' should have been rejected'
        assert self.feed.find_entry('accepted', title='regexp5'), '\'regexp5\' should have been accepted'

    def test_multiple_excluding(self):
        self.execute_feed('test_complicated')
        assert self.feed.find_entry('accepted', title='regular'), '\'regular\' should have been accepted'
        assert self.feed.find_entry('accepted', title='expression'), '\'expression\' should have been accepted'
        assert self.feed.find_entry('accepted', title='regexp9'), '\'regexp9\' should have been accepted'
        assert self.feed.find_entry('rejected', title='regexp5'), '\'regexp5\' should have been rejected'

    def test_match_in_list(self):
        self.execute_feed('test_match_in_list')
        assert self.feed.find_entry('accepted', title='expression'), '\'expression\' should have been accepted'
        assert self.feed.find_entry('entries', title='regular') not in self.feed.accepted, '\'regular\' should not have been accepted'
