from django import forms
from time_tracker.models import Module, Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["date", "minutes", "module", "text"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "minutes": forms.NumberInput(attrs={"min": 1}),
            "text": forms.TextInput(attrs={"maxlength": 300, "style": "width: 420px;"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Nur aktive Module auswählbar (und beim Edit das bereits gewählte Modul zulassen)
        active = Module.objects.filter(is_active=True).order_by("name")
        if self.instance and self.instance.pk and self.instance.module_id:
            active = active | Module.objects.filter(pk=self.instance.module_id)
        self.fields["module"].queryset = active.distinct()

        # Optional: kleine Labels (Template bleibt clean)
        self.fields["date"].label = "Datum"
        self.fields["minutes"].label = "Minuten"
        self.fields["module"].label = "Modul"
        self.fields["text"].label = "Kurzbericht"

    def clean_minutes(self):
        minutes = self.cleaned_data["minutes"]
        if minutes <= 0:
            raise forms.ValidationError("Minuten müssen eine positive Zahl sein.")
        return minutes

    def clean_text(self):
        text = (self.cleaned_data.get("text") or "").strip()
        if not text:
            raise forms.ValidationError("Bitte Kurzbericht ausfüllen.")
        return text[:300]
