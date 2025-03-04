from django import template
import jdatetime

# register = template.Library()

# @register.filter(name='mytruncate')
# def cutter(value, arg):
#     return value[:arg]




register = template.Library()

@register.simple_tag
def current_time(format_string):
    return jdatetime.datetime.now().strftime(format_string)



# @register.filter
# def separate_thousands(value):
#     """جدا کردن اعداد به صورت سه رقم سه رقم"""
#     try:
#         return f"{int(value):,}"  # تبدیل به عدد و اعمال جداکننده
#     except (ValueError, TypeError):
#         return value