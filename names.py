"""Normalise pub names and group them into themes."""
import re

STOP = re.compile(r"\b(the|ye|olde?|inn|hotel|tavern|pub|public house|bar|arms?|ph|& restaurant|and restaurant|restaurant|bar & grill|freehouse|free house|country|village|lounge|kitchen|bistro|grill|dining rooms?|eatery|house)\b")

def norm(name):
    s = name.lower().replace('’', "'").replace('`', "'")
    s = re.sub(r"\(.*?\)", " ", s)
    s = s.split(' - ')[0].split(',')[0]
    s = s.replace('&', ' and ').replace('+', ' and ')
    s = re.sub(r"\bst\.?\b", 'st', s)
    s = re.sub(r"[^a-z0-9' ]", ' ', s)
    s = re.sub(r"'s\b", 's', s).replace("'", '')
    s = re.sub(r"\s+", ' ', s).strip()
    s = re.sub(r"^(the|ye) ", '', s)
    s = re.sub(r" (inn|hotel|tavern|pub|public house|bar|ph|free house|freehouse)$", '', s)
    s = re.sub(r" (inn|hotel|tavern|pub)$", '', s)
    s = re.sub(r"^(old|olde|ye olde) ", '', s) if s.startswith(('olde ', 'ye olde ')) else s
    s = re.sub(r"\bkings\b", 'kings', s)
    return s.strip()

# Canonical forms for common variants
ALIAS = {
    'kings head': 'kings head', 'king head': 'kings head', 'queens head': 'queens head',
    'rose and crown': 'rose and crown', 'red lion': 'red lion', 'royal oak': 'royal oak',
    'white hart': 'white hart', 'swan': 'swan', 'white swan': 'white swan', 'black swan': 'black swan',
    'plough': 'plough', 'plow': 'plough', 'the plough': 'plough', 'ploughshare': 'plough',
    'wheat sheaf': 'wheatsheaf', 'coach and horses': 'coach and horses', 'fox and hounds': 'fox and hounds',
    'railway': 'railway', 'railway hotel': 'railway', 'station': 'station', 'station hotel': 'station',
    'marquis of granby': 'marquis of granby', 'marquess of granby': 'marquis of granby', 'granby': 'marquis of granby',
    'nags head': 'nags head', 'kings arms': 'kings arms', 'crown and anchor': 'crown and anchor',
    'lord nelson': 'lord nelson', 'nelson': 'lord nelson', 'admiral nelson': 'lord nelson',
    'duke of wellington': 'duke of wellington', 'wellington': 'duke of wellington',
    'bulls head': 'bulls head', 'bull': 'bull', 'black bull': 'black bull', 'red bull': 'red bull',
    'eagle and child': 'eagle and child', 'bird in hand': 'bird in hand', 'cross keys': 'cross keys',
    'three horseshoes': 'three horseshoes', 'horseshoe': 'horseshoe', 'new inn': 'new inn', 'new': 'new inn',
}

THEMES = {
    'Crown and monarchy': ['crown', 'kings head', 'queens head', 'kings arms', 'queens arms', 'royal oak', 'rose and crown',
                           'crown and anchor', 'prince of wales', 'princess', 'prince albert', 'queen victoria', 'king william',
                           'george', 'royal', 'kings', 'queens', 'victoria', 'jubilee', 'coronation', 'king edward', 'king charles'],
    'Heraldry and great families': ['red lion', 'white hart', 'white horse', 'black bull', 'bear and ragged staff', 'eagle and child',
                                    'talbot', 'white lion', 'golden lion', 'black lion', 'blue boar', 'white bear', 'spread eagle',
                                    'feathers', 'three tuns', 'greyhound', 'rising sun', 'sun', 'star', 'unicorn', 'griffin', 'dolphin',
                                    'black horse', 'red cow', 'dun cow', 'chequers', 'bell', 'blue bell', 'swan', 'white swan', 'black swan',
                                    'falcon', 'stag', 'black boy', 'saracens head', 'blue bell', 'bear', 'george and dragon', 'green dragon',
                                    'red dragon', 'castle', 'portcullis', 'three crowns', 'mitre'],
    'Farming and trades': ['plough', 'wheatsheaf', 'woolpack', 'shepherd', 'shepherds', 'harrow', 'barley mow', 'hop pole', 'malt shovel',
                           'carpenters', 'bricklayers', 'masons', 'blacksmiths', 'smiths', 'weavers', 'butchers', 'bakers', 'farmers',
                           'millers', 'miners', 'colliers', 'drovers', 'wagon and horses', 'waggon and horses', 'jolly farmer', 'farmers boy',
                           'three horseshoes', 'horseshoe', 'horseshoes', 'shoulder of mutton', 'fleece', 'golden fleece', 'hare and hounds',
                           'boot', 'cooper', 'tanners', 'sawyers', 'gardeners', 'hop', 'malt', 'brewers', 'jolly sailor', 'fishermans', 'anchor'],
    'Roads, rails and canals': ['railway', 'station', 'coach and horses', 'navigation', 'packhorse', 'pack horse', 'boat', 'canal', 'junction',
                                'locomotive', 'railway tavern', 'travellers rest', 'wheel', 'turnpike', 'tollgate', 'toll house', 'bridge',
                                'ferry', 'packet', 'post house', 'stage coach', 'coach house', 'steam packet', 'lock', 'wharf', 'engine'],
    'Faith and pilgrimage': ['lamb', 'lamb and flag', 'cross keys', 'angel', 'mitre', 'bishops', 'abbey', 'priory', 'monk', 'monks', 'friar',
                             'pilgrims', 'seven stars', 'salutation', 'church', 'chapel', 'catherine wheel', 'trip to jerusalem', 'adam and eve',
                             'noahs ark', 'ark', 'three kings', 'holy', 'bell', 'rose'],
    'War and heroes': ['marquis of granby', 'lord nelson', 'duke of wellington', 'admiral', 'general', 'volunteer', 'rifleman', 'grenadier',
                       'trafalgar', 'waterloo', 'alma', 'balaclava', 'sebastopol', 'lord raglan', 'duke of york', 'hero of', 'cannon',
                       'drum', 'soldier', 'sailor', 'britannia', 'nelson', 'wellington', 'garibaldi', 'lord clyde'],
    'Animals and sport': ['fox', 'fox and hounds', 'hare and hounds', 'dog and duck', 'cock', 'fighting cocks', 'cricketers', 'bat and ball',
                          'bowling green', 'fox and goose', 'pheasant', 'partridge', 'feathers', 'otter', 'kingfisher', 'pelican', 'peacock',
                          'jolly anglers', 'anglers', 'racehorse', 'horse and jockey', 'jockey', 'huntsman', 'hounds', 'greyhound', 'falcon',
                          'magpie', 'owl', 'raven', 'robin', 'wren', 'dog', 'cat', 'goat', 'ram', 'bull', 'lion', 'hart', 'stag', 'swan'],
}


def theme(n):
    """Return the theme for a normalised name, by first matching key phrase (longest first)."""
    best = None
    for th, keys in THEMES.items():
        for k in keys:
            if re.search(r'\b' + re.escape(k) + r'\b', n):
                if best is None or len(k) > len(best[1]):
                    best = (th, k)
    return best[0] if best else None
