from django import template

register = template.Library()



@register.filter
def getTotalPoints(matchSummary, player):
    return matchSummary.getTotalPoints(player)
