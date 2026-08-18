---
source_path: ".pi/.claude/shell-snapshots/snapshot-bash-1786513455921-jajfmk.sh"
source_filename: "snapshot-bash-1786513455921-jajfmk.sh"
source_type: "text"
source_size_bytes: 3388
source_modified_at: "2026-08-12T14:44:39+09:00"
source_sha256: "566a7960af314e7e8aa67ea89b876fec71aaa1899c269ecaa978a3996409eb49"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# Snapshot file
# Unset all aliases to avoid conflicts with functions
unalias -a 2>/dev/null || true
shopt -s expand_aliases
# Check for rg availability
if ! (unalias rg 2>/dev/null; command -v rg) >/dev/null 2>&1; then
  function rg {
  local _cc_bin="${CLAUDE_CODE_EXECPATH:-}"
  [[ -x $_cc_bin ]] || _cc_bin=/c/Users/user/.local/bin/claude.exe
  if [[ ! -x $_cc_bin ]]; then command rg ${1+"$@"}; return; fi
  if [[ -n ${ZSH_VERSION:-} ]]; then
    ARGV0=rg "$_cc_bin" ${1+"$@"}
  elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
    ARGV0=rg "$_cc_bin" ${1+"$@"}
  else
    (exec -a rg "$_cc_bin" ${1+"$@"})
  fi
}
fi
# Shadow pkill to refuse patterns matching the CLI process
unalias pkill 2>/dev/null || true
function pkill {
  if [ -n "${CLAUDE_PID:-}" ] && [ -r "/proc/${CLAUDE_PID}/comm" ]; then
    local _cc_skip="" _cc_a
    local -a _cc_probe=()
    for _cc_a in ${1+"$@"}; do
      if [ -n "$_cc_skip" ]; then _cc_skip=""; continue; fi
      case "$_cc_a" in
        --signal) _cc_skip=1 ;;
        --signal=*|-e|--echo) ;;
        -[0-9]*) ;;
        -[PUGOF]?*) _cc_probe+=("$_cc_a") ;;
        -[ABCDEFGHIJKLMNOPQRSTUVWXYZ][ABCDEFGHIJKLMNOPQRSTUVWXYZ0-9]*) ;;
        *) _cc_probe+=("$_cc_a") ;;
      esac
    done
    if command pgrep ${_cc_probe[@]+"${_cc_probe[@]}"} 2>/dev/null | command grep -qx "${CLAUDE_PID}"; then
      printf 'pkill: refusing to run — this pattern matches the Claude CLI process (PID %s). Narrow the pattern, or target your own children with `pkill -P $$ ...`.\n' "${CLAUDE_PID}" >&2
      return 1
    fi
  fi
  command pkill ${1+"$@"}
}
export PATH='C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0\;C:\WINDOWS\System32\OpenSSH\;C:\Program Files\dotnet\;C:\Program Files\nodejs\;C:\Program Files\Git\cmd;C:\Users\user\AppData\Local\Microsoft\WindowsApps;C:\Users\user\AppData\Roaming\npm;C:\Program Files\nodejs;C:\Program Files\Git\mingw64\bin:/c/Users/user/AppData/Roaming/Claude/local-agent-mode-sessions/494dcd67-8ae4-4369-819e-8297c0535b3a/5ddd9182-9f25-4e7e-85f3-8d5dbf29da61/rpm/plugin_014WxCYbLf7f3uw2isHFR9US/bin:/c/Users/user/AppData/Roaming/Claude/local-agent-mode-sessions/494dcd67-8ae4-4369-819e-8297c0535b3a/5ddd9182-9f25-4e7e-85f3-8d5dbf29da61/rpm/plugin_0155zZVATbJU3jHUmPP9NvMC/bin:/c/Users/user/AppData/Roaming/Claude/local-agent-mode-sessions/494dcd67-8ae4-4369-819e-8297c0535b3a/5ddd9182-9f25-4e7e-85f3-8d5dbf29da61/rpm/plugin_016u9h5nGGKuX18riDTJ7otg/bin:/c/Users/user/AppData/Roaming/Claude/local-agent-mode-sessions/494dcd67-8ae4-4369-819e-8297c0535b3a/5ddd9182-9f25-4e7e-85f3-8d5dbf29da61/rpm/plugin_017zncz89kmhdPgdpZQZm5Dj/bin:/c/Users/user/AppData/Roaming/Claude/local-agent-mode-sessions/494dcd67-8ae4-4369-819e-8297c0535b3a/5ddd9182-9f25-4e7e-85f3-8d5dbf29da61/rpm/plugin_019iPNgSpqW7kdNT72VAaUud/bin:/c/Users/user/AppData/Roaming/Claude/local-agent-mode-sessions/494dcd67-8ae4-4369-819e-8297c0535b3a/5ddd9182-9f25-4e7e-85f3-8d5dbf29da61/rpm/plugin_019TBdWa5NQJJuDFmEc4k6BJ/bin:/c/Users/user/AppData/Roaming/Claude/local-agent-mode-sessions/494dcd67-8ae4-4369-819e-8297c0535b3a/5ddd9182-9f25-4e7e-85f3-8d5dbf29da61/rpm/plugin_01Eeb9y5m4iFuY3yRtytYfdc/bin:/c/Users/user/AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin/5ddd9182-9f25-4e7e-85f3-8d5dbf29da61/494dcd67-8ae4-4369-819e-8297c0535b3a/bin'
