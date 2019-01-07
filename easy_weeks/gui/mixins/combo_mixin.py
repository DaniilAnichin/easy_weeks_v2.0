from easy_weeks.database import Logger
from easy_weeks.gui.components import CompleterCombo

logger = Logger()


class ComboMixin:
    def make_combo(self, choice_list, selected, name, sort_key):
        combo = CompleterCombo()
        combo.items = sorted(choice_list, key=sort_key)
        combo.addItems([sort_key(item) for item in combo.items])
        setattr(self, name, combo)
        if selected:
            combo.setCurrentIndex(combo.items.index(selected))
        logger.info(f'Added combobox with name "{name}"')
        return combo
