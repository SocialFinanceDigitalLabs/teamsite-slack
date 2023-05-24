def text(text, params={}, type="mrkdwn"):
    text = {
        "type": type,
        "text": text.format(**params),
    }
    if type == "plain_text":
        text["emoji"] = True
    return text


def section(text, accessory=None):
    section = {"type": "section", "text": text}
    if accessory is not None:
        section["accessory"] = accessory
    return section


def image(image_url, alt_text=None):
    image = {"type": "image", "image_url": image_url, "alt_text": alt_text}
    return image


def button(label, value, action=None):
    if not isinstance(label, dict):
        label = text(label, type="plain_text")
    button = {"type": "button", "text": label, "value": value}
    if action is not None:
        button["action_id"] = action
    return button


def actions(elements):
    actions = {"type": "actions", "elements": elements}
    return actions


def context(text):
    context = {"type": "context", "elements": [{"type": "mrkdwn", "text": text}]}
    return context


def divider():
    return dict(type="divider")


def dropdown(action_id, label, options):
    dropdown = {
        "type": "static_select",
        "action_id": action_id,
        "placeholder": {
            "type": "plain_text",
            "text": label,
        },
        "options": [],
    }
    for o in options:
        if isinstance(o, str):
            dropdown["options"].append(
                dict(text=dict(type="plain_text", text=o), value=o)
            )
        else:
            dropdown["options"].append(
                dict(text=dict(type="plain_text", text=o[0]), value=o[1])
            )
    return dropdown


def input_text(action_id, placeholder, label=None, multiline=False, initial_value=None):
    label = placeholder
    input_text = {
        "type": "input",
        "block_id": action_id,
        "element": {
            "type": "plain_text_input",
            "action_id": action_id,
            "multiline": multiline,
            "placeholder": {
                "type": "plain_text",
                "text": placeholder,
            },
        },
    }
    if label is not None:
        input_text["label"] = dict(type="plain_text", text=label)
    if initial_value:
        input_text["element"]["initial_value"] = initial_value
    return input_text
