from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime  # for checking renewal date range.

from django import forms
# from catalog.models import BookInstance

class RenewBookForm(forms.Form):
    """Form for a librarian to renew books."""
    renewal_date = forms.DateField(
        help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date'] #self.cleaned_data 是 Django 表单中的一个字典，存储表单字段 验证通过后 的数据

        # Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        # Check date is in range librarian allowed to change (+4 weeks)
        if data > datetime.date.today() + datetime.timedelta(weeks=4): #生成一个时间增量（timedelta 对象），表示 4 周（28 天）
            raise ValidationError(
                _('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data
    
    # class Meta:
    #     model = BookInstance
    #     fields = ['due_back']
    #     labels = {'due_back': _('Renewal date')}
    #     help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}