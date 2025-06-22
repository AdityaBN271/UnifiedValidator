# Configuration for Unified XML Validator

# Comprehensive list of valid entities (names only, no ampersand or semicolon)
CUSTOM_ENTITIES = {
    "cacute", "itilde", "Lstrok", "nacute", "Sacute", "sacute",
    "Agrave", "Aacute", "Acirc", "Atilde", "Auml", "Aring", "AElig",
    "Ccedil", "Egrave", "Eacute", "Ecirc", "Euml", "Igrave", "Iacute",
    "Icirc", "Iuml", "ETH", "Ntilde", "Ograve", "Oacute", "Ocirc",
    "Otilde", "Ouml", "Oslash", "Ugrave", "Uacute", "Ucirc", "Uuml",
    "Yacute", "THORN", "szlig", "agrave", "aacute", "acirc", "atilde",
    "auml", "aring", "aelig", "ccedil", "egrave", "eacute", "ecirc",
    "euml", "igrave", "iacute", "icirc", "iuml", "eth", "ntilde", "ograve",
    "oacute", "ocirc", "otilde", "ouml", "oslash", "ugrave", "uacute",
    "ucirc", "uuml", "yacute", "thorn", "yuml", "abreve", "Abreve", "amacr",
    "Amacr", "aogon", "Aogon", "Cacute", "ccaron", "Ccaron", "ccirc",
    "Ccirc", "cdot", "Cdot", "dcaron", "Dcaron", "dstrok", "Dstrok",
    "ecaron", "Ecaron", "edot", "Edot", "emacr", "Emacr", "eogon", "Eogon",
    "gacute", "gbreve", "Gbreve", "Gcedil", "gcirc", "Gcirc", "gdot",
    "Gdot", "hcirc", "Hcirc", "hstrok", "Hstrok", "Idot", "Imacr", "imacr",
    "ijlig", "IJlig", "inodot", "iogon", "Iogon", "Itilde", "jcirc", "Jcirc",
    "kcedil", "Kcedil", "kgreen", "lacute", "Lacute", "lcaron", "Lcaron",
    "lcedil", "Lcedil", "lmidot", "Lmidot", "lstrok", "Nacute", "eng", "ENG",
    "napos", "ncaron", "Ncaron", "ncedil", "Ncedil", "odblac", "Odblac",
    "Omacr", "omacr", "oelig", "OElig", "racute", "Racute", "rcaron", "Rcaron",
    "rcedil", "Rcedil", "scaron", "Scaron", "scedil", "Scedil", "scirc",
    "Scirc", "tcaron", "Tcaron", "tcedil", "Tcedil", "tstrok", "Tstrok",
    "ubreve", "Ubreve", "udblac", "Udblac", "umacr", "Umacr", "uogon",
    "Uogon", "uring", "Uring", "utilde", "Utilde", "wcirc", "Wcirc",
    "ycirc", "Ycirc", "Yuml", "zacute", "Zacute", "zcaron", "Zcaron",
    "zdot", "Zdot", "emsp", "ensp", "emsp13", "emsp14", "numsp", "puncsp",
    "thinsp", "hairsp", "mdash", "ndash", "dash", "blank", "hellip", "nldr",
    "block", "uhblk", "lhblk", "blk14", "blk12", "blk34", "marker", "cir",
    "squ", "rect", "utri", "dtri", "star", "bull", "squf", "utrif", "dtrif",
    "ltrif", "rtrif", "clubs", "diams", "hearts", "spades", "malt", "dagger",
    "Dagger", "check", "cross", "sharp", "flat", "male", "female", "phone",
    "telrec", "copysr", "caret", "lsquor", "ldquor", "fflig", "filig",
    "fjlig", "ffilig", "ffllig", "fllig", "mldr", "rdquor", "rsquor",
    "vellip", "hybull", "loz", "lozf", "ltri", "rtri", "starf", "natur",
    "rx", "sext", "target", "dlcrop", "drcrop", "ulcrop", "urcrop",
    "scriptE", "le", "leEq", "ge", "radic", "half", "frac12", "frac14",
    "frac34", "rlarr2", "swungdash", "approx", "cuwed", "sup1", "sup2",
    "sup3", "plus", "plusmn", "equals", "gt", "divide", "times", "curren",
    "pound", "dollar", "cent", "yen", "num", "percnt", "ast", "commat",
    "lsqb", "bsol", "rsqb", "lcub", "horbar", "verbar", "rcub", "micro",
    "ohm", "deg", "ordm", "ordf", "sect", "para", "middot", "larr", "rarr",
    "uarr", "darr", "copy", "reg", "trade", "brvbar", "not", "sung", "excl",
    "iexcl", "quot", "apos", "lpar", "rpar", "comma", "lowbar", "hyphen",
    "period", "sol", "colon", "semi", "quest", "iquest", "lsquo", "rsquo",
    "ldquo", "rdquo", "nbsp", "shy", "schwa", "alpha", "Alpha", "beta",
    "Beta", "gamma", "Gamma", "delta", "Delta", "epsilon", "Epsilon",
    "zeta", "Zeta", "eta", "Eta", "theta", "Theta", "iota", "Iota",
    "kappa", "Kappa", "lambda", "Lambda", "mu", "Mu", "nu", "Nu", "xi",
    "Xi", "omicron", "Omicron", "pi", "Pi", "rho", "Rho", "fsigma",
    "sigma", "Sigma", "tau", "Tau", "upsilon", "Upsilon", "phi", "Phi",
    "chi", "Chi", "psi", "Psi", "omega", "Omega", "aacgr", "Aacgr",
    "eacgr", "Eacgr", "eeacgr", "EEacgr", "idigr", "Idigr", "iacgr",
    "Iacgr", "idiagr", "oacgr", "Oacgr", "udigr", "Udigr", "uacgr",
    "Uacgr", "udiagr", "Udiagr", "ohacgr", "OHacgr", "aleph", "and",
    "ang90", "angsph", "ap", "becaus", "bottom", "cap", "cong", "conint",
    "cup", "equiv", "exist", "forall", "fnof", "iff", "infin", "int",
    "isin", "lang", "lArr", "minus", "mnplus", "nabla", "ne", "ni", "or",
    "par", "part", "permil", "perp", "prime", "Prime", "prop", "rang",
    "rArr", "sim", "sime", "square", "sub", "sube", "sup", "supe",
    "there4", "Verbar", "angst", "bernou", "compfn", "Dot", "DotDot",
    "hamilt", "lagran", "lowast", "notin", "order", "phmmat", "tdot",
    "tprime", "wedgeq", "rdArr", "Acircle", "Bcircle", "Ccircle",
    "Dcircle", "Ecircle", "Fcircle", "Gcircle", "Hcircle", "Icircle",
    "Jcircle", "Kcircle", "Lcircle", "Mcircle", "Ncircle", "Ocircle",
    "Pcircle", "Qcircle", "Rcircle", "Scircle", "Tcircle", "Ucircle",
    "Vcircle", "Wcircle", "Xcircle", "Ycircle", "Zcircle", "acircle",
    "bcircle", "ccircle", "dcircle", "ecircle", "fcircle", "gcircle",
    "hcircle", "icircle", "jcircle", "kcircle", "lcircle", "mcircle",
    "ncircle", "ocircle", "pcircle", "qcircle", "rcircle", "scircle",
    "tcircle", "ucircle", "vcircle", "wcircle", "xcircle", "ycircle",
    "zcircle", "circle0", "circle1", "circle2", "circle3", "circle4",
    "circle5", "circle6", "circle7", "circle8", "circle9", "circle10",
    "circle11", "circle12", "circle13", "circle14", "circle15", "circle16",
    "circle17", "circle18", "circle19", "circle20", "euro", "laquo", "raquo"
}

# List of tags including non-closing tags
SUPPORTED_TAGS = {
    'EM', 'EMB', 'EMU', 'EMS', 'EMBI', 'EMBU', 'EMBUI', 'EMBSUI', 'EMBUSI',
    'EMUI', 'EMSI', 'EMSUI', 'SUP', 'SUB', 'FN', 'T', 'A', 'fnr', 'fnt', 'p20'
}

# Non-closing tags that don't require closing validation
NON_CLOSING_TAGS = {'fnr', 'fnt','fnt*', 'P20','PAGE'}

# List of required tags for structure validation
DEFAULT_REQUIRED_TAGS = [
    'case', 'title', 'judgment', 'court', 'date'
]
