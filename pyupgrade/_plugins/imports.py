from __future__ import annotations

import ast
import bisect
import collections
import functools
from typing import Iterable
from typing import Mapping
from typing import NamedTuple

from tokenize_rt import Offset
from tokenize_rt import Token

from pyupgrade._ast_helpers import ast_to_offset
from pyupgrade._data import register
from pyupgrade._data import State
from pyupgrade._data import TokenFunc
from pyupgrade._token_helpers import find_end
from pyupgrade._token_helpers import find_token
from pyupgrade._token_helpers import has_space_before
from pyupgrade._token_helpers import indented_amount

# GENERATED VIA generate-imports
# Using reorder-python-imports==3.9.0
REMOVALS = {
    (3,): {
        '__future__': {
            'absolute_import', 'division', 'generators', 'nested_scopes',
            'print_function', 'unicode_literals', 'with_statement',
        },
        'builtins': {
            '*', 'ascii', 'bytes', 'chr', 'dict', 'filter', 'hex', 'input',
            'int', 'isinstance', 'list', 'map', 'max', 'min', 'next', 'object',
            'oct', 'open', 'pow', 'range', 'round', 'str', 'super', 'zip',
        },
        'io': {'open'},
        'six': {'callable', 'next'},
        'six.moves': {'filter', 'input', 'map', 'range', 'zip'},
    },
    (3, 7): {'__future__': {'generator_stop'}},
}
REMOVALS[(3,)]['six.moves.builtins'] = REMOVALS[(3,)]['builtins']
REPLACE_EXACT = {
    (3,): {
        ('collections', 'AsyncGenerator'): 'collections.abc',
        ('collections', 'AsyncIterable'): 'collections.abc',
        ('collections', 'AsyncIterator'): 'collections.abc',
        ('collections', 'Awaitable'): 'collections.abc',
        ('collections', 'ByteString'): 'collections.abc',
        ('collections', 'Callable'): 'collections.abc',
        ('collections', 'Collection'): 'collections.abc',
        ('collections', 'Container'): 'collections.abc',
        ('collections', 'Coroutine'): 'collections.abc',
        ('collections', 'Generator'): 'collections.abc',
        ('collections', 'Hashable'): 'collections.abc',
        ('collections', 'ItemsView'): 'collections.abc',
        ('collections', 'Iterable'): 'collections.abc',
        ('collections', 'Iterator'): 'collections.abc',
        ('collections', 'KeysView'): 'collections.abc',
        ('collections', 'Mapping'): 'collections.abc',
        ('collections', 'MappingView'): 'collections.abc',
        ('collections', 'MutableMapping'): 'collections.abc',
        ('collections', 'MutableSequence'): 'collections.abc',
        ('collections', 'MutableSet'): 'collections.abc',
        ('collections', 'Reversible'): 'collections.abc',
        ('collections', 'Sequence'): 'collections.abc',
        ('collections', 'Set'): 'collections.abc',
        ('collections', 'Sized'): 'collections.abc',
        ('collections', 'ValuesView'): 'collections.abc',
        ('pipes', 'quote'): 'shlex',
        ('six', 'BytesIO'): 'io',
        ('six', 'StringIO'): 'io',
        ('six', 'wraps'): 'functools',
        ('six.moves', 'StringIO'): 'io',
        ('six.moves', 'UserDict'): 'collections',
        ('six.moves', 'UserList'): 'collections',
        ('six.moves', 'UserString'): 'collections',
        ('six.moves', 'filterfalse'): 'itertools',
        ('six.moves', 'getcwd'): 'os',
        ('six.moves', 'getcwdb'): 'os',
        ('six.moves', 'getoutput'): 'subprocess',
        ('six.moves', 'intern'): 'sys',
        ('six.moves', 'reduce'): 'functools',
        ('six.moves', 'zip_longest'): 'itertools',
        ('six.moves.urllib', 'error'): 'urllib',
        ('six.moves.urllib', 'parse'): 'urllib',
        ('six.moves.urllib', 'request'): 'urllib',
        ('six.moves.urllib', 'response'): 'urllib',
        ('six.moves.urllib', 'robotparser'): 'urllib',
        ('qcodes.dataset.measurements', 'Measurement'): 'qcodes.dataset',
        ('qcodes.dataset.data_set_protocol', 'DataSetProtocol'): 'qcodes.dataset',
        ('qcodes.dataset.data_set', 'load_by_guid'): 'qcodes.dataset',
        ('qcodes.dataset.sqlite.database', 'connect'): 'qcodes.dataset',
        ('qcodes.instrument.parameter', 'Parameter'): 'qcodes.parameters',
        ('qcodes.instrument.parameter', 'DelegateParameter'): 'qcodes.parameters',
        ('qcodes.instrument.parameter', 'ParameterWithSetpoints'): 'qcodes.parameters',
        ('qcodes.instrument.parameter', 'ManualParameter'): 'qcodes.parameters',
        ('qcodes.instrument.base', 'Instrument'): 'qcodes.instrument',
        ('qcodes.dataset.sqlite.database', 'initialise_or_create_database_at'): 'qcodes.dataset',
        ('qcodes.dataset.experiment_container', 'load_or_create_experiment'): 'qcodes.dataset',
        ('qcodes.dataset.plotting', 'plot_dataset'): 'qcodes.dataset',
        ('qcodes.dataset.plotting', 'plot_by_id'): 'qcodes.dataset',
        ('qcodes.utils.dataset.doNd', 'AbstractSweep'): 'qcodes.dataset',
        ('qcodes.utils.dataset.doNd', 'LinSweep'): 'qcodes.dataset',
        ('qcodes.utils.dataset.doNd', 'ArraySweep'): 'qcodes.dataset',
        ('qcodes.utils.dataset.doNd', 'LogSweep'): 'qcodes.dataset',
        ('qcodes.utils.dataset.doNd', 'dond'): 'qcodes.dataset',
        ('qcodes.utils.dataset.doNd', 'do0d'): 'qcodes.dataset',
        ('qcodes.utils.dataset.doNd', 'do1d'): 'qcodes.dataset',
        ('qcodes.utils.dataset.doNd', 'do2d'): 'qcodes.dataset',
        ('qcodes', 'Measurement'): 'qcodes.dataset',
        ('qcodes', 'ParamSpec'): 'qcodes.dataset',
        ('qcodes', 'SQLiteSettings'): 'qcodes.dataset',
        ('qcodes', 'get_guids_by_run_spec'): 'qcodes.dataset',
        ('qcodes', 'initialise_database'): 'qcodes.dataset',
        ('qcodes', 'initialise_or_create_database_at'): 'qcodes.dataset',
        ('qcodes', 'initialised_database_at'): 'qcodes.dataset',
        ('qcodes', 'load_by_counter'): 'qcodes.dataset',
        ('qcodes', 'load_by_guid'): 'qcodes.dataset',
        ('qcodes', 'load_by_id'): 'qcodes.dataset',
        ('qcodes', 'load_by_run_spec'): 'qcodes.dataset',
        ('qcodes', 'load_experiment'): 'qcodes.dataset',
        ('qcodes', 'load_experiment_by_name'): 'qcodes.dataset',
        ('qcodes', 'load_last_experiment'): 'qcodes.dataset',
        ('qcodes', 'load_or_create_experiment'): 'qcodes.dataset',
        ('qcodes', 'load_experiment'): 'qcodes.dataset',
        ('qcodes', 'new_data_set'): 'qcodes.dataset',
        ('qcodes', 'new_experiment'): 'qcodes.dataset',
        ('qcodes', 'ChannelList'): 'qcodes.instrument',
        ('qcodes', 'ChannelTuple'): 'qcodes.instrument',
        ('qcodes', 'Instrument'): 'qcodes.instrument',
        ('qcodes', 'InstrumentChannel'): 'qcodes.instrument',
        ('qcodes', 'IPInstrument'): 'qcodes.instrument',
        ('qcodes', 'VisaInstrument'): 'qcodes.instrument',
        ('qcodes', 'find_or_create_instrument'): 'qcodes.instrument',
        ('qcodes', 'Monitor'): 'qcodes.monitor',
        ('qcodes', 'ArrayParameter'): 'qcodes.parameters',
        ('qcodes', 'CombinedParameter'): 'qcodes.parameters',
        ('qcodes', 'DelegateParameter'): 'qcodes.parameters',
        ('qcodes', 'Function'): 'qcodes.parameters',
        ('qcodes', 'ManualParameter'): 'qcodes.parameters',
        ('qcodes', 'MultiParameter'): 'qcodes.parameters',
        ('qcodes', 'Parameter'): 'qcodes.parameters',
        ('qcodes', 'ParameterWithSetpoints'): 'qcodes.parameters',
        ('qcodes', 'ScaledParameter'): 'qcodes.parameters',
        ('qcodes', 'SweepFixedValues'): 'qcodes.parameters',
        ('qcodes', 'SweepValues'): 'qcodes.parameters',
        ('qcodes', 'combine'): 'qcodes.parameters',
        ('qcodes', 'Station'): 'qcodes.station',
        ('qcodes.dataset.data_set', 'load_by_run_spec'): 'qcodes.dataset',
        ('qcodes.dataset.data_set', 'load_by_id'): 'qcodes.dataset',
        ('qcodes.instrument.specialized_parameters', 'ElapsedTimeParameter'): 'qcodes.parameters',
        ('qcodes.dataset.experiment_container', 'new_experiment'): 'qcodes.dataset',
        ('qcodes.dataset.experiment_container', 'experiments'): 'qcodes.dataset',
        ('qcodes.dataset.experiment_container', 'load_experiment'): 'qcodes.dataset',
        ('qcodes.dataset.experiment_container', 'load_experiment_by_name'): 'qcodes.dataset',
        ('qcodes.dataset.experiment_container', 'load_last_experiment'): 'qcodes.dataset',
        ('qcodes.dataset.experiment_settings', 'get_default_experiment_id'): 'qcodes.dataset',
        ('qcodes.dataset.experiment_settings', 'reset_default_experiment_id'): 'qcodes.dataset',
        ('qcodes.dataset.data_set', 'new_data_set'): 'qcodes.dataset',
        ('qcodes.dataset.legacy_import', 'import_dat_file'): 'qcodes.dataset',
        ('qcodes.instrument.parameter', 'ArrayParameter'): 'qcodes.parameters',
        ('qcodes.instrument.parameter', 'MultiParameter'): 'qcodes.parameters',
        ('qcodes.dataset.sqlite.database', 'initialise_database'): 'qcodes.dataset',

    },
    (3, 6): {
        ('typing_extensions', 'AsyncIterable'): 'typing',
        ('typing_extensions', 'AsyncIterator'): 'typing',
        ('typing_extensions', 'Awaitable'): 'typing',
        ('typing_extensions', 'ClassVar'): 'typing',
        ('typing_extensions', 'ContextManager'): 'typing',
        ('typing_extensions', 'Coroutine'): 'typing',
        ('typing_extensions', 'DefaultDict'): 'typing',
        ('typing_extensions', 'NewType'): 'typing',
        ('typing_extensions', 'TYPE_CHECKING'): 'typing',
        ('typing_extensions', 'Text'): 'typing',
        ('typing_extensions', 'Type'): 'typing',
    },
    (3, 7): {
        ('mypy_extensions', 'NoReturn'): 'typing',
        ('typing_extensions', 'AsyncContextManager'): 'typing',
        ('typing_extensions', 'AsyncGenerator'): 'typing',
        ('typing_extensions', 'ChainMap'): 'typing',
        ('typing_extensions', 'Counter'): 'typing',
        ('typing_extensions', 'Deque'): 'typing',
        ('typing_extensions', 'NoReturn'): 'typing',
    },
    (3, 8): {
        ('mypy_extensions', 'TypedDict'): 'typing',
        ('typing_extensions', 'Final'): 'typing',
        ('typing_extensions', 'Literal'): 'typing',
        ('typing_extensions', 'OrderedDict'): 'typing',
        ('typing_extensions', 'Protocol'): 'typing',
        ('typing_extensions', 'SupportsIndex'): 'typing',
        ('typing_extensions', 'runtime_checkable'): 'typing',
    },
    (3, 9): {
        ('typing', 'AsyncGenerator'): 'collections.abc',
        ('typing', 'AsyncIterable'): 'collections.abc',
        ('typing', 'AsyncIterator'): 'collections.abc',
        ('typing', 'Awaitable'): 'collections.abc',
        ('typing', 'ByteString'): 'collections.abc',
        ('typing', 'ChainMap'): 'collections',
        ('typing', 'Collection'): 'collections.abc',
        ('typing', 'Container'): 'collections.abc',
        ('typing', 'Coroutine'): 'collections.abc',
        ('typing', 'Counter'): 'collections',
        ('typing', 'Generator'): 'collections.abc',
        ('typing', 'Hashable'): 'collections.abc',
        ('typing', 'ItemsView'): 'collections.abc',
        ('typing', 'Iterable'): 'collections.abc',
        ('typing', 'Iterator'): 'collections.abc',
        ('typing', 'KeysView'): 'collections.abc',
        ('typing', 'Mapping'): 'collections.abc',
        ('typing', 'MappingView'): 'collections.abc',
        ('typing', 'Match'): 're',
        ('typing', 'MutableMapping'): 'collections.abc',
        ('typing', 'MutableSequence'): 'collections.abc',
        ('typing', 'MutableSet'): 'collections.abc',
        ('typing', 'OrderedDict'): 'collections',
        ('typing', 'Pattern'): 're',
        ('typing', 'Reversible'): 'collections.abc',
        ('typing', 'Sequence'): 'collections.abc',
        ('typing', 'Sized'): 'collections.abc',
        ('typing', 'ValuesView'): 'collections.abc',
        ('typing.re', 'Match'): 're',
        ('typing.re', 'Pattern'): 're',
        ('typing_extensions', 'Annotated'): 'typing',
        ('typing_extensions', 'get_type_hints'): 'typing',
    },
    (3, 10): {
        ('typing', 'Callable'): 'collections.abc',
        ('typing_extensions', 'Concatenate'): 'typing',
        ('typing_extensions', 'ParamSpecArgs'): 'typing',
        ('typing_extensions', 'ParamSpecKwargs'): 'typing',
        ('typing_extensions', 'TypeAlias'): 'typing',
        ('typing_extensions', 'TypeGuard'): 'typing',
        ('typing_extensions', 'get_args'): 'typing',
        ('typing_extensions', 'get_origin'): 'typing',
        ('typing_extensions', 'is_typeddict'): 'typing',
    },
    (3, 11): {
        ('typing_extensions', 'Any'): 'typing',
        ('typing_extensions', 'LiteralString'): 'typing',
        ('typing_extensions', 'NamedTuple'): 'typing',
        ('typing_extensions', 'Never'): 'typing',
        ('typing_extensions', 'NotRequired'): 'typing',
        ('typing_extensions', 'Required'): 'typing',
        ('typing_extensions', 'Self'): 'typing',
        ('typing_extensions', 'TypedDict'): 'typing',
        ('typing_extensions', 'Unpack'): 'typing',
        ('typing_extensions', 'assert_never'): 'typing',
        ('typing_extensions', 'assert_type'): 'typing',
        ('typing_extensions', 'clear_overloads'): 'typing',
        ('typing_extensions', 'dataclass_transform'): 'typing',
        ('typing_extensions', 'final'): 'typing',
        ('typing_extensions', 'get_overloads'): 'typing',
        ('typing_extensions', 'overload'): 'typing',
        ('typing_extensions', 'reveal_type'): 'typing',
    },
}
REPLACE_MODS = {
    'six.moves.BaseHTTPServer': 'http.server',
    'six.moves.CGIHTTPServer': 'http.server',
    'six.moves.SimpleHTTPServer': 'http.server',
    'six.moves._dummy_thread': '_dummy_thread',
    'six.moves._thread': '_thread',
    'six.moves.builtins': 'builtins',
    'six.moves.cPickle': 'pickle',
    'six.moves.collections_abc': 'collections.abc',
    'six.moves.configparser': 'configparser',
    'six.moves.copyreg': 'copyreg',
    'six.moves.dbm_gnu': 'dbm.gnu',
    'six.moves.dbm_ndbm': 'dbm.ndbm',
    'six.moves.email_mime_base': 'email.mime.base',
    'six.moves.email_mime_image': 'email.mime.image',
    'six.moves.email_mime_multipart': 'email.mime.multipart',
    'six.moves.email_mime_nonmultipart': 'email.mime.nonmultipart',
    'six.moves.email_mime_text': 'email.mime.text',
    'six.moves.html_entities': 'html.entities',
    'six.moves.html_parser': 'html.parser',
    'six.moves.http_client': 'http.client',
    'six.moves.http_cookiejar': 'http.cookiejar',
    'six.moves.http_cookies': 'http.cookies',
    'six.moves.queue': 'queue',
    'six.moves.reprlib': 'reprlib',
    'six.moves.socketserver': 'socketserver',
    'six.moves.tkinter': 'tkinter',
    'six.moves.tkinter_colorchooser': 'tkinter.colorchooser',
    'six.moves.tkinter_commondialog': 'tkinter.commondialog',
    'six.moves.tkinter_constants': 'tkinter.constants',
    'six.moves.tkinter_dialog': 'tkinter.dialog',
    'six.moves.tkinter_dnd': 'tkinter.dnd',
    'six.moves.tkinter_filedialog': 'tkinter.filedialog',
    'six.moves.tkinter_font': 'tkinter.font',
    'six.moves.tkinter_messagebox': 'tkinter.messagebox',
    'six.moves.tkinter_scrolledtext': 'tkinter.scrolledtext',
    'six.moves.tkinter_simpledialog': 'tkinter.simpledialog',
    'six.moves.tkinter_tix': 'tkinter.tix',
    'six.moves.tkinter_tkfiledialog': 'tkinter.filedialog',
    'six.moves.tkinter_tksimpledialog': 'tkinter.simpledialog',
    'six.moves.tkinter_ttk': 'tkinter.ttk',
    'six.moves.urllib.error': 'urllib.error',
    'six.moves.urllib.parse': 'urllib.parse',
    'six.moves.urllib.request': 'urllib.request',
    'six.moves.urllib.response': 'urllib.response',
    'six.moves.urllib.robotparser': 'urllib.robotparser',
    'six.moves.urllib_error': 'urllib.error',
    'six.moves.urllib_parse': 'urllib.parse',
    'six.moves.urllib_robotparser': 'urllib.robotparser',
    'six.moves.xmlrpc_client': 'xmlrpc.client',
    'six.moves.xmlrpc_server': 'xmlrpc.server',
    'xml.etree.cElementTree': 'xml.etree.ElementTree',
    'visa': 'pyvisa',
    'qcodes.utils.validators': 'qcodes.validators'
}
# END GENERATED


@functools.lru_cache(maxsize=None)
def _for_version(
        version: tuple[int, ...],
        *,
        keep_mock: bool,
) -> tuple[
        Mapping[str, set[str]],
        Mapping[tuple[str, str], str],
        Mapping[str, str],
]:
    removals = collections.defaultdict(set)
    for ver, ver_removals in REMOVALS.items():
        if ver <= version:
            for base, names in ver_removals.items():
                removals[base].update(names)

    exact = {}
    for ver, ver_exact in REPLACE_EXACT.items():
        if ver <= version:
            exact.update(ver_exact)

    mods = {**REPLACE_MODS}
    if not keep_mock:
        exact['mock', 'mock'] = 'unittest'
        mods.update({
            'mock': 'unittest.mock',
            'mock.mock': 'unittest.mock',
        })

    return removals, exact, mods


def _remove_import(i: int, tokens: list[Token]) -> None:
    del tokens[i:find_end(tokens, i)]


class FromImport(NamedTuple):
    start: int
    mod_start: int
    mod_end: int
    names: tuple[int, ...]
    end: int

    @classmethod
    def parse(cls, i: int, tokens: list[Token]) -> FromImport:
        if has_space_before(i, tokens):
            start = i - 1
        else:
            start = i

        j = i + 1
        # XXX: does not handle explicit relative imports
        while tokens[j].name != 'NAME':
            j += 1
        mod_start = j

        import_token = find_token(tokens, j, 'import')
        j = import_token - 1
        while tokens[j].name != 'NAME':
            j -= 1
        mod_end = j

        end = find_end(tokens, import_token)

        # XXX: does not handle `*` imports
        names = [
            j
            for j in range(import_token + 1, end)
            if tokens[j].name == 'NAME'
        ]
        for i in reversed(range(len(names))):
            if tokens[names[i]].src == 'as':
                del names[i:i + 2]

        return cls(start, mod_start, mod_end + 1, tuple(names), end)

    def remove_self(self, tokens: list[Token]) -> None:
        del tokens[self.start:self.end]

    def replace_modname(self, tokens: list[Token], modname: str) -> None:
        tokens[self.mod_start:self.mod_end] = [Token('CODE', modname)]

    def remove_parts(self, tokens: list[Token], idxs: list[int]) -> None:
        for idx in reversed(idxs):
            if idx == 0:  # look forward until next name and del
                del tokens[self.names[idx]:self.names[idx + 1]]
            else:  # look backward for comma and del
                j = end = self.names[idx]
                while tokens[j].src != ',':
                    j -= 1
                del tokens[j:end + 1]


def _alias_to_s(alias: ast.alias) -> str:
    if alias.asname:
        return f'{alias.name} as {alias.asname}'
    else:
        return alias.name


def _replace_from_modname(
        i: int,
        tokens: list[Token],
        *,
        modname: str,
) -> None:
    FromImport.parse(i, tokens).replace_modname(tokens, modname)


def _replace_from_mixed(
        i: int,
        tokens: list[Token],
        *,
        removal_idxs: list[int],
        exact_moves: list[tuple[int, str, ast.alias]],
        module_moves: list[tuple[int, str, ast.alias]],
) -> None:
    try:
        indent = indented_amount(i, tokens)
    except ValueError:
        return

    parsed = FromImport.parse(i, tokens)

    added_from_imports = collections.defaultdict(list)
    for idx, mod, alias in exact_moves:
        added_from_imports[mod].append(_alias_to_s(alias))
        bisect.insort(removal_idxs, idx)

    new_imports = []
    for idx, new_mod, alias in module_moves:
        new_mod, _, new_sym = new_mod.rpartition('.')
        new_alias = ast.alias(name=new_sym, asname=alias.asname)
        if new_mod:
            added_from_imports[new_mod].append(_alias_to_s(new_alias))
        else:
            new_imports.append(f'{indent}import {_alias_to_s(new_alias)}\n')
        bisect.insort(removal_idxs, idx)

    new_imports.extend(
        f'{indent}from {mod} import {", ".join(names)}\n'
        for mod, names in added_from_imports.items()
    )
    new_imports.sort()

    if new_imports and tokens[parsed.end - 1].src != '\n':
        new_imports.insert(0, '\n')

    tokens[parsed.end:parsed.end] = [Token('CODE', ''.join(new_imports))]

    # all names rewritten -- delete import
    if len(parsed.names) == len(removal_idxs):
        parsed.remove_self(tokens)
    else:
        parsed.remove_parts(tokens, removal_idxs)


@register(ast.ImportFrom)
def visit_ImportFrom(
        state: State,
        node: ast.ImportFrom,
        parent: ast.AST,
) -> Iterable[tuple[Offset, TokenFunc]]:
    removals, exact, mods = _for_version(
        state.settings.min_version,
        keep_mock=state.settings.keep_mock,
    )

    # we don't have any relative rewrites
    if node.level != 0 or node.module is None:
        return

    mod = node.module

    removal_idxs = []
    if node.col_offset == 0:
        removals_for_mod = removals.get(mod)
        if removals_for_mod is not None:
            removal_idxs = [
                i
                for i, alias in enumerate(node.names)
                if not alias.asname and alias.name in removals_for_mod
            ]

    exact_moves = []
    for i, alias in enumerate(node.names):
        new_mod = exact.get((mod, alias.name))
        if new_mod is not None:
            exact_moves.append((i, new_mod, alias))

    module_moves = []
    for i, alias in enumerate(node.names):
        new_mod = mods.get(f'{node.module}.{alias.name}')
        if new_mod is not None and (alias.asname or alias.name == new_mod):
            module_moves.append((i, new_mod, alias))

    if len(removal_idxs) == len(node.names):
        yield ast_to_offset(node), _remove_import
    elif (
            len(exact_moves) == len(node.names) and
            len({mod for _, mod, _ in exact_moves}) == 1
    ):
        _, modname, _ = exact_moves[0]
        func = functools.partial(_replace_from_modname, modname=modname)
        yield ast_to_offset(node), func
    elif removal_idxs or exact_moves or module_moves:
        func = functools.partial(
            _replace_from_mixed,
            removal_idxs=removal_idxs,
            exact_moves=exact_moves,
            module_moves=module_moves,
        )
        yield ast_to_offset(node), func
    elif mod in mods:
        func = functools.partial(_replace_from_modname, modname=mods[mod])
        yield ast_to_offset(node), func


def _replace_import(
        i: int,
        tokens: list[Token],
        *,
        exact_moves: list[tuple[int, str, ast.alias]],
        to_from: list[tuple[int, str, str, ast.alias]],
) -> None:
    try:
        indent = indented_amount(i, tokens)
    except ValueError:
        return

    if has_space_before(i, tokens):
        start = i - 1
    else:
        start = i
    end = find_end(tokens, i)

    parts = []
    start_idx = None
    end_idx = None
    for j in range(i + 1, end):
        if start_idx is None and tokens[j].name == 'NAME':
            start_idx = j
            end_idx = j + 1
        elif start_idx is not None and tokens[j].name == 'NAME':
            end_idx = j + 1
        elif tokens[j].src == ',':
            assert start_idx is not None and end_idx is not None
            parts.append((start_idx, end_idx))
            start_idx = end_idx = None

    assert start_idx is not None and end_idx is not None
    parts.append((start_idx, end_idx))

    for idx, new_mod, alias in reversed(exact_moves):
        new_alias = ast.alias(name=new_mod, asname=alias.asname)
        tokens[slice(*parts[idx])] = [Token('CODE', _alias_to_s(new_alias))]

    new_imports = sorted(
        f'{indent}from {new_mod} import '
        f'{_alias_to_s(ast.alias(name=new_sym, asname=alias.asname))}\n'
        for _, new_mod, new_sym, alias in to_from
    )

    if new_imports and tokens[end - 1].src != '\n':
        new_imports.insert(0, '\n')

    tokens[end:end] = [Token('CODE', ''.join(new_imports))]

    if len(to_from) == len(parts):
        del tokens[start:end]
    else:
        for idx, _, _, _ in reversed(to_from):
            if idx == 0:  # look forward until next name and del
                del tokens[parts[idx][0]:parts[idx + 1][0]]
            else:  # look backward for comma and del
                j = part_end = parts[idx][0]
                while tokens[j].src != ',':
                    j -= 1
                del tokens[j:part_end + 1]


@register(ast.Import)
def visit_Import(
        state: State,
        node: ast.Import,
        parent: ast.AST,
) -> Iterable[tuple[Offset, TokenFunc]]:
    _, _, mods = _for_version(
        state.settings.min_version,
        keep_mock=state.settings.keep_mock,
    )

    to_from = []
    exact_moves = []
    for i, alias in enumerate(node.names):
        new_mod = mods.get(alias.name)
        if new_mod is not None:
            alias_base, _, _ = alias.name.partition('.')
            new_mod_base, _, new_sym = new_mod.rpartition('.')
            if new_mod_base and new_sym == alias_base:
                to_from.append((i, new_mod_base, new_sym, alias))
            elif alias.asname is not None:
                exact_moves.append((i, new_mod, alias))

    if to_from or exact_moves:
        func = functools.partial(
            _replace_import,
            exact_moves=exact_moves,
            to_from=to_from,
        )
        yield ast_to_offset(node), func
