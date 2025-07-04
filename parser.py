from lxml import etree
import re

# ========== CLEANER ==========
# In parser.py
# In parser.py
def preprocess_file_content(raw_content):
    """Convert special tags to make XML valid."""
    # Handle Page tags
    page_tag_pattern = re.compile(r"<\s*Page\s+\d+\s*>", re.IGNORECASE)
    # Handle non-closing tags (fnr*, fnt*, fmt*, etc.)
    non_closing_pattern = re.compile(r"<\s*(fnr\*|fnt\*|fmt\*|fnt\d+|fmt\d+|fnt)\b[^>]*>", re.IGNORECASE)
    
    cleaned_lines = []
    for line in raw_content.splitlines():
        # Handle Page tags
        new_line = page_tag_pattern.sub("<Page/>", line)
        # Handle non-closing tags by converting them to self-closing tags
        new_line = non_closing_pattern.sub(lambda m: f"<{m.group(1).lower()}/>", new_line)
        cleaned_lines.append(new_line)

    return "\n".join(cleaned_lines)

# ========== ENTITY CONVERTER ==========
ENTITY_TO_NUMERIC = {
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

# ========== AMPERSAND SANITIZER ==========
def sanitize_unescaped_ampersands(xml_str):
    """
    Replaces unsafe & with &amp;, while preserving:
    - Valid entities (&amp;, &lt;, etc.)
    - Legal-style usage (space & space)
    - Numeric entities (&#123;, &#x1F600;)
    """
    def replacer(match):
        full_match = match.group(0)
        # Skip valid entities
        if full_match.startswith('&#'):
            return full_match
        if full_match in {'&amp;', '&lt;', '&gt;', '&quot;', '&apos;'}:
            return full_match
        # Skip legal-style & surrounded by spaces
        if re.match(r'[ ]&[ ]', full_match):
            return full_match
        # Skip & followed by punctuation
        if re.match(r'&[,.;:)]', full_match):
            return full_match
        return '&amp;'

    return re.sub(r'&(?!#|amp;|lt;|gt;|quot;|apos;|[a-zA-Z0-9]+;)', replacer, xml_str)
# ========== PARSER ==========
def parse_xml(raw_content):
    """
    Parses XML after cleaning page tags and escaping bad characters.
    Returns: (tree, errors, None)
    """
    try:
        # STEP 1: Pre-cleaning
        cleaned_content = preprocess_file_content(raw_content)

        # STEP 2: Sanitize & only after validation — so nothing is lost before validation
        cleaned_content = sanitize_unescaped_ampersands(cleaned_content)

        # STEP 3: Replace known entities AFTER validation
        cleaned_content = replace_entities_with_numeric(cleaned_content)

        wrapped = f"<root>{cleaned_content}</root>"
        parser = etree.XMLParser(recover=False)
        tree = etree.fromstring(wrapped.encode("utf-8"), parser)
        return tree, [], None

    except etree.XMLSyntaxError as e:
        categorized_errors = []
        seen_positions = set()  # Tracks unique (line, column)

        for entry in e.error_log:
           msg = entry.message.strip()
           key = (entry.line, entry.column)

        # Skip duplicates from same position
           if key in seen_positions:
              continue
           seen_positions.add(key)

        # Category classification
           lower_msg = msg.lower()
           if any(x in lower_msg for x in [
               "xmlparseentityref", "unescaped", "no name", "amp", "lt", "gt", "semicolon"
           ]):
               category = "Repent"
           elif "tag mismatch" in lower_msg or "misnested" in lower_msg or "start tag" in lower_msg:
               category = "Reptag"
           else:
               category = "CheckSGM"

           categorized_errors.append((
               category,
               entry.line,
               entry.column,
               f"XML Syntax error: {msg}"
            ))

        return None, categorized_errors, None

    except Exception as e:
        return None, [("CheckSGM", 0, 0, f"Unexpected error: {str(e)}")], None


    


        


    





