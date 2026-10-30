"""ACE mutation-harness code-identity attestation hook (WP-RD-B, R1 s7.3.4).

Injected through PYTHONPATH, so `site` imports it in every interpreter of the attested
process tree. It is INERT unless ACE_ATTEST_OUT is set.

When active it writes <pid>.start.json at start-up and <pid>.end.json from atexit. It
never prints, never changes the exit status, never imports an attestation target (it
inspects only modules already in sys.modules, through __dict__ lookups), and imports
nothing at start-up beyond `atexit`. Any internal failure is written to
<pid>.hookerror.json and otherwise swallowed. The harness treats a missing, malformed or
error record as a failure, so a silent hook failure can never become a pass.

Environment:
  ACE_ATTEST_OUT      directory for records (must exist)
  ACE_ATTEST_TARGETS  "module:qualname;module:qualname" (may be empty)
  ACE_ATTEST_PHASE    free-text phase label
"""

import os as _os
import sys as _sys


def _jstr(text):
    out = ['"']
    for ch in text:
        code = ord(ch)
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif code < 0x20 or 0xD800 <= code <= 0xDFFF:
            out.append("\\u%04x" % code)
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def _dump(value):
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return _jstr(value)
    if isinstance(value, (list, tuple)):
        return "[" + ",".join(_dump(item) for item in value) + "]"
    if isinstance(value, dict):
        return "{" + ",".join(_jstr(str(key)) + ":" + _dump(item) for key, item in value.items()) + "}"
    return _jstr(repr(value))


def _write(name, record):
    directory = _os.environ["ACE_ATTEST_OUT"]
    final = _os.path.join(directory, name)
    temporary = final + ".tmp"
    with open(temporary, "w", encoding="utf-8") as handle:
        handle.write(_dump(record))
        handle.flush()
        _os.fsync(handle.fileno())
    _os.replace(temporary, final)


def _flags():
    flags = _sys.flags
    return {
        "isolated": flags.isolated,
        "ignore_environment": flags.ignore_environment,
        "no_site": flags.no_site,
        "no_user_site": flags.no_user_site,
        "optimize": flags.optimize,
        "dont_write_bytecode": flags.dont_write_bytecode,
    }


def _record_error(stage, exc):
    try:
        _write("%d.hookerror.json" % _os.getpid(),
               {"kind": "hookerror", "pid": _os.getpid(), "stage": stage, "error": repr(exc)})
    except BaseException:  # noqa: BLE001 - must never disturb the attested program
        pass


def _canon(code):
    consts = tuple(_canon(c) if hasattr(c, "co_code") else ("const", type(c).__name__, repr(c))
                   for c in code.co_consts)
    return (code.co_name, code.co_qualname, code.co_argcount, code.co_posonlyargcount,
            code.co_kwonlyargcount, code.co_flags, code.co_code, code.co_names, code.co_varnames,
            code.co_freevars, code.co_cellvars, code.co_firstlineno, tuple(code.co_lines()),
            tuple(code.co_positions()), consts)


def _find_code(code, qualname):
    if code.co_qualname == qualname:
        return code
    for const in code.co_consts:
        if hasattr(const, "co_code"):
            found = _find_code(const, qualname)
            if found is not None:
                return found
    return None


def _attest_target(module_name, qualname, hashlib):
    module = _sys.modules.get(module_name)
    if module is None:
        return {"module": module_name, "qualname": qualname, "loaded": False}
    entry = {"module": module_name, "qualname": qualname, "loaded": True}
    obj = module
    for part in qualname.split("."):
        namespace = getattr(obj, "__dict__", None)
        obj = namespace.get(part) if isinstance(namespace, dict) else None
        if obj is None:
            break
    code = getattr(obj, "__code__", None)
    source_path = module.__dict__.get("__file__")
    entry["file"] = source_path
    entry["cached"] = module.__dict__.get("__cached__")
    if code is None or not source_path:
        entry["resolved"] = False
        return entry
    entry["resolved"] = True
    entry["loaded_digest"] = hashlib.sha256(repr(_canon(code)).encode("utf-8")).hexdigest()
    with open(source_path, "rb") as handle:
        source = handle.read()
    entry["source_sha256"] = hashlib.sha256(source).hexdigest()
    fresh_module = compile(source, source_path, "exec", dont_inherit=True, optimize=_sys.flags.optimize)
    fresh = _find_code(fresh_module, code.co_qualname)
    entry["disk_digest"] = (hashlib.sha256(repr(_canon(fresh)).encode("utf-8")).hexdigest()
                            if fresh is not None else None)
    entry["disk_match"] = fresh is not None and entry["disk_digest"] == entry["loaded_digest"]
    return entry


def _finish():
    try:
        import hashlib

        targets = []
        for item in _os.environ.get("ACE_ATTEST_TARGETS", "").split(";"):
            if item:
                module_name, _, qualname = item.partition(":")
                targets.append(_attest_target(module_name, qualname, hashlib))
        main = _sys.modules.get("__main__")
        with open(__file__, "rb") as handle:
            hook_sha256 = hashlib.sha256(handle.read()).hexdigest()
        _write("%d.end.json" % _os.getpid(), {
            "kind": "end",
            "pid": _os.getpid(),
            "ppid": _os.getppid(),
            "phase": _os.environ.get("ACE_ATTEST_PHASE", ""),
            "argv": list(getattr(_sys, "argv", [])),
            "orig_argv": list(getattr(_sys, "orig_argv", [])),
            "main_file": getattr(main, "__file__", None),
            "path": list(_sys.path),
            "hook_sha256": hook_sha256,
            "targets": targets,
        })
    except BaseException as exc:  # noqa: BLE001
        _record_error("end", exc)


def _start():
    try:
        _write("%d.start.json" % _os.getpid(), {
            "kind": "start",
            "pid": _os.getpid(),
            "ppid": _os.getppid(),
            "phase": _os.environ.get("ACE_ATTEST_PHASE", ""),
            "executable": _sys.executable,
            "orig_argv": list(getattr(_sys, "orig_argv", [])),
            "flags": _flags(),
            "pycache_prefix": _sys.pycache_prefix,
            "hook_file": __file__,
        })
        import atexit

        atexit.register(_finish)
    except BaseException as exc:  # noqa: BLE001
        _record_error("start", exc)


if _os.environ.get("ACE_ATTEST_OUT"):
    _start()
