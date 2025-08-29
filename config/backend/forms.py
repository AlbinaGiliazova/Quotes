from django import forms
from .models import Quote


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["text", "source", "weight"]
        widgets = {
            "weight": forms.NumberInput(attrs={"min": 1, "value": 1}),
        }

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        source = cleaned_data.get("source")

        # Проверка на дубль
        if text and source:
            if Quote.objects.filter(text=text, source=source).exists():
                raise forms.ValidationError(
                    "Такая цитата уже существует от этого источника."
                )

            # Проверка на максимум цитат от источника
            if Quote.objects.filter(source=source).count() >= 3:
                raise forms.ValidationError(
                    "Нельзя добавить более трёх цитат от одного источника."
                )
        return cleaned_data
