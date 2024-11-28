import base64
import os

import quizgen.parser.common

# Cache the results of any image callbacks using (original src, base dir) as the key.
_callback_cache = {}

def handle_callback(callback, original_src, base_dir):
    key = (original_src, base_dir)

    computed_src = _callback_cache.get(key, None)
    if (computed_src is not None):
        return computed_src

    if (callback is None):
        return original_src

    computed_src = callback(original_src, base_dir)
    _callback_cache[key] = computed_src

    return computed_src

def encode_image(path):
    ext = os.path.splitext(path)[-1].lower()
    mime = f"image/{ext}"

    with open(path, 'rb') as file:
        data = file.read()

    content = base64.standard_b64encode(data)
    return mime, content.decode(quizgen.parser.common.ENCODING)
