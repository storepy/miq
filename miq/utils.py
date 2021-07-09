def get_text_choices(TextChoiceModel):
    return [
        {'name': choice.name, 'label': choice.label, 'value': choice.value}
        for choice in TextChoiceModel
    ]