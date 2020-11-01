import io
import syntacticalAnalyzer


def test_one_simple_file(monkeypatch, tmp_path, capsys):
    (tmp_path / 'a.txt').write_text('hello :- f; g; f, g, f, g, f, g, ggg, g, ggg, fgfgfg, fg.\n')
    monkeypatch.chdir(tmp_path)
    syntacticalAnalyzer.main(['-s', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Correct\n'


def test_simple_files(monkeypatch, tmp_path, capsys):
    (tmp_path / 'a.txt').write_text('hello :- f; g; f, g, f, g, f, g, ggg, g, ggg, fgfgfg, fg.\n')
    (tmp_path / 'b.txt').write_text('_hASDasdellfoasf :- fasd; g_as; fAD, _g, f, g, f, g, ggg, g, ggg, fgfgfg, fg.\n')
    monkeypatch.chdir(tmp_path)
    syntacticalAnalyzer.main(['-s', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt: Correct\n' \
                  'b.txt: Correct\n'


def test_simple_files2(monkeypatch, tmp_path, capsys):
    (tmp_path / 'a.txt').write_text('f. \n f :- g.\n'
                                    'f:- g, h, t. \n f:- g, h; t.\n'
                                    'f :- g, (h,\t\t t).\n f :- g, a (h t).\n'
                                    'f a :- g, h (t \tc d).\n f (cons h t) :- g h, f g.')
    (tmp_path / 'b.txt').write_text('_hASDasdellfoasf \t:-\t fas41124d; g_as; fA412D, _g, f, g, f, g, ggg, g, ggg, '
                                    'a (fg f_g _fg), fg; (asdasd ; asfa412s fas m afs, asfa4124sda ); asd123s_ad .\n')
    monkeypatch.chdir(tmp_path)
    syntacticalAnalyzer.main(['-s', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt: Correct\n' \
                  'b.txt: Correct\n'


def test_line(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO('_hASDasdellfoasf :- a. asdas:- ((((asd)))).'))
    syntacticalAnalyzer.main(['-s'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Correct\n'


def test_multi_line(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        '_hASDasdellfoasf :- a.\n'
        'asd\n :-\n asd, \n\n\n sa\n\n\n\n.'
        'aasdaSALKJFDNAFKLAjdsljdsajflkKJBFKJQWNf\n\n dsfhldsajf \t\n\t hkjsd\n\n hfkj dhfkjd (shfkj ehkjskd bcjhbea)'
        ':- aasdaSALKJFDNAFKLAjdsljdsajflkKJBFKJQWNfdsfhldsajfhkjsdhfkjdhfkjdshfkjehkjskdbcjhbea,\n\n\n\n\n sad\n\n\n'
        ',\n\n\n\n\n (\n\n\n\t\t\n asd;\n\t\t\t\n\n asd\n\n\n)\n\n\n.'))
    syntacticalAnalyzer.main(['-s'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Correct\n'


def test_error_line_lex(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        '_hASDa/sdellfoasf :- a.\n'
        'asd\n :-\n asd, \n\n\n sa\n\n\n\n.'
        'asdafdscjhbea'
        ':- aasdaSALKJFDNAFKLAjdsljdsajflkKJBFKJQWNfdsfhldsajfhkjsdhfkjdhfkjdshfkjehkjskdbcjhbea,\n\n\n\n\n sad\n\n\n'
        ',\n\n\n\n\n (\n\n\n\n asd;\n\n\n asd\n\n\n)\n\n\n.'))
    syntacticalAnalyzer.main(['-s'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'IllegalCharacter: \'/\', line 53\n'


def test_error_line_par(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        '_hASDasdellfoasf :- a.\n'
        'asd\n :-\n asd, \n\n\n sa\n\n\n\n.'
        'asdafdscjhbea'
        ':- (aasdaSALKJFDNAFKLAjdsljdsajflkKJBFKJQWNfdsfhldsajfhkjsdhfkjdhfkjdshfkjehkjskdbcjhbea)\n\n\n\n\n '
        'sad asd\n\n\n,\n\n\n\n\n (\n\n\n\n asd;\n\n\n asd\n\n\n)\n\n\n.'))
    syntacticalAnalyzer.main(['-s'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'IncompleteToken: LexToken(ID,\'sad\',68,156)\n'


def test_error_files(monkeypatch, tmp_path, capsys):
    (tmp_path / 'a').write_text('hello :- f; g; f, g, f, g, (((((f)), ((g, ggg)), g, ggg, fgfgfg, fg))).\n')
    (tmp_path / 'b').write_text('hello :- (f; g)); f, g, f, g, f, g, ggg, g, ggg, fgfgfg, fg.\n')
    (tmp_path / 'c').write_text('Ahello :- f; g; f, g, f, g, f, g, ggg, g, ggg, fgfgfg, fg.\n')
    (tmp_path / 'd').write_text('9hello :- f; g; f, g, f, g, f, g, ggg, g, ggg, fgfgfg, fg.\n')
    (tmp_path / 'e').write_text('hello :- f; g; f, g, f, g, f\\, g, ggg, g, ggg, fgfgfg, fg.\n')
    (tmp_path / 'f').write_text('hello :- f; g; (f, g, f, g, f,) g, ggg, g, ggg, fgfgfg, fg.\n')

    monkeypatch.chdir(tmp_path)
    syntacticalAnalyzer.main(['-s', 'a', 'b', 'c', 'd', 'e', 'f'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a: Correct\n' \
                  'b: IncompleteToken: LexToken(DELIMITERR,\')\',69,15)\n' \
                  'c: Correct\n' \
                  'd: IllegalCharacter: \'9\', line 70\n' \
                  'e: IllegalCharacter: \'\\\', line 70\n' \
                  'f: IncompleteToken: LexToken(DELIMITERR,\')\',70,30)\n'


def test_error(monkeypatch, tmp_path, capsys):
    (tmp_path / 'a').write_text('f')
    (tmp_path / 'b').write_text(':- f.')
    (tmp_path / 'c').write_text('f :- .')
    (tmp_path / 'd').write_text('f :- g; h, .')
    (tmp_path / 'e').write_text('f :- (g; (f).')
    (tmp_path / 'f').write_text('f ().')

    monkeypatch.chdir(tmp_path)
    syntacticalAnalyzer.main(['-s', 'a', 'b', 'c', 'd', 'e', 'f'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a: IncompleteToken: None\n' \
                  'b: IncompleteToken: LexToken(CORKSCREW,\':-\',70,0)\n' \
                  'c: IncompleteToken: LexToken(DOT,\'.\',70,5)\n' \
                  'd: IncompleteToken: LexToken(DOT,\'.\',70,11)\n' \
                  'e: IncompleteToken: LexToken(DOT,\'.\',70,12)\n' \
                  'f: IncompleteToken: LexToken(DELIMITERR,\')\',70,3)\n'


def test_atom(monkeypatch, tmp_path, capsys):
    (tmp_path / 'a').write_text('odd (cons H (cons H1 T)) (cons H T1) :- odd T T1.')
    (tmp_path / 'b').write_text('odd (cons H nil) nil.')
    (tmp_path / 'c').write_text('odd nil nil.')
    (tmp_path / 'd').write_text('a (((((b))))).')
    (tmp_path / 'e').write_text('f :- a ((((b)))).')
    (tmp_path / 'f').write_text('f :- a (a (a a)).')
    (tmp_path / 'g').write_text('f :- a (a (((a a))) a (a a)).')
    (tmp_path / 'h').write_text('f :- a ((((a a))) a (a a)).')
    (tmp_path / 'j').write_text('f :- (a) (a (((a a))) a (a a)).')

    monkeypatch.chdir(tmp_path)
    syntacticalAnalyzer.main(['-s', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a: Correct\n' \
                  'b: Correct\n' \
                  'c: Correct\n' \
                  'd: Correct\n' \
                  'e: Correct\n' \
                  'f: Correct\n' \
                  'g: Correct\n' \
                  'h: IncompleteToken: LexToken(ID,\'a\',70,18)\n' \
                  'j: IncompleteToken: LexToken(DELIMITERL,\'(\',70,9)\n'
