if !exists("b:_tractools_did_python_init")
    python << EOF
import vim
import os.path
import sys

# get the directory this script is in and add to syspath
scriptdir = os.path.dirname(vim.eval('expand("<sfile>")'))
sys.path.insert(0, os.path.abspath(scriptdir))
import tractools
sys.path = sys.path[1:]
EOF
    let b:_tractools_did_python_init = 1
endif

function s:TracOpenBrowser()
    python tractools.open_in_browser(vim.current.buffer.name)
endfunction

command TracOpenBrowser :call s:TracOpenBrowser()

