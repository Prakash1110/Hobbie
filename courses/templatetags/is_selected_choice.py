from django import template
register = template.Library()


@register.filter
def is_selected_choice(choice, quiztaker):
    return choice.selectedchoice_set.filter(quiztaker=quiztaker).exists()