from lxml import etree
import re
def sanitize_unescaped_ampersands(xml_str):
    """
    Replaces unsafe & with &amp;, while preserving valid entities and legal-style usage.
    - Skips replacements for: &entity;, &#number;
    - Skips if & is surrounded by whitespace or punctuation (legal citations)
    """
    def replacer(match):
        before, amp, after = match.group(1), match.group(2), match.group(3)
        
        # Do not escape if it looks like a valid entity (&name;)
        if re.match(r'^[a-zA-Z0-9#]+;$', after.strip()):
            return match.group(0)

        # Do not escape if & is surrounded by spaces (e.g., "A & B")
        if before.endswith(' ') and after.startswith(' '):
            return match.group(0)

        # Do not escape if & is followed by punctuation
        if re.match(r'^\s*[.,;:\)]', after):
            return match.group(0)

        # Otherwise escape
        return f"{before}&amp;{after}"

    # Pattern to find ampersand with some context before/after
    pattern = re.compile(r'(.{0,10}?)(\&)(.{0,10}?)')
    return pattern.sub(replacer, xml_str)

# ========== CLEANER ==========
def preprocess_file_content(raw_content):
    """Convert <Page N> to <Page/> to make XML valid."""
    page_tag_pattern = re.compile(r"<\s*Page\s+\d+\s*>", re.IGNORECASE)
    cleaned_lines = []

    for line in raw_content.splitlines():
        new_line = page_tag_pattern.sub("<Page/>", line)
        cleaned_lines.append(new_line)

    return "\n".join(cleaned_lines)


# ========== ENTITY CONVERTER ==========
ENTITY_TO_NUMERIC = {
    "amp": "&#38;",
    "mdash": "&#8212;",
    "nbsp": "&#160;",
    "copy": "&#169;",
    "AElig": "&#198;",
    'Aacute': '&#193;', 'Abreve': '&#258;', 'Acirc': '&#194;', 'Agrave': '&#192;', 'Amacr': '&#256;',
    'Aogon': '&#260;', 'Aring': '&#197;', 'Atilde': '&#195;', 'Auml': '&#196;', 'Cacute': '&#262;',
    'Ccaron': '&#268;', 'Ccedil': '&#199;', 'Ccirc': '&#264;', 'Cdot': '&#266;', 'Dcaron': '&#270;',
    'Dstrok': '&#272;', 'ENG': '&#330;', 'ETH': '&#208;', 'Eacute': '&#201;', 'Ecaron': '&#282;',
    'Ecirc': '&#202;', 'Edot': '&#278;', 'Egrave': '&#200;', 'Emacr': '&#274;', 'Eogon': '&#280;',
    'Euml': '&#203;', 'Gbreve': '&#286;', 'Gcedil': '&#290;', 'Gcirc': '&#284;', 'Gdot': '&#288;',
    'Hcirc': '&#292;', 'Hstrok': '&#294;', 'IJlig': '&#306;', 'Iacute': '&#205;', 'Icirc': '&#206;',
    'Idot': '&#304;', 'Igrave': '&#204;', 'Imacr': '&#298;', 'Iogon': '&#302;', 'Itilde': '&#296;',
    'Iuml': '&#207;', 'Jcirc': '&#308;', 'Kcedil': '&#310;', 'Lacute': '&#313;', 'Lcaron': '&#317;',
    'Lcedil': '&#315;', 'Lmidot': '&#319;', 'Lstrok': '&#321;', 'Nacute': '&#323;', 'Ncaron': '&#327;',
    'Ncedil': '&#325;', 'Ntilde': '&#209;', 'OElig': '&#338;', 'Oacute': '&#211;', 'Ocirc': '&#212;',
    'Odblac': '&#336;', 'Ograve': '&#210;', 'Omacr': '&#332;', 'Oslash': '&#216;', 'Otilde': '&#213;',
    'Ouml': '&#214;', 'Racute': '&#340;', 'Rcaron': '&#344;', 'Rcedil': '&#342;', 'Sacute': '&#346;',
    'Scaron': '&#352;', 'Scedil': '&#350;', 'Scirc': '&#348;', "sect": "&#167;", 'THORN': '&#222;',
    'Tcaron': '&#356;', 'Tcedil': '&#354;', 'Tstrok': '&#358;', 'Uacute': '&#218;', 'Ubreve': '&#364;',
    'Ucirc': '&#219;', 'Udblac': '&#368;', 'Ugrave': '&#217;', 'Umacr': '&#362;', 'Uogon': '&#370;',
    'Uring': '&#366;', 'Utilde': '&#360;', 'Uuml': '&#220;', 'Wcirc': '&#372;', 'Yacute': '&#221;',
    'Ycirc': '&#374;', 'Yuml': '&#376;', 'Zacute': '&#377;', 'Zcaron': '&#381;', 'Zdot': '&#379;',
    'aacute': '&#225;', 'abreve': '&#259;', 'acirc': '&#226;', 'aelig': '&#230;', 'agrave': '&#224;',
    'amacr': '&#257;', 'aogon': '&#261;', 'aring': '&#229;', 'atilde': '&#227;', 'auml': '&#228;',
    'cacute': '&#263;', 'ccaron': '&#269;', 'ccedil': '&#231;', 'ccirc': '&#265;', 'cdot': '&#267;',
    'dcaron': '&#271;', 'dstrok': '&#273;', 'eacute': '&#233;', 'ecaron': '&#283;', 'ecirc': '&#234;',
    'edot': '&#279;', 'egrave': '&#232;', 'emacr': '&#275;', 'eng': '&#331;', 'eogon': '&#281;',
    'eth': '&#240;', 'euml': '&#235;', 'gacute': '&#501;', 'gbreve': '&#287;', 'gcirc': '&#285;',
    'gdot': '&#289;', 'hcirc': '&#293;', 'hstrok': '&#295;', 'iacute': '&#237;', 'icirc': '&#238;',
    'igrave': '&#236;', 'ijlig': '&#307;', 'imacr': '&#299;', 'inodot': '&#305;', 'iogon': '&#303;',
    'itilde': '&#297;', 'iuml': '&#239;', 'jcirc': '&#309;', 'kcedil': '&#311;', 'kgreen': '&#312;',
    'lacute': '&#314;', 'lcaron': '&#318;', 'lcedil': '&#316;', 'lmidot': '&#320;', 'lstrok': '&#322;',
    'nacute': '&#324;', 'napos': '&#329;', 'ncaron': '&#328;', 'ncedil': '&#326;', 'ntilde': '&#241;',
    'oacute': '&#243;', 'ocirc': '&#244;', 'odblac': '&#337;', 'oelig': '&#339;', 'ograve': '&#242;',
    'omacr': '&#333;', 'oslash': '&#248;', 'otilde': '&#245;', 'ouml': '&#246;', 'racute': '&#341;',
    'rcaron': '&#345;', 'rcedil': '&#343;', 'sacute': '&#347;', 'scaron': '&#353;', 'scedil': '&#351;',
    'scirc': '&#349;', 'szlig': '&#223;', 'tcaron': '&#357;', 'tcedil': '&#355;', 'thorn': '&#254;',
    'tstrok': '&#359;', 'uacute': '&#250;', 'ubreve': '&#365;', 'ucirc': '&#251;', 'udblac': '&#369;',
    'ugrave': '&#249;', 'umacr': '&#363;', 'uogon': '&#371;', 'uring': '&#367;', 'utilde': '&#361;',
    'uuml': '&#252;', 'wcirc': '&#373;', 'yacute': '&#253;', 'ycirc': '&#375;', 'yuml': '&#255;',
    'zacute': '&#378;', 'zcaron': '&#382;', 'zdot': '&#380;'
}


def replace_entities_with_numeric(xml_str):
    """Replaces named entities with numeric character references."""
    for entity, numeric in ENTITY_TO_NUMERIC.items():
        xml_str = xml_str.replace(f"&{entity};", numeric)
    return xml_str





# ========== PARSER ==========
def parse_xml(raw_content):
    """
    Parses XML after cleaning page tags, replacing named entities,
    and escaping invalid ampersands.
    Returns: (tree, errors, None)
    """
    try:
        # Step 1: Remove <Page N> tags
        cleaned_content = preprocess_file_content(raw_content)

        cleaned_content = sanitize_unescaped_ampersands(cleaned_content)

        # Step 2: Replace valid named entities with numeric refs
        cleaned_content = replace_entities_with_numeric(cleaned_content)

        # Step 3: Sanitize remaining unescaped ampersands


        # Step 4: Wrap and parse
        wrapped = f"<root>{cleaned_content}</root>"
        parser = etree.XMLParser(recover=False)
        tree = etree.fromstring(wrapped.encode('utf-8'), parser)

        return tree, [], None

    except FileNotFoundError:
        return None, [("CheckSGM", 0, 0, "File not found")], None

    except PermissionError:
        return None, [("CheckSGM", 0, 0, "Permission denied")], None

    except etree.XMLSyntaxError as e:
        error_log = e.error_log
        categorized_errors = []
        for entry in error_log:
            msg = entry.message.strip().lower()
            if any(kw in msg for kw in ["xmlparseentityref", "unescaped", "no name", "amp", "lt", "gt", "semicolon"]):
                category = "Repent"
            elif "tag mismatch" in msg or "misnested" in msg or "start tag" in msg:
                category = "Reptag"
            else:
                category = "CheckSGM"
            categorized_errors.append((
                category,
                entry.line,
                entry.column,
                f"XML Syntax error: {entry.message.strip()}"
            ))
        return None, categorized_errors, None

    except Exception as e:
        return None, [("CheckSGM", 0, 0, f"Unexpected error: {str(e)}")], None
